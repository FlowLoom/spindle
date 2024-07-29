import os
import logging
import configparser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def remove_non_ascii(text):
    """
    Removes non-ASCII characters from a string using encoding.

    :param text: str - The text to process.
    :return: str - The processed text with non-ASCII characters removed.
    """
    return text.encode("ascii", errors="ignore").decode("ascii")


def parse_src_to_txt(src_folder, output_file, excluded_dirs, excluded_files, file_extensions):
    """
    Parses files in a src directory with specified extensions, excluding specified directories and files,
    and outputs their full paths and content to a text document.

    :param src_folder: str - Path to the src folder.
    :param output_file: str - Name/Path of the output text file.
    :param excluded_dirs: list - Directories to exclude from parsing.
    :param excluded_files: list - Filenames to exclude from parsing.
    :param file_extensions: list - File extensions to include in parsing.
    """
    with open(output_file, "w", encoding="utf-8") as out_file:
        for root, dirs, files in os.walk(src_folder):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file in files:
                if file in excluded_files or not any(file.endswith(ext) for ext in file_extensions):
                    logging.info(f"Skipping file: {file} with extension not in {file_extensions} or in {excluded_files}")
                    continue

                module_path = os.path.join(root, file)
                logging.info(f"Processing file: {module_path}")

                out_file.write(f"{module_path}:\n")

                try:
                    with open(module_path, "r", encoding="utf-8", errors="ignore") as code_file:
                        for line in code_file:
                            line = line.rstrip()
                            if line and not line.startswith("#"):
                                line = remove_non_ascii(line)
                                out_file.write(line + "\n")
                        out_file.write("\n\n")
                except IOError as e:
                    logging.error(f"Failed to process file {module_path}: {e}")


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    src_folder = config['Settings']['src_folder']
    output_file = config['Settings']['output_file']
    excluded_dirs = config['Exclusions']['excluded_dirs'].split(', ')
    excluded_files = config['Exclusions']['excluded_files'].split(', ')
    file_extensions = config['Extensions']['file_extensions'].split(', ')

    parse_src_to_txt(src_folder, output_file, excluded_dirs, excluded_files, file_extensions)
    logging.info(f"Parsed code written to {output_file}")