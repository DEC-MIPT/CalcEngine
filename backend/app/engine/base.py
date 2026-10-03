from abc import ABC, abstractmethod


class Calculator[InputsT, ParametersT, ResultT](ABC):
    """Чистый расчёт: на входе типизированные входы и разрешённые параметры, на выходе результат."""

    @abstractmethod
    def calculate(self, inputs: InputsT, parameters: ParametersT) -> ResultT: ...
