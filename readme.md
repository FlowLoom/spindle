# Spindle

Spindle is a powerful CLI tool for parsing and processing data from various sources including source code, git repositories, and web content. It provides a flexible and extensible architecture for fetching, processing, and handling data with support for multiple output formats and customization options.

## Features

- Parse and process source code files
- Fetch and analyze git commit history
- Extract and process web content
- Modular architecture with support for custom fetchers, processors, and handlers
- Multiple output formats including JSON, YAML, and plain text
- Configurable processing options (e.g., comment removal, line trimming)
- Extensible design pattern implementation (Factory, Visitor, Decorator)
- Integration with AI services (OpenAI, Claude, Google AI, Ollama)

## Installation

```bash
pip install spindle
```

## Usage

Spindle provides several command-line interfaces for different data sources:

### Code Parsing

```bash
spindle code --src /path/to/source --output output.txt --excluded-dirs node_modules,venv --extensions .py,.js
```

### Git Commit Analysis

```bash
spindle git --repo /path/to/repo --output commits.json --start 0 --end 100 --extract-ticket
```

### Web Content Extraction

```bash
spindle web --url https://example.com --output content.txt --method readability --remove-html
```

### Fabric Integration

```bash
spindle fabric process --text "Your input text" --pattern example_pattern --model gpt-4
```

## Configuration

Spindle uses a configuration file located at `~/.config/spindle/.env`. You can set up API keys and default settings:

```
OPENAI_API_KEY=your_openai_key
CLAUDE_API_KEY=your_claude_key
GOOGLE_API_KEY=your_google_key
DEFAULT_MODEL=gpt-4-turbo-preview
```

## Architecture

Spindle follows a modular architecture with the following key components:

- Fetchers: Responsible for retrieving raw data from various sources
- Processors: Handle the processing and transformation of fetched data
- Handlers: Manage the output and storage of processed data
- Factories: Create instances of fetchers, processors, and handlers
- Decorators: Add additional functionality to fetchers (e.g., logging, timing)
- Visitors: Implement operations on fetchers without modifying their classes

## Extending Spindle

You can extend Spindle by creating custom fetchers, processors, and handlers:

1. Implement the relevant interface (IFetcher, IProcessor, IHandler)
2. Create a factory for your new component
3. Register your factory with the appropriate command in the CLI

## Contributing

Contributions to Spindle are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature
3. Implement your changes
4. Write tests for your new functionality
5. Submit a pull request

## License

Spindle is released under the MIT License. See the LICENSE file for details.

## Contact

For questions or support, please contact the project maintainer at josh.magady@gmail.com.