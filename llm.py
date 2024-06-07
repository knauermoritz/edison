from groq import Groq
import os

class LLM:
    def __init__(self, system_prompt, model="llama3-70b-8192"):
        self.model = model
        self.client = Groq(api_key='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')
        self.system_prompt = system_prompt
        self.history = [{'role': 'system', 'content': system_prompt}]

    def message(self, user_message, system_prompt=None):
        if system_prompt:
            self.system_prompt = system_prompt
            self.history[-1]['content'] = self.system_prompt
        self.history.append({'role': 'user', 'content': user_message})

        completion = self.client.chat.completions.create(
            messages=self.history,
            model=self.model
        )
        answer = completion.choices[0].message.content

        self.history.append({'role': 'assistant', 'content': answer})
        return answer
