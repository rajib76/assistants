import builtins
import json
from typing import List, Any

from openai.types.beta import Assistant
from openai.types.beta.assistant import Tool


def get_assistant_metadata(assistant:Assistant):
    id:str = assistant.id
    created_at:int = assistant.created_at
    description:str = assistant.description
    file_ids:List[str] = assistant.file_ids
    instructions:str = assistant.instructions
    metadata:builtins.object = assistant.metadata
    model:str = assistant.model
    name:str = assistant.name
    object = assistant.object
    tools:List = assistant.tools

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
        "tools": tools
    }

    # Serialize the dictionary to JSON
    print(assistant_metadata)
    # assistant_metadata_json = json.dumps(assistant_metadata, indent=4)
    # print(assistant_metadata_json)

    return assistant_metadata



