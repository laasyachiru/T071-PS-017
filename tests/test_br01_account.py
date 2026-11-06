
import pytest
from banking_engine import SavingsAccount


def test_create_regular_account():
    account = SavingsAccount(101, "Laasya", "REGULAR", 50000)

    assert account.account_number == 101
    assert account.account_type == "Regular"
    assert account.balance == 50000


def test_create_salary_account():
    account = SavingsAccount(102, "Asha", "SALARY", 30000)

    assert account.account_type == "Salary"


def test_create_senior_account():
    account = SavingsAccount(103, "Ravi", "SENIOR", 40000)

    assert account.account_type == "Senior"


def test_create_basic_account():
    account = SavingsAccount(104, "Anu", "BASIC", 1000)

    assert account.account_type == "Basic"


def test_invalid_account_type():
    with pytest.raises(ValueError):
        SavingsAccount(105, "Ravi", "GOLD", 10000)


def test_invalid_branch_category():
    with pytest.raises(ValueError):
        SavingsAccount(106, "Asha", "REGULAR", 10000,
                       branch_category="VILLAGE")


def test_negative_opening_balance():
    with pytest.raises(ValueError):
        SavingsAccount(107, "Anu", "REGULAR", -500)


def test_basic_account_cannot_use_sweep_in():
    with pytest.raises(ValueError):
        SavingsAccount(108, "Ravi", "BASIC", 30000,
                       sweep_in_enabled=True)


def test_sweep_threshold_below_minimum():
    with pytest.raises(ValueError):
        SavingsAccount(109, "Asha", "REGULAR", 30000,
                       sweep_threshold=20000)


def test_valid_branch_category():
    account = SavingsAccount(110, "Ravi", "REGULAR", 30000,
                             branch_category="RURAL")

    assert account.branch_category == "RURAL"
