class IRobotError(Exception):
    pass

class AIError(IRobotError):
    pass

class IllegalOperation(AIError):
    pass

class ConfigError(IRobotError):
    pass
