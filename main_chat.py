from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

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

# Criando um prompt de sugestão

prompt_sugestao = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um guia de viagem especializado em destinos brasileiros. Apresente-se como Mr.Guia"),
        ("placeholder", "{historico}"),
        ("human", "{query}")
    ]
)

cadeia = prompt_sugestao | modelo | StrOutputParser()

# Criando o histórico

memoria = {}
sessao = "projeto_langchain"

def historico_por_sessao(sessao: str):
    if sessao not in memoria:
        memoria[sessao] = InMemoryChatMessageHistory()
    return memoria[sessao]

# Criando uma lista de perguntas

lista_perguntas = [
    "Quero visitar um lugar no Brasil, famoso por praias e cultura. Pode sugerir?",
    "Qual a melhor época do ano para ir?"
]

# Criando a cadeia com memoria

cadeia_com_memoria = RunnableWithMessageHistory(
    runnable=cadeia,
    get_session_history=historico_por_sessao,
    input_messages_key="query",
    history_messages_key="historico"
)

# Criando o output

for uma_pergunta in lista_perguntas:
    resposta = cadeia_com_memoria.invoke(
        {
            "query" : uma_pergunta
        },
        config={"session_id":sessao}
    )
    print("Usuário: ", uma_pergunta)
    print("IA: ", resposta, "\n")
