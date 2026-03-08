from __future__ import annotations

from abc import ABC, abstractmethod

from backend.pipeline.context import PipelineContext


class BaseStep(ABC):
    name: str
    order: int
    output_level: str | None = None

    @abstractmethod
    def execute(self, ctx: PipelineContext) -> PipelineContext: ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name} order={self.order}>"
