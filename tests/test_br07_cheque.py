from banking_engine import SavingsAccount


def create_account():
    return SavingsAccount(701, "Asha", "REGULAR", 100000)


def test_inward_cheque_return_charge():
    account = create_account()
    account.process_cheque_return("INWARD", 1000, "2026-07-01")
    assert account.balance == 99410


def test_inward_cheque_debit_reversal():
    account = create_account()
    account.process_cheque_return(
        "INWARD", 1000, "2026-07-01",
        debit_reversal=1000
    )
    assert account.balance == 100410


def test_outward_cheque_return_charge():
    account = create_account()
    account.process_cheque_return("OUTWARD", 1000, "2026-07-01")
    assert account.balance == 99900


def test_three_inward_returns_freeze_cheque_facility():
    account = create_account()
    account.process_cheque_return("INWARD", 100, "2026-07-01")
    account.process_cheque_return("INWARD", 100, "2026-07-10")
    account.process_cheque_return("INWARD", 100, "2026-07-20")
    assert account.cheque_frozen is True


def test_two_inward_returns_do_not_freeze_cheque_facility():
    account = create_account()
    account.process_cheque_return("INWARD", 100, "2026-07-01")
    account.process_cheque_return("INWARD", 100, "2026-07-10")
    assert account.cheque_frozen is False


def test_inward_return_count_resets_next_quarter():
    account = create_account()
    account.process_cheque_return("INWARD", 100, "2026-06-20")
    account.process_cheque_return("INWARD", 100, "2026-06-25")
    account.process_cheque_return("INWARD", 100, "2026-07-01")
    assert account.cheque_frozen is False


def test_frozen_account_cannot_issue_cheque():
    account = create_account()

    account.process_cheque_return("INWARD", 100, "2026-07-01")
    account.process_cheque_return("INWARD", 100, "2026-07-10")
    account.process_cheque_return("INWARD", 100, "2026-07-20")

    old_balance = account.balance

    result = account.issue_cheque(1000, "2026-07-21")

    assert result is False
    assert account.balance == old_balance