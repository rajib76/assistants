from abc import abstractmethod

from pydantic.v1 import BaseModel


class BaseAssistant(BaseModel):

    @abstractmethod
    def deploy_assistant(self):
        pass

    @abstractmethod
    def register_assistant(self):
        pass

