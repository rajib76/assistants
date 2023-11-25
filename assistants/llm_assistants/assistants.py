from abc import abstractmethod

from openai.types.beta import Thread
from pydantic.v1 import BaseModel


class Assistants(BaseModel):

    @abstractmethod
    def deploy_assistant(self):
        pass

    @abstractmethod
    def register_assistant(self):
        pass

    @abstractmethod
    def init_assistant(self, question="Hi"):
        pass

    @abstractmethod
    def ask_assistant(self,question,thread,assistant_id):
        pass

    @abstractmethod
    def update_assistant(self,assistant_record):
        pass

    @abstractmethod
    def destroy_thread(self):
        pass

