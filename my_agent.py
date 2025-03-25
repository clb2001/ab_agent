import os
import sys
sys.path.append('/Users/clb/Desktop/project/code/paper/utils')
from autogen import AssistantAgent
from descriptions import *
from tools import *

config_list = [
    {
       "model": "gpt-4o-2024-08-06",
       "api_key": "",
       "base_url": "",
       "timeout": 300,
       "max_tokens": 4096,
    },
]

llm_config = {"config_list": [config_list[0]], "cache_seed": 42}        

class MyAssistantAgent(AssistantAgent):
    def __init__(self, name, append_system_message="", default_auto_reply="Please continue. If everything is done, reply 'TERMINATE'."):
        if name == 'xiaoming':
            description = DESCRIPTION_XIAOMING
        elif name == 'xiaosheng':
            description = DESCRIPTION_XIAOSHENG
        elif name == 'xiaopan':
            description = DESCRIPTION_XIAOPAN
        elif name == 'xiaoli':
            description = DESCRIPTION_XIAOLI
        message = SYSTEM_MESSAGE + description + append_system_message
        super(MyAssistantAgent, self).__init__(
            name=name, 
            system_message=message,
            llm_config=llm_config, 
            description=description,
            default_auto_reply=default_auto_reply
        ) 
