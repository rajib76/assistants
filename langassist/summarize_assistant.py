import sqlite3

import openai
from openai.types.beta.assistant_create_params import ToolAssistantToolsRetrieval

from langassist.base import BaseAssistant


class SummarizeAssistant(BaseAssistant):
    type: ToolAssistantToolsRetrieval = {"type": "retrieval"}
    file: str = ""
    model_name = "gpt-4-1106-preview"
    assistant_name:str="summarize_assistant"

    INSTRUCTIONS = f"""You are a helpful summarization agent.You help summarize the content provided to you"""

    def deploy_assistant(self):
        file = openai.files.create(
            file=open(self.file, "rb"),
            purpose='assistants'
        )

        try:
            self.register_assistant()
            assistant = openai.beta.assistants.create(
                name=self.assistant_name,
                instructions=self.INSTRUCTIONS,
                model=self.model_name,
                tools=[self.type],
                file_ids=[file.id]
            )
            return file, assistant
        except Exception as e:
            print(e)



    def register_assistant(self):
        duplicate_assistant=False
        conn = sqlite3.connect('../assistant_db/assistants.db')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS assistants (id INTEGER PRIMARY KEY,assistant_name TEXT)""")

        cursor.execute("SELECT count(*) FROM assistants where assistant_name='{name}'".format(name=self.assistant_name))
        rows = cursor.fetchall()
        for row in rows:
            duplicate_assistant = True if row[0] > 0 else False

        if duplicate_assistant:
            raise Exception("Assistant with same name exists")
        else:
            cursor.execute("INSERT INTO assistants (assistant_name) VALUES (?)", (self.assistant_name,))
            conn.commit()
            conn.close()