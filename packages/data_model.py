from pydantic import BaseModel, Field


class PythonCode(BaseModel):
    """Information about a PythonCode."""
    query: str = Field(description="Users query")
    code: str = Field(description="Code of the python function")
