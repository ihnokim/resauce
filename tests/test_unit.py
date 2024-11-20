from resauce.resources.models.units import CpuUnit, NumericUnit, StorageUnit


def test_cpu_unit_equality():
    unit1 = CpuUnit(name="MyUnit", factor=1)
    unit2 = CpuUnit(name="MyUnit", factor=2)
    unit3 = CpuUnit(name="MyUnit", factor=1)
    unit4 = CpuUnit(name="AliasedUnit", factor=1)
    assert hash(unit1) != hash(unit2)
    assert unit1 != unit2
    assert hash(unit1) == hash(unit3)
    assert unit1 == unit3
    assert hash(unit1) == hash(unit4)
    assert unit1 == unit4
    assert len({unit1, unit2, unit3, unit4}) == 2


def test_numeric_unit_equality():
    unit1 = NumericUnit(name="MyUnit", type_=int)
    unit2 = NumericUnit(name="MyUnit", type_=float)
    unit3 = NumericUnit(name="MyUnit", type_=int)
    unit4 = NumericUnit(name="AliasedUnit", type_=int)
    assert hash(unit1) != hash(unit2)
    assert unit1 != unit2
    assert hash(unit1) == hash(unit3)
    assert unit1 == unit3
    assert hash(unit1) == hash(unit4)
    assert unit1 == unit4
    assert len({unit1, unit2, unit3, unit4}) == 2


def test_storage_unit_equality():
    unit1 = StorageUnit(name="MyUnit", factor=1)
    unit2 = StorageUnit(name="MyUnit", factor=2)
    unit3 = StorageUnit(name="MyUnit", factor=1)
    unit4 = StorageUnit(name="AliasedUnit", factor=1)
    assert hash(unit1) != hash(unit2)
    assert unit1 != unit2
    assert hash(unit1) == hash(unit3)
    assert unit1 == unit3
    assert hash(unit1) == hash(unit4)
    assert unit1 == unit4
    assert len({unit1, unit2, unit3, unit4}) == 2
