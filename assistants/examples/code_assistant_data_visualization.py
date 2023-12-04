import os

from dotenv import load_dotenv
from openai import OpenAI

from assistants.langregister.mongo_db_atlas import MongoAtlas
from assistants.llm_assistants.openai_assistants import OpenAIRetrievalAssistant, OpenAICodeInterpreterAssistant

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")


class DataVisulaizationCodeAssistant():
    def __init__(self):
        self.instructions = f"""You are a helpful data visualization assistant. When asked an operation on a dataset, you write and run code to create the visualization"""
        self.file = ["/Users/joyeed/assistants/assistants/assistants/example_data/titanic.csv"]
        self.assistant = OpenAICodeInterpreterAssistant(instructions=self.instructions,
                                                        assistant_name="data_viz_assistant",
                                                        files=self.file)
        self.mongo_client = MongoAtlas()
        self.mongo_client.uri = "mongodb+srv://rajib76:{MONGO_PASSWORD}@cluster0.cp3rxai.mongodb.net/?retryWrites=true&w=majority".format(
            MONGO_PASSWORD=MONGO_PASSWORD)

    def deploy_assistant(self):
        self.assistant.deploy_assistant(self.mongo_client)

    def ask_assisant(self):
        answer, thread, assistant_id = self.assistant.init_assistant(greeting="Hi", client=self.mongo_client)
        while True:
            question = input(answer + "\n")
            if question.lower() == "exit":
                answer = "Thanks for using my expertise"
                print(answer)
                deleted = self.assistant.destroy_thread(thread)
                if deleted:
                    print("Thread has been deleted")
                    exit(0)
            answer, image_message_content = self.assistant.ask_assistant(question, thread, assistant_id)
            print(answer, image_message_content)
            if image_message_content:
                self.store_image_outputs(image_message_content)

    def store_image_outputs(self, image_message_content):
        for image in image_message_content:
            client = OpenAI()
            image_data = client.files.content(image)
            image_data_bytes = image_data.read()

            with open(f"../example_data/{image}.png", "wb") as file:
                file.write(image_data_bytes)


if __name__ == "__main__":
    sc = DataVisulaizationCodeAssistant()
    # sc.deploy_assistant()
    sc.ask_assisant()
