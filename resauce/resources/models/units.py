from __future__ import annotations
from typing import Union, Type, Optional
import abc


class Unit(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @classmethod
    @abc.abstractmethod
    def base(cls) -> Unit:
        pass

    @abc.abstractmethod
    def to_base(self, value: float) -> float:
        pass

    @abc.abstractmethod
    def from_base(self, value: float) -> float:
        pass

    @abc.abstractmethod
    def operatable(self, other: Union[Unit]) -> bool:
        pass

    def convert(self, value: float, to: Optional[Unit] = None) -> float:
        if to is None:
            return value
        if not self.operatable(other=to):
            raise TypeError(f"unsupported unit: '{type(to)}'")
        return to.from_base(value=self.to_base(value=value))

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return self.__str__()

    @abc.abstractmethod
    def __hash__(self) -> int:
        pass

    @abc.abstractmethod
    def __eq__(self, other: Unit) -> bool:
        pass


class UnitGroup(metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def base_unit(cls) -> Unit:
        pass


class CpuUnit(Unit):
    def __init__(self, name: str, factor: float) -> None:
        self._name = name
        self._factor = factor

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    def base(cls) -> CpuUnit:
        return CpuUnit(name="core", factor=1)

    def to_base(self, value: float) -> float:
        return value * self._factor

    def from_base(self, value: float) -> float:
        return value / self._factor

    def operatable(self, other: Union[Unit]) -> bool:
        return other is None or isinstance(other, CpuUnit)

    def __hash__(self) -> int:
        return hash((self.__class__, self._factor))

    def __eq__(self, other: CpuUnit) -> bool:
        return self.__class__ == other.__class__ and self._factor == other._factor


class CpuUnits(UnitGroup):
    millicore: CpuUnit = CpuUnit(name="millicore", factor=1 / 1000)
    core: CpuUnit = CpuUnit(name="core", factor=1)

    # aliases
    m: CpuUnit = millicore

    @classmethod
    def base_unit(cls) -> CpuUnit:
        return CpuUnit.base()


class NumericUnit(Unit):
    def __init__(self, name: str, type_: Type) -> None:
        self._name = name
        if type_ not in {int, float}:
            raise TypeError(f"unsupported type: '{type_}'")
        self._type = type_

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    def base(cls) -> CpuUnit:
        return CpuUnit(name="float", type_=float)

    def to_base(self, value: float) -> float:
        return float(value)

    def from_base(self, value: float) -> float:
        return float(self._type(value))

    def operatable(self, other: Union[Unit]) -> bool:
        return other is None or isinstance(other, NumericUnit)

    def __hash__(self) -> int:
        return hash((self.__class__, self._type))

    def __eq__(self, other: NumericUnit):
        return self.__class__ == other.__class__ and self._type == other._type


class NumericUnits(UnitGroup):
    float: NumericUnit = NumericUnit(name="float", type_=float)
    int: NumericUnit = NumericUnit(name="int", type_=int)

    @classmethod
    def base_unit(cls) -> NumericUnit:
        return NumericUnit.base()


class StorageUnit(Unit):
    def __init__(self, name: str, factor: float) -> None:
        self._name = name
        self._factor = factor

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    def base(cls) -> StorageUnit:
        return StorageUnit(name="B", factor=1)

    def to_base(self, value: float) -> float:
        return value * self._factor

    def from_base(self, value: float) -> float:
        return value / self._factor

    def operatable(self, other: Union["Unit"]) -> bool:
        return other is None or isinstance(other, StorageUnit)

    def __hash__(self) -> int:
        return hash((self.__class__, self._factor))

    def __eq__(self, other: StorageUnit):
        return self.__class__ == other.__class__ and self._factor == other._factor


class StorageUnits:
    mB: StorageUnit = StorageUnit(name="mB", factor=1 / 1000)
    B: StorageUnit = StorageUnit(name="B", factor=1)

    KiB: StorageUnit = StorageUnit(name="KiB", factor=1024)
    MiB: StorageUnit = StorageUnit(name="MiB", factor=1024 ** 2)
    GiB: StorageUnit = StorageUnit(name="GiB", factor=1024 ** 3)
    TiB: StorageUnit = StorageUnit(name="TiB", factor=1024 ** 4)
    PiB: StorageUnit = StorageUnit(name="PiB", factor=1024 ** 5)

    KB: StorageUnit = StorageUnit(name="KB", factor=1000)
    MB: StorageUnit = StorageUnit(name="MB", factor=1000 ** 2)
    GB: StorageUnit = StorageUnit(name="GB", factor=1000 ** 3)
    TB: StorageUnit = StorageUnit(name="TB", factor=1000 ** 4)
    PB: StorageUnit = StorageUnit(name="PB", factor=1000 ** 5)

    # aliases
    millibyte: StorageUnit = mB
    m: StorageUnit = mB
    byte: StorageUnit = B
    kibibyte: StorageUnit = KiB
    kilobyte: StorageUnit = KB
    kib: StorageUnit = KiB
    kb: StorageUnit = KB
    ki: StorageUnit = KiB
    Ki: StorageUnit = KiB
    K: StorageUnit = KB
    mebibyte: StorageUnit = MiB
    megabyte: StorageUnit = MB
    mib: StorageUnit = MiB
    mb: StorageUnit = MB
    mi: StorageUnit = MiB
    Mi: StorageUnit = MiB
    M: StorageUnit = MB
    gibibyte: StorageUnit = GiB
    gigabyte: StorageUnit = GB
    gib: StorageUnit = GiB
    gb: StorageUnit = GB
    gi: StorageUnit = GiB
    Gi: StorageUnit = GiB
    G: StorageUnit = GB
    tebibyte: StorageUnit = TiB
    terabyte: StorageUnit = TB
    tib: StorageUnit = TiB
    tb: StorageUnit = TB
    ti: StorageUnit = TiB
    Ti: StorageUnit = TiB
    T: StorageUnit = TB
    pebibyte: StorageUnit = PiB
    petabyte: StorageUnit = PB
    pib: StorageUnit = PiB
    pb: StorageUnit = PB
    pi: StorageUnit = PiB
    Pi: StorageUnit = PiB
    P: StorageUnit = PB

    @classmethod
    def base_unit(cls) -> StorageUnit:
        return StorageUnit.base()
