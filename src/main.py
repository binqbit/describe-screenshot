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
### Task Description
Your task is translating and describing the information in the screenshot to `{LANGUAGE}` language.
Required use provided language for the description: `{LANGUAGE}`.

### Result should be a JSON object with the following structure
```json
{{
    "text": "Translated text",
    "no_text": "Description is not text information",
    "description": "Described text without special characters"
}}
```

### Requirements
#### text:
- This field should contain the translated text from the screenshot.
- You need to extract all the text information from the screenshot.
- It is necessary to systematize the input information in order to convey it more correctly.
- Use the provided language.

#### no_text:
- This field should contain a message that the information in the screenshot is not text.
- You need to describe the information that can be useful, but it is not text.
- You need to describe all the useful information in as much detail as possible.
- For better understanding, the information must be somehow systematized.
- It is important to describe the information as it is, without further explanation.
- Use the provided language.

#### description:
- The field should contain a summarized version of the description without using special characters.
- You have to describe the content, but do not mention the content itself.
- You should not focus on different elements that are already clear. You only need to convey the very essence of what is happening.
- If the content contains text information, which is not in the language specified by the user, it is necessary to translate this information and convey the essence of what is happening.
- You need to summarize the information, but do not miss the essence itself, so that everything is as clear as possible.
- It is important to convey information that can be very useful to the user.
- It is important to prioritize the information, for example, the one that the user may not understand on the screenshot.
- To improve the quality of the user's understanding, you should translate everything you want to convey to the user, even the name of the file. You should not say the original name of the file, you should describe this file.
- Nothing should remain in other languages. Everything should be translated and conveyed in the user's language.
- Use the provided language.

### Example
```json
{{
    "text": "python main.py --file data.txt",
    "no_text": "The powershell window with the command",
    "description": "run the main program with the data text file"
}}
```
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
    while True:
        screenshot = listen_screenshot()
        result = describe_screenshot(screenshot)
        print_tab("Text", result["text"])
        print_tab("Screenshot Description", result["no_text"])
        print_tab("Content Description", result["description"])
        text_to_audio(result["description"], TEMP_FILE)
        play_audio(TEMP_FILE)
        print()

if __name__ == "__main__":
    main()
