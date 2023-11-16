import os

from dotenv import load_dotenv

from langassist.summarize_assistant import SummarizeAssistant

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

if __name__=="__main__":
    sc = SummarizeAssistant(file="/Users/joyeed/assistants/assistants/example_data/gen_ai.pdf",assistant_name="test_assist")
    sc.deploy_assistant()
