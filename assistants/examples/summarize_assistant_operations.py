import os

from assistants.langassist.summarize_assistant import SummarizeAssistant

from dotenv import load_dotenv

from assistants.langregister.mongo_db_atlas import MongoAtlas

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

if __name__ == "__main__":
    # deploy the summarization assistant
    mongo_client = MongoAtlas()
    mongo_client.uri =  "mongodb+srv://rajib76:{MONGO_PASSWORD}@cluster0.cp3rxai.mongodb.net/?retryWrites=true&w=majority".format(
        MONGO_PASSWORD=MONGO_PASSWORD)

    file = "/Users/joyeed/assistants/assistants/assistants/example_data/gen_ai.pdf"
    assistant_name = "summarize_assistant_01"
    # sc = SummarizeAssistant(file=file,
    #                         assistant_name=assistant_name)
    # sc.deploy_assistant(mongo_client)

    # Run the assistant
    sc = SummarizeAssistant(assistant_name=assistant_name)
    question = "Summarize the content in 300 words. Please ensure all points are covered"
    print(sc.run_assistant(question,client=mongo_client))