from spindle.abstracts import AbstractSerializerFactory, ISerializer
from spindle.serializers import JSONSerializer, PlainTextSerializer, YAMLSerializer
from typing import Dict, List, Type


__All__ = ['SerializerFactory']


class SerializerFactory(AbstractSerializerFactory):
    def __init__(self):
        self._serializers: Dict[str, Type[ISerializer]] = {
            'json': JSONSerializer,
            'plaintext': PlainTextSerializer,
            'yaml': YAMLSerializer,
        }

    def _create_serializer(self, format: str) -> ISerializer:
        format = format.lower()
        if format not in self._serializers:
            raise ValueError(f"Unsupported serialization format: {format}")
        return self._serializers[format]()

    def register_serializer(self, format: str, serializer_class: Type[ISerializer]) -> None:
        """
        Register a new serializer type.
        """
        self._serializers[format.lower()] = serializer_class

    def unregister_serializer(self, format: str) -> None:
        """
        Unregister a serializer type.
        """
        format = format.lower()
        if format in self._serializers:
            del self._serializers[format]

    def get_supported_formats(self) -> List[str]:
        """
        Get a list of supported serialization formats.
        """
        return list(self._serializers.keys())