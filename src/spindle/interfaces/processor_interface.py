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
    def process(self, content: Any) -> Any:
        """
        Process the given content.
        This method orchestrates the entire processing workflow.

        Args:
            content (Any): The content to be processed.

        Returns:
            Any: The fully processed content.
        """
        pass

    @abstractmethod
    def _preprocess(self, content: Any) -> Any:
        """
        Preprocess the content before extraction and main processing.

        Args:
            content (Any): The content to be preprocessed.

        Returns:
            Any: The preprocessed content.
        """
        pass

    @abstractmethod
    def _extract_content(self, content: Any) -> Any:
        """
        Extract relevant content from the preprocessed data.

        Args:
            content (Any): The content to extract from.

        Returns:
            Any: The extracted content.
        """
        pass

    @abstractmethod
    def _main_process(self, content: Any) -> Any:
        """
        Main processing step.

        Args:
            content (Any): The content to be processed.

        Returns:
            Any: The processed content.
        """
        pass

    @abstractmethod
    def _postprocess(self, content: Any) -> Any:
        """
        Postprocess the content after main processing.

        Args:
            content (Any): The content to be postprocessed.

        Returns:
            Any: The postprocessed content.
        """
        pass