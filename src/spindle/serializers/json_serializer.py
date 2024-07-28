import json
from typing import Dict, Any
from spindle.exceptions import SerializationException
from spindle.interfaces import ISerializer

__All__ = ["JSONSerializer"]

# TODO: Create a abstract class for all serializers
class JSONSerializer(ISerializer):
    def encode(self, data: Dict[str, Any]) -> str:
        try:
            return json.dumps(data, indent=2)
        except (TypeError, ValueError) as e:
            raise SerializationException(f"JSON serialization error: {str(e)}")

    def decode(self, data: str) -> Dict[str, Any]:
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            raise SerializationException(f"JSON deserialization error: {str(e)}")