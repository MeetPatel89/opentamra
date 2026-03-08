class OpenTamraError(Exception):
    """Base exception for OpenTAMRA."""


class ValidationError(OpenTamraError):
    """Raised when input data fails validation."""


class PipelineError(OpenTamraError):
    """Raised when a pipeline step fails."""


class DataSourceError(OpenTamraError):
    """Raised when a data source operation fails."""


class JobError(OpenTamraError):
    """Raised when a job operation fails."""
