# Modern Markdown Editor

A simple, modern, and easy-to-use desktop markdown editor built with Python and `tkinter`. It provides a live preview that updates as you type, in a clean, split-pane interface.

## Features

- **Live Preview**: See your rendered markdown on the right as you type on the left.
- **Modern Dark UI**: A professional and comfortable dark theme.
- **Core File Operations**: Create, open, save, and save as markdown files (`.md`).
- **Unsaved Changes Prompt**: The editor will ask you to save any unsaved work before quitting or opening a new file.
- **Keyboard Shortcuts**: Common shortcuts like `Ctrl+S` for saving are supported.
- **Cross-Platform**: Built with `tkinter`, it runs on Windows, macOS, and Linux.

## Installation

To run this markdown editor, you will need Python 3 installed on your system.

1.  **Clone the repository (or download the files):**
    ```bash
    git clone https://github.com/makeralchemy/simple-markdown-editor.git
    cd simple-markdown-editor
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```
    Activate it:
    -   On Windows: `venv\Scripts\activate`
    -   On macOS/Linux: `source venv/bin/activate`

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Once you have completed the installation steps, you can easily run the application using the provided scripts.

### On Windows

Simply double-click the `run.bat` file, or open a command prompt and run:

```bash
run.bat
```

### On macOS / Linux

1.  **Make the script executable (only needs to be done once):**
    ```bash
    chmod +x run.sh
    ```

2.  **Run the script:**
    ```bash
    ./run.sh
    ```

The script will handle activating the virtual environment, installing dependencies, and launching the editor.

## Acknowledgments

This program was created with the assistance of Cascade, a powerful agentic AI coding assistant from Windsurf, powered by the Gemini 2.5 Pro LLM.
