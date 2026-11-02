class SavingsAccount:

    def __init__(self, account_number, customer_name, account_type, balance):
        self.account_number = account_number
        self.customer_name = customer_name
        self.account_type = account_type
        self.balance = balance
        self.transactions = []

    # Display account details
    def display_account(self):
        print("\n--- ACCOUNT DETAILS ---")
        print("Account Number:", self.account_number)
        print("Customer Name:", self.customer_name)
        print("Account Type:", self.account_type)
        print("Balance: Rs.", self.balance)

    # Deposit money
    def deposit(self, amount):
        if amount <= 0:
            print("Invalid deposit amount!")
            return False

        self.balance += amount
        self.transactions.append("Deposit: Rs. " + str(amount))
        print("Deposit successful!")
        return True

    # Withdraw money
    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal amount!")
            return False

        if amount > self.balance:
            print("Insufficient balance!")
            return False

        self.balance -= amount
        self.transactions.append("Withdrawal: Rs. " + str(amount))
        print("Withdrawal successful!")
        return True

    # Check balance
    def check_balance(self):
        print("Current Balance: Rs.", self.balance)
        return self.balance

    # Calculate interest using the account's applicable rate
    def calculate_interest(self, annual_rate=3.0):
        if self.account_type == "SENIOR":
            annual_rate += 0.5

        interest = self.balance * annual_rate / 100
        print("Estimated annual interest: Rs.", round(interest, 2))
        return round(interest, 2)

    # Display transaction history
    def display_transactions(self):
        print("\n--- TRANSACTION HISTORY ---")

        if not self.transactions:
            print("No transactions yet.")
        else:
            for transaction in self.transactions:
                print(transaction)