import pytest

from organisation import UnitManager, OrganisationUnit

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
    client = unit_manager.organisation_unit("client")

    calculate_membership_fee(MIN_WEEKLY_AMOUNT, "week", client)
    calculate_membership_fee(MAX_WEEKLY_AMOUNT, "week", client)
    calculate_membership_fee(MIN_MONTHLY_AMOUNT, "month", client)
    calculate_membership_fee(MAX_MONTHLY_AMOUNT, "month", client)

    with pytest.raises(ValueError):
        calculate_membership_fee(MIN_WEEKLY_AMOUNT, "not_month_or_week", client)


def test_rent_amount_raises_if_out_of_range(unit_manager):
    client = unit_manager.organisation_unit("client")

    calculate_membership_fee(MIN_WEEKLY_AMOUNT, "week", client)
    calculate_membership_fee(MAX_WEEKLY_AMOUNT, "week", client)
    calculate_membership_fee(MIN_MONTHLY_AMOUNT, "month", client)
    calculate_membership_fee(MAX_MONTHLY_AMOUNT, "month", client)

    with pytest.raises(ValueError):
        calculate_membership_fee(MIN_WEEKLY_AMOUNT - 1, "week", client)
        calculate_membership_fee(MAX_WEEKLY_AMOUNT + 1, "week", client)
        calculate_membership_fee(MIN_MONTHLY_AMOUNT - 1, "month", client)
        calculate_membership_fee(MAX_MONTHLY_AMOUNT + 1, "month", client)


def test_default_fee_happy_path():
    expected = MIN_WEEKLY_AMOUNT * VAT

    assert default_fee(MIN_WEEKLY_AMOUNT) == expected


def test_default_fee_if_weekly_too_low():
    weekly_amount = MIN_WEEKLY_AMOUNT - 1

    assert default_fee(weekly_amount) == default_fee(MIN_WEEKLY_AMOUNT)


def test_unit_manager_returns_organisation_unit(unit_manager):
    assert type(unit_manager.organisation_unit("division_b")) == OrganisationUnit


def test_unit_manager_happy_path(unit_manager):
    # same as config file
    assert unit_manager.organisation_unit("division_b").config == {
        "has_fixed_membership_fee": True,
        "fixed_membership_fee_amount": 35000,
    }


def test_unit_manager_returns_ancestor_config_if_not_defined(unit_manager):
    # branch_a config == {} in config test file, area_a is the parent
    branch_a = unit_manager.organisation_unit("branch_a")
    area_a = unit_manager.organisation_unit("area_a")

    assert branch_a.config == area_a.config


def test_fixed_membership_fee_amount(unit_manager):
    division_b = unit_manager.organisation_unit("division_b")

    assert (
        calculate_membership_fee(MIN_WEEKLY_AMOUNT, "week", division_b)
        == division_b.config["fixed_membership_fee_amount"]
    )


def test_returns_amount_if_not_fixed_membership_fee(unit_manager):
    branch_h = unit_manager.organisation_unit("branch_h")
    assert calculate_membership_fee(MIN_WEEKLY_AMOUNT, "week", branch_h) == default_fee(
        MIN_WEEKLY_AMOUNT
    )
