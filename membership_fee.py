from organisation import OrganisationUnit

# amounts are in pence
MIN_WEEKLY_AMOUNT = 2500
MAX_WEEKLY_AMOUNT = 200000
MIN_MONTHLY_AMOUNT = 11000
MAX_MONTHLY_AMOUNT = 866000

MIN_WEEKLY_FEE = 12000

VAT = 1.2


def default_fee(weekly_amount: int) -> int:
    """Returns the default fee from the weekly rent amount"""
    if weekly_amount < MIN_WEEKLY_AMOUNT:
        weekly_amount = MIN_WEEKLY_AMOUNT

    return int(weekly_amount * VAT)


def calculate_membership_fee(
    rent_amount: int,
    rent_period: str,
    organisation_unit: OrganisationUnit,
) -> int:
    """Returns fixed membership fee amount if the organisation unit config has fixed membership fee, else returns the default fee"""

    if rent_period not in ["week", "month"]:
        raise ValueError("rent_period == week or month")

    if (
        rent_period == "week"
        and not MIN_WEEKLY_AMOUNT <= rent_amount <= MAX_WEEKLY_AMOUNT
    ):
        raise ValueError(
            f"{MIN_WEEKLY_AMOUNT} < weekly rent amount < {MAX_WEEKLY_AMOUNT}"
        )

    if (
        rent_period == "month"
        and not MIN_MONTHLY_AMOUNT <= rent_amount <= MAX_MONTHLY_AMOUNT
    ):
        raise ValueError(
            f"{MIN_MONTHLY_AMOUNT} < monthly rent amount < {MAX_MONTHLY_AMOUNT}"
        )

    if organisation_unit.config["has_fixed_membership_fee"]:
        return organisation_unit.config["fixed_membership_fee_amount"]

    weekly_amount = (
        rent_amount
        if rent_period == "week"
        else rent_amount / 4.33  # 4.33 weeks in a month
    )

    return default_fee(weekly_amount)
