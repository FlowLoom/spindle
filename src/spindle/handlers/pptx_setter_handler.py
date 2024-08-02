from spindle.abstracts import AbstractHandler
from typing import Dict, Any
import click

__all__ = ['PPTXSetterHandler']


class PPTXSetterHandler(AbstractHandler):
    def __init__(self, output_file):
        self.output_file = output_file

    def handle(self, data: Dict[str, Any]) -> None:
        """
        Handle the processed PPTX data.
        """
        presentation = data['presentation']
        self.write(presentation)

    def preprocess(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocess the data. In this case, we're just passing it through.
        """
        return data

    def write(self, presentation) -> None:
        """
        Write the modified presentation to a file.
        """
        presentation.save(self.output_file)
        click.echo(f"Modified presentation saved to {self.output_file}")
