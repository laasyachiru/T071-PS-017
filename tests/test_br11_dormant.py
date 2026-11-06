from datetime import date
from banking_engine import SavingsAccount


def test_account_becomes_dormant_after_24_months():
    account = SavingsAccount(1101, "Asha", "REGULAR", 10000)
    account.last_customer_transaction_date = date(2024, 1, 1)

    account.update_dormancy("2026-01-01")

    assert account.account_status == "DORMANT"


def test_account_remains_active_before_24_months():
    account = SavingsAccount(1102, "Ravi", "REGULAR", 10000)
    account.last_customer_transaction_date = date(2024, 1, 1)

    account.update_dormancy("2025-12-31")

    assert account.account_status == "ACTIVE"


def test_dormant_account_rejects_withdrawal():
    account = SavingsAccount(1103, "Anu", "REGULAR", 10000)
    account.account_status = "DORMANT"

    old_balance = account.balance
    result = account.withdraw(1000, "BRANCH", "2026-01-01")

    assert result is False
    assert account.balance == old_balance


def test_dormant_account_allows_interest_credit():
    account = SavingsAccount(1104, "Kiran", "REGULAR", 10000)
    account.account_status = "DORMANT"

    account.calculate_quarterly_interest = lambda end_date: 100

    account.credit_quarterly_interest("2026-03-31")

    assert account.balance == 10100
    assert account.account_status == "DORMANT"


def test_reactivate_changes_status_to_active():
    account = SavingsAccount(1105, "Meena", "REGULAR", 10000)
    account.account_status = "DORMANT"

    result = account.reactivate("2026-01-02")

    assert result is True
    assert account.account_status == "ACTIVE"
    assert account.last_customer_transaction_date == date(2026, 1, 2)


def test_dormant_account_rejects_cheque():
    account = SavingsAccount(1106, "Arun", "REGULAR", 10000)
    account.account_status = "DORMANT"

    result = account.issue_cheque(1000, "2026-01-01")

    assert result is False