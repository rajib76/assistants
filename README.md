# Assistants
Developing language assistants with LLMs in a low-code way.

## Quick Install

Install using pip:

```bash
pip install langassist
```
The framework requires a database to register the assistants. The default database used is MongoAtlas. Future versions of the framework will support additional database types. Currently, there is a MongoDB collection named assistants which registers each assistant as shown below:

```
_id : 6556db6cf114addad09420c6
assistant_name: "test_assist"
assistant_id: "asst_52TLl1OdJW6ulmLCEsDlizz8"
file_id: "file-lZUBJ3ZnxtkTfqsuE0WYMXDI"

```
## What are Assistants?
Assistants is a framework for developing language-based assistants using micro agents, akin to the microservices concept. Each micro agent, like a microservice, can be independently developed and deployed. The framework adheres to the Single Responsibility Principle (SRP), allowing these assistants to be combined to address complex business processes through workflows.

## Capabilities of the Framework
In time, the framework will include built-in assistants for immediate deployment within OpenAI environments. It will also support the development of custom assistants.

## Contribution
Contributions are welcome in any form, be it through new features or improved documentation.

## Example Usage
The repository includes various examples demonstrating framework usage.
```commandline

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


```