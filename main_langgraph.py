from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
import asyncio

# Configurações do LM Studio
local_url = "http://localhost:1234/v1" 
api_key = "lm-studio" 

# Instanciando o modelo
modelo = ChatOpenAI(
    base_url=local_url,      # <--- OBRIGATÓRIO: Redireciona para o seu PC
    api_key=api_key,         # <--- OBRIGATÓRIO: Qualquer string serve
    model="local-model",     # O LM Studio usa o modelo que estiver carregado na interface
    temperature=0.7
)

prompt_consultor_praia = ChatPromptTemplate.from_messages(
    [
        ("system", "Apresente-se com Sra.Praia. Você é um especialista em selecionar viagens com praias"),
        ("human", "{query}")
    ]
)

prompt_consultor_montanha = ChatPromptTemplate.from_messages(
    [
        ("system", "Apresente-se com Sr.Montanha. Você é um especialista em selecionar viagens com montanhas"),
        ("human", "{query}")
    ]
)

cadeia_praia = prompt_consultor_praia | modelo | StrOutputParser()
cadeia_montanha = prompt_consultor_montanha | modelo | StrOutputParser()

class Rota(TypedDict):
    destino: Literal["praia", "montanha"]

prompt_roteador = ChatPromptTemplate.from_messages(
    [
        ("system", "Responda apenas com praia ou montanha"),
        ("human", "{query}")
    ]
)

roteador = prompt_roteador | modelo.with_structured_output(Rota)

class Estado(TypedDict):
    query:str
    destino: Rota
    resposta:str

async def no_roteador(estado: Estado, config=RunnableConfig):
    return {"destino": await roteador.ainvoke({"query":estado["query"]}, config)}

async def no_praia(estado: Estado, config=RunnableConfig):
    return {"resposta": await cadeia_praia.ainvoke({"query":estado["query"]}, config)}

async def no_montanha(estado: Estado, config=RunnableConfig):
    return {"resposta": await cadeia_montanha.ainvoke({"query":estado["query"]}, config)}

def escolha_no(estado:Estado)->Literal["praia", "montanha"]:
    return "praia" if estado["destino"]["destino"] == "praia" else "montanha"

grafo = StateGraph(Estado)
grafo.add_node("roteador", no_roteador)
grafo.add_node("praia", no_praia)
grafo.add_node("montanha", no_montanha)

grafo.add_edge(START, "roteador")
grafo.add_conditional_edges("roteador", escolha_no)
grafo.add_edge("praia", END)
grafo.add_edge("montanha", END)

app = grafo.compile()
async def main():
    resposta = await app.ainvoke(
        {"query": "Quero visitar um lugar famoso no Brasil por praias e cultura"}
    )
    print(resposta["resposta"])
asyncio.run(main())