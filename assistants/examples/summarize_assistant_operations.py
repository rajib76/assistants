# This is an example that shows how to use and deploy the summarization agent
# Deploy the agent first
# and then run the assistant
import os

from assistants.langassist.summarize_assistant import SummarizeAssistant

from dotenv import load_dotenv

from assistants.langregister.mongo_db_atlas import MongoAtlas

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

mongo_client = MongoAtlas()
mongo_client.uri = "mongodb+srv://rajib76:{MONGO_PASSWORD}@cluster0.cp3rxai.mongodb.net/?retryWrites=true&w=majority".format(
    MONGO_PASSWORD=MONGO_PASSWORD)

assistant_name = "summarize_assistant_03"
file = "gen_ai.pdf"
def deploy_assistant():
    sc = SummarizeAssistant(file=file,assistant_name=assistant_name)
    fileobj, assistantobj = sc.deploy_assistant(mongo_client)
    print(fileobj,assistantobj)

def run_assistant():
    sc = SummarizeAssistant(assistant_name=assistant_name)
    question = "Summarize the content in 300 words. Please ensure all points are covered"
    print(sc.run_assistant(question,client=mongo_client))



if __name__ == "__main__":
    # First deploy
    # deploy_assistant()

    #Then run
    run_assistant()

