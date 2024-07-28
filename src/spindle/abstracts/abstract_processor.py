from typing import Any
from spindle.interfaces import IProcessor

__All__ = ["AbstractProcessor"]


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
        processed = self._main_process(preprocessed)
        return self._postprocess(processed)

    def _preprocess(self, content: Any) -> Any:
        """
        Preprocess the content before main processing.

        This method is intended for any initial cleaning or preparation of the content.

        Args:
            content (Any): The content to be preprocessed.

        Returns:
            Any: The preprocessed content.

        Raises:
            NotImplementedError: If not implemented by a subclass.
        """
        raise NotImplementedError("_preprocess must be implemented by subclasses")

    def _main_process(self, content: Any) -> Any:
        """
        Main processing step.

        This method should contain the core processing logic.

        Args:
            content (Any): The content to be processed.

        Returns:
            Any: The processed content.

        Raises:
            NotImplementedError: If not implemented by a subclass.
        """
        raise NotImplementedError("_main_process must be implemented by subclasses")

    def _postprocess(self, content: Any) -> Any:
        """
        Postprocess the content after main processing.

        This method is intended for any final adjustments or formatting of the processed content.

        Args:
            content (Any): The content to be postprocessed.

        Returns:
            Any: The postprocessed content.

        Raises:
            NotImplementedError: If not implemented by a subclass.
        """
        raise NotImplementedError("_postprocess must be implemented by subclasses")