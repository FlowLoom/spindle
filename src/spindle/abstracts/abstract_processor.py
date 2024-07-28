from spindle.interfaces import IProcessor
from abc import abstractmethod
from typing import Any

__All__ = ['AbstractProcessor']


class AbstractProcessor(IProcessor):
    """
    An abstract base class for content processors implementing the IProcessor interface.

    This class defines the structure for content processing with preprocessing, main processing,
    and postprocessing steps. Subclasses must implement the _preprocess, _main_process, and
    _postprocess methods.
    """

    def process(self, content: Any) -> Any:
        """
        Process the given content.
        This method orchestrates the entire processing workflow.

        Args:
            content (Any): The content to be processed.

        Returns:
            Any: The fully processed content.
        """
        preprocessed = self._preprocess(content)
        #extracted = self._extract_content(preprocessed)
        processed = self._main_process(preprocessed)
        return self._postprocess(processed)

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