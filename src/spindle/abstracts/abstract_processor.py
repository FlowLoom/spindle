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
        content = args[0] if args else kwargs.get('content')
        preprocessed = self._preprocess(content,  **kwargs)
        extracted = self._extract_content(preprocessed,  **kwargs)
        processed = self._main_process(extracted,  **kwargs)
        return self._postprocess(processed,  **kwargs)

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
