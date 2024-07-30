from spindle.abstracts import AbstractProcessor
from typing import Any, Dict
from datetime import datetime

__all__ = ['SaveProcessor']


class SaveProcessor(AbstractProcessor):
    def __init__(self, config):
        self.config = config

    def process(self, content: str, **kwargs: Any) -> Dict[str, Any]:
        stub = kwargs.get('stub', '')
        tags = kwargs.get('tags', [])
        nofabric = kwargs.get('nofabric', False)

        FM_KEY = "FABRIC_FRONTMATTER_TAGS"
        DATE_FORMAT = self.config.get("SAVE_DATE_FORMAT", "%Y-%m-%d")

        frontmatter_tags = self.config.get(FM_KEY, "") if not nofabric else ""

        frontmatter = ""
        if frontmatter_tags or tags:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            frontmatter = "---\n"
            frontmatter += f"generation_date: {now}\n"
            frontmatter += f"tags: {frontmatter_tags} {stub} {' '.join(tags)}\n"
            frontmatter += "---\n"

        return {
            'content': content,
            'frontmatter': frontmatter,
            'stub': stub,
            'date_format': DATE_FORMAT
        }

    def _preprocess(self, content: Any) -> Any:
        return content

    def _extract_content(self, content: Any) -> Any:
        return content

    def _main_process(self, content: Any) -> Any:
        return content

    def _postprocess(self, content: Any) -> Any:
        return content
