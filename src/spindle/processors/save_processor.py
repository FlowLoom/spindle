from spindle.abstracts import AbstractProcessor
from typing import Any, Dict
from datetime import datetime

__all__ = ['SaveProcessor']


class SaveProcessor(AbstractProcessor):
    def __init__(self, config):
        self.config = config

    def _preprocess(self, content: str, **kwargs) -> Dict[str, Any]:
        """Prepare the input data and options."""
        #if isinstance(content, tuple):
        #    content, options = content
        #else:
        #    options = {}
        return {'content': content, 'options': kwargs}

    def _extract_content(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Extract relevant information from the preprocessed data."""
        options = data['options']
        return {
            'content': data['content'],
            'stub': options.get('stub', ''),
            'tags': options.get('tags', []),
            'nofabric': options.get('nofabric', False)
        }

    def _main_process(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Generate frontmatter and process the content."""
        FM_KEY = "FABRIC_FRONTMATTER_TAGS"
        DATE_FORMAT = self.config.get("SAVE_DATE_FORMAT", "%Y-%m-%d")

        frontmatter_tags = self.config.get(FM_KEY, "") if not data['nofabric'] else ""

        frontmatter = ""
        if frontmatter_tags or data['tags']:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            frontmatter = "---\n"
            frontmatter += f"generation_date: {now}\n"
            frontmatter += f"tags: {frontmatter_tags} {data['stub']} {' '.join(data['tags'])}\n"
            frontmatter += "---\n"

        data['frontmatter'] = frontmatter
        data['date_format'] = DATE_FORMAT
        return data

    def _postprocess(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Perform any final processing or formatting."""
        # In this case, we don't need any additional processing
        return data
