# Additional DAX Measures
## First Capital Bank Insights BI System

Useful measures for enhanced visualizations beyond the basic set.

---

## Customer & Account Measures

```dax
// Total Customers
Total Customers = DISTINCTCOUNT(customers[customer_id])

// Total Accounts
Total Accounts = COUNTROWS(accounts)

// Average Accounts per Customer
Avg Accounts per Customer = 
DIVIDE(
    [Total Accounts],
    [Total Customers],
    0
)

// Customers by Branch
Customers by Branch = 
CALCULATE(
    DISTINCTCOUNT(accounts[customer_id]),
    ALL(branches[branch_name])
)
```

---

## Transaction Analysis Measures

```dax
// Total Transaction Volume (all types)
Total Transaction Volume = SUM(transactions[amount])

// Average Deposit Amount
Avg Deposit Amount = 
CALCULATE(
    AVERAGE(transactions[amount]),
    transactions[type] = "deposit"
)

// Average Withdrawal Amount
Avg Withdrawal Amount = 
CALCULATE(
    AVERAGE(transactions[amount]),
    transactions[type] = "withdrawal"
)

// Deposit to Withdrawal Ratio
Deposit Withdrawal Ratio = 
DIVIDE(
    [Total Deposits],
    [Total Withdrawals],
    0
)

// Transaction Count by Type
Deposit Count = 
CALCULATE(
    COUNTROWS(transactions),
    transactions[type] = "deposit"
)

Withdrawal Count = 
CALCULATE(
    COUNTROWS(transactions),
    transactions[type] = "withdrawal"
)

Transfer Count = 
CALCULATE(
    COUNTROWS(transactions),
    transactions[type] = "transfer"
)
```

---

## Time-Based Measures

```dax
// Transactions This Month
Transactions This Month = 
CALCULATE(
    [Transaction Count],
    FILTER(
        transactions,
        YEAR(transactions[date]) = YEAR(TODAY()) &&
        MONTH(transactions[date]) = MONTH(TODAY())
    )
)

// Transactions Last Month
Transactions Last Month = 
CALCULATE(
    [Transaction Count],
    FILTER(
        transactions,
        YEAR(transactions[date]) = YEAR(EDATE(TODAY(), -1)) &&
        MONTH(transactions[date]) = MONTH(EDATE(TODAY(), -1))
    )
)

// Month-over-Month Growth
MoM Growth = 
DIVIDE(
    [Transactions This Month] - [Transactions Last Month],
    [Transactions Last Month],
    0
)

// Transactions Today
Transactions Today = 
CALCULATE(
    [Transaction Count],
    transactions[date] = TODAY()
)

// Transactions This Week
Transactions This Week = 
CALCULATE(
    [Transaction Count],
    WEEKNUM(transactions[date]) = WEEKNUM(TODAY()) &&
    YEAR(transactions[date]) = YEAR(TODAY())
)
```

---

## Risk Analysis Measures

```dax
// Total Risky Transaction Amount
Total Risky Amount = 
CALCULATE(
    SUM(transactions[amount]),
    transactions[risk_flag] = 1
)

// Average Risky Transaction Amount
Avg Risky Amount = 
CALCULATE(
    AVERAGE(transactions[amount]),
    transactions[risk_flag] = 1
)

// Max Risky Transaction Amount
Max Risky Amount = 
CALCULATE(
    MAX(transactions[amount]),
    transactions[risk_flag] = 1
)

// Risk Percentage (risky transactions / total transactions)
Risk Percentage = 
DIVIDE(
    [Risky Transaction Count],
    [Transaction Count],
    0
) * 100

// Risky Transactions by Customer
Risky Transactions by Customer = 
CALCULATE(
    [Risky Transaction Count],
    ALL(customers[name])
)
```

---

## Branch Performance Measures

```dax
// Branch Transaction Volume
Branch Transaction Volume = 
CALCULATE(
    [Total Transaction Volume],
    ALL(branches[branch_name])
)

// Branch Performance Rank
Branch Performance Rank = 
RANKX(
    ALL(branches[branch_name]),
    [Total Transaction Volume],
    ,
    DESC,
    DENSE
)

// Top Branch
Top Branch = 
CALCULATE(
    FIRSTNONBLANK(branches[branch_name], 1),
    TOPN(1, ALL(branches[branch_name]), [Total Transaction Volume], DESC)
)

// Branch Market Share
Branch Market Share = 
DIVIDE(
    [Total Transaction Volume],
    CALCULATE(
        [Total Transaction Volume],
        ALL(branches[branch_name])
    ),
    0
) * 100
```

---

## Account Type Analysis

```dax
// Savings Account Transactions
Savings Transactions = 
CALCULATE(
    [Transaction Count],
    accounts[account_type] = "savings"
)

// Current Account Transactions
Current Transactions = 
CALCULATE(
    [Transaction Count],
    accounts[account_type] = "current"
)

// Savings Account Volume
Savings Volume = 
CALCULATE(
    [Total Transaction Volume],
    accounts[account_type] = "savings"
)

// Current Account Volume
Current Volume = 
CALCULATE(
    [Total Transaction Volume],
    accounts[account_type] = "current"
)
```

---

## Percentage and Ratio Measures

```dax
// Deposit Percentage
Deposit Percentage = 
DIVIDE(
    [Total Deposits],
    [Total Transaction Volume],
    0
) * 100

// Withdrawal Percentage
Withdrawal Percentage = 
DIVIDE(
    [Total Withdrawals],
    [Total Transaction Volume],
    0
) * 100

// Net Flow Percentage
Net Flow Percentage = 
DIVIDE(
    [Net Flow],
    [Total Deposits],
    0
) * 100
```

---

## Conditional Formatting Measures

These measures return values that can be used for conditional formatting:

```dax
// Net Flow Status (for conditional formatting)
Net Flow Status = 
IF(
    [Net Flow] > 0,
    1,  // Green
    IF(
        [Net Flow] < 0,
        -1,  // Red
        0    // Yellow/Neutral
    )
)

// Risk Level (for conditional formatting)
Risk Level = 
IF(
    [Risky Transaction Count] > 20,
    3,  // High risk (Red)
    IF(
        [Risky Transaction Count] > 10,
        2,  // Medium risk (Orange)
        1   // Low risk (Green)
    )
)
```

---

## Quick Reference: Common DAX Patterns

### Filtering by Date Range
```dax
Measure = 
CALCULATE(
    [Base Measure],
    transactions[date] >= DATE(2024, 1, 1),
    transactions[date] <= DATE(2024, 12, 31)
)
```

### Top N Items
```dax
Top N Measure = 
CALCULATE(
    [Base Measure],
    TOPN(10, ALL(customers[customer_id]), [Base Measure], DESC)
)
```

### Year-over-Year Comparison
```dax
YoY Growth = 
VAR CurrentYear = [This Year Measure]
VAR LastYear = 
    CALCULATE(
        [This Year Measure],
        DATEADD(transactions[date], -1, YEAR)
    )
RETURN
    DIVIDE(CurrentYear - LastYear, LastYear, 0) * 100
```

### Running Total
```dax
Running Total = 
CALCULATE(
    [Base Measure],
    FILTER(
        ALL(transactions[date]),
        transactions[date] <= MAX(transactions[date])
    )
)
```

---

## Usage Tips

1. **Create measures in the appropriate table** - Usually in the `transactions` table for transaction measures
2. **Test measures individually** - Create a simple card visual to verify each measure works
3. **Use variables for complex calculations** - Improves readability and performance
4. **Format measures** - Right-click measure → Format → Set number format (Currency, Percentage, etc.)
5. **Document measures** - Add descriptions in Power BI (Right-click measure → Properties → Description)

---

**Note**: Replace `transactions`, `accounts`, `customers`, `branches` with your actual table names if different.


