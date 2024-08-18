from openai import OpenAI
from datetime import datetime
import os
import json
import urllib

class gptwrapper:
    model_gpt4 = "gpt-4"
    model_tts1 = "tts-1"
    model_dalle3 = "dall-e-3"
    def __init__(self, system_prompt="", model="gpt-4", temperature=1):
        self._user_prompt = None
        self._gpt_response = None
        self._system_prompt = system_prompt
        self._model = model
        self._temperature = temperature
        self._filepath = None
        self._client = OpenAI()
        return

    def dump(self, filepath = os.path.dirname(os.path.realpath(__file__)), ip = "0.0.0.0"):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}-{ip.replace('.', '_')}.txt"

        filename = os.path.join(filepath, "..\log", filename)

        with open(filename, "w") as f:
            json.dump(self.to_json(), f)

    def to_json(self):
        return {
            "user_prompt": self._user_prompt,
            "system_prompt": self._system_prompt,
            "model": self._model,
            "temperature": self._temperature,
            "response": self.response,
            "filepath": self._filepath
        }

    @property
    def response(self):
        if self._gpt_response is None:
            raise Exception("First use prompt().")
        if self._model == 'tts-1': return f'audio @ `{self._filepath}`'
        if self._model == 'dall-e-3': return f'image @ `{self._filepath}`'
        return self._gpt_response.choices[0].message.content

    @property
    def user_prompt(self):
        return self._user_prompt

    @property
    def system_prompt(self):
        return self._system_prompt

    def request_text(self, user_prompt):
        self._user_prompt = user_prompt
        messages = [
            {"role": "user", "content": self._user_prompt},
            {"role": "system", "content": self._system_prompt},
        ]
        self._gpt_response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=self._temperature,  # this is the degree of randomness of the model's output
        )

        return 1

    def request_audio(self, user_prompt, voice = "alloy", filepath = os.path.dirname(os.path.realpath(__file__))):
        self._model = 'tts-1'
        filepath = os.path.join(filepath, "..\log", datetime.now().strftime('%Y%m%d%H%M%S') + ".mp3")
        self._user_prompt = user_prompt
        self._gpt_response = self._client.audio.speech.create(
              model=self._model,
              voice=voice,
              input=self._user_prompt
        )
        self._filepath = filepath
        self._gpt_response.stream_to_file(filepath)
        return 1

    def request_image(self, story, filepath = os.path.dirname(os.path.realpath(__file__))):
        self._model = "dall-e-3"
        self._user_prompt = story
        filepath = os.path.join(filepath, "..\log", datetime.now().strftime('%Y%m%d%H%M%S') + ".png")
        # prompt = f"Use the following story to generate a realistic image without any text in the image: {story}",
        self._gpt_response = self._client.images.generate(
          model=self._model,
          prompt=f"{story}",
          size="1024x1024",
          quality="standard",
          n=1,
        )

        self._filepath = filepath
        image_url = self._gpt_response.data[0].url
        urllib.request.urlretrieve(image_url, filepath)
        return 1