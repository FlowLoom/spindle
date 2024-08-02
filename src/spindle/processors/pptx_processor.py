import logging
from spindle.abstracts import AbstractProcessor
from typing import Any, Dict, List, Optional
from pptx import Presentation

__all__ = ['PPTXProcessor']

logger = logging.getLogger(__name__)

class PPTXProcessor(AbstractProcessor):
    def _preprocess(self, content: Presentation, **kwargs) -> Presentation:
        logger.info(f"Processing presentation with {len(content.slides)} slides")
        return content

    def _extract_content(self, presentation: Presentation, **kwargs) -> Dict[str, Any]:
        slide_index = kwargs.get('slide_index')
        if slide_index is not None:
            return self._extract_single_slide(presentation, slide_index)
        else:
            return self._extract_all_slides(presentation)

    def _main_process(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return data

    def _postprocess(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        if 'slide' in data:  # Single slide case
            if kwargs.get('only_content'):
                data['slide'] = {'slide_number': data['slide']['slide_number'], 'content': data['slide']['content']}
            elif kwargs.get('only_notes'):
                data['slide'] = {'slide_number': data['slide']['slide_number'], 'notes': data['slide']['notes']}
        else:  # All slides case
            if kwargs.get('only_content'):
                data['slides'] = [{'slide_number': slide['slide_number'], 'content': slide['content']} for slide in data['slides']]
            elif kwargs.get('only_notes'):
                data['slides'] = [{'slide_number': slide['slide_number'], 'notes': slide['notes']} for slide in data['slides']]
        return data

    def _extract_single_slide(self, presentation: Presentation, index: int) -> Dict[str, Any]:
        if 0 <= index < len(presentation.slides):
            slide = presentation.slides[index]
            return {
                'slide': {
                    'slide_number': index + 1,
                    'content': self._extract_slide_content(slide),
                    'notes': self._extract_speaker_notes(slide)
                },
                'metadata': self._extract_metadata(presentation)
            }
        else:
            raise ValueError(f"Slide index {index} is out of range. Presentation has {len(presentation.slides)} slides.")

    def _extract_all_slides(self, presentation: Presentation) -> Dict[str, Any]:
        slides = []
        for i, slide in enumerate(presentation.slides):
            try:
                slides.append({
                    'slide_number': i + 1,
                    'content': self._extract_slide_content(slide),
                    'notes': self._extract_speaker_notes(slide)
                })
            except Exception as e:
                logger.error(f"Error processing slide {i + 1}: {str(e)}")

        return {
            'slides': slides,
            'metadata': self._extract_metadata(presentation)
        }

    def _extract_slide_content(self, slide) -> str:
        return ' '.join(shape.text for shape in slide.shapes if hasattr(shape, 'text'))

    def _extract_speaker_notes(self, slide) -> str:
        return slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ''

    def _extract_metadata(self, presentation: Presentation) -> Dict[str, Any]:
        core_properties = presentation.core_properties
        return {
            'title': core_properties.title or 'Untitled',
            'author': core_properties.author or 'Unknown',
            'created': str(core_properties.created) if core_properties.created else 'Unknown',
            'modified': str(core_properties.modified) if core_properties.modified else 'Unknown',
            'slide_count': len(presentation.slides)
        }

