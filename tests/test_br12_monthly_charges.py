from banking_engine import SavingsAccount


def test_monthly_charge_order():
    account = SavingsAccount(1201, "Asha", "REGULAR", 20000)

    account.calculate_mab_penalty = lambda month: 150
    account.monthly_atm_withdrawals[("2026-01", "OWN")] = 6
    account.monthly_branch_withdrawals["2026-01"] = 5

    account.process_monthly_charges("2026-02-01", "2026-01")

    charge_names = [
        transaction for transaction in account.transactions
        if "Charge" in transaction or "Penalty" in transaction
    ]

    assert charge_names[0].startswith("MAB")
    assert charge_names[1].startswith("ATM")
    assert charge_names[2].startswith("Branch")


def test_unpaid_charges_create_lien():
    account = SavingsAccount(1202, "Ravi", "REGULAR", 100)

    account.calculate_mab_penalty = lambda month: 500

    account.process_monthly_charges("2026-02-01", "2026-01")

    assert account.balance == 100
    assert account.lien_amount > 0


def test_lien_is_recovered_from_next_deposit():
    account = SavingsAccount(1203, "Anu", "REGULAR", 100)

    account.lien_amount = 500

    account.deposit(1000)

    assert account.lien_amount == 0
    assert account.balance == 600


def test_salary_account_can_go_negative_for_charges():
    account = SavingsAccount(1204, "Kiran", "SALARY", 100)

    account.calculate_mab_penalty = lambda month: 500

    account.process_monthly_charges("2026-02-01", "2026-01")

    assert account.balance < 0