import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class AIClient:
    def __init__(self, api_key: str, base_url: str = None, model: str = None):
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def chat(self, prompt: str, message: str):
        self.response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": message},
            ],
            stream=True,
        )
        return self

    def stream_print(self):
        for chunk in self.response:
            if chunk.choices:
                delta = chunk.choices[0].delta
                content = delta.content if delta.content else ""
                print(content, end="", flush=True)
        print()

    def collect(self):
        result = ""
        for chunk in self.response:
            if chunk.choices:
                delta = chunk.choices[0].delta
                content = delta.content if delta.content else ""
                result += content
        return result


openai_client = AIClient(
    os.getenv("OPENAI_API_KEY"),
    model="chatgpt-4o-latest",
)

deepseek_client = AIClient(
    os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    model="deepseek-reasoner",
)


siliconflow_client = AIClient(
    os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn",
    model="deepseek-ai/DeepSeek-R1",
)

ark_client = AIClient(
    os.getenv("VOLCEENGINE_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    model="deepseek-r1-250120",
)

gptdos_client = AIClient(
    os.getenv("GPTDOS_API_KEY"),
    base_url="https://api.gptdos.com/v1",
    model="gpt-4o-mini",
)

gemini_client = AIClient(
    api_key=os.getenv("GEMINI_API_KEY", ""),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    model="gemini-2.0-flash",
)
