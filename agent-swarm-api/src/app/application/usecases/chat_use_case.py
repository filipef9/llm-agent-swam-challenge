from app.application.agents import RouterAgent
from app.domain.models import RouterAgentState


class ChatUseCase:
    def __init__(self, router_agent: RouterAgent) -> None:
        self.router_agent = router_agent

    def execute(self, user_id: str, message: str) -> str:
        initial_state = RouterAgentState(user_id=user_id, message=message)
        response = self.router_agent.get_graph().invoke(initial_state)
        return response["answer"]
