import os
import dotenv
dotenv.load_dotenv()

from utils.console import print_tab
from utils.ttl import play_audio, text_to_audio
from utils.chatgpt import send_message
from utils.screenshot_listener import listen_screenshot

LANGUAGE = os.getenv("LANGUAGE")
TEMP_FILE = "./data/audio.mp3"

def describe_screenshot(screenshot):
    print("Describing screenshot...")
    messages = [
        {
            "role": "system",
            "content": f"""
### User Information
User Language: `{LANGUAGE}` - The language in which the user wants to receive information about the screenshot.

### Task Description
Your task is to describe to the user what is happening on the screenshot. The user needs to understand the content of the screenshot.
First, you need to define what exactly is not clear to the user. You must operate with all available information to determine and help the user understand what is happening on the screenshot.

Here are some options why the user can provide a screenshot:
- He may need to translate the information on the screen. The screen can contain information in another language that is not understood by the user.
- There may be a lot of information on the screen. The user needs to summarize the general information in a screenshot and explain it in an accessible language.
- There may be very specific information on the screen that is difficult to understand. You should explain to the user in a simpler language what this information is.
- The information on the screen can be quite confusing. You should simplify this information and convey it in an accessible language.
etc.

Therefore, when describing the content on the screenshot, you should adhere to these rules:
- You have to translate all the content into the user's language: `{LANGUAGE}`. This is important. All information must be translated.
- You need to determine the key points and focus on them to convey as much useful information as possible to what is happening on the screen.
- You need to describe the content in a way that is understandable to the user. You should not use complex terms or professional slang.
- Don't describe 'on screenshot', 'on the screen' what's going on there, just describe the situation itself. 
- You need to summarize the information and convey the essence of what is happening on the screen.
etc.

### Result Format
Result should be a JSON object with the following structure:
```json
{{
    "text": "All the text information from the screenshot",
    "no_text": "Described information that is not text",
    "description": "Summary description of the content",
    "voice": "Summary description without special characters (for voice output)"
}}
```

### Requirements
- text:
    - All the text information from the screenshot should be extracted.
    - Since the information on the screen is very specific, you need to structure this information in a more understandable format.
    - Use the user language: `{LANGUAGE}`.

- no_text:
    - All the useful non-text information from the screenshot should be extracted.
    - You should somehow organize and systematize the obtained data, so that it is more understandable to the user.
    - Use the user language: `{LANGUAGE}`.

- description:
    - The full description of what is happening on the screen, so that it is as clear as possible.
    - You should describe what is happening on the screen with your own words, since the information on the screen is not always clear.
    - When describing the content on the screen, you need to understand that you must convey as much useful information as possible to the user.
    - In the description, it is important to put the priorities on the information that the user most likely may not understand.
    - Use the user language: `{LANGUAGE}`.
    
- voice:
    - The description of what is happening on the screen without special characters.
    - It is important to describe only useful information. Also, do not describe visual information, because the user already sees it.
    - This is almost the same as the description of what is happening on the screen, but with the omission of unimportant points that are not necessary for understanding. For example:
        - file names: You should just describe what kind of file it is. For example, instead of 'main.py', you should say 'Python script'.
        - paths: You should describe the path in words. For example, instead of '/home/user', you should say 'home user'.
        - commands: You should describe the command in words. For example, instead of 'cd /home/user', you should say 'change directory to home user'.
        - tools: You should describe the tool in words. For example, instead of 'Node.js', you should say 'Node'.
        - etc.
    - You should not use different specific symbols. You have to describe everything in words. For example:
        - '$' symbol: 'dollar'
        - '%' symbol: 'percent'
        - '&' symbol: 'and'
        - '<' symbol: 'less than'
        - '>' symbol: 'greater than'
        - etc.
    - You have to ignore the symbols that do not carry any information. For example: '!', '?', '.', ',', '[', ']', etc.
    - You should not use the original names of files, commands, tools, and so on. You must try to describe it with words. For example:
        - 'user_config.json': User configuration file
        - 'README.md': Project documentation file
        - '.gitignore': File with ignored files for Git
        - 'package.json': Project configuration file with dependencies
        - 'npm install': Install dependencies with Node project
        - 'docker compose down -v': Stop and remove containers with Docker
        - 'python main.py': Run the main Python script
        - 'rm -rf ./data': Remove the data folder recursively
        - 'Node.js': Node
        - 'npm': Node package manager
        - 'MongoDB': Mongo database
        - 'React.js': React framework
        - etc.
    - You have to translate all the names of the tools, files, commands, that is, you have to translate everything into the user language, and nothing should remain in the original.
    - You have to find an analog of the description of the word, if it is difficult to pronounce. For example:
        - NFT: Non-fungible token
        - usdt: Tether coin
        - app: application
        - src: source code
        - utils: utilities
        - config: configuration
        - xlsx: Excel file
        - etc.
    - You should describe to the user the information that he is not able to understand. For example, such information as numbers, some names, he already understands it in principle. It is enough to simply mention it in some easy way, but not to speak directly as it is.
    - Use the user language: `{LANGUAGE}`.

### Examples

#### Example 1
- text: "> python main.py --file ./config/test/data.txt\nData successfully loaded from the file data.txt\nData Size: 100.25kb"
- no_text: "PowerShell window with the command"
- description: "The user runs the main.py script with the file ./config/test/data.txt. The data is successfully loaded from the file data.txt with a size of 100.25kb."
- voice: "The user runs the main Python script with the file data text. The data is successfully loaded from the file data text with a size of one hundred point twenty-five kilobytes."

#### Example 2
- text: "Node.js v14.17.0\nWelcome to Node.js v14.17.0.\nType 'help' for more information."
- no_text: "Terminal with the Node.js command"
- description: "The user has installed Node.js version 14.17.0 and the system welcomes the user with the message to type 'help' for more information."
- voice: "The user has installed Node version fourteen point seventeen zero and the system welcomes the user with the message to type help for more information."

#### Example 3
- text: "[2021-07-15 12:00:00] [INFO] sign_data: {{ amount: 2.47, currency: 'USDT', payment: 'Ethereum' }}"
- no_text: "Server log with information"
- description: "The log contains information with the date 2021-07-15 12:00:00 and the message about signing a payment transaction of 2.47 USDT in the Ethereum network."
- voice: "The log contains information with the date two thousand twenty-one July fifteen twelve o'clock and the message about signing a payment transaction of two point forty-seven Tether coin in the Ethereum network."

#### Example 4
- text: "Files: sign_data.py, edit_text.py, remove_data.py and folders: data, config, src"
- no_text: "File explorer with the files and folders"
- description: "The screen displays files sign_data.py, edit_text.py, remove_data.py and folders data, config, src."
- voice: "The screen displays python script sign data, edit text, remove data and folders data, configiguration and source code."
"""
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": screenshot
                    }
                }
            ]
        }
    ]

    res = send_message(messages, is_json=True)
    return res

def main():
    is_voice = "-v" in os.sys.argv
    while True:
        screenshot = listen_screenshot()
        result = describe_screenshot(screenshot)
        print_tab("Text", result["text"])
        print_tab("Screenshot Description", result["no_text"])
        print_tab("Content Description", result["description"])
        if is_voice:
            print_tab("Voiced Description", result["voice"])
            text_to_audio(result["voice"], TEMP_FILE)
            play_audio(TEMP_FILE)
        print()

if __name__ == "__main__":
    main()
