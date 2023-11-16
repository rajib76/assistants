import ast
import os

import openai
import requests
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


def deploy_assistant():
    tool_list = [{
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
    }, {
        "type": "function",
        "function": {
            "name": "getNickname",
            "description": "Get the nickname of a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
                },
                "required": ["location"]
            }
        }
    }]

    # Add the file to the assistant
    assistant = openai.beta.assistants.create(
        name="injection_identifier_assistant",
        instructions="You are a weather bot. Use the provided functions to answer questions.",
        model="gpt-4-1106-preview",
        tools=tool_list
    )

    return assistant


def run_assistant(assistant_id, question):
    thread = openai.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    return run, thread


def get_function_name(run, thread):
    print("Looking for an answer to your question...")
    while run.status != "requires_action":
        run = openai.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    print(run)
    functions = run.required_action.submit_tool_outputs.tool_calls
    tool_calls = run.required_action.submit_tool_outputs.tool_calls
    # print("ttt ", run.required_action.submit_tool_outputs.tool_calls[0].id)
    #
    # print("Phew, that was a lot of reading...")
    # messages = openai.beta.threads.messages.list(
    #     thread_id=thread.id
    # )
    # print(messages)
    # # print(messages.data[0].content[0].text.value)
    # annotations = messages.data[0].content[0].text.annotations
    # message_content = messages.data[0].content[0].text.value
    # tool_call_id = run.required_action.submit_tool_outputs.tool_calls
    return functions,tool_calls


def get_answer(run, thread):
    print("Looking for an answer to your question...")
    while run.status != "completed":
        run = openai.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(run.status)

    print("Phew, that was a lot of reading...")
    messages = openai.beta.threads.messages.list(
        thread_id=thread.id
    )
    print(messages)
    # print(messages.data[0].content[0].text.value)
    annotations = messages.data[0].content[0].text.annotations
    message_content = messages.data[0].content[0].text.value
    return annotations, message_content


def execute_run(run, thread, tool_call_id,temp):
    run = openai.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=[
            {
                "tool_call_id": tool_call_id[0].id,
                "output": temp,
            }
        ]
    )


def getCurrentWeather(location, unit="c"):
    return "26C"


if __name__ == "__main__":
    # assistant = deploy_assistant()
    # print(assistant)
    run, thread = run_assistant("asst_ZDB6kA9gHNVG6zenjAcbLU6W", "what is the weather in LA in celsius?")
    print(run)
    print(thread)
    functions,tool_calls = get_function_name(run, thread)
    for function in functions:
        name = function.function.name
        arguments = ast.literal_eval(function.function.arguments)
        # print("Function name :", name)
        # print("arguments :", arguments)
        location = arguments["location"]
        unit = arguments["unit"]
        # print(location,unit)
        temp = eval(name)(location,unit)
        print(temp)
    # print(len(tool_call_id))
        run_execution = execute_run(run,thread,tool_calls,temp)
        a,m=get_answer(run,thread)
        print(m)
