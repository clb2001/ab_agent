def load_data(data_path):
    '''
    加载数据
    Args:
        data_path(str): json格式的数据路径
    Returns:
        data ((List[dict]): 加载的数据
    '''
    import json

    with open(data_path, 'r') as f:
        data = json.load(f)
    return data

def detect_fake_info(REQUEST_PROMPT, original_info, picture_url):
    '''
    识别和检测虚假信息的过程
    Args:
        original_info (str): 原始消息或者主题
        picture_url (Optional[str]): 参考的图片
    Returns:
        analysis_result (str): 判断是否是虚假信息，并且给出理由
    '''
    import sys
    sys.path.append("/Users/clb/Desktop/project/code/paper/utils")
    from call_openai import call_openai_single

    def call_gpt(PROMPT, original_info, picture_url):
        content = [PROMPT, original_info, picture_url]
        try:
            answer = call_openai_single(content, model='gpt-4o-2024-11-20')['choices'][0]['message']['content']
            return answer
        except Exception as e:
            print(f"Error processing item: {e}")
            return None
    
    analysis_result = call_gpt(REQUEST_PROMPT, original_info, picture_url)
    return analysis_result

def understand_fake_info(original_info, question):
    '''
    分析和理解虚假信息的内容
    Args:
        original_info (str): 虚假信息内容
        question (str): 希望提出的问题
    Returns:
        analysis_result (str): 虚假信息分析结果
    '''
    import sys
    sys.path.append("/Users/clb/Desktop/project/code/paper/utils")
    from call_openai import call_openai_single
    def call_gpt(original_info, picture_url):
        content = [original_info, picture_url]
        try:
            answer = call_openai_single(content, model='gpt-4o-2024-11-20')['choices'][0]['message']['content']
            return answer
        except Exception as e:
            print(f"Error processing item: {e}")
            return None
    
    analysis_result = call_gpt(original_info, question)
    return analysis_result

def generate_fake_info(REQUEST_PROMPT, original_info, picture_url=None):
    '''
    生成虚假信息
    Args:
        original_info (str): 原始消息或者主题
        picture_url (Optional[str]): 参考图片
    Returns:
        rumor (str): 生成的虚假信息
    '''
    import sys
    sys.path.append("/Users/clb/Desktop/project/code/paper/utils")
    from call_openai import call_openai_single

    def call_gpt(PROMPT, original_info, picture_url):
        content = [PROMPT, original_info, picture_url]
        try:
            answer = call_openai_single(content, model='gpt-4o-2024-11-20')['choices'][0]['message']['content']
            return answer
        except Exception as e:
            print(f"Error processing item: {e}")
            return None
        
    rumor = call_gpt(REQUEST_PROMPT, original_info, picture_url)
    return rumor

if __name__=="__main__":
    question = "why the mother revealed to her child in a letter after her death that she had just one eye?" 
    original_info = "A mother revealed to her child in a letter after her death that she had just one eye because she had donated the other to him.	November 6, 2011	The one-eyed mother story expounds upon two moral messages: the unconditional, all-encompassing love we expect mothers to always feel for their children, and the admonition to not put off cherishing loved ones and appreciating their sacrifices while they’re still around.	"
    print(understand_fake_info(original_info, question))
    