# T071-PS-017 — Decision Log

## Business Rule Register

### BR-01: Interest Calculation
Calculate interest using daily closing balances and progressive slabs:
- Up to ₹1,00,000: 3.0% per annum
- ₹1,00,000 to ₹10,00,000: 3.5% per annum
- Above ₹10,00,000: 4.0% per annum
- SENIOR accounts receive an additional 0.5% on all slabs.
- Credit accumulated interest quarterly at the end of March, June, September and December, rounded to the nearest rupee.

### BR-02: Minimum Average Balance
Calculate MAB as the sum of daily closing balances divided by the number of days in the month. Requirements depend on branch category. SALARY and BASIC accounts are exempt.

### BR-03: MAB Penalty
Apply the specified penalty band to the MAB shortfall, add 18% GST, and ensure the penalty does not exceed the shortfall amount. Waive the penalty in the account's opening month.

### BR-04: Transaction Charges
Track free ATM withdrawals separately for own-bank and other-bank ATMs. Apply charges after the monthly free limits are exceeded. Apply branch cash withdrawal charges after four free withdrawals.

### BR-05: Cheque Returns
Apply inward and outward cheque-return charges according to the specification. Reverse the debit for an inward return where applicable. Freeze cheque facilities after the third inward return in a quarter.

### BR-06: Sweep-In
On the month-end run, create ₹10,000 FD units from eligible surplus above the configured threshold. The threshold must be at least ₹25,000. Use the specified regular and SENIOR FD rates.

### BR-07: Sweep-Out
Break FD units in last-created-first order when a debit exceeds the available savings balance. Calculate interest for the actual holding period and apply the specified premature-break penalty.

### BR-08: Overdraft
REGULAR and SENIOR accounts cannot overdraw. SALARY accounts may overdraw up to ₹50,000. BASIC accounts cannot overdraw and cannot use sweep-in.

### BR-09: Dormancy
Mark an account DORMANT after 24 months without customer-initiated transactions. Interest credits do not reset customer activity. Reject debits until the account is reactivated.

### BR-10: Charges and Liens
Post monthly charges on the first day of the following month in this order: MAB penalty, ATM charges, branch charges, then cheque charges. Carry unrecovered charges as a lien for accounts that cannot go negative.

### BR-11: Standing Instructions
Execute standing instructions at the start of their due date before other debits. Retry a failed instruction once on the following day. Apply the specified ₹50 charge if it fails again.

## Pending Clarifications
- Exact MAB penalty boundaries at 50% and 75% shortfall.
- Annual interest day-count convention.
- Exact sweep-in unit calculation at threshold boundaries.
- Partial FD breakage and salary overdraft interaction.
- Precise ordering of month-end postings and daily balance updates.

## Decision Log Entries
Record each confirmed interpretation, its reason, and the tests used to verify it.