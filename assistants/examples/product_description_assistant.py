import ast
import base64
import mimetypes
import os

from dotenv import load_dotenv
from openai import OpenAI

from assistants.langregister.mongo_db_atlas import MongoAtlas
from assistants.llm_assistants.openai_assistants import OpenAIFunctionCallingAssistant

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")


def getCurrentWeather(location, unit="c"):
    return "26C"


def get_product_description(image_source,question):
    client = OpenAI(api_key=OPENAI_API_KEY)
    image_url = ""
    """ This function automatically determines the MIME type and encodes the image to base64."""
    mime_type, _ = mimetypes.guess_type(image_source)
    if mime_type is None:
        raise ValueError(f"Mime type determination failed for {image_source}")

    with open(image_source, "rb") as image_content:
        encoded_image_string = base64.b64encode(image_content.read()).decode('utf-8')
        image_url = f"data:{mime_type};base64,{encoded_image_string}"

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url,
                                      "detail": "high", }
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content

instructions = f"""You are a helpful function calling bot. You output the function and the arguments required to be 
executed to get the answer """
tool_list = [{
    "type": "function",
    "function": {
        "name": "get_product_description",
        "description": "Get the product description based on the provided image",
        "parameters": {
            "type": "object",
            "properties": {
                "image_source": {"type": "string", "description": "The file name of the image"},
                "question": {"type": "string", "description": "The question to be answered"}
            },
            "required": ["image_source","question"]
        }
    }
},
    {
        "type": "function",
        "function": {
            "name": "getCurrentWeather",
            "description": "Get the weather in location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
                    "unit": {"type": "string", "enum": ["c", "f"]}
                },
                "required": ["location", "unit"]
            }
        }
    }
]


assistant = OpenAIFunctionCallingAssistant(instructions=instructions,
                                           assistant_name="function_calling_assistant",
                                           tools=tool_list,
                                           model="gpt-4-1106-preview"
                                           )
mongo_client = MongoAtlas()
mongo_client.uri = "mongodb+srv://rajib76:{MONGO_PASSWORD}@cluster0.cp3rxai.mongodb.net/?retryWrites=true&w=majority".format(
    MONGO_PASSWORD=MONGO_PASSWORD)

assistant.deploy_assistant(client=mongo_client)

# Initialize the assistant
# Returns
# answer : answer to the greeting
# thread : Thread object of the conversation
# assistant_id : Id of the assistant that will be used
answer, thread, assistant_id = assistant.init_assistant(client=mongo_client)

# This is the question that we will ask the assistant
question = "Please give detailed product description of the image /Users/joyeed/assistants/assistants/assistants/example_data/product_images/tv.jpg in a JSON format?"
# question = "What is the weather in CA"
# Calling the assistant with the question
# It will return the run object and all the functions that are required to be
# called to get the answer
run, functions = assistant.ask_assistant(question, thread, assistant_id)
print(functions)
# We are now getting the function name and the arguments to be used
# to call the function
tool_outputs = []
tool_output = {}
for function in functions:
    tool_call_id = function["tool_call_id"]
    function_name = function["function_name"]
    arguments = ast.literal_eval(function["arguments"])
    # This is where we are calling the function to get the response
    output = eval(function_name)(**arguments)
    # Now preparing the function output as tool_output which will
    # be sent to the assistant to get the final response
    tool_output["tool_call_id"] = tool_call_id
    tool_output["output"] = output
    tool_outputs.append(tool_output)
    tool_output = {}

# This is where we are calling the assistant again by passing the tool/function output
annotations, message_content = assistant.execute_run(run=run, thread=thread, tool_outputs=tool_outputs)
# This is the final answer from the assistant
print(message_content)

# Now, we are done, deleting the thread for this conversation
deleted = assistant.destroy_thread(thread)
if deleted:
    print("Thread has been deleted")
    exit(0)
else:
    print("Thread could not be deleted")