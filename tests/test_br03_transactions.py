
import pytest
from banking_engine import SavingsAccount


def test_deposit_transaction():
    account = SavingsAccount(301, "Asha", "REGULAR", 10000)
    account.deposit(2000)
    assert account.balance == 12000


def test_atm_withdrawal():
    account = SavingsAccount(302, "Ravi", "REGULAR", 10000)
    account.withdraw(1000)
    assert account.balance == 9000


def test_branch_withdrawal():
    account = SavingsAccount(303, "Anu", "REGULAR", 10000)
    account.withdraw(2000)
    assert account.balance == 8000


def test_neft_credit():
    account = SavingsAccount(304, "Kiran", "REGULAR", 10000)
    account.deposit(5000)
    assert account.balance == 15000


def test_cheque_credit():
    account = SavingsAccount(305, "Meena", "REGULAR", 10000)
    account.deposit(3000)
    assert account.balance == 13000


def test_transaction_history():
    account = SavingsAccount(306, "Asha", "REGULAR", 10000)
    account.deposit(2000)
    account.withdraw(1000)

    assert len(account.transactions) == 2


def test_invalid_deposit():
    account = SavingsAccount(307, "Ravi", "REGULAR", 10000)
    account.deposit(-500)
    assert account.balance == 10000


def test_insufficient_balance():
    account = SavingsAccount(308, "Anu", "REGULAR", 1000)
    account.withdraw(2000)
    assert account.balance == 1000

    
def test_neft_transaction_type():
    account = SavingsAccount(309, "Asha", "REGULAR", 10000)
    account.deposit(5000, "NEFT")
    assert "NEFT" in account.transactions[-1]


def test_cheque_transaction_type():
    account = SavingsAccount(310, "Ravi", "REGULAR", 10000)
    account.deposit(3000, "CHEQUE")
    assert "CHEQUE" in account.transactions[-1]


def test_atm_transaction_type():
    account = SavingsAccount(311, "Anu", "REGULAR", 10000)
    account.withdraw(1000, "ATM")
    assert "ATM" in account.transactions[-1]


def test_branch_transaction_type():
    account = SavingsAccount(312, "Kiran", "REGULAR", 10000)
    account.withdraw(2000, "BRANCH")
    assert "BRANCH" in account.transactions[-1]


def test_invalid_deposit_transaction_type():
    account = SavingsAccount(313, "Meena", "REGULAR", 10000)
    account.deposit(1000, "INVALID")
    assert account.balance == 10000


def test_invalid_withdrawal_transaction_type():
    account = SavingsAccount(314, "Asha", "REGULAR", 10000)
    account.withdraw(1000, "INVALID")
    assert account.balance == 10000

