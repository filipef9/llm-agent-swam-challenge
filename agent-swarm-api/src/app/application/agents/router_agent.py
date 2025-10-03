from typing import Literal

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langgraph.graph import END, START, StateGraph

from app.application.agents import CustomerSupportAgent, KnowledgeAgent
from app.domain.models import Router, RouterAgentState


class RouterAgent:
    def __init__(
        self,
        knowledge_agent: KnowledgeAgent,
        customer_support_agent: CustomerSupportAgent,
        llm: BaseChatModel,
    ):
        graph = StateGraph(RouterAgentState)

        graph.add_node("router", self.__router_node)
        graph.add_node("knowledge_agent", knowledge_agent.get_graph())
        graph.add_node("customer_support_agent", customer_support_agent.get_graph())

        graph.add_edge(START, "router")

        graph.add_conditional_edges(
            "router",
            self.__call_next_agent,
        )

        graph.add_edge("knowledge_agent", END)
        graph.add_edge("customer_support_agent", END)

        self.graph = graph
        self.llm = llm

    def __call_next_agent(
        self,
        state: RouterAgentState,
    ) -> Literal["knowledge_agent", "customer_support_agent"]:
        return state.next_agent

    def __router_node(self, state: RouterAgentState) -> RouterAgentState:
        system_prompt = SystemMessagePromptTemplate.from_template(
            """
            You are a router agent tasked with managing a conversation between the
            following agents: 
            - knowledge_agent: This agent will be responsible for answer questions about
              the company's products and services. This agent is also capable of
              answer general purpose questions. 
            - customer_support_agent: This agent will provide customer support, retrieving
              relevant user data to answer the inquiries.

            Given the following user message, respond with the agent to act next.
        """
        )

        user_prompt = HumanMessagePromptTemplate.from_template(
            "user message: {message}"
        )

        router_prompt = ChatPromptTemplate.from_messages([system_prompt, user_prompt])

        chain = router_prompt | self.llm.with_structured_output(Router)

        message = state.message
        response = chain.invoke({"message": message})

        return {"next_agent": response.next}

    def get_graph(self):
        return self.graph.compile()
