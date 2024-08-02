from spindle.abstracts import AbstractFetcher
from typing import Any, Dict
from pptx import Presentation

class PPTXSetterFetcher(AbstractFetcher):
    def _fetch_content(self, source: str, **kwargs: Any) -> Presentation:
        """
        Fetch content from a PPTX file.
        """
        return Presentation(source)

    def _process_content(self, content: Presentation, **kwargs: Any) -> Dict[str, Any]:
        """
        Process the content using the associated processor.
        """
        return self.processor.process(content, **kwargs)

    def _format_output(self, processed_content: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        """
        Format the processed content. In this case, we're just returning it as-is.
        """
        return processed_content
