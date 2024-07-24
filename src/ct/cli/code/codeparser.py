import os
import logging

__ALL__ = ["CodeParser"]

class CodeParser:
    def __init__(self, src_folder, output_file, excluded_dirs, excluded_files, file_extensions):
        self.src_folder = src_folder
        self.output_file = output_file
        self.excluded_dirs = excluded_dirs
        self.excluded_files = excluded_files
        self.file_extensions = file_extensions

    @staticmethod
    def remove_non_ascii(text):
        """Removes non-ASCII characters from a string using encoding."""
        return text.encode("ascii", errors="ignore").decode("ascii")

    def should_process_file(self, file):
        """Determines if a file should be processed based on exclusion rules and extensions."""
        return (file not in self.excluded_files and
                any(file.endswith(ext) for ext in self.file_extensions))

    def process_file(self, file_path):
        """Processes a single file and returns its content."""
        content = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as code_file:
                for line in code_file:
                    line = line.rstrip()
                    if line and not line.startswith("#"):
                        line = self.remove_non_ascii(line)
                        content.append(line)
        except IOError as e:
            logging.error(f"Failed to process file {file_path}: {e}")
        return content

    def parse(self):
        """Parses files in the src directory and writes their content to the output file."""
        with open(self.output_file, "w", encoding="utf-8") as out_file:
            for root, dirs, files in os.walk(self.src_folder):
                dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
                for file in files:
                    if not self.should_process_file(file):
                        logging.info(f"Skipping file: {file}")
                        continue

                    module_path = os.path.join(root, file)
                    logging.info(f"Processing file: {file}")

                    out_file.write(f"{file}:\n")
                    content = self.process_file(module_path)
                    out_file.write("\n".join(content))
                    out_file.write("\n\n")

        logging.info(f"Parsed code written to {self.output_file}")