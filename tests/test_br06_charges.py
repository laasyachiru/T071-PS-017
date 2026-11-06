
import pytest
from banking_engine import SavingsAccount


def create_account():
    return SavingsAccount(601, "Asha", "REGULAR", 100000)


def test_first_five_own_atm_withdrawals_are_free():
    account = create_account()

    for _ in range(5):
        account.withdraw(
            100, "ATM",
            transaction_date="2026-07-01",
            bank_type="OWN"
        )

    assert account.balance == 99500


def test_sixth_own_atm_withdrawal_has_charge():
    account = create_account()

    for _ in range(6):
        account.withdraw(
            100, "ATM",
            transaction_date="2026-07-01",
            bank_type="OWN"
        )

    # ₹21 + 18% GST = ₹24.78, rounded to ₹25
    assert account.balance == 99375


def test_first_three_other_bank_atm_withdrawals_are_free():
    account = create_account()

    for _ in range(3):
        account.withdraw(
            100, "ATM",
            transaction_date="2026-07-01",
            bank_type="OTHER"
        )

    assert account.balance == 99700


def test_fourth_other_bank_atm_withdrawal_has_charge():
    account = create_account()

    for _ in range(4):
        account.withdraw(
            100, "ATM",
            transaction_date="2026-07-01",
            bank_type="OTHER"
        )

    assert account.balance == 99575


def test_first_four_branch_withdrawals_are_free():
    account = create_account()

    for _ in range(4):
        account.withdraw(
            100, "BRANCH",
            transaction_date="2026-07-01"
        )

    assert account.balance == 99600


def test_fifth_branch_withdrawal_has_charge():
    account = create_account()

    for _ in range(5):
        account.withdraw(
            100, "BRANCH",
            transaction_date="2026-07-01"
        )

    assert account.balance == 99350
