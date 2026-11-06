
from banking_engine import SavingsAccount


def test_metro_minimum_balance():
    account = SavingsAccount(201, "Asha", "REGULAR", 20000,
                             branch_category="METRO")
    assert account.get_required_mab() == 10000


def test_urban_minimum_balance():
    account = SavingsAccount(202, "Ravi", "REGULAR", 10000,
                             branch_category="URBAN")
    assert account.get_required_mab() == 5000


def test_semi_urban_minimum_balance():
    account = SavingsAccount(203, "Anu", "REGULAR", 5000,
                             branch_category="SEMI_URBAN")
    assert account.get_required_mab() == 2500


def test_rural_minimum_balance():
    account = SavingsAccount(204, "Kiran", "REGULAR", 3000,
                             branch_category="RURAL")
    assert account.get_required_mab() == 1000


def test_salary_account_exemption():
    account = SavingsAccount(205, "Asha", "SALARY", 0,
                             branch_category="METRO")
    assert account.get_required_mab() == 0


def test_basic_account_exemption():
    account = SavingsAccount(206, "Ravi", "BASIC", 0,
                             branch_category="METRO")
    assert account.get_required_mab() == 0
