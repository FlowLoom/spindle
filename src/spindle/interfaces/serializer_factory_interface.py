from abc import ABC, abstractmethod
from .serializer_interface import ISerializer

__All__ = ['ISerializerFactory']


class ISerializerFactory(ABC):
    @abstractmethod
    def create_serializer(self, format: str) -> ISerializer:
        pass