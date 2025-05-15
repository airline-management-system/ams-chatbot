from application.model.client import GeminiClient
from application.model.prompt_manager import PromptManager
from langchain_community.agent_toolkits import create_sql_agent
from application.database.postgres import PostgreDB
from langchain.agents import AgentExecutor
from application.retriaval.rag import RAG


client = GeminiClient()
llm = client.get_llm()
db = PostgreDB()
db_conn = db.get_langchain_type_connection()

rag = RAG()

prompt_manager = PromptManager()


def query_model(prompt:str):
    result = ""
    try:
        # Create the SQL agent (returns just the agent, not executor)
        agent = create_sql_agent(llm=llm, db=db_conn, verbose=True)

        # Wrap it with AgentExecutor and enable parsing error handling
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent.agent,  # Get the internal agent logic
            tools=agent.tools,  # Get the tools used
            handle_parsing_errors=True,
            verbose=True
        )

        # Invoke the executor
        result = agent_executor.invoke({
            "input": prompt_manager.enhanced_prompt(user_prompt=prompt),
        })

    except ValueError as e:
        return f"ValueError: {str(e)}"

    return result

def similarity_search(prompt:str):
    chunks = rag.query_similar_chunks(query=prompt, n_results=5)

    rag_prompt = prompt_manager.rag_prompt(chunks=chunks,prompt=prompt)

    response = llm.invoke(input=rag_prompt)

    return response
