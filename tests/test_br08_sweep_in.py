
from banking_engine import SavingsAccount


def test_sweep_in_creates_one_fd_unit():
    account = SavingsAccount(
        801, "Asha", "REGULAR", 44999,
        sweep_in_enabled=True,
        sweep_threshold=25000
    )

    result = account.process_sweep_in("2026-07-31")

    assert result is True
    assert account.balance == 34999
    assert len(account.fixed_deposits) == 1
    assert account.fixed_deposits[0]["amount"] == 10000


def test_sweep_in_creates_two_fd_units():
    account = SavingsAccount(
        802, "Asha", "REGULAR", 45000,
        sweep_in_enabled=True,
        sweep_threshold=25000
    )

    account.process_sweep_in("2026-07-31")

    assert account.balance == 25000
    assert len(account.fixed_deposits) == 2


def test_sweep_in_does_not_create_fd_below_minimum_excess():
    account = SavingsAccount(
        803, "Asha", "REGULAR", 34999,
        sweep_in_enabled=True,
        sweep_threshold=25000
    )

    result = account.process_sweep_in("2026-07-31")

    assert result is False
    assert account.balance == 34999
    assert len(account.fixed_deposits) == 0


def test_sweep_in_disabled_account_does_not_create_fd():
    account = SavingsAccount(
        804, "Asha", "REGULAR", 50000,
        sweep_in_enabled=False
    )

    result = account.process_sweep_in("2026-07-31")

    assert result is False
    assert account.balance == 50000
    assert len(account.fixed_deposits) == 0


def test_regular_account_fd_interest_rate():
    account = SavingsAccount(
        805, "Asha", "REGULAR", 45000,
        sweep_in_enabled=True
    )

    account.process_sweep_in("2026-07-31")

    assert account.fixed_deposits[0]["interest_rate"] == 6.5


def test_senior_account_fd_interest_rate():
    account = SavingsAccount(
        806, "Ravi", "SENIOR", 45000,
        sweep_in_enabled=True
    )

    account.process_sweep_in("2026-07-31")

    assert account.fixed_deposits[0]["interest_rate"] == 7.0
