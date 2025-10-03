from langgraph.graph import END, START, StateGraph

from app.domain.models import CustomerSupportAgentState


class CustomerSupportAgent:
    def __init__(self):
        graph = StateGraph(CustomerSupportAgentState)

        graph.add_node("answer_question", self.__answer_question)

        graph.add_edge(START, "answer_question")
        graph.add_edge("answer_question", END)

        self.graph = graph

    def __answer_question(self, state: CustomerSupportAgentState):
        return {"answer": "answer from customer support agent"}

    def get_graph(self):
        return self.graph.compile()
