
from datetime import date
from banking_engine import SavingsAccount


def test_money_calculation_accuracy():
    account = SavingsAccount(1501, "Asha", "REGULAR", 0.20)

    account.deposit(0.10)

    assert round(account.balance, 2) == 0.30


def test_leap_year_february_date_handling():
    account = SavingsAccount(1502, "Ravi", "REGULAR", 5000)

    result = account._add_months(date(2024, 1, 31), 1)

    assert result == date(2024, 2, 29)


def test_normal_year_february_date_handling():
    account = SavingsAccount(1503, "Anu", "REGULAR", 5000)

    result = account._add_months(date(2025, 1, 31), 1)

    assert result == date(2025, 2, 28)


def test_year_end_date_handling():
    account = SavingsAccount(1504, "Kiran", "REGULAR", 5000)

    result = account._add_months(date(2026, 12, 31), 1)

    assert result == date(2027, 1, 31)


def test_month_end_date_handling():
    account = SavingsAccount(1505, "Meena", "REGULAR", 5000)

    result = account._add_months(date(2026, 3, 31), 1)

    assert result == date(2026, 4, 30)
