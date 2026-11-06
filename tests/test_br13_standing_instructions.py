
from banking_engine import SavingsAccount


def test_standing_instruction_executes_on_due_date():
    account = SavingsAccount(1301, "Asha", "REGULAR", 10000)

    account.add_standing_instruction(
        "SI001", 2000, "2026-11-10"
    )

    account.process_standing_instructions("2026-11-10")

    assert account.balance == 8000



def test_failed_instruction_retries_next_day():
    account = SavingsAccount(1302, "Ravi", "REGULAR", 500)

    account.add_standing_instruction(
        "SI002", 1000, "2026-11-10"
    )

    account.process_standing_instructions("2026-11-10")

    assert account.balance == 500

    account.deposit(1000, transaction_date="2026-11-11")
    account.process_standing_instructions("2026-11-11")

    assert account.balance == 500



def test_failure_fee_after_two_failed_attempts():
    account = SavingsAccount(1303, "Anu", "REGULAR", 100)

    account.add_standing_instruction(
        "SI003", 1000, "2026-11-10"
    )

    account.process_standing_instructions("2026-11-10")
    account.process_standing_instructions("2026-11-11")

    assert account.balance == 50

    assert any(
        "Standing Instruction Failure Fee: Rs. 50" in item
        for item in account.transactions
    )


def test_successful_instruction_is_not_executed_again():
    account = SavingsAccount(1304, "Kiran", "REGULAR", 5000)

    account.add_standing_instruction(
        "SI004", 1000, "2026-11-10"
    )

    account.process_standing_instructions("2026-11-10")
    account.process_standing_instructions("2026-11-11")

    assert account.balance == 4000


def test_invalid_standing_instruction_amount():
    account = SavingsAccount(1305, "Meena", "REGULAR", 5000)

    try:
        account.add_standing_instruction(
            "SI005", -1000, "2026-11-10"
        )
        assert False, "Expected ValueError"
    except ValueError:
        assert True
