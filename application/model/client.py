from application.config import Config
from google import genai


class GeminiClient:
    def __init__(self):
        self.__client = genai.Client(api_key=Config.API_KEY)

    def generate_response(self, prompt:str) -> str:
        response = self.__client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

        return response.text