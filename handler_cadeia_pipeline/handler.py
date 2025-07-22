from abc import ABC, abstractmethod
from typing import Optional
from context.pipeline_context import PipelineContext

class Handler(ABC):

    def __init__(self):
        self._next_handler : Optional['Handler'] = None

    def set_next(self, hander: "Handler")-> "Handler":
        self._next_handler = hander
        return hander

    @abstractmethod
    def handle(self, context: PipelineContext):
        pass
