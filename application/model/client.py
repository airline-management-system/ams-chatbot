from application.config import Config
from google import genai
from langchain_google_genai import GoogleGenerativeAI


class GeminiClient:
    __llm:GoogleGenerativeAI

    def __init__(self):
        self.__llm = GoogleGenerativeAI(model="gemini-2.0-flash",api_key=Config.API_KEY)

    def get_llm(self):
        return self.__llm

    def generate_response(self, prompt:str) -> str:
        response = self.__llm.invoke(input=prompt)

        return response