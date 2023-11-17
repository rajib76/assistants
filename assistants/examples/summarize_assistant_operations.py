import os

from assistants.langassist.summarize_assistant import SummarizeAssistant

from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

if __name__ == "__main__":
    # deploy the summarization assistant
    file = "gen_ai.pdf"
    assistant_name = "summarize_assistant"
    # sc = SummarizeAssistant(file=file,
    #                         assistant_name=assistant_name)
    # sc.deploy_assistant()

    # Run the assistant
    sc = SummarizeAssistant(assistant_name=assistant_name)
    question = "Summarize the content in 300 words. Please ensure all points are covered"
    print(sc.run_assistant(question))