class PromptBuilderError(Exception):
    """Base exception for all Study-Aware Prompt Builder errors.
    Inherit from this to ensure consistent exception handling across the framework.
    """
    pass

class TemplateLoadError(PromptBuilderError):
    """Raised when a template JSON cannot be found, read, or is improperly formatted."""
    pass

class MissingParameterError(PromptBuilderError):
    """Raised when a prompt generation request is missing required template placeholders."""
    pass

class ParameterTypeError(PromptBuilderError):
    """Raised when injected variables are of an invalid type (e.g., passing nested dicts instead of strings)."""
    pass
