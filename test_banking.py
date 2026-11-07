
import unittest
from banking_engine import SavingsAccount


class TestSavingsAccount(unittest.TestCase):

    def setUp(self):
        self.account = SavingsAccount(
            101, "Laasya", "REGULAR", 50000
        )

    def test_account_creation(self):
        self.assertEqual(self.account.balance, 50000)

    def test_deposit(self):
        self.account.deposit(5000)
        self.assertEqual(self.account.balance, 55000)

    def test_invalid_deposit(self):
        result = self.account.deposit(-1000)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 50000)

    def test_withdrawal(self):
        self.account.withdraw(2000)
        self.assertEqual(self.account.balance, 48000)

    def test_insufficient_balance(self):
        result = self.account.withdraw(60000)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 50000)

    def test_regular_interest(self):
        interest = self.account.calculate_interest()
        self.assertAlmostEqual(interest, 1500 / 365)

    def test_senior_interest(self):
        senior = SavingsAccount(102, "Lavanya", "SENIOR", 100000)
        interest = senior.calculate_interest()
        self.assertAlmostEqual(interest, 3500 / 365)


if __name__ == "__main__":
    unittest.main()
