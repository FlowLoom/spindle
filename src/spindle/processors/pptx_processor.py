from spindle.abstracts import AbstractProcessor
from typing import Any, Dict
from pptx import Presentation

__all__ = ['PPTXProcessor']


class PPTXProcessor(AbstractProcessor):
    def _preprocess(self, content: Presentation, **kwargs) -> Presentation:
        """
        Preprocess the PPTX content. In this case, we're just passing it through.
        """
        return content

    def _extract_content(self, presentation: Presentation, **kwargs) -> Dict[str, Any]:
        """
        Extract slide content and speaker notes from the presentation.
        """
        slides = []
        for slide in presentation.slides:
            slide_content = self._extract_slide_content(slide)
            speaker_notes = self._extract_speaker_notes(slide)
            slides.append({
                'content': slide_content,
                'notes': speaker_notes
            })
        return {'slides': slides}

    def _main_process(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Main processing step. In this case, we're just passing the data through.
        """
        return data

    def _postprocess(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Postprocess the data. Here we filter based on the options.
        """
        if kwargs.get('only_content'):
            data['slides'] = [{'content': slide['content']} for slide in data['slides']]
        elif kwargs.get('only_notes'):
            data['slides'] = [{'notes': slide['notes']} for slide in data['slides']]
        return data

    def _extract_slide_content(self, slide, **kwargs):
        """
        Extract text content from a slide.
        """
        return ' '.join(shape.text for shape in slide.shapes if hasattr(shape, 'text'))

    def _extract_speaker_notes(self, slide, **kwargs):
        """
        Extract speaker notes from a slide.
        """
        return slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ''
