from abc import abstractmethod
from spindle.interfaces import ISerializer, ISerializerFactory

__All__ = ['AbstractSerializerFactory']


class AbstractSerializerFactory(ISerializerFactory):
    def create_serializer(self, format: str) -> ISerializer:
        serializer = self._create_serializer(format)
        return self._configure_serializer(serializer)

    @abstractmethod
    def _create_serializer(self, format: str) -> ISerializer:
        pass

    def _configure_serializer(self, serializer: ISerializer) -> ISerializer:
        # Default implementation does no additional configuration
        return serializer


