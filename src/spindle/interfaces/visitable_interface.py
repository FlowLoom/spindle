from abc import ABC, abstractmethod
from spindle.interfaces.visitor_interface import IVisitor

__All__ = ['IVisitable']


class IVisitable(ABC):
    """
    An abstract base class representing a visitable object in the Visitor pattern.

    This class defines the interface for objects that can be visited by a Visitor.
    Classes that implement this interface agree to accept a Visitor object as an argument
    to their accept method, allowing the Visitor to perform operations on the Visitable object.
    """

    @abstractmethod
    def accept(self, visitor: IVisitor):
        """
        Accept a Visitor object to perform operations on this Visitable object.

        This method should be implemented by concrete classes to allow a Visitor
        to perform operations on the Visitable object.

        Args:
            visitor (IVisitor): The Visitor object that will perform operations on this Visitable.

        Returns:
            None
        """
        pass
