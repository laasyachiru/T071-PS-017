
import pytest
from banking_engine import SavingsAccount


def test_metro_mab_requirement():
    account = SavingsAccount(501, "Asha", "REGULAR", 20000,
                             branch_category="METRO")
    assert account.get_required_mab() == 10000


def test_urban_mab_requirement():
    account = SavingsAccount(502, "Ravi", "REGULAR", 10000,
                             branch_category="URBAN")
    assert account.get_required_mab() == 5000


def test_semi_urban_mab_requirement():
    account = SavingsAccount(503, "Anu", "REGULAR", 5000,
                             branch_category="SEMI_URBAN")
    assert account.get_required_mab() == 2500


def test_rural_mab_requirement():
    account = SavingsAccount(504, "Kiran", "REGULAR", 3000,
                             branch_category="RURAL")
    assert account.get_required_mab() == 1000


def test_salary_account_mab_exemption():
    account = SavingsAccount(505, "Meena", "SALARY", 0,
                             branch_category="METRO")
    assert account.get_required_mab() == 0


def test_basic_account_mab_exemption():
    account = SavingsAccount(506, "Asha", "BASIC", 0,
                             branch_category="METRO")
    assert account.get_required_mab() == 0


def test_calculate_monthly_average_balance():
    account = SavingsAccount(507, "Ravi", "REGULAR", 10000)

    for day in range(1, 32):
        if day == 1:
            account.balance = 10000
        elif day == 2:
            account.balance = 20000
        elif day == 3:
            account.balance = 30000
        else:
            account.balance = 20000

        account.record_daily_balance(f"2026-07-{day:02d}")

    assert account.calculate_mab("2026-07") == pytest.approx(
        (10000 + 20000 + 30000 + 28 * 20000) / 31
    )


def test_mab_with_single_day():
    account = SavingsAccount(508, "Anu", "REGULAR", 15000)

    # Record the same closing balance for all 31 days.
    for day in range(1, 32):
        account.record_daily_balance(f"2026-07-{day:02d}")

    assert account.calculate_mab("2026-07") == 15000
