import json
import os
import openai

MODEL_GPT_4O = "gpt-4o"
MODEL_GPT_4O_MINI = "gpt-4o-mini"

TEMP_ACCURATE = 0.5
TEMP_NORMAL = 0.8
TEMP_CREATIVE = 1.0

openai.api_key = os.getenv('OPENAI_API_KEY')

def send_message(messages, gpt_model = MODEL_GPT_4O, temperature = 1.0, is_json = False):
    try:
        response = openai.ChatCompletion.create(
            messages = messages,
            model = gpt_model,
            temperature = temperature,
            response_format = { "type": "json_object" if is_json else "text" },
            max_tokens = 4000,
        )
        
        result = response['choices'][0]['message']['content']

        if is_json:
            return json.loads(result)
        else:
            return result
    except Exception as e:
        print(f"GPT request error: {e}")
        return None