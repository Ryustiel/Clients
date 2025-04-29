
import os
import dotenv
dotenv.load_dotenv(override=True)

from langchain_openai import ChatOpenAI
from clients.sqlachemy import PostgreDatabaseClient
from clients.openai import OpenAIVectorClient
from ragraph import RagraphClient


O3_MINI = ChatOpenAI(
    api_key = os.environ["OPENAI_API_KEY"],
    model= "o3-mini",
)

GPT_4O_MINI = O3_MINI = ChatOpenAI(
    api_key = os.environ["OPENAI_API_KEY"],
    model= "gpt-4o-mini",
)

VECTOR_CLIENT = OpenAIVectorClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="text-embedding-3-large",
)

RAGRAPH_POSTGRE_CLIENT = PostgreDatabaseClient(
    connection_string=os.environ["RAGRAPH_CONNECTION_STRING"]
)

RAGRAPH_CLIENT = RagraphClient(
    ragraph_db_client=RAGRAPH_POSTGRE_CLIENT,
    vector_client=VECTOR_CLIENT,
)
