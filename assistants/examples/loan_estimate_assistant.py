import os

from dotenv import load_dotenv

from assistants.langregister.mongo_db_atlas import MongoAtlas
from assistants.llm_assistants.openai_assistants import OpenAIRetrievalAssistant

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

instructions = f"""You are a helpful assistant who helps answering questions from a loan estimate"""
file = "../example_data/loan_estimate.pdf"

assistant = OpenAIRetrievalAssistant(instructions=instructions,
                                     assistant_name="loan_estimate_assistant",
                                     file=file
)
mongo_client = MongoAtlas()
mongo_client.uri = "mongodb+srv://rajib76:{MONGO_PASSWORD}@cluster0.cp3rxai.mongodb.net/?retryWrites=true&w=majority".format(
    MONGO_PASSWORD=MONGO_PASSWORD)

# assistant.deploy_assistant(client=mongo_client)

answer, thread, assistant_id = assistant.init_assistant(client=mongo_client)
while True:
    question = input(answer + "\n")
    if question.lower() == "exit":
        answer = "Thanks for using my expertise"
        print(answer)
        deleted = assistant.destroy_thread(thread)
        if deleted:
            print("Thread has been deleted")
            exit(0)
    answer = assistant.ask_assistant(question, thread, assistant_id)
