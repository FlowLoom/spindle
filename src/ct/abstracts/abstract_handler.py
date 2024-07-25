from ct.interfaces import IHandler

__All__ = ["AbstractHandler"]


class AbstractHandler(IHandler):
    def handle(self, parsed_files: Dict[str, List[str]]) -> None:
        """Handles the parsed files' content."""
        pass