import os
import logging
from typing import Dict, Any, Union
from spindle.serializers import ISerializer, SerializationException
from spindle.abstracts import AbstractHandler

__All__ = ["FileHandler"]


class FileHandler(AbstractHandler):
    def __init__(self, serializer: ISerializer, output_file: str, append: bool = False, create_dirs: bool = True):
        super().__init__(serializer)
        self.output_file = output_file
        self.append = append
        self.create_dirs = create_dirs
        self.logger = logging.getLogger(self.__class__.__name__)

    def preprocess(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocess the data before serialization.
        This method can be overridden in subclasses to implement specific preprocessing logic.
        """
        # Example preprocessing: add a timestamp to the data
        from datetime import datetime
        data['timestamp'] = datetime.now().isoformat()
        return data

    def write(self, data: str) -> None:
        """
        Write the serialized data to the specified file.
        """
        try:
            # Ensure the directory exists
            if self.create_dirs:
                os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

            # Determine the write mode
            mode = 'a' if self.append else 'w'

            # Write the data to the file
            with open(self.output_file, mode, encoding='utf-8') as f:
                f.write(data)
                # Ensure the data ends with a newline
                if not data.endswith('\n'):
                    f.write('\n')

            self.logger.info(f"Data successfully written to {self.output_file}")

        except IOError as e:
            self.logger.error(f"Error writing to file {self.output_file}: {e}")
            raise

    def handle(self, data: Union[Dict[str, Any], str]) -> None:
        """
        Process and write the data to the file.
        """
        try:
            # If data is already a string, assume it's serialized
            if isinstance(data, str):
                serialized_data = data
            else:
                preprocessed_data = self.preprocess(data)
                serialized_data = self.serializer.encode(preprocessed_data)

            self.write(serialized_data)

        except SerializationException as e:
            self.logger.error(f"Serialization error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error handling data: {e}")
            raise

    def set_append_mode(self, append: bool) -> None:
        """
        Set whether to append to the file or overwrite it.
        """
        self.append = append

    def set_create_dirs(self, create_dirs: bool) -> None:
        """
        Set whether to create directories if they don't exist.
        """
        self.create_dirs = create_dirs

    def get_file_size(self) -> int:
        """
        Get the current size of the output file.
        """
        try:
            return os.path.getsize(self.output_file)
        except OSError as e:
            self.logger.error(f"Error getting file size for {self.output_file}: {e}")
            return -1

    def clear_file(self) -> None:
        """
        Clear the contents of the output file.
        """
        try:
            open(self.output_file, 'w').close()
            self.logger.info(f"File {self.output_file} has been cleared")
        except IOError as e:
            self.logger.error(f"Error clearing file {self.output_file}: {e}")
            raise