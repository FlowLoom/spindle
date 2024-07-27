from abc import ABC, abstractmethod
from spindle.interfaces.visitor_interface import IVisitor

__All__ = ['IVisitable']


class IVisitable(ABC):
    @abstractmethod
    def accept(self, visitor: IVisitor):
        pass
