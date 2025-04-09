# Zip File Extractor

Extract images and PDFs from zip files. Available in both command-line and GUI versions.

## Quick Start

1. Clone and setup:
```bash
git clone https://github.com/yourusername/imageExtractor.git
cd imageExtractor
python -m venv env
.\env\Scripts\activate  # Windows
# OR
source env/bin/activate  # macOS/Linux
```

2. Run the program:
```bash
python src/gui.py      # For GUI version
# OR
python src/extractor.py  # For command-line version
```

## Features
- Extracts: .jpg, .jpeg, .png, .gif, .bmp, .webp, .pdf
- Handles duplicate filenames automatically
- Works on Windows, macOS, and Linux
- GUI shows progress and status 