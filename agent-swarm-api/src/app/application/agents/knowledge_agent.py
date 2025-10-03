from langgraph.graph import END, START, StateGraph

from app.domain.models import KnowledgeAgentState


class KnowledgeAgent:
    def __init__(self):
        graph = StateGraph(KnowledgeAgentState)

        graph.add_node("answer_question", self.__answer_question)

        graph.add_edge(START, "answer_question")
        graph.add_edge("answer_question", END)

        self.graph = graph

    def __answer_question(self, state: KnowledgeAgentState):
        return {"answer": "answer from knowledge agent"}

    def get_graph(self):
        return self.graph.compile()
