from spindle.abstracts import AbstractProcessor
from typing import Any, Dict
from pptx import Presentation
from pptx.shapes.autoshape import Shape
from pptx.shapes.base import BaseShape

__all__ = ['PPTXSetterProcessor']


class PPTXSetterProcessor(AbstractProcessor):
    def _preprocess(self, content: Presentation, **kwargs) -> Presentation:
        return content

    def _extract_content(self, presentation: Presentation, **kwargs) -> Dict[str, Any]:
        return {'presentation': presentation}

    def _main_process(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        presentation = data['presentation']
        slide_content = kwargs.get('slide_content')
        slide_notes = kwargs.get('slide_notes')
        slide_index = kwargs.get('slide_index')

        if slide_index is not None:
            self._set_single_slide(presentation, slide_index, slide_content, slide_notes)
        else:
            self._set_all_slides(presentation, slide_content, slide_notes)

        return {'presentation': presentation}

    def _postprocess(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return data

    def _set_single_slide(self, presentation: Presentation, index: int, content: str, notes: str):
        if 0 <= index < len(presentation.slides):
            slide = presentation.slides[index]
            self._set_slide_content(slide, content)
            self._set_slide_notes(slide, notes)
        else:
            raise ValueError(f"Slide index {index} is out of range. Presentation has {len(presentation.slides)} slides.")

    def _set_all_slides(self, presentation: Presentation, content: str, notes: str):
        for slide in presentation.slides:
            self._set_slide_content(slide, content)
            self._set_slide_notes(slide, notes)

    def _set_slide_content(self, slide, content: str):
        if content:
            text_frame = self._get_or_create_text_frame(slide)
            text_frame.text = content

    def _set_slide_notes(self, slide, notes: str):
        if notes:
            notes_slide = slide.notes_slide
            text_frame = notes_slide.notes_text_frame
            text_frame.text = notes

    def _get_or_create_text_frame(self, slide) -> Shape:
        for shape in slide.shapes:
            if isinstance(shape, BaseShape) and hasattr(shape, 'text_frame'):
                return shape.text_frame

        # If no suitable shape is found, create a new text box
        left = top = width = height = Inches(1)
        txBox = slide.shapes.add_textbox(left, top, width, height)
        return txBox.text_frame
