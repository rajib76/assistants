import builtins
from typing import List, Optional

import openai
from openai.types.beta import Assistant, Thread
from openai.types.beta.assistant_create_params import ToolAssistantToolsRetrieval, Tool

from assistants.langregister.mongo_db_atlas import MongoAtlas
from assistants.llm_assistants.assistants import Assistants


class OpenAIRetrievalAssistant(Assistants):
    assistant_id: str = ""
    assistant_name: str = ""
    type: ToolAssistantToolsRetrieval = {"type": "retrieval"}
    created_at: int = 0
    description: str = ""
    file: str = ""
    file_ids: List = []
    instructions: str = ""
    metadata: dict = {}
    model: str = "gpt-4-1106-preview"
    object: str = "assistant"
    tools: List[Tool] = None

    def deploy_assistant(self, client=MongoAtlas()):
        try:
            self.register_assistant(client)
            file = openai.files.create(
                file=open(self.file, "rb"),
                purpose='assistants'
            )
            assistant = openai.beta.assistants.create(
                name=self.assistant_name,
                instructions=self.instructions,
                model=self.model,
                tools=[self.type],
                file_ids=[file.id]
            )
            # assistant_record = {"assistant_name": assistant.name, "assistant_id": assistant.id, "file_id": file.id}
            assistant_record = self.get_assistant_metadata(assistant)
            self.update_assistant(assistant_record, client)
            return assistant
        except Exception as e:
            print(e)

    def register_assistant(self, client=MongoAtlas()):
        duplicate_assistant = False
        assistant_record = {"assistant_name": self.assistant_name}
        try:
            duplicate_assistant, _, _ = client.get_assistant(assistant_record)
        except Exception as e:
            print(e)

        if duplicate_assistant:
            raise Exception("Assistant with same name exists")
        else:
            client.add_assistant([assistant_record])

    def update_assistant(self, assistant_record, client=MongoAtlas()):
        client.update_assistant(assistant_record)

    def get_answer(self, run, thread, type: [Optional]):
        if type == "init":
            print("Initializing the assistant")
        else:
            print("Looking for an answer to your question...")

        while run.status != "completed":
            run = openai.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        if type == "init":
            print("Done initializing")
        else:
            print("Phew, that was a lot of reading...")

        messages = openai.beta.threads.messages.list(
            thread_id=thread.id
        )

        annotations = messages.data[0].content[0].text.annotations
        message_content = messages.data[0].content[0].text.value
        return annotations, message_content

    def init_assistant(self, greeting="Hi Summarizer", client=MongoAtlas()):
        assistant_record = {"assistant_name": self.assistant_name}
        _, assistant_id, file_id = client.get_assistant(assistant_record)
        thread = openai.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": greeting,
                    "file_ids": file_id
                }
            ]
        )

        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        _, answer = self.get_answer(run, thread, type="init")
        return answer, thread, assistant_id

    def ask_assistant(self, question, thread, assistant_id):
        messages = openai.beta.threads.messages.create(
            thread_id=thread.id,
            content=question,
            role="user"
        )
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id)
        _, answer = self.get_answer(run, thread, type="")
        answer = answer + "\n\n" + "What else can I help with?"
        return answer

    def destroy_thread(self, thread: Thread = None):
        try:
            if thread is None:
                raise Exception("Thread was not deleted as no thread id passed")
            status = openai.beta.threads.delete(thread_id=thread.id)
            if status.deleted:
                print("Deleting thread id: ", status.id)
                return True
            else:
                print(status)
                raise Exception("Thread could not be deleted")
        except Exception as e:
            print(e)

    def get_assistant_metadata(self, assistant: Assistant):
        id: str = assistant.id
        created_at: int = assistant.created_at
        description: str = assistant.description
        file_ids: List[str] = assistant.file_ids
        instructions: str = assistant.instructions
        metadata: builtins.object = assistant.metadata
        model: str = assistant.model
        name: str = assistant.name
        object = assistant.object
        tools: List = assistant.tools

        assistant_metadata = {
            "id": id,
            "name": name,
            "created_at": created_at,
            "description": description,
            "file_ids": file_ids,
            "instructions": instructions,
            "metadata": metadata,
            "model": model,
            "object": object,
            "tools": str(tools)
        }

        return assistant_metadata
