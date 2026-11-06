
from datetime import date, timedelta
import calendar


class SavingsAccount:

    def __init__(self, account_number, customer_name, account_type, balance,
                 branch_category="METRO", sweep_in_enabled=False,
                 sweep_threshold=25000):

        # BR-01: Account Management
        valid_account_types = ["REGULAR", "SALARY", "SENIOR", "BASIC"]
        valid_branches = ["METRO", "URBAN", "SEMI_URBAN", "RURAL"]

        if not account_number:
            raise ValueError("Account number is required!")

        if not customer_name:
            raise ValueError("Customer name is required!")

        if not isinstance(account_type, str):
            raise ValueError("Invalid account type!")

        account_type = account_type.strip().upper()

        if account_type not in valid_account_types:
            raise ValueError("Invalid account type!")

        if not isinstance(balance, (int, float)) or isinstance(balance, bool):
            raise ValueError("Opening balance must be a number!")

        if balance < 0:
            raise ValueError("Opening balance cannot be negative!")

        if not isinstance(branch_category, str):
            raise ValueError("Invalid branch category!")

        branch_category = branch_category.strip().upper()

        if branch_category not in valid_branches:
            raise ValueError("Invalid branch category!")

        if not isinstance(sweep_in_enabled, bool):
            raise ValueError("Sweep-in must be True or False!")

        if sweep_in_enabled and account_type == "BASIC":
            raise ValueError("Basic accounts cannot use sweep-in!")

        if not isinstance(sweep_threshold, (int, float)) or isinstance(sweep_threshold, bool):
            raise ValueError("Sweep threshold must be a number!")

        if sweep_threshold < 25000:
            raise ValueError("Sweep threshold must be at least Rs. 25000!")

        self.account_number = account_number
        self.customer_name = customer_name
        self.account_type = account_type.title()
        self.balance = balance
        self.branch_category = branch_category
        self.sweep_in_enabled = sweep_in_enabled
        self.sweep_threshold = sweep_threshold

        self.transactions = []
        self.daily_balances = {}
        self.credited_quarters = set()

        # BR-06: Monthly withdrawal tracking
        self.monthly_atm_withdrawals = {}
        self.monthly_branch_withdrawals = {}

        # BR-07: Cheque tracking
        self.cheque_frozen = False
        self.inward_cheque_returns = 0
        self.cheque_return_quarter = None

        # BR-08: Fixed deposit tracking
        self.fixed_deposits = []

        # BR-11: Dormant account tracking
        self.account_status = "ACTIVE"
        self.last_customer_transaction_date = date.today()

        # BR-12: Unpaid charge tracking
        self.lien_amount = 0
        self.processed_charge_months = set()

        # BR-13: Standing instruction tracking
        self.standing_instructions = {}

    # BR-11: Add calendar months to a date
    def _add_months(self, original_date, months):

        month_index = original_date.month - 1 + months
        year = original_date.year + month_index // 12
        month = month_index % 12 + 1

        last_day = calendar.monthrange(year, month)[1]
        day = min(original_date.day, last_day)

        return date(year, month, day)

    # BR-11: Check dormant status
    def update_dormancy(self, as_of_date):

        if isinstance(as_of_date, str):
            try:
                as_of_date = date.fromisoformat(as_of_date)
            except ValueError:
                raise ValueError("Invalid date!")

        if not isinstance(as_of_date, date):
            raise ValueError("Invalid date!")

        dormant_date = self._add_months(
            self.last_customer_transaction_date, 24
        )

        if as_of_date >= dormant_date:
            self.account_status = "DORMANT"
        else:
            self.account_status = "ACTIVE"

        return self.account_status

    # BR-11: Reactivate account
    def reactivate(self, reactivation_date=None):

        if reactivation_date is None:
            reactivation_date = date.today()

        if isinstance(reactivation_date, str):
            try:
                reactivation_date = date.fromisoformat(reactivation_date)
            except ValueError:
                raise ValueError("Invalid reactivation date!")

        if not isinstance(reactivation_date, date):
            raise ValueError("Invalid reactivation date!")

        self.account_status = "ACTIVE"
        self.last_customer_transaction_date = reactivation_date

        self.transactions.append("Account Reactivated")

        print("Account Reactivated Successfully!")

        return True

    # Display account details
    def display_account(self):

        print("\n--- Account Details ---")
        print("Account Number:", self.account_number)
        print("Customer Name:", self.customer_name)
        print("Account Type:", self.account_type)
        print("Branch Category:", self.branch_category)
        print("Account Status:", self.account_status)
        print("Last Customer Transaction:", self.last_customer_transaction_date)
        print("Sweep-in Enabled:", self.sweep_in_enabled)
        print("Sweep Threshold: Rs.", self.sweep_threshold)
        print("Balance: Rs.", self.balance)
        print("Unpaid Lien: Rs.", self.lien_amount)

    # BR-02 and BR-05: Required MAB
    def get_required_mab(self):

        if self.account_type in ["Salary", "Basic"]:
            return 0

        mab_requirements = {
            "METRO": 10000,
            "URBAN": 5000,
            "SEMI_URBAN": 2500,
            "RURAL": 1000
        }

        return mab_requirements[self.branch_category]

    # BR-03, BR-11, BR-12 and BR-13: Deposit
    def deposit(self, amount, transaction_type="CASH",
                transaction_date=None):

        valid_types = ["CASH", "NEFT", "CHEQUE"]

        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            print("Invalid Deposit Amount!")
            return

        if amount <= 0:
            print("Invalid Deposit Amount!")
            return

        if not isinstance(transaction_type, str):
            print("Invalid Transaction Type!")
            return

        transaction_type = transaction_type.strip().upper()

        if transaction_type not in valid_types:
            print("Invalid Transaction Type!")
            return

        if transaction_date is None:
            transaction_date = date.today()

        elif isinstance(transaction_date, str):
            try:
                transaction_date = date.fromisoformat(transaction_date)
            except ValueError:
                print("Invalid Transaction Date!")
                return

        if not isinstance(transaction_date, date):
            print("Invalid Transaction Date!")
            return

        self.balance += amount

        # BR-12: Recover outstanding lien from the deposit
        recovered_amount = min(self.balance, self.lien_amount)

        if recovered_amount > 0:
            self.balance -= recovered_amount
            self.lien_amount -= recovered_amount

            self.transactions.append(
                "Lien Recovered: Rs. " + str(recovered_amount)
            )

        self.last_customer_transaction_date = transaction_date

        self.transactions.append(
            transaction_type + " Deposit: Rs. " + str(amount)
        )

        print("Deposit Successful!")
        print("Updated Balance: Rs.", self.balance)
        print("Remaining Lien: Rs.", self.lien_amount)

    # BR-03, BR-06, BR-10 and BR-11: Withdrawal
    def withdraw(self, amount, transaction_type="BRANCH",
                 transaction_date=None, bank_type="OWN"):

        valid_types = ["ATM", "BRANCH"]

        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            print("Invalid Withdrawal Amount!")
            return

        if amount <= 0:
            print("Invalid Withdrawal Amount!")
            return

        if not isinstance(transaction_type, str):
            print("Invalid Transaction Type!")
            return

        transaction_type = transaction_type.strip().upper()

        if transaction_type not in valid_types:
            print("Invalid Transaction Type!")
            return

        if not isinstance(bank_type, str):
            print("Invalid Bank Type!")
            return

        bank_type = bank_type.strip().upper()

        if transaction_type == "ATM" and bank_type not in ["OWN", "OTHER"]:
            print("Invalid Bank Type!")
            return

        if transaction_date is None:
            transaction_date = date.today()

        elif isinstance(transaction_date, str):
            try:
                transaction_date = date.fromisoformat(transaction_date)
            except ValueError:
                print("Invalid Transaction Date!")
                return

        if not isinstance(transaction_date, date):
            print("Invalid Transaction Date!")
            return

        if self.account_status == "DORMANT":
            print("Withdrawal Rejected! Account is DORMANT.")
            return False

        month_key = transaction_date.strftime("%Y-%m")
        charge = 0

        if transaction_type == "ATM":

            key = (month_key, bank_type)
            count = self.monthly_atm_withdrawals.get(key, 0)

            free_limit = 5 if bank_type == "OWN" else 3

            if count >= free_limit:
                charge = 21 * 1.18

        elif transaction_type == "BRANCH":

            count = self.monthly_branch_withdrawals.get(month_key, 0)

            if count >= 4:
                charge = 150

        total_amount = amount + round(charge)

        if total_amount > self.balance:

            overdraft_required = total_amount - self.balance

            if self.account_type != "Salary":
                print("Overdraft Not Allowed for This Account!")
                return False

            if overdraft_required > 50000:
                print("Salary Overdraft Limit Exceeded!")
                return False

        self.balance -= total_amount

        if transaction_type == "ATM":
            self.monthly_atm_withdrawals[key] = count + 1

        elif transaction_type == "BRANCH":
            self.monthly_branch_withdrawals[month_key] = count + 1

        self.last_customer_transaction_date = transaction_date

        self.transactions.append(
            transaction_type + " Withdrawal: Rs. " + str(amount)
        )

        if charge > 0:
            self.transactions.append(
                "Withdrawal Charge: Rs. " + str(round(charge))
            )

        print("Withdrawal Successful!")
        print("Updated Balance: Rs.", self.balance)

        return True

    # BR-04: Daily interest calculation
    def calculate_daily_interest(self, balance=None):

        if balance is None:
            balance = self.balance

        if balance <= 0:
            return 0

        senior_bonus = 0.005 if self.account_type == "Senior" else 0

        rate1 = 0.03 + senior_bonus
        rate2 = 0.035 + senior_bonus
        rate3 = 0.04 + senior_bonus

        if balance <= 100000:
            interest = balance * rate1 / 365

        elif balance <= 1000000:
            interest = (
                100000 * rate1
                + (balance - 100000) * rate2
            ) / 365

        else:
            interest = (
                100000 * rate1
                + 900000 * rate2
                + (balance - 1000000) * rate3
            ) / 365

        return interest

    def calculate_interest(self):
        interest = self.calculate_daily_interest()
        print("Daily Interest: Rs.", round(interest, 4))
        return interest

    # BR-04: Record daily balance
    def record_daily_balance(self, transaction_date):

        if isinstance(transaction_date, str):
            transaction_date = date.fromisoformat(transaction_date)

        if not isinstance(transaction_date, date):
            raise ValueError("Invalid transaction date!")

        date_key = transaction_date.isoformat()
        self.daily_balances[date_key] = self.balance

    # BR-04: Calculate quarterly interest
    def calculate_quarterly_interest(self, end_date):

        if isinstance(end_date, str):
            end_date = date.fromisoformat(end_date)

        quarter_start_month = ((end_date.month - 1) // 3) * 3 + 1

        quarter_start = date(
            end_date.year, quarter_start_month, 1
        )

        total_interest = 0

        for recorded_date, closing_balance in self.daily_balances.items():

            current_date = date.fromisoformat(recorded_date)

            if quarter_start <= current_date <= end_date:
                total_interest += self.calculate_daily_interest(
                    closing_balance
                )

        return total_interest

    # BR-04: Credit quarterly interest
    def credit_quarterly_interest(self, end_date):

        if isinstance(end_date, str):
            end_date = date.fromisoformat(end_date)

        if end_date.month not in [3, 6, 9, 12]:
            raise ValueError("Invalid quarter-end month!")

        if end_date.day != calendar.monthrange(
            end_date.year, end_date.month
        )[1]:
            raise ValueError("Invalid quarter-end date!")

        quarter_key = (
            end_date.year,
            (end_date.month - 1) // 3 + 1
        )

        if quarter_key in self.credited_quarters:
            raise ValueError("Interest already credited!")

        interest = self.calculate_quarterly_interest(end_date)
        credited_amount = round(interest)

        self.balance += credited_amount
        self.credited_quarters.add(quarter_key)

        self.transactions.append(
            "Quarterly Interest Credited: Rs. " + str(credited_amount)
        )

        print("Quarterly Interest Credited: Rs.", credited_amount)

        return credited_amount

    # BR-05: Calculate monthly average balance
    def calculate_mab(self, year_month):

        try:
            year, month = map(int, year_month.split("-"))
            days_in_month = calendar.monthrange(year, month)[1]

        except (ValueError, AttributeError):
            raise ValueError("Month must be in YYYY-MM format!")

        if month < 1 or month > 12:
            raise ValueError("Invalid month!")

        total_balance = 0

        for day in range(1, days_in_month + 1):

            date_key = date(year, month, day).isoformat()

            if date_key not in self.daily_balances:
                raise ValueError(
                    "Missing daily balance record for " + date_key
                )

            total_balance += self.daily_balances[date_key]

        return total_balance / days_in_month

    # BR-05: Calculate MAB penalty
    def calculate_mab_penalty(self, year_month, opening_month=False):

        if opening_month:
            return 0

        required_mab = self.get_required_mab()

        if required_mab == 0:
            return 0

        average_balance = self.calculate_mab(year_month)

        if average_balance >= required_mab:
            return 0

        shortfall = required_mab - average_balance
        shortfall_percentage = (shortfall / required_mab) * 100

        if shortfall_percentage <= 50:
            penalty = 150
        elif shortfall_percentage <= 75:
            penalty = 300
        else:
            penalty = 500

        penalty = min(penalty, shortfall)

        return round(penalty * 1.18)

    # BR-07: Cheque return processing
    def process_cheque_return(self, cheque_type, amount,
                              transaction_date, debit_reversal=0):

        if not isinstance(cheque_type, str):
            raise ValueError("Invalid cheque type!")

        cheque_type = cheque_type.strip().upper()

        if cheque_type not in ["INWARD", "OUTWARD"]:
            raise ValueError("Invalid cheque type!")

        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise ValueError("Invalid cheque amount!")

        if amount <= 0:
            raise ValueError("Cheque amount must be positive!")

        if not isinstance(debit_reversal, (int, float)) or isinstance(debit_reversal, bool):
            raise ValueError("Invalid debit reversal amount!")

        if debit_reversal < 0:
            raise ValueError("Debit reversal cannot be negative!")

        if isinstance(transaction_date, str):
            try:
                transaction_date = date.fromisoformat(transaction_date)
            except ValueError:
                raise ValueError("Invalid transaction date!")

        if not isinstance(transaction_date, date):
            raise ValueError("Invalid transaction date!")

        if cheque_type == "INWARD":

            quarter = (
                transaction_date.year,
                (transaction_date.month - 1) // 3 + 1
            )

            if self.cheque_return_quarter != quarter:
                self.cheque_return_quarter = quarter
                self.inward_cheque_returns = 0
                self.cheque_frozen = False

            self.balance += debit_reversal

            charge = round(500 * 1.18)
            self.balance -= charge

            self.inward_cheque_returns += 1

            if self.inward_cheque_returns >= 3:
                self.cheque_frozen = True

            self.transactions.append(
                "Inward Cheque Return: Rs. " + str(amount)
            )

            self.transactions.append(
                "Inward Cheque Return Charge: Rs. " + str(charge)
            )

            if debit_reversal > 0:
                self.transactions.append(
                    "Cheque Debit Reversed: Rs. " + str(debit_reversal)
                )

        else:

            charge = 100
            self.balance -= charge

            self.transactions.append(
                "Outward Cheque Return: Rs. " + str(amount)
            )

            self.transactions.append(
                "Outward Cheque Return Charge: Rs. " + str(charge)
            )

        print("Cheque Return Processed!")
        print("Updated Balance: Rs.", self.balance)

    # BR-07 and BR-11: Issue cheque
    def issue_cheque(self, amount, transaction_date):

        if self.account_status == "DORMANT":
            print("Cheque Rejected! Account is DORMANT.")
            return False

        if self.cheque_frozen:
            print("Cheque facility is frozen!")
            return False

        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            print("Invalid cheque amount!")
            return False

        if amount <= 0:
            print("Cheque amount must be positive!")
            return False

        if isinstance(transaction_date, str):
            try:
                transaction_date = date.fromisoformat(transaction_date)
            except ValueError:
                print("Invalid transaction date!")
                return False

        if not isinstance(transaction_date, date):
            print("Invalid transaction date!")
            return False

        if amount > self.balance:
            print("Insufficient Balance!")
            return False

        self.balance -= amount
        self.last_customer_transaction_date = transaction_date

        self.transactions.append(
            "Cheque Issued: Rs. " + str(amount)
        )

        print("Cheque Issued Successfully!")
        print("Updated Balance: Rs.", self.balance)

        return True

    # BR-08: Sweep-in FD creation
    def process_sweep_in(self, transaction_date):

        if not self.sweep_in_enabled:
            print("Sweep-in is disabled for this account!")
            return False

        if isinstance(transaction_date, str):
            try:
                transaction_date = date.fromisoformat(transaction_date)
            except ValueError:
                raise ValueError("Invalid transaction date!")

        if not isinstance(transaction_date, date):
            raise ValueError("Invalid transaction date!")

        last_day = calendar.monthrange(
            transaction_date.year,
            transaction_date.month
        )[1]

        if transaction_date.day != last_day:
            raise ValueError("Sweep-in can only be processed at month-end!")

        excess_balance = self.balance - self.sweep_threshold

        if excess_balance < 10000:
            print("No eligible balance for sweep-in!")
            return False

        number_of_units = int(excess_balance // 10000)

        if number_of_units <= 0:
            return False

        fd_interest_rate = (
            7.0 if self.account_type == "Senior" else 6.5
        )

        for unit_number in range(number_of_units):

            fd = {
                "fd_id": len(self.fixed_deposits) + 1,
                "amount": 10000,
                "interest_rate": fd_interest_rate,
                "tenure_years": 1,
                "created_date": transaction_date.isoformat()
            }

            self.fixed_deposits.append(fd)

        total_sweep_amount = number_of_units * 10000
        self.balance -= total_sweep_amount

        self.transactions.append(
            "Sweep-in FD Created: Rs. " + str(total_sweep_amount)
        )

        print("Sweep-in Successful!")
        print("FD Units Created:", number_of_units)
        print("Total FD Amount: Rs.", total_sweep_amount)
        print("Remaining Savings Balance: Rs.", self.balance)

        return True

    # BR-09 and BR-11: Reverse sweep and FD breakage
    def process_sweep_out(self, amount, transaction_date):

        if self.account_status == "DORMANT":
            print("Reverse sweep rejected! Account is DORMANT.")
            return False

        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise ValueError("Invalid withdrawal amount!")

        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive!")

        if isinstance(transaction_date, str):
            try:
                transaction_date = date.fromisoformat(transaction_date)
            except ValueError:
                raise ValueError("Invalid transaction date!")

        if not isinstance(transaction_date, date):
            raise ValueError("Invalid transaction date!")

        shortfall = amount - self.balance

        if shortfall <= 0:

            self.balance -= amount
            self.last_customer_transaction_date = transaction_date

            self.transactions.append(
                "Reverse Sweep Withdrawal: Rs. " + str(amount)
            )

            print("Withdrawal Successful!")
            print("Updated Balance: Rs.", self.balance)

            return True

        required_units = int((shortfall + 9999) // 10000)

        if len(self.fixed_deposits) < required_units:
            print("Insufficient balance and FD funds!")
            return False

        selected_fds = self.fixed_deposits[-required_units:]

        total_fd_principal = 0
        total_fd_interest = 0

        for fd in reversed(selected_fds):

            fd_start_date = date.fromisoformat(fd["created_date"])
            days = (transaction_date - fd_start_date).days

            if days < 0:
                raise ValueError(
                    "FD breakage date cannot be before FD creation!"
                )

            if days <= 90:
                interest_rate = 0.04
            else:
                interest_rate = 0.06

            interest_rate -= 0.005

            interest = fd["amount"] * interest_rate * days / 365

            total_fd_principal += fd["amount"]
            total_fd_interest += interest

        self.balance += total_fd_principal
        self.balance += round(total_fd_interest)

        self.fixed_deposits = self.fixed_deposits[:-required_units]

        self.balance -= amount
        self.last_customer_transaction_date = transaction_date

        self.transactions.append(
            "Reverse Sweep FD Broken: Rs. " + str(total_fd_principal)
        )

        self.transactions.append(
            "FD Breakage Interest: Rs. " + str(round(total_fd_interest))
        )

        self.transactions.append(
            "Reverse Sweep Withdrawal: Rs. " + str(amount)
        )

        print("Reverse Sweep Successful!")
        print("FD Units Broken:", required_units)
        print("FD Principal: Rs.", total_fd_principal)
        print("FD Interest: Rs.", round(total_fd_interest))
        print("Remaining Savings Balance: Rs.", self.balance)

        return True

    # BR-10: Calculate overdraft interest
    def calculate_overdraft_interest(self, days):

        if not isinstance(days, int) or isinstance(days, bool) or days < 0:
            raise ValueError("Days must be a non-negative integer!")

        if self.account_type != "Salary":
            if self.balance < 0:
                raise ValueError("Overdraft is not allowed for this account!")
            return 0

        if self.balance >= 0:
            return 0

        overdraft_amount = abs(self.balance)

        return overdraft_amount * 0.12 * days / 365

    # BR-12: Monthly charge processing
    def process_monthly_charges(self, processing_date, charge_month):

        if isinstance(processing_date, str):
            try:
                processing_date = date.fromisoformat(processing_date)
            except ValueError:
                raise ValueError("Invalid processing date!")

        if not isinstance(processing_date, date):
            raise ValueError("Invalid processing date!")

        if processing_date.day != 1:
            raise ValueError("Monthly charges must run on the 1st!")

        try:
            year, month = map(int, charge_month.split("-"))

            if month < 1 or month > 12:
                raise ValueError

            date(year, month, 1)

        except (ValueError, AttributeError):
            raise ValueError("Charge month must be YYYY-MM!")

        if charge_month in self.processed_charge_months:
            raise ValueError("Monthly charges already processed!")

        total_charges = 0

        # 1. MAB penalty
        mab_charge = self.calculate_mab_penalty(charge_month)

        if mab_charge > 0:
            self.transactions.append(
                "MAB Penalty: Rs. " + str(mab_charge)
            )
            total_charges += mab_charge

        # 2. ATM charges
        atm_charge = 0

        for (month_key, bank_type), count in self.monthly_atm_withdrawals.items():

            if month_key == charge_month:

                free_limit = 5 if bank_type == "OWN" else 3
                extra = max(0, count - free_limit)

                atm_charge += extra * round(21 * 1.18)

        if atm_charge > 0:
            self.transactions.append(
                "ATM Charge: Rs. " + str(atm_charge)
            )
            total_charges += atm_charge

        # 3. Branch charges
        branch_count = self.monthly_branch_withdrawals.get(
            charge_month, 0
        )

        branch_charge = max(0, branch_count - 4) * 150

        if branch_charge > 0:
            self.transactions.append(
                "Branch Charge: Rs. " + str(branch_charge)
            )
            total_charges += branch_charge

        # 4. Cheque return charges
        # Cheque charges are currently recorded by BR-07.

        if self.account_type == "Salary":
            self.balance -= total_charges

        else:
            if total_charges > self.balance:
                self.lien_amount += total_charges
            else:
                self.balance -= total_charges

        self.processed_charge_months.add(charge_month)

        self.transactions.append(
            "Monthly Charges Processed: Rs. " + str(total_charges)
        )

        print("Monthly Charges Processed!")
        print("Total Charges: Rs.", total_charges)
        print("Updated Balance: Rs.", self.balance)
        print("Unpaid Lien: Rs.", self.lien_amount)

        return total_charges

    # BR-13: Add a standing instruction
    def add_standing_instruction(self, instruction_id, amount, due_date):

        if not instruction_id:
            raise ValueError("Instruction ID is required!")

        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise ValueError("Invalid standing instruction amount!")

        if amount <= 0:
            raise ValueError("Amount must be positive!")

        if isinstance(due_date, str):
            try:
                due_date = date.fromisoformat(due_date)
            except ValueError:
                raise ValueError("Invalid due date!")

        if not isinstance(due_date, date):
            raise ValueError("Invalid due date!")

        if instruction_id in self.standing_instructions:
            raise ValueError("Instruction ID already exists!")

        self.standing_instructions[instruction_id] = {
            "amount": amount,
            "due_date": due_date,
            "attempts": 0,
            "status": "PENDING",
            "retry_date": None
        }

        self.transactions.append(
            "Standing Instruction Added: " + str(instruction_id)
        )

        return True

    # BR-13: Process standing instructions
    def process_standing_instructions(self, processing_date):

        if isinstance(processing_date, str):
            try:
                processing_date = date.fromisoformat(processing_date)
            except ValueError:
                raise ValueError("Invalid processing date!")

        if not isinstance(processing_date, date):
            raise ValueError("Invalid processing date!")

        for instruction_id, instruction in self.standing_instructions.items():

            if instruction["status"] != "PENDING":
                continue

            due_date = instruction["due_date"]
            retry_date = instruction["retry_date"]

            if retry_date is not None:
                if processing_date != retry_date:
                    continue
            elif processing_date != due_date:
                continue

            amount = instruction["amount"]

            # Attempt to execute the instruction
            if self.account_status == "ACTIVE" and self.balance >= amount:

                self.balance -= amount
                instruction["status"] = "COMPLETED"

                self.last_customer_transaction_date = processing_date

                self.transactions.append(
                    "Standing Instruction Executed: "
                    + str(instruction_id)
                    + " Rs. "
                    + str(amount)
                )

                print("Standing Instruction Successful:", instruction_id)

            else:

                instruction["attempts"] += 1

                self.transactions.append(
                    "Standing Instruction Failed: "
                    + str(instruction_id)
                )

                # First failure: retry next day
                if instruction["attempts"] == 1:

                    instruction["retry_date"] = (
                        processing_date + timedelta(days=1)
                    )

                    print("Standing Instruction Failed. Retry Tomorrow.")

                # Second failure: apply Rs. 50 fee
                else:

                    instruction["status"] = "FAILED"

                    failure_fee = 50

                    if self.account_type == "Salary":
                        self.balance -= failure_fee

                    elif self.balance >= failure_fee:
                        self.balance -= failure_fee

                    else:
                        self.lien_amount += failure_fee

                    self.transactions.append(
                        "Standing Instruction Failure Fee: Rs. 50"
                    )

                    print("Standing Instruction Failed Twice!")
                    print("Failure Fee: Rs. 50")

    # Display transaction history
    def display_transactions(self):

        print("\n--- Transaction History ---")

        if not self.transactions:
            print("No transactions available.")

        else:
            for transaction in self.transactions:
                print(transaction)
