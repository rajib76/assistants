import openai
from openai.types.beta.assistant_create_params import ToolAssistantToolsRetrieval

from assistants.langassist.base import BaseAssistant
from assistants.langregister.mongo_db_atlas import MongoAtlas


class SummarizeAssistant(BaseAssistant):
    type: ToolAssistantToolsRetrieval = {"type": "retrieval"}
    file: str = ""
    model_name = "gpt-4-1106-preview"
    assistant_name: str = "summarize_assistant"

    INSTRUCTIONS = f"""You are a helpful summarization agent.You help summarize the content provided to you"""

    def list_assistant(self):
        assistants = openai.beta.assistants.list()
        return assistants

    def deploy_assistant(self, client=MongoAtlas()):
        try:
            self.register_assistant(client)
            file = openai.files.create(
                file=open(self.file, "rb"),
                purpose='assistants'
            )
            assistant = openai.beta.assistants.create(
                name=self.assistant_name,
                instructions=self.INSTRUCTIONS,
                model=self.model_name,
                tools=[self.type],
                file_ids=[file.id]
            )
            assistant_record = {"assistant_name": assistant.name, "assistant_id": assistant.id, "file_id": file.id}
            self.update_assistant(assistant_record, client)
            return file, assistant
        except Exception as e:
            print(e)

    def run_assistant(self, question, client=MongoAtlas()):
        assistant_record = {"assistant_name": self.assistant_name}
        _, assistant_id, file_id = client.get_assistant(assistant_record)
        thread = openai.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": question,
                    "file_ids": [file_id]
                }
            ]
        )

        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        _, answer = self.get_answer(run, thread)
        return answer

    def get_answer(self, run, thread):
        print("Looking for an answer to your question...")
        while run.status != "completed":
            run = openai.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        print("Phew, that was a lot of reading...")
        messages = openai.beta.threads.messages.list(
            thread_id=thread.id
        )

        annotations = messages.data[0].content[0].text.annotations
        message_content = messages.data[0].content[0].text.value
        return annotations, message_content

    def update_assistant(self, assistant_record, client=MongoAtlas()):
        client.update_assistant(assistant_record)

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
