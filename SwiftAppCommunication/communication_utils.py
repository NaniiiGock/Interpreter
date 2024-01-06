import asyncio
from abc import ABC
from typing import abstractmethod
from enum import Enum



class ClientServerCommunicationProtocol(ABC):
    @abstractmethod 
    def for_SendingUserInput(message_uuid: int, user_input: str, date: str):pass

    @abstractmethod
    def for_ReturningLLMResponse(message_uuid: int, llm_response: str, statusCode: int): pass

    @abstractmethod
    def for_SendingConfirmation(message_uuid: int): pass

    @abstractmethod
    def for_ReturningCommandsResults(message_uuid: int, std_out: str, std_err: str, statusCode: int): pass

    @abstractmethod
    def for_AskingRerun(message_uuid: int): pass

    @abstractmethod
    def for_SaveToBookmarks(message_uuid: int): pass

    @abstractmethod
    def for_RemoveFromBookmarks(message_uuid: int): pass

    @abstractmethod
    def for_DeleteAllUnsavedFromDB(): pass

    @abstractmethod
    def for_DeleteUserMessage(message_uuid: int): pass
