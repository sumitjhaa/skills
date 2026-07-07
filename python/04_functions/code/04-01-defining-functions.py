"""Financial calculator — compound interest and loan payment functions."""


def compound_interest(principal: float, rate: float, years: int) -> float:
    return principal * (1 + rate) ** years


def monthly_loan_payment(principal: float, annual_rate: float, months: int) -> float:
    monthly_rate = annual_rate / 12
    if monthly_rate == 0:
        return principal / months
    payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    return round(payment, 2)


def investment_growth(principal: float, rate: float, years: int) -> float:
    return compound_interest(principal, rate, years)


calc = compound_interest
print(f"$1000 at 5% for 10 years: ${calc(1000, 0.05, 10):.2f}")
print(f"$30000 loan, 6% APR, 60 months: ${monthly_loan_payment(30000, 0.06, 60)}")
print(f"$5000 at 7% for 30 years: ${investment_growth(5000, 0.07, 30):.2f}")
print(f"Docstring: {compound_interest.__doc__}")
