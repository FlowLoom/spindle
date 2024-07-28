from typing import Any, Dict
import yaml
from spindle.exceptions import SerializationException
from spindle.interfaces import ISerializer

__All__ = ["YAMLSerializer"]


class YAMLSerializer(ISerializer):
    def encode(self, data: Dict[str, Any]) -> str:
        try:
            return yaml.dump(data, default_flow_style=False)
        except yaml.YAMLError as e:
            raise SerializationException(f"YAML serialization error: {str(e)}")

    def decode(self, data: str) -> Dict[str, Any]:
        try:
            return yaml.safe_load(data)
        except yaml.YAMLError as e:
            raise SerializationException(f"YAML deserialization error: {str(e)}")