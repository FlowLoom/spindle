import traceback
from typing import Optional, Any

__All__ = ['HandlerException']


class HandlerException(Exception):
    """
    Custom exception class for handler-related errors.

    This exception provides additional context and debugging information
    for errors that occur during the handling process.

    Attributes:
        message (str): The error message.
        handler_name (str): The name of the handler where the error occurred.
        data (Any): The data being processed when the error occurred.
        original_exception (Exception): The original exception that was caught, if any.
    """

    def __init__(self, message: str, handler_name: Optional[str] = None,
                 data: Optional[Any] = None, original_exception: Optional[Exception] = None):
        """
        Initialize the HandlerException.

        Args:
            message (str): The error message.
            handler_name (Optional[str]): The name of the handler where the error occurred.
            data (Optional[Any]): The data being processed when the error occurred.
            original_exception (Optional[Exception]): The original exception that was caught, if any.
        """
        self.message = message
        self.handler_name = handler_name
        self.data = data
        self.original_exception = original_exception
        self.traceback = traceback.format_exc()

        # Construct the full error message
        full_message = f"Handler Error: {message}"
        if handler_name:
            full_message += f" (in handler: {handler_name})"
        if original_exception:
            full_message += f"\nOriginal Exception: {str(original_exception)}"

        super().__init__(full_message)

    def __str__(self):
        """
        Return a string representation of the exception.

        Returns:
            str: A formatted string containing all relevant error information.
        """
        result = f"HandlerException: {self.message}"
        if self.handler_name:
            result += f"\nHandler: {self.handler_name}"
        if self.data:
            result += f"\nData: {str(self.data)[:100]}..."  # Truncate data if it's too long
        if self.original_exception:
            result += f"\nOriginal Exception: {str(self.original_exception)}"
        result += f"\nTraceback:\n{self.traceback}"
        return result

    def get_details(self) -> dict:
        """
        Get a dictionary containing all the details of the exception.

        This method is useful for logging or serializing the exception information.

        Returns:
            dict: A dictionary containing all exception details.
        """
        return {
            "message": self.message,
            "handler_name": self.handler_name,
            "data": str(self.data)[:100] if self.data else None,  # Truncate data if it's too long
            "original_exception": str(self.original_exception) if self.original_exception else None,
            "traceback": self.traceback
        }

# Usage example
if __name__ == "__main__":
    try:
        # Simulate an error in a handler
        raise ValueError("Simulated error in handler")
    except ValueError as e:
        # Catch the error and wrap it in a HandlerException
        handler_exception = HandlerException(
            message="Failed to process data",
            handler_name="ExampleHandler",
            data={"sample": "data"},
            original_exception=e
        )

        # Print the exception
        print(handler_exception)

        # Get and print the exception details
        details = handler_exception.get_details()
        print("\nException Details:")
        for key, value in details.items():
            print(f"{key}: {value}")