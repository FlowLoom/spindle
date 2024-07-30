from abc import ABC, abstractmethod
from typing import Any

__All__ = ["IProcessor"]


class IProcessor(ABC):
    """
    Interface for a content processor.

    This abstract base class defines the structure and workflow for processing content.
    Concrete implementations should provide specific logic for each processing step.
    """

    @abstractmethod
    def process(self, *args: Any, **kwargs: Any) -> Any:
        """
        Process the given content.
        This method orchestrates the entire processing workflow.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The fully processed content.
        """
        pass

    @abstractmethod
    def _preprocess(self, *args: Any, **kwargs: Any) -> Any:
        """
        Preprocess the content before extraction and main processing.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The preprocessed content.
        """
        pass

    @abstractmethod
    def _extract_content(self, *args: Any, **kwargs: Any) -> Any:
        """
        Extract relevant content from the preprocessed data.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The extracted content.
        """
        pass

    @abstractmethod
    def _main_process(self, *args: Any, **kwargs: Any) -> Any:
        """
        Main processing step.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The processed content.
        """
        pass

    @abstractmethod
    def _postprocess(self, *args: Any, **kwargs: Any) -> Any:
        """
        Postprocess the content after main processing.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The postprocessed content.
        """
        pass

