from datetime import datetime

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, create_react_agent, tools_condition

from app.domain.models import CustomerSupportAgentState


class CustomerSupportAgent:
    def __init__(
        self,
        llm: BaseChatModel,
        customer_products_tool: BaseTool,
        customer_financial_information_tool: BaseTool,
    ):
        tools = [customer_products_tool, customer_financial_information_tool]
        self.llm = llm.bind_tools(tools)

        graph = StateGraph(CustomerSupportAgentState)

        graph.add_node("assistant", self.__assistant)
        graph.add_node("tools", ToolNode(tools))
        graph.add_node("return_final_answer", self.__return_final_answer)

        graph.add_edge(START, "assistant")
        graph.add_edge("tools", "assistant")

        graph.add_conditional_edges(
            "assistant",
            tools_condition,
            {"tools": "tools", "__end__": "return_final_answer"},
        )
        graph.add_edge("return_final_answer", END)

        self.graph = graph

    def __assistant(self, state: CustomerSupportAgentState):
        system_message = SystemMessage(
            content=(
                "You are an assistant for question-answering tasks. "
                "Solve the user question using available tools only. "
                "Your job is to choose the correct tool and return the result"
            )
        )

        today = datetime.now().strftime("%d/%m/%y")
        customer_id = state.user_id
        message = state.message

        user_prompt_template = HumanMessagePromptTemplate.from_template(
            """
            Today is {today}.
            Customer ID: {customer_id}

            <instructions>
            1. If you don't know the answer, just say that you don't know.
            2. Identify the language of the question and store it between the <language> tags.
            3. Always respond in the same language in <language> tags.
            3. Keep your response terse.
            </instructions>

            <language></language>

            Answer the following question:
            <question>{message}</question>
        """
        )

        user_message = HumanMessage(
            content=user_prompt_template.format(
                today=today, customer_id=customer_id, message=message
            ).content
        )

        messages = state.messages

        if not state.messages:
            messages = [system_message, user_message]

        response = self.llm.invoke(messages)
        return {"messages": [response]}

    def __return_final_answer(
        self, state: CustomerSupportAgentState
    ) -> CustomerSupportAgentState:
        answer = state.messages[-1]
        return {"answer": answer.content}

    def get_graph(self):
        return self.graph.compile()
