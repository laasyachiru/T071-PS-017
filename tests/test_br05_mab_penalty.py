
import pytest
from banking_engine import SavingsAccount


def create_account_with_mab(account_number, average_balance):
    account = SavingsAccount(
        account_number, "Asha", "REGULAR", average_balance,
        branch_category="METRO"
    )

    # Record the same balance for all 31 days of July.
    for day in range(1, 32):
        account.record_daily_balance(f"2026-07-{day:02d}")

    return account


def test_mab_shortfall_up_to_50_percent():
    account = create_account_with_mab(601, 5000)
    assert account.calculate_mab_penalty("2026-07") == 177


def test_mab_shortfall_above_50_to_75_percent():
    account = create_account_with_mab(602, 4000)
    assert account.calculate_mab_penalty("2026-07") == 354


def test_mab_shortfall_above_75_percent():
    account = create_account_with_mab(603, 2000)
    assert account.calculate_mab_penalty("2026-07") == 590


def test_no_penalty_when_required_mab_is_met():
    account = create_account_with_mab(604, 12000)
    assert account.calculate_mab_penalty("2026-07") == 0


def test_no_penalty_in_opening_month():
    account = create_account_with_mab(605, 2000)
    assert account.calculate_mab_penalty(
        "2026-07", opening_month=True
    ) == 0
