from spindle.interfaces.visitor_interface import IVisitor
from typing import Any

__All__ = ['AbstractVisitor']


class AbstractVisitor(IVisitor):
    def visit(self, element: Any):
        method_name = f'visit_{element.__class__.__name__.lower()}'
        method = getattr(self, method_name, self.default_visit)
        return method(element)

    def default_visit(self, element: Any):
        pass
