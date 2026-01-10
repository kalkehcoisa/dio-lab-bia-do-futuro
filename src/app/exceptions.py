"""
Exceções customizadas para o agente financeiro
"""


class AgentException(Exception):
    """Exceção base para o agente"""
    pass


class ValidationError(AgentException):
    """Erro de validação de dados"""
    pass


class DataLoadError(AgentException):
    """Erro ao carregar dados"""
    pass


class DataSaveError(AgentException):
    """Erro ao salvar dados"""
    pass


class ExtractionError(AgentException):
    """Erro na extração de dados"""
    pass


class LLMError(AgentException):
    """Erro ao interagir com LLM"""
    pass
