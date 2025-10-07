from datetime import datetime
from typing import Literal

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    AIMessagePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.retrievers import BaseRetriever
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph

from app.domain.models import KnowledgeAgentState, RouterRetriever


class KnowledgeAgent:
    def __init__(
        self,
        llm: BaseChatModel,
        vector_store_retriever: BaseRetriever,
        web_search_tool: BaseTool,
    ):
        graph = StateGraph(KnowledgeAgentState)

        graph.add_node("router_question", self.__router_question_node)
        graph.add_node(
            "retriever_from_vector_store", self.__retriever_from_vector_store_node
        )
        graph.add_node(
            "retriever_from_web_search", self.__retriever_from_web_search_node
        )
        graph.add_node("answer_question", self.__answer_question_node)

        graph.add_edge(START, "router_question")

        graph.add_conditional_edges(
            "router_question",
            self.__call_selected_retriever,
            {
                "vector_store": "retriever_from_vector_store",
                "web_search": "retriever_from_web_search",
            },
        )

        graph.add_edge("retriever_from_vector_store", "answer_question")
        graph.add_edge("retriever_from_web_search", "answer_question")
        graph.add_edge("answer_question", END)

        self.graph = graph
        self.llm = llm
        self.vector_store_retriever = vector_store_retriever
        self.web_search_tool = web_search_tool

    def __router_question_node(self, state: KnowledgeAgentState) -> KnowledgeAgentState:
        system_prompt = SystemMessagePromptTemplate.from_template(
            """
            You are an expert at routing a user question to a vector store or web search. 
            Use the vectore store for questions about the company's products and services. 
            You do not need to be stringet with the keywords in the question related to 
            these topics. Otherwise, for general purpose questions, use web search. 
        """
        )

        user_prompt = HumanMessagePromptTemplate.from_template(
            """
            Given the following user message, respond with the retriever to use.
            <user-message>{message}</user-message>
            """
        )

        prefill_assistant_prompt = AIMessagePromptTemplate.from_template(
            """selected_retriever:"""
        )

        router_prompt = ChatPromptTemplate.from_messages(
            [system_prompt, user_prompt, prefill_assistant_prompt]
        )

        chain = router_prompt | self.llm.with_structured_output(RouterRetriever)

        message = state.message
        response = chain.invoke({"message": message})

        return {"selected_retriever": response.selected_retriever}

    def __retriever_from_vector_store_node(
        self, state: KnowledgeAgentState
    ) -> KnowledgeAgentState:

        message = state.message
        documents = self.vector_store_retriever.invoke(message)
        knowledgebase = "\n\n".join(document.page_content for document in documents)
        return {"knowledgebase": knowledgebase}

    def __retriever_from_web_search_node(
        self, state: KnowledgeAgentState
    ) -> KnowledgeAgentState:
        today = datetime.now().strftime("%d/%m/%y")
        message = f"Hoje é {today}. {state.message}"
        response = self.web_search_tool.invoke({"query": message})

        knowledgebase = "\n\n".join(result["content"] for result in response["results"])

        return {"knowledgebase": knowledgebase}

    def __call_selected_retriever(
        self, state: KnowledgeAgentState
    ) -> Literal["vector_store", "web_search"]:
        return state.selected_retriever

    def __answer_question_node(self, state: KnowledgeAgentState) -> KnowledgeAgentState:
        system_prompt = SystemMessagePromptTemplate.from_template(
            """You are an assistant for question-answering tasks."""
        )

        today = datetime.now().strftime("%d/%m/%y")

        user_prompt = HumanMessagePromptTemplate.from_template(
            """
            Today is {today}.

            Use the following pieces of retrieved context to answer the question:
            <context>
            {documents}
            </context>

            <instructions>
            1. If you don't know the answer, just say that you don't know.
            2. Always respond in the same language as the question.
            </instructions>

            Here is the question:
            <question>{message}</question>
        """
        )

        answer_prompt = ChatPromptTemplate.from_messages([system_prompt, user_prompt])

        documents = state.knowledgebase
        message = state.message

        chain = answer_prompt | self.llm | StrOutputParser()
        response = chain.invoke(
            {"today": today, "documents": documents, "message": message}
        )

        return {"answer": response}

    def get_graph(self):
        return self.graph.compile()
