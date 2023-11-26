import os

from dotenv import load_dotenv

from assistants.langregister.mongo_db_atlas import MongoAtlas
from assistants.llm_assistants.openai_assistants import OpenAIRetrievalAssistant

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")


class SummarizationAgent():
    def __init__(self):
        self.instructions = f"""You are a helpful summarization agent.You help summarize the content provided to you"""
        self.file = ["/Users/joyeed/assistants/assistants/assistants/example_data/gen_ai.pdf"]
        self.assistant = OpenAIRetrievalAssistant(instructions=self.instructions,
                                                  assistant_name="summarize_assistant",
                                                  files=self.file)
        self.mongo_client = MongoAtlas()
        self.mongo_client.uri = "mongodb+srv://rajib76:{MONGO_PASSWORD}@cluster0.cp3rxai.mongodb.net/?retryWrites=true&w=majority".format(
            MONGO_PASSWORD=MONGO_PASSWORD)

    def deploy_assistant(self):
        self.assistant.deploy_assistant(self.mongo_client)

    def ask_assisant(self):
        answer, thread, assistant_id = self.assistant.init_assistant(greeting="Hi",client=self.mongo_client)
        while True:
            question = input(answer + "\n")
            if question.lower() == "exit":
                answer = "Thanks for using my expertise"
                print(answer)
                deleted = self.assistant.destroy_thread(thread)
                if deleted:
                    print("Thread has been deleted")
                    exit(0)
            answer = self.assistant.ask_assistant(question, thread, assistant_id)
            print(answer)


if __name__ == "__main__":
    sc = SummarizationAgent()
    # sc.deploy_assistant()
    sc.ask_assisant()
