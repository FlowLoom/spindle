import logging
from typing import List, Dict, Any, Union
from spindle.interfaces import IHandler, ISerializer
from spindle.exceptions import HandlerException

__All__ = ['CompositeHandler']


class CompositeHandler(IHandler):
    """
    A handler that composes multiple other handlers and delegates operations to them.
    This handler allows for combining multiple output strategies (e.g., file and console output).
    """

    def __init__(self):
        self.handlers: List[IHandler] = []
        self.logger = logging.getLogger(self.__class__.__name__)

    def add_handler(self, handler: IHandler) -> None:
        """
        Add a handler to the composite.

        Args:
            handler (IHandler): The handler to add.
        """
        if handler not in self.handlers:
            self.handlers.append(handler)
            self.logger.info(f"Added handler: {handler.__class__.__name__}")
        else:
            self.logger.warning(f"Handler already exists: {handler.__class__.__name__}")

    def remove_handler(self, handler: IHandler) -> None:
        """
        Remove a handler from the composite.

        Args:
            handler (IHandler): The handler to remove.
        """
        if handler in self.handlers:
            self.handlers.remove(handler)
            self.logger.info(f"Removed handler: {handler.__class__.__name__}")
        else:
            self.logger.warning(f"Handler not found: {handler.__class__.__name__}")

    def handle(self, data: Union[Dict[str, Any], str]) -> None:
        """
        Process and write the data using all contained handlers.

        Args:
            data (Union[Dict[str, Any], str]): The data to be handled.
        """
        if not self.handlers:
            raise HandlerException("No handlers available in the composite.")

        for handler in self.handlers:
            try:
                handler.handle(data)
            except Exception as e:
                self.logger.error(f"Error in handler {handler.__class__.__name__}: {str(e)}")
                # Optionally, re-raise the exception if you want to stop processing
                # raise HandlerException(f"Error in handler {handler.__class__.__name__}: {str(e)}") from e

    def write(self, data: str) -> None:
        """
        Write the data using all contained handlers.

        Args:
            data (str): The data to be written.
        """
        if not self.handlers:
            raise HandlerException("No handlers available in the composite.")

        for handler in self.handlers:
            try:
                handler.write(data)
            except Exception as e:
                self.logger.error(f"Error in handler {handler.__class__.__name__}: {str(e)}")
                # Optionally, re-raise the exception if you want to stop processing
                # raise HandlerException(f"Error in handler {handler.__class__.__name__}: {str(e)}") from e

    def get_handler_count(self) -> int:
        """
        Get the number of handlers in the composite.

        Returns:
            int: The number of handlers.
        """
        return len(self.handlers)

    def get_handler_types(self) -> List[str]:
        """
        Get a list of the types of handlers in the composite.

        Returns:
            List[str]: A list of handler class names.
        """
        return [handler.__class__.__name__ for handler in self.handlers]

    def clear_handlers(self) -> None:
        """
        Remove all handlers from the composite.
        """
        self.handlers.clear()
        self.logger.info("All handlers have been removed.")

    def set_serializer_for_all(self, serializer: ISerializer) -> None:
        """
        Set the same serializer for all handlers that support it.

        Args:
            serializer (ISerializer): The serializer to set.
        """
        for handler in self.handlers:
            if hasattr(handler, 'serializer'):
                handler.serializer = serializer
        self.logger.info(f"Set serializer {serializer.__class__.__name__} for all compatible handlers.")

# Usage example
if __name__ == "__main__":
    from spindle.handlers import FileHandler, ConsoleHandler
    from spindle.serializers import JSONSerializer, PlainTextSerializer

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Create serializers
    json_serializer = JSONSerializer()
    plaintext_serializer = PlainTextSerializer()

    # Create individual handlers
    file_handler = FileHandler(json_serializer, "output.json")
    console_handler = ConsoleHandler(plaintext_serializer)

    # Create composite handler
    composite_handler = CompositeHandler()
    composite_handler.add_handler(file_handler)
    composite_handler.add_handler(console_handler)

    # Sample data
    data = {"key1": "value1", "key2": "value2"}

    # Handle data
    composite_handler.handle(data)

    # Get handler information
    print(f"Number of handlers: {composite_handler.get_handler_count()}")
    print(f"Handler types: {composite_handler.get_handler_types()}")

    # Change serializer for all handlers
    new_serializer = JSONSerializer()
    composite_handler.set_serializer_for_all(new_serializer)

    # Handle data again with new serializer
    composite_handler.handle(data)

    # Remove a handler
    composite_handler.remove_handler(file_handler)

    # Clear all handlers
    composite_handler.clear_handlers()