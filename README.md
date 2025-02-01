# Cursor Reset Tool

This is a tool designed to reset the Cursor editor's machine code and automatically generate new email aliases. This tool helps users restart their Cursor free trial period.

## Features

- Automatically updates Cursor's machine identifiers
- Automatically manages addy.io email aliases
- Automatically terminates existing Cursor processes
- Complete logging functionality

## System Requirements

- Python 3.6 or higher
- macOS operating system
- Valid addy.io API key

## Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/bleuren/cursor-refresh
cd cursor-refresh
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Modify the environment variables in the `.env` file:
```bash
ADDY_API_KEY=your_api_key
```

## Usage

1. Ensure the Cursor editor is closed
2. Run the program:
```bash
python main.py
```

The program will automatically:
- Terminate all Cursor processes
- Update machine identifiers
- Delete old addy.io aliases
- Create new email aliases

## Important Notes

- Please ensure important data is backed up before running the program
- Requires a valid addy.io API key
- This tool only supports macOS systems
- Please comply with relevant terms of service when using this tool

## Disclaimer

This tool is for educational and research purposes only. Users assume all risks associated with its use and must ensure compliance with relevant service terms and conditions.