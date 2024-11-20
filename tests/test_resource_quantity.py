from resauce.resources.models.resource_quantity import ResourceQuantity
from resauce.resources.models.units import StorageUnits, CpuUnits
from decimal import Decimal


def test_equality():
    quantity1 = ResourceQuantity(value=3.5, unit=StorageUnits.GiB)
    quantity2 = ResourceQuantity(value=3.5, unit=StorageUnits.GiB)
    assert quantity1 == quantity2


def test_hash():
    quantity1 = ResourceQuantity(value=3.5, unit=StorageUnits.GiB)
    quantity2 = ResourceQuantity(value=3.5, unit=StorageUnits.GiB)
    unit1 = StorageUnits.m
    unit2 = CpuUnits.m
    unit3 = CpuUnits.millicore
    assert hash(quantity1) == hash(quantity2)
    assert hash(unit1) != hash(unit2)
    assert hash(unit2) == hash(unit3)


def test_uniqueness():
    quantity1 = ResourceQuantity(value=3.5, unit=StorageUnits.GiB)
    quantity2 = ResourceQuantity(value=3.5, unit=StorageUnits.GiB)
    s = set([quantity1, quantity2])
    assert len(s) == 1


def test_operation_between_storage_units():
    quantity1 = ResourceQuantity(value=3.5, unit=StorageUnits.GiB)
    quantity2 = ResourceQuantity(value=520, unit=StorageUnits.MiB)
    result = quantity1 + quantity2
    raw_result = ((3.5 * (1024 ** 3)) + (520 * (1024 ** 2))) / (1024 ** 3)
    assert id(result) != id(quantity1)
    assert id(result) != id(quantity2)
    assert result.value == Decimal(str(raw_result))
    assert result == raw_result
    result = quantity1 - quantity2
    raw_result = ((3.5 * (1024 ** 3)) - (520 * (1024 ** 2))) / (1024 ** 3)
    assert result.value == Decimal(str(raw_result))
    assert result == raw_result


def test_operation_between_storage_unit_and_scalar():
    quantity1 = ResourceQuantity(value=3.5, unit=StorageUnits.GiB)
    quantity2 = 3
    result = quantity1 + quantity2
    assert result == 6.5
    assert result != 2.5


def test_unit_operability_with_none():
    quantity1 = ResourceQuantity(value=3.5, unit=StorageUnits.GiB)
    quantity2 = ResourceQuantity(2, None)
    preprocessed_quantity1 = quantity2._preprocess_operand(operand=quantity1)
    preprocessed_quantity2 = quantity1._preprocess_operand(operand=quantity2)
    assert quantity1.unit.operatable(quantity2.unit)
    assert preprocessed_quantity1.unit == StorageUnits.GiB
    assert preprocessed_quantity2.unit == StorageUnits.GiB


def test_value_comparison():
    quantity1 = ResourceQuantity(value=5.6, unit=StorageUnits.MiB)
    quantity2 = quantity1.convert(unit=StorageUnits.GiB)
    assert quantity2.unit == StorageUnits.GiB
    assert quantity1 < 6
    assert quantity1 > 3.5
    assert quantity1 <= 6
    assert quantity1 >= 3.5
    assert quantity1 == quantity2
    assert quantity1 < quantity2 + 3
