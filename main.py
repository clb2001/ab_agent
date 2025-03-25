from autogen import UserProxyAgent
from autogen.coding import LocalCommandLineCodeExecutor
from my_agent import MyAssistantAgent
import sys
sys.path.append('/Users/clb/Desktop/project/code/paper/utils')
from tools import *

def get_agent_name(data):
    for entry in data[::-1]:
        content = entry['content']
        if 'xiaoming' in content:
            return 'xiaoming'
        if 'xiaopan' in content:
            return 'xiaopan'
        if 'xiaoli' in content:
            return 'xiaoli'
        if 'xiaosheng' in content:
            return 'xiaosheng'
    raise ValueError('没有符合要求的agent！')

executor = LocalCommandLineCodeExecutor(
    timeout=60,
    work_dir="coding",
    functions=[generate_fake_info, understand_fake_info, detect_fake_info],
)

agent_user = UserProxyAgent(
    name="user",
    code_execution_config={"executor": executor},
)

agent_xiaoming = MyAssistantAgent(
    name="xiaoming",
)

init_chat_result = agent_user.initiate_chat(
    agent_xiaoming,
    message=f'''你是一个虚假信息问题专家，支持虚假信息判别、、虚假信息理解、虚假信息生成等任务，需要帮助我解决问题。
    你需要给出所有任务的名称，让我确定任务，完成任务的agent分配，并把输出的结果作为参数传递到后面的对话中。
    如果希望进行虚假信息生成任务，请转发给名叫xiaosheng的agent；
    如果希望进行虚假信息判别任务，请转发给名叫xiaopan的agent；
    如果希望进行虚假信息理解任务，请转发给名叫xiaoli的agent；
    如果输出其他回答，请再输入一次。
    一旦我给出符合要求的回答，请输出“收到，我将把您的任务转发给对应的agent，请您继续。”并且输出agent的名字。请我输入“exit”以便进行下一步。
    ''',    
)

agent_service = MyAssistantAgent(
    name=get_agent_name(init_chat_result.chat_history),
    append_system_message=executor.format_functions_for_prompt(),
    default_auto_reply="Please continue. If everything is done, reply 'TERMINATE'."
)

chat_result = agent_user.initiate_chat(
    agent_service,
    message=f'''你需要根据以下流程，一步一步和我进行交互。
    1、如果有任务规则，请输出任务规则并让我确定，以我修改的任务规则为准；
    2、请输出注释中的任务流程，结合我的需求规划并拆解任务，制定执行方案并输出，让我确认方案；
    3、根据任务需求合理选择函数，执行任务。这里如果有需要我输入的参数，请输出参数名称及意义，让我输入；
    4、执行完任务后，如果有反馈，需要根据我的反馈修改结果。
    5、如果任务已经执行完成，请提示我输出“exit”
    你需要自动执行程序，不能让我自己操作。''',
)
