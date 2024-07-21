from openai import OpenAI

class gptwrapper:
    def __init__(self, system_prompt="", model="gpt-4", temperature=1):
        self._user_prompt = None
        self._gpt_response = None
        self._system_prompt = system_prompt
        self._model = model
        self._temperature = temperature
        self._client = OpenAI()
        return

    def to_json(self):
        return {
            "user_prompt": self._user_prompt,
            "system_prompt": self._system_prompt,
            "model": self._model,
            "temperature": self._temperature,
            "response": self.response
        }

    @property
    def response(self):
        if self._gpt_response is None:
            raise Exception("First use prompt().")
        return self._gpt_response.choices[0].message.content

    @property
    def user_prompt(self):
        return self._user_prompt

    @property
    def system_prompt(self):
        return self._system_prompt

    def create(self, user_prompt):
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
