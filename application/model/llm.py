from application.model.client import GeminiClient
from application.model.prompt_manager import PromptManager
from langchain_community.agent_toolkits import create_sql_agent
from application.database.database import PostgreDB


client = GeminiClient()
llm = client.get_llm()
db = PostgreDB()
db_conn = db.get_langchain_type_connection()

prompt_manager = PromptManager()

def query_model():
    agent_executor = create_sql_agent(llm=llm, db=db_conn, verbose=True)
    result = agent_executor.invoke({
        "input": "give me the top 3 cheapest flights from izmir to istanbul in july"
    })

    return result
