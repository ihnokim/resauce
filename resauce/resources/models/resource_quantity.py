from __future__ import annotations
from typing import Optional, Union
from decimal import Decimal
from resauce.resources.models.units import Unit


class ResourceQuantity:  # immutable
    def __init__(self, value: Union[int, float, Decimal] = 0.0, unit: Optional[Unit] = None) -> None:
        self._value: Decimal = self._refine_value(value=value)
        self._unit: Optional[Unit] = unit

    @property
    def value(self) -> Decimal:
        return self._value

    @property
    def unit(self) -> Optional[Unit]:
        return self._unit

    @staticmethod
    def _refine_value(value: Union[int, float, Decimal]) -> Decimal:
        if isinstance(value, int) or isinstance(value, float):
            _value = Decimal(str(value))
        else:
            _value = value
        return _value

    def convert(self, unit: Optional[Unit] = None) -> ResourceQuantity:
        if self._unit is not None:
            return ResourceQuantity(
                value=self.unit.convert(value=self._value, to=unit),
                unit=unit,
            )
        else:
            return ResourceQuantity(value=self._value, unit=unit)

    def __hash__(self) -> int:
        return hash((self.__class__, self._value, hash(self._unit)))

    def _preprocess_operand(self, operand: Union[int, float, Decimal, ResourceQuantity]) -> ResourceQuantity:
        type_error_message = f"unsupported operand type(s) for +: '{self.__class__.__name__}' and '{type(operand)}'"
        if isinstance(operand, ResourceQuantity):
            if self.unit is None:
                return ResourceQuantity(value=operand.value, unit=operand.unit)
            elif self.unit.operatable(operand.unit):
                return operand.convert(unit=self.unit)
            else:
                raise TypeError(type_error_message)
        elif isinstance(operand, int) or isinstance(operand, float) or isinstance(operand, Decimal):
            result = ResourceQuantity(value=operand, unit=None)
        else:
            raise TypeError(type_error_message)
        return result

    def __add__(self, other: Union[int, float, Decimal, ResourceQuantity]) -> ResourceQuantity:
        operand = self._preprocess_operand(operand=other)
        return ResourceQuantity(
            value=self.value + operand.value,
            unit=self.unit or operand.unit,
        )

    def __sub__(self, other: Union[int, float, Decimal, ResourceQuantity]) -> ResourceQuantity:
        operand = self._preprocess_operand(operand=other)
        return ResourceQuantity(
            value=self.value - operand.value,
            unit=self.unit or operand.unit,
        )

    def __mul__(self, other: Union[int, float, Decimal, ResourceQuantity]) -> ResourceQuantity:
        operand = self._preprocess_operand(operand=other)
        return ResourceQuantity(
            value=self.value * operand.value,
            unit=self.unit or operand.unit,
        )

    def __truediv__(self, other: Union[int, float, Decimal, ResourceQuantity]) -> ResourceQuantity:
        operand = self._preprocess_operand(operand=other)
        return ResourceQuantity(
            value=self.value / operand.value,
            unit=self.unit or operand.unit,
        )

    def __floordiv__(self, other: Union[int, float, Decimal, ResourceQuantity]) -> ResourceQuantity:
        operand = self._preprocess_operand(operand=other)
        return ResourceQuantity(
            value=self.value // operand.value,
            unit=self.unit or operand.unit,
        )

    def __mod__(self, other: Union[int, float, Decimal, ResourceQuantity]) -> ResourceQuantity:
        operand = self._preprocess_operand(operand=other)
        return ResourceQuantity(
            value=self.value % operand.value,
            unit=self.unit or operand.unit,
        )

    def __eq__(self, other: Union[int, float, Decimal, ResourceQuantity]) -> bool:
        operand = self._preprocess_operand(operand=other)
        return self.value == operand.value

    def __ne__(self, other: Union[int, float, Decimal, ResourceQuantity]) -> bool:
        operand = self._preprocess_operand(operand=other)
        return self.value != operand.value

    def __gt__(self, other: Union[int, float, Decimal, ResourceQuantity]) -> bool:
        operand = self._preprocess_operand(operand=other)
        return self.value > operand.value

    def __lt__(self, other: Union[int, float, Decimal, ResourceQuantity]) -> bool:
        operand = self._preprocess_operand(operand=other)
        return self.value < operand.value

    def __ge__(self, other: Union[int, float, Decimal, ResourceQuantity]) -> bool:
        operand = self._preprocess_operand(operand=other)
        return self.value >= operand.value

    def __le__(self, other: Union[int, float, Decimal, ResourceQuantity]) -> bool:
        operand = self._preprocess_operand(operand=other)
        return self.value <= operand.value

    def __bool__(self) -> bool:
        return bool(self._value)

    def __str__(self) -> str:
        result = f"{self._value}"
        if self._unit is not None:
            result += f" {self._unit}"
        return result

    def __repr__(self) -> str:
        return self.__str__()
