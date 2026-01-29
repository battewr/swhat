# swhat

Specification-driven development CLI - Transform natural language feature descriptions into AI-implementable execution plans.

## Installation

### Prerequisites

- Python 3.10 or higher
- [UV](https://github.com/astral-sh/uv) package manager
- CMake 3.16 or higher

### From Source (Development)

```bash
# Clone the repository
git clone <repository-url>
cd swhat

# Configure and setup dev environment
cmake -B build
cmake --build build --target dev
source .venv/bin/activate
swhat --version
```

### System Install

```bash
# Build and install to system
cmake -B build
cmake --build build --target build
cmake --install build  # May require sudo
```

## Usage

```bash
# Show help
swhat --help

# Show version
swhat --version
```

## Development

### CMake Build Commands

```bash
cmake -B build                        # Configure
cmake --build build --target build    # Build package (dist/)
cmake --build build --target dev      # Dev install (editable)
cmake --build build --target lint     # Run linter
cmake --build build --target format   # Format code
cmake --build build --target pyclean  # Clean artifacts
cmake --install build                 # Install to system
```

### Manual Setup

```bash
# Install with dev dependencies
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Run linting
ruff check src/

# Run formatting
ruff format src/
```

### Project Structure

```
src/
└── swhat/
    ├── __init__.py      # Package version
    └── cli.py           # CLI entry point
```

## License

MIT
