from spindle.interfaces import IHandler, ISerializer
from abc import abstractmethod
from typing import Dict, List, Any, Union
from spindle.exceptions import SerializationException

__All__ = ["AbstractHandler"]


class AbstractHandler(IHandler):
    def __init__(self, serializer: ISerializer):
        self.serializer = serializer

    def handle(self, data: Union[Dict[str, Any], str]) -> None:
        try:
            if isinstance(data, str):
                # If data is a string, assume it's serialized and decode it
                data = self.serializer.decode(data)
            preprocessed_data = self.preprocess(data)
            serialized_data = self.serializer.encode(preprocessed_data)
            self.write(serialized_data)
        except SerializationException as e:
            print(f"Serialization error: {e}")
        except Exception as e:
            print(f"Error handling data: {e}")

    @abstractmethod
    def preprocess(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Preprocess the data before serialization."""
        pass
