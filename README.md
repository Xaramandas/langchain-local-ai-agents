# Assistentes Inteligentes e RAG com LangChain e Python (Execução 100% Local)

Este repositório contém uma série de aplicações de Inteligência Artificial Generativa desenvolvidas com **LangChain**, **LangGraph** e **Python**. 

O principal diferencial arquitetural deste projeto é o foco em **Privacidade e Segurança de Dados (Data Privacy by Design)**. Toda a inferência dos modelos de linguagem (LLMs) e a geração de Embeddings são realizadas localmente utilizando o **LM Studio**, garantindo que nenhum dado sensível (como regulamentos financeiros ou contratos) seja enviado para APIs na nuvem.

## Arquitetura dos Projetos

O repositório está dividido em três aplicações principais que demonstram a evolução na construção de agentes autônomos:

### 1. Gestão de Estado e Memória (`main_chat.py`)
Implementação de um chatbot capaz de manter o contexto da conversa utilizando `RunnableWithMessageHistory`. Demonstra a transição de um modelo *stateless* (sem memória) para um sistema *stateful* isolando sessões de usuários.

### 2. Orquestração de Agentes com LangGraph (`main_langgraph.py`)
Saindo de cadeias lineares para **Grafos de Estado Assíncronos**. 
* **Semantic Routing:** A aplicação utiliza a LLM como um roteador lógico que decide, com base na intenção do usuário, qual agente especialista acionar (ex: Especialista em Praia vs. Especialista em Montanha).
* Saídas estruturadas rigorosas com **Pydantic**.

### 3. Sistema RAG para Auditoria de Normativas (`main_rag.py`)
Uma aplicação de **Retrieval-Augmented Generation** voltada para o setor financeiro/compliance.
* Ingestão em lote de múltiplos regulamentos de cartões de crédito em PDF (`PyPDFLoader`).
* Quebra de texto inteligente e criação de vetores (Embeddings).
* Busca semântica ultrarrápida utilizando o banco de dados vetorial **FAISS**.
* O agente é capaz de analisar cláusulas específicas (ex: regras de acionamento de seguro) citando a fonte exata no documento original, mitigando riscos de alucinação.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Framework AI:** LangChain, LangGraph
* **Vector Store:** FAISS
* **Validação de Dados:** Pydantic
* **Infraestrutura/Inferência:** LM Studio (Localhost)

## Como Executar o Projeto

1. Clone o repositório:
```bash
git clone [https://github.com/xaramandas/langchain-local-ai-agents.git](https://github.com/SEU_USUARIO/langchain-local-ai-agents.git)
