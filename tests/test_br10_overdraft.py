
from banking_engine import SavingsAccount


def test_salary_account_can_use_overdraft():
    account = SavingsAccount(1001, "Asha", "SALARY", 20000)

    account.withdraw(60000, "BRANCH", "2026-07-01")

    assert account.balance == -40000


def test_salary_overdraft_limit_is_50000():
    account = SavingsAccount(1002, "Asha", "SALARY", 10000)

    account.withdraw(61000, "BRANCH", "2026-07-01")

    assert account.balance == 10000


def test_regular_account_cannot_use_overdraft():
    account = SavingsAccount(1003, "Asha", "REGULAR", 10000)

    account.withdraw(15000, "BRANCH", "2026-07-01")

    assert account.balance == 10000


def test_senior_account_cannot_use_overdraft():
    account = SavingsAccount(1004, "Ravi", "SENIOR", 10000)

    account.withdraw(15000, "BRANCH", "2026-07-01")

    assert account.balance == 10000


def test_basic_account_cannot_use_overdraft():
    account = SavingsAccount(1005, "Asha", "BASIC", 10000)

    account.withdraw(15000, "BRANCH", "2026-07-01")

    assert account.balance == 10000



def test_salary_overdraft_interest_for_30_days():
    account = SavingsAccount(1006, "Asha", "SALARY", 0)

    # Simulate an existing overdraft of Rs. 40,000
    account.balance = -40000

    interest = account.calculate_overdraft_interest(30)

    expected_interest = 40000 * 0.12 * 30 / 365

    assert round(interest, 2) == round(expected_interest, 2)

