from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')
U = TypeVar('U')

class InputFlow(Generic[T]):
    class Step(Generic[U], ABC):
        def __init__(self, cmd: U):
            self.cmd = cmd
        @abstractmethod
        def is_complete(self) -> bool:
            pass
        # Called after show() on the first non complete step
        def activate(self):
            pass
        # Called after show() when this step is complete
        def complete(self):
            pass
        # Called when this step is not complete, or this is the first non complete step
        def show(self):
            pass
        # Called when a previous step is not complete
        def hide(self):
            pass

    def __init__(self, cmd: T):
        self.steps: list[InputFlow[T].Step[T]] = []

    def add_step(self, step: Step[T]):
        self.steps.append(step)

    def validate(self) -> bool:
        for step in self.steps:
            if not step.is_complete():
                return False
        return True

    def process(self):
        positive_invariant = True
        for step in self.steps:
            this_invariant = step.is_complete()
            if not positive_invariant:
                step.hide()
            else:
                step.show()
                if not this_invariant:
                    step.activate()
                else:
                    step.complete()
            positive_invariant = positive_invariant and this_invariant
