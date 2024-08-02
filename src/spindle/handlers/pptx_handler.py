from spindle.abstracts import AbstractHandler
from typing import Dict, Any
import json

__all__ = ['PPTXHandler']


class PPTXHandler(AbstractHandler):
    def __init__(self, output_file=None):
        self.output_file = output_file

    def handle(self, data: Dict[str, Any]) -> None:
        """
        Handle the processed PPTX data.
        """
        formatted_data = self.preprocess(data)
        self.write(formatted_data)

    def preprocess(self, data: Dict[str, Any]) -> str:
        """
        Preprocess the data by converting it to a JSON string.
        """
        return json.dumps(data, indent=2)

    def write(self, data: str) -> None:
        """
        Write the data to a file or stdout.
        """
        if self.output_file:
            with open(self.output_file, 'w') as f:
                f.write(data)
        else:
            print(data)
