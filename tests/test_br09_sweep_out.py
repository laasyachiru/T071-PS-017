
from banking_engine import SavingsAccount


def create_account():
    account = SavingsAccount(
        901, "Asha", "REGULAR", 5000,
        sweep_in_enabled=True
    )

    account.fixed_deposits = [
        {
            "fd_id": 1,
            "amount": 10000,
            "interest_rate": 6.5,
            "tenure_years": 1,
            "created_date": "2026-01-01"
        },
        {
            "fd_id": 2,
            "amount": 10000,
            "interest_rate": 6.5,
            "tenure_years": 1,
            "created_date": "2026-02-01"
        }
    ]

    return account


def test_sweep_out_breaks_fd_when_balance_is_insufficient():
    account = create_account()

    result = account.process_sweep_out(
        15000, "2026-02-01"
    )

    assert result is True
    assert account.balance >= 0
    assert len(account.fixed_deposits) == 1


def test_sweep_out_uses_lifo_order():
    account = create_account()

    account.process_sweep_out(
        15000, "2026-02-01"
    )

    # The latest FD (FD 2) should be broken first.
    assert account.fixed_deposits[0]["fd_id"] == 1


def test_sweep_out_uses_savings_balance_first():
    account = create_account()

    result = account.process_sweep_out(
        5000, "2026-02-01"
    )

    assert result is True
    assert account.balance == 0
    assert len(account.fixed_deposits) == 2


def test_sweep_out_fails_when_total_funds_are_insufficient():
    account = create_account()

    old_balance = account.balance
    old_fd_count = len(account.fixed_deposits)

    result = account.process_sweep_out(
        40000, "2026-02-01"
    )

    assert result is False
    assert account.balance == old_balance
    assert len(account.fixed_deposits) == old_fd_count
