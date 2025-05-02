class RequestAI:
    def __init__(self, text: str, context: str = None, system: str = None):
        self.text = text
        self.context = context
        self.system = system  # Mensaje del sistema para API GPT


class ResponseAI:
    def __init__(self, content: str, sources: list = None, metadata: dict = None):
        self.content = content
        self.sources = sources or []
        self.metadata = metadata or {}


class ToolCall:
    def __init__(self, tool_name: str, args: dict):
        self.tool_name = tool_name
        self.args = args


class ToolResponse:
    def __init__(self, tool_name: str, result: dict, error: str = None):
        self.tool_name = tool_name
        self.result = result
        self.error = error


class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content