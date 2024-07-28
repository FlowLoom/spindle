from spindle.abstracts import AbstractSerializerFactory, ISerializer
from spindle.serializers import JSONSerializer, PlainTextSerializer

__All__ = ['SerializerFactory']


class SerializerFactory(AbstractSerializerFactory):
    def _create_serializer(self, format: str) -> ISerializer:
        if format.lower() == 'json':
            return JSONSerializer()
        elif format.lower() == 'plaintext':
            return PlainTextSerializer()
        else:
            raise ValueError(f"Unsupported serialization format: {format}")