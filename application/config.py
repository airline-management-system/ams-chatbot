from os import environ as env

class Config:
    API_KEY = env.get("API_KEY")