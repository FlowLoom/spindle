import sys
from typing import Dict, Any, Union
from enum import Enum
import logging
from spindle.serializers import ISerializer, SerializationException
from spindle.abstracts import AbstractHandler

__All__ = ["Color", "ConsoleHandler"]

class Color(Enum):
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'

class ConsoleHandler(AbstractHandler):
    def __init__(self, serializer: ISerializer, color: Color = None, indent: int = 0, prefix: str = '', use_stderr: bool = False):
        super().__init__(serializer)
        self.color = color
        self.indent = indent
        self.prefix = prefix
        self.use_stderr = use_stderr
        self.logger = logging.getLogger(self.__class__.__name__)

    def preprocess(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocess the data before serialization.
        This method can be overridden in subclasses to implement specific preprocessing logic.
        """
        # Example preprocessing: add a type indicator to the data
        data['_type'] = 'console_output'
        return data

    def write(self, data: str) -> None:
        """
        Write the serialized data to the console.
        """
        try:
            # Apply indentation and prefix
            formatted_data = self._format_output(data)

            # Apply color if specified
            if self.color:
                formatted_data = f"{self.color.value}{formatted_data}{Color.RESET.value}"

            # Write to console
            output_stream = sys.stderr if self.use_stderr else sys.stdout
            print(formatted_data, file=output_stream)

            self.logger.debug("Data successfully written to console")

        except IOError as e:
            self.logger.error(f"Error writing to console: {e}")
            raise

    def handle(self, data: Union[Dict[str, Any], str]) -> None:
        """
        Process and write the data to the console.
        """
        try:
            # If data is already a string, assume it's serialized
            if isinstance(data, str):
                serialized_data = data
            else:
                preprocessed_data = self.preprocess(data)
                serialized_data = self.serializer.encode(preprocessed_data)

            self.write(serialized_data)

        except SerializationException as e:
            self.logger.error(f"Serialization error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error handling data: {e}")
            raise

    def _format_output(self, data: str) -> str:
        """
        Apply indentation and prefix to the output.
        """
        lines = data.split('\n')
        indentation = ' ' * self.indent
        return '\n'.join(f"{self.prefix}{indentation}{line}" for line in lines)


    def set_color(self, color: Color) -> None:
        """
        Set the output color.
        """
        self.color = color

    def set_indent(self, indent: int) -> None:
        """
        Set the indentation level.
        """
        self.indent = max(0, indent)  # Ensure non-negative indentation

    def set_prefix(self, prefix: str) -> None:
        """
        Set the output prefix.
        """
        self.prefix = prefix

    def set_use_stderr(self, use_stderr: bool) -> None:
        """
        Set whether to use stderr instead of stdout.
        """
        self.use_stderr = use_stderr

    def clear_screen(self) -> None:
        """
        Clear the console screen.
        """
        print("\033c", end="")

    def print_separator(self, char: str = '-', length: int = 50) -> None:
        """
        Print a separator line to the console.
        """
        self.write(char * length)

# Usage example
if __name__ == "__main__":
    from serializers import ConcreteSerializerFactory

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Create serializer
    serializer_factory = ConcreteSerializerFactory()
    json_serializer = serializer_factory.create_serializer('json')

    # Create ConsoleHandler
    console_handler = ConsoleHandler(json_serializer, color=Color.CYAN, indent=2, prefix=">> ")

    # Sample data
    data = {"key1": "value1", "key2": "value2"}

    # Handle data
    console_handler.handle(data)

    # Change color and print separator
    console_handler.set_color(Color.YELLOW)
    console_handler.print_separator('=', 30)

    # Handle another piece of data
    data2 = {"key3": "value3"}
    console_handler.handle(data2)

    # Clear screen
    # console_handler.clear_screen()