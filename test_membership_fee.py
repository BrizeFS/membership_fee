import pytest

from unit_manager import UnitManager

from membership_fee import (
    calculate_membership_fee,
    default_fee,
    VAT,
    MIN_MONTHLY_AMOUNT,
    MAX_MONTHLY_AMOUNT,
    MIN_WEEKLY_AMOUNT,
    MAX_WEEKLY_AMOUNT,
    MIN_WEEKLY_FEE,
)


@pytest.fixture
def unit_manager():
    return UnitManager("./test.adjlist", "./test.config")


def test_rent_period_raises_if_not_month_or_week(unit_manager):
    calculate_membership_fee(MIN_WEEKLY_AMOUNT, "week", "client", unit_manager)
    calculate_membership_fee(MAX_WEEKLY_AMOUNT, "week", "client", unit_manager)
    calculate_membership_fee(MIN_MONTHLY_AMOUNT, "month", "client", unit_manager)
    calculate_membership_fee(MAX_MONTHLY_AMOUNT, "month", "client", unit_manager)

    with pytest.raises(ValueError):
        calculate_membership_fee(
            MIN_WEEKLY_AMOUNT, "not_month_or_week", "client", unit_manager
        )


def test_rent_amount_raises_if_out_of_range(unit_manager):
    calculate_membership_fee(MIN_WEEKLY_AMOUNT, "week", "client", unit_manager)
    calculate_membership_fee(MAX_WEEKLY_AMOUNT, "week", "client", unit_manager)
    calculate_membership_fee(MIN_MONTHLY_AMOUNT, "month", "client", unit_manager)
    calculate_membership_fee(MAX_MONTHLY_AMOUNT, "month", "client", unit_manager)

    with pytest.raises(ValueError):
        calculate_membership_fee(MIN_WEEKLY_AMOUNT - 1, "week", "client", unit_manager)
        calculate_membership_fee(MAX_WEEKLY_AMOUNT + 1, "week", "client", unit_manager)
        calculate_membership_fee(
            MIN_MONTHLY_AMOUNT - 1, "month", "client", unit_manager
        )
        calculate_membership_fee(
            MAX_MONTHLY_AMOUNT + 1, "month", "client", unit_manager
        )


def test_default_fee_happy_path():
    expected = MIN_WEEKLY_AMOUNT * VAT

    assert default_fee(MIN_WEEKLY_AMOUNT) == expected


def test_default_fee_if_weekly_too_low():
    weekly_amount = MIN_WEEKLY_AMOUNT - 1

    assert default_fee(weekly_amount) == default_fee(MIN_WEEKLY_AMOUNT)


def test_unit_manager_returns_unit_config(unit_manager):
    assert unit_manager.config("division_b") == {
        "has_fixed_membership_fee": True,
        "fixed_membership_fee_amount": 35000,
    }


def test_unit_manager_returns_ancestor_config_if_not_defined(unit_manager):
    # branch_m config == {} in config test file, area_d is the parent
    assert unit_manager.config("branch_m") == unit_manager.config("area_d")


def test_has_fixed_membership_fee(unit_manager):
    assert unit_manager.has_fixed_membership_fee("division_b") == True


def test_has_fixed_membership_fee_of_parent(unit_manager):
    assert unit_manager.has_fixed_membership_fee(
        "branch_m"
    ) == unit_manager.has_fixed_membership_fee("area_d")


def test_fixed_membership_fee_amount(unit_manager):
    assert calculate_membership_fee(
        MIN_WEEKLY_AMOUNT, "week", "division_b", unit_manager
    ) == unit_manager.fixed_membership_fee_amount("division_b")


def test_returns_amount_if_not_fixed_membership_fee(unit_manager):
    assert calculate_membership_fee(
        MIN_WEEKLY_AMOUNT, "week", "branch_h", unit_manager
    ) == default_fee(MIN_WEEKLY_AMOUNT)
