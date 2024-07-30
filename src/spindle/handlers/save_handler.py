from spindle.abstracts import AbstractHandler
from spindle.exceptions import HandlerException
from typing import Dict, Any
import os
from datetime import datetime
import click

__all__ = ['SaveHandler']


class SaveHandler(AbstractHandler):
    def __init__(self, config, silent=False, passthrough=False):
        self.config = config
        self.silent = silent
        self.passthrough = passthrough
        self.target_file = None

    def handle(self, data: Dict[str, Any]) -> None:
        preprocessed_data = self.preprocess(data)
        self.write(preprocessed_data)

        if not self.silent:
            click.echo(f"Content saved to {self.target_file}", err=True)

        if not self.silent or self.passthrough:
            click.echo(preprocessed_data['content'], nl=False)

    def preprocess(self, data: Dict[str, Any]) -> Dict[str, Any]:
        PATH_KEY = "FABRIC_OUTPUT_PATH"
        out = self.config.get(PATH_KEY)
        if out is None:
            raise HandlerException(f"'{PATH_KEY}' not set in configuration or environment.")

        out = os.path.expanduser(out)
        if not os.path.isdir(out):
            raise HandlerException(f"'{out}' does not exist. Create it and try again.")

        if not out.endswith("/"):
            out += "/"

        stub = data['stub']
        date_format = data['date_format']

        if date_format:
            yyyymmdd = datetime.now().strftime(date_format)
            target = f"{out}{yyyymmdd}-{stub}.md"
        else:
            target = f"{out}{stub}.md"

        # Avoid overwriting existing files
        inc = 0
        while os.path.exists(target):
            inc += 1
            if date_format:
                target = f"{out}{yyyymmdd}-{stub}-{inc}.md"
            else:
                target = f"{out}{stub}-{inc}.md"

        self.target_file = target
        return data

    def write(self, data: Dict[str, Any]) -> None:
        content = data['content']
        frontmatter = data['frontmatter']

        with open(self.target_file, "w") as fp:
            fp.write(frontmatter)
            fp.write(content)
