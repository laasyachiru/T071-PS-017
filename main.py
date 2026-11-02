from banking_engine import SavingsAccount

# Create sample customer accounts
account1 = SavingsAccount(101, "Laasya", "REGULAR", 50000)
account2 = SavingsAccount(102, "Lavanya", "SENIOR", 100000)
account3 = SavingsAccount(103, "Customer 3", "SALARY", 25000)

# Store all accounts
accounts = [account1, account2, account3]

# Display account details
for account in accounts:
    account.display_account()

# Test deposit and withdrawal
print("\n===== BANKING OPERATIONS =====")

account1.deposit(5000)
account1.withdraw(2000)
account1.check_balance()

# Test interest calculation
print("\n===== INTEREST CALCULATION =====")

for account in accounts:
    account.calculate_interest()

# Test transaction history
print("\n===== TRANSACTION HISTORY =====")

account1.display_transactions()

# Test invalid withdrawal
print("\n===== INSUFFICIENT BALANCE TEST =====")

account1.withdraw(100000)