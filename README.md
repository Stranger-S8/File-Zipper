# File Zipper

A desktop file compression and decompression tool built with CustomTkinter and custom compression modules.

## Overview

File Zipper provides a GUI for selecting files or folders, compressing them into `.zlib` outputs, and decompressing generated archives. The implementation includes DEFLATE and Huffman modules for the core compression workflow.

## Key Features

- Add individual files or entire folders
- Display selected files with type and size
- Compress files into the `output/compression/` folder
- Decompress files into the `output/decompression/` folder
- Desktop UI with progress feedback

## Tech Stack

- Python
- CustomTkinter
- Tkinter file dialogs
- Custom DEFLATE and Huffman logic

## Project Structure

```text
.
|-- run.py        # App launcher
|-- main.py       # CustomTkinter GUI
|-- DEFLATE.py    # Compression/decompression implementation
|-- Huffman.py    # Huffman helper logic
|-- data/         # Local assets/data
`-- output/       # Generated compressed/decompressed files
```

## Getting Started

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

## GitHub Notes

Generated files in `output/` should not be committed. Add small sample files only if they help demonstrate the project.
