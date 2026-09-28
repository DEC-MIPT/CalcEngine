from abc import ABC, abstractmethod


class Calculator[InputsT, ParametersT, ResultT](ABC):
    """A pure calculation: typed inputs and resolved parameters in, a result out."""

    @abstractmethod
    def calculate(self, inputs: InputsT, parameters: ParametersT) -> ResultT: ...
