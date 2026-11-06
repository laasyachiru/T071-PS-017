
from banking_engine import SavingsAccount


def test_successful_deposit_is_recorded():
    account = SavingsAccount(1401, "Asha", "REGULAR", 5000)

    account.deposit(1000)

    assert account.balance == 6000
    assert any("Deposit: Rs. 1000" in t for t in account.transactions)


def test_successful_withdrawal_is_recorded():
    account = SavingsAccount(1402, "Ravi", "REGULAR", 5000)

    result = account.withdraw(1000, "BRANCH")

    assert result is True
    assert account.balance == 4000
    assert any("Withdrawal: Rs. 1000" in t for t in account.transactions)


def test_failed_withdrawal_does_not_change_balance():
    account = SavingsAccount(1403, "Anu", "REGULAR", 500)

    old_balance = account.balance
    old_transactions = account.transactions.copy()

    result = account.withdraw(1000, "BRANCH")

    assert result is False
    assert account.balance == old_balance
    assert account.transactions == old_transactions


def test_invalid_deposit_does_not_change_balance():
    account = SavingsAccount(1404, "Kiran", "REGULAR", 5000)

    old_balance = account.balance
    old_transactions = account.transactions.copy()

    account.deposit(-500)

    assert account.balance == old_balance
    assert account.transactions == old_transactions


def test_successful_cheque_is_recorded():
    account = SavingsAccount(1405, "Meena", "REGULAR", 5000)

    result = account.issue_cheque(1000, "2026-11-06")

    assert result is True
    assert account.balance == 4000
    assert any("Cheque Issued: Rs. 1000" in t for t in account.transactions)


def test_failed_cheque_does_not_change_balance():
    account = SavingsAccount(1406, "Arun", "REGULAR", 500)

    old_balance = account.balance
    old_transactions = account.transactions.copy()

    result = account.issue_cheque(1000, "2026-11-06")

    assert result is False
    assert account.balance == old_balance
    assert account.transactions == old_transactions
