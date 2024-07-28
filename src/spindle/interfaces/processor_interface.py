from abc import ABC, abstractmethod
from typing import Any

__All__ = ['IProcessor']

class IProcessor(ABC):
    """
    An abstract base class defining the interface for content processors.

    This class provides a template for implementing content processing workflows
    with distinct preprocessing, main processing, and postprocessing steps.
    """

    @abstractmethod
    def process(self, content: Any) -> Any:
        """
        Process the given content.

        This method orchestrates the entire processing workflow by calling
        _preprocess, _main_process, and _postprocess methods in sequence.

        Args:
            content (Any): The content to be processed.

        Returns:
            Any: The fully processed content.
        """

        pass

    @abstractmethod
    def _preprocess(self, content: Any) -> Any:
        """
        Preprocess the content before main processing.

        This method is intended for any initial cleaning or preparation of the content.

        Args:
            content (Any): The content to be preprocessed.

        Returns:
            Any: The preprocessed content.
        """

        pass

    @abstractmethod
    def _main_process(self, content: Any) -> Any:
        """
        Main processing step.

        This method should contain the core processing logic.

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

        This method is intended for any final adjustments or formatting of the processed content.

        Args:
            content (Any): The content to be postprocessed.

        Returns:
            Any: The postprocessed content.
        """

        pass