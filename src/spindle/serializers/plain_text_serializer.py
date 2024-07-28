from typing import Dict, Any
from spindle.exceptions import SerializationException
from spindle.interfaces import ISerializer

_All_ = ["PlainTextSerializer"]

# TODO: Create a abstract class for all serializers
class PlainTextSerializer(ISerializer):
    def encode(self, data: Dict[str, Any]) -> str:
        try:
            return "\n".join([f"{k}: {v}" for k, v in data.items()])
        except Exception as e:
            raise SerializationException(f"PlainText serialization error: {str(e)}")

    def decode(self, data: str) -> Dict[str, Any]:
        try:
            return dict(line.split(": ", 1) for line in data.split("\n") if line)
        except Exception as e:
            raise SerializationException(f"PlainText deserialization error: {str(e)}")
