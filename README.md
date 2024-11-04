# Describe Screenshot - A simple tool to describe screenshots

This is a simple tool, it can be useful for translating and describing any information in a screenshot.

### Installation
```bash
pip install -r requirements.txt
```

### Environment Variables
- Create `.env` file in root directory
- Add `OPENAI_API_KEY = <your_api_key>`
- Add `LANGUAGE = <language>` - language for translation and description (en, ru, ...)

### Commands
- Start the tool: `describe-screenshot`

### Flags
- `--admin` - Run the tool with admin privileges
- `-v` - Allow voice output

### How To Use
- Run `describe-screenshot -v`
- Take a screenshot
- The tool will automatically translate and describe the information in the screenshot.

### How To Use With Ueli
- Open ueli settings
- Go to shortcuts
- Add new shortcut
- Name: `Describe Screenshot`
- Command: `describe-screenshot --admin -v`
