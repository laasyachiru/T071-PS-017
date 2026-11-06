
import pytest
from banking_engine import SavingsAccount


def test_interest_for_balance_below_one_lakh():
    account = SavingsAccount(401, "Asha", "REGULAR", 50000)

    interest = account.calculate_daily_interest()

    assert interest == pytest.approx(50000 * 0.03 / 365)


def test_interest_at_one_lakh():
    account = SavingsAccount(402, "Ravi", "REGULAR", 100000)

    interest = account.calculate_daily_interest()

    assert interest == pytest.approx(100000 * 0.03 / 365)


def test_interest_above_one_lakh():
    account = SavingsAccount(403, "Anu", "REGULAR", 200000)

    expected = (100000 * 0.03 + 100000 * 0.035) / 365

    assert account.calculate_daily_interest() == pytest.approx(expected)


def test_interest_above_ten_lakh():
    account = SavingsAccount(404, "Kiran", "REGULAR", 1100000)

    expected = (
        100000 * 0.03
        + 900000 * 0.035
        + 100000 * 0.04
    ) / 365

    assert account.calculate_daily_interest() == pytest.approx(expected)


def test_senior_citizen_extra_interest():
    account = SavingsAccount(405, "Meena", "SENIOR", 50000)

    expected = 50000 * 0.035 / 365

    assert account.calculate_daily_interest() == pytest.approx(expected)


def test_senior_citizen_interest_above_one_lakh():
    account = SavingsAccount(406, "Ravi", "SENIOR", 200000)

    expected = (
        100000 * 0.035
        + 100000 * 0.04
    ) / 365

    assert account.calculate_daily_interest() == pytest.approx(expected)

    
def test_record_daily_balance():
    account = SavingsAccount(407, "Asha", "REGULAR", 50000)

    account.record_daily_balance("2026-06-29")

    assert account.daily_balances["2026-06-29"] == 50000


def test_quarterly_interest_calculation():
    account = SavingsAccount(408, "Ravi", "REGULAR", 50000)

    account.record_daily_balance("2026-06-29")
    account.record_daily_balance("2026-06-30")

    expected = (50000 * 0.03 / 365) * 2

    assert account.calculate_quarterly_interest(
        "2026-06-30"
    ) == pytest.approx(expected)


def test_quarterly_interest_credit():
    account = SavingsAccount(409, "Anu", "REGULAR", 50000)

    account.record_daily_balance("2026-06-29")
    account.record_daily_balance("2026-06-30")

    account.credit_quarterly_interest("2026-06-30")

    # Two days' interest is approximately Rs. 8.22,
    # so the credited amount should be Rs. 8.
    assert account.balance == 50008

