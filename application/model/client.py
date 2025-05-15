from application.config import Config
from langchain_google_genai import GoogleGenerativeAI


class GeminiClient:
    _llm:GoogleGenerativeAI

    def __init__(self):
        self._llm = GoogleGenerativeAI(model="gemini-2.0-flash",api_key=Config.API_KEY)

    def get_llm(self):
        return self._llm

    def generate_response(self, prompt:str) -> str:
        response = self._llm.invoke(input=prompt)

        return response