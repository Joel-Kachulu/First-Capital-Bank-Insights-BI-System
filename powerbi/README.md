# Power BI Dashboard Setup Guide
## First Capital Bank Insights BI System

This guide provides instructions for creating the Power BI dashboards for the First Capital Bank Insights BI System.

---

## Dashboard Structure

The Power BI solution consists of **3 main pages**:

### 1. Executive Overview
**Purpose**: High-level KPIs and trends for senior management

**Visualizations**:
- **Total Deposits** (Card/KPI visual)
- **Total Withdrawals** (Card/KPI visual)
- **Net Flow** (Deposits - Withdrawals) (Card/KPI visual)
- **Transaction Trend** (Line chart showing deposits/withdrawals over time by month)
- **Transaction Volume by Type** (Pie or Donut chart)
- **Risk Flag Count** (Card showing number of risky transactions)

**Filters**:
- Date range slicer
- Branch slicer (optional)

---

### 2. Branch Performance
**Purpose**: Compare branch performance and identify top performers

**Visualizations**:
- **Branch Performance Ranking** (Bar chart - horizontal, sorted by total transaction volume)
- **Branch Comparison** (Table showing key metrics per branch)
- **Branch Map** (Map visual showing branches in Malawi cities - if coordinates available)
- **Deposits vs Withdrawals by Branch** (Clustered bar chart)
- **Customer Count by Branch** (Bar chart)

**Metrics to Display**:
- Total Deposits (MWK)
- Total Withdrawals (MWK)
- Net Flow (MWK)
- Transaction Count
- Customer Count
- Account Count
- Risky Transaction Count

**Filters**:
- Date range slicer
- Branch multi-select slicer

---

### 3. Risk Monitoring
**Purpose**: Monitor and analyze risky transactions

**Visualizations**:
- **Risky Transactions Table** (Detailed table with all risky transactions)
- **Risky Transactions by Branch** (Bar chart)
- **Risky Transaction Trend** (Line chart over time)
- **Top Risky Customers** (Table showing customers with most risky transactions)
- **Risk Amount Distribution** (Histogram or box plot)

**Filters**:
- Date range slicer
- Branch slicer
- Customer slicer (optional)
- Amount threshold slicer

---

## Data Connection Steps

### Option 1: Direct CSV Import (Recommended for Portfolio)

1. Open Power BI Desktop
2. Click **Get Data** → **Text/CSV**
3. Navigate to `data/clean/` folder
4. Import the following files:
   - `customers.csv`
   - `branches.csv`
   - `accounts.csv`
   - `transactions.csv`

5. **Create Relationships**:
   - `accounts.customer_id` → `customers.customer_id`
   - `accounts.branch_id` → `branches.branch_id`
   - `transactions.account_id` → `accounts.account_id`

6. **Set Data Types**:
   - Amount columns: Decimal Number
   - Date columns: Date
   - ID columns: Whole Number

### Option 2: SQL Database Connection

1. Connect to your SQL database (PostgreSQL, MySQL, SQL Server, etc.)
2. Import the star schema tables:
   - `dim_customer`
   - `dim_branch`
   - `dim_account`
   - `dim_date`
   - `fact_transactions`

3. Relationships should be automatically detected if foreign keys are set correctly.

---

## Calculated Measures (DAX)

Add these measures to enhance your dashboards:

```dax
// Total Deposits
Total Deposits = 
CALCULATE(
    SUM(transactions[amount]),
    transactions[type] = "deposit"
)

// Total Withdrawals
Total Withdrawals = 
CALCULATE(
    SUM(transactions[amount]),
    transactions[type] = "withdrawal"
)

// Net Flow
Net Flow = [Total Deposits] - [Total Withdrawals]

// Risky Transaction Count
Risky Transaction Count = 
CALCULATE(
    COUNTROWS(transactions),
    transactions[risk_flag] = 1
)

// Average Transaction Amount
Avg Transaction Amount = AVERAGE(transactions[amount])

// Transaction Count
Transaction Count = COUNTROWS(transactions)
```

---

## Design Recommendations

### Color Scheme
- Primary: Blue (#1E88E5) - Trust, stability
- Secondary: Green (#43A047) - Growth, deposits
- Warning: Orange (#FB8C00) - Risk, withdrawals
- Accent: Purple (#7B1FA2) - Premium services

### Layout
- Use consistent spacing and alignment
- Group related visuals together
- Use clear section headers
- Include data refresh timestamp

### Formatting
- Format currency as: **MWK #,##0** (e.g., MWK 1,234,567)
- Format dates as: **MMM YYYY** or **DD MMM YYYY**
- Use thousands separators for large numbers

---

## Export and Sharing

1. **Save as .pbix file** in the `powerbi/` folder
2. **Publish to Power BI Service** (optional, for online sharing)
3. **Export to PDF** for portfolio documentation

---

## Screenshots

After creating your dashboards, take screenshots and save them in this folder:
- `executive_overview.png`
- `branch_performance.png`
- `risk_monitoring.png`

These can be included in your README.md for portfolio presentation.

---

## Notes

- All amounts are in **Malawian Kwacha (MWK)**
- Dates should be formatted consistently across all visuals
- Ensure all filters work correctly and don't break relationships
- Test with different date ranges to ensure data accuracy

