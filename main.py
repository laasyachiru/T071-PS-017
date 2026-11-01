from banking_engine import SavingsAccount

Create a sample customer account

account1 = SavingsAccount(101, "Laasya", "REGULAR", 50000)

Display account details

account1.display_account()

Deposit money

print("\n--- Deposit Operation ---")
account1.deposit(5000)

Withdraw money

print("\n--- Withdrawal Operation ---")
account1.withdraw(2000)

Calculate interest

print("\n--- Interest Calculation ---")
account1.calculate_interest()

Display transaction history

account1.display_transactions()
