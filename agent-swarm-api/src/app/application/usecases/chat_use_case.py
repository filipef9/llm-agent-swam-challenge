from app.application.agents import RouterAgent


class ChatUseCase:
    def __init__(self, router_agent: RouterAgent) -> None:
        self.router_agent = router_agent

    def execute(self, user_id: str, message: str) -> str:
        return "Hello, world, from use case execute method."
