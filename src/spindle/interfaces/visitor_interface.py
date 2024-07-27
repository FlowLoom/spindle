from abc import ABC, abstractmethod
from typing import Any

__All__ = ['IVisitor']


class IVisitor(ABC):
    @abstractmethod
    def visit(self, element: Any):
        pass
