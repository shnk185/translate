import enum

class PromptType(str, enum.Enum):
    SYSTEM = "system"
    USER = "user"