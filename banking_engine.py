class SavingsAccount:

def __init__(self, account_number, customer_name, account_type, balance):
    self.account_number = account_number
    self.customer_name = customer_name
    self.account_type = account_type
    self.balance = balance
    self.transactions = []

# Display account details
def display_account(self):
    print("\n--- Account Details ---")
    print("Account Number:", self.account_number)
    print("Customer Name:", self.customer_name)
    print("Account Type:", self.account_type)
    print("Balance: Rs.", self.balance)

# Deposit money
def deposit(self, amount):
    if amount > 0:
        self.balance += amount
        self.transactions.append("Deposited Rs. " + str(amount))
        print("Deposit Successful!")
        print("Updated Balance: Rs.", self.balance)
    else:
        print("Invalid Deposit Amount!")

# Withdraw money
def withdraw(self, amount):
    if amount <= 0:
        print("Invalid Withdrawal Amount!")
    elif amount <= self.balance:
        self.balance -= amount
        self.transactions.append("Withdrawn Rs. " + str(amount))
        print("Withdrawal Successful!")
        print("Updated Balance: Rs.", self.balance)
    else:
        print("Insufficient Balance!")

# Calculate simple savings interest
def calculate_interest(self, rate=4.0):
    interest = self.balance * rate / 100
    print("Calculated Interest: Rs.", round(interest, 2))
    return interest

# Display transaction history
def display_transactions(self):
    print("\n--- Transaction History ---")
    if not self.transactions:
        print("No transactions available.")
    else:
        for transaction in self.transactions:
            print(transaction)
