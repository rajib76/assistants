from abc import abstractmethod
from typing import Any

from pydantic.v1 import BaseModel


class RegistrationClient(BaseModel):
    client:Any = None

    @abstractmethod
    def get_client(self):
        pass
    @abstractmethod
    def add_assistant(self,assistant_record):
        pass
    @abstractmethod
    def update_assistant(self,assistant_record):
        pass
    @abstractmethod
    def delete_assistant(self,assistant_record):
        pass