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

**Important**: When importing CSV files, Power BI names tables after the filename. 
- If you import `transactions.csv`, the table will be named `transactions` (lowercase)
- Adjust the table name in the measures below if your table has a different name

**To check your table name**: Look in the **Fields** pane on the right side of Power BI Desktop.

**To create a measure**: 
1. Right-click on your **transactions** table in the Fields pane
2. Select **"New measure"**
3. Paste the DAX code below
4. Name the measure exactly as shown (e.g., "Total Deposits")

---

### Step 1: Create Base Measures First

Create these measures **one at a time** in this order:

```dax
// Measure 1: Total Deposits
Total Deposits = 
CALCULATE(
    SUM(transactions[amount]),
    transactions[type] = "deposit"
)
```

```dax
// Measure 2: Total Withdrawals
Total Withdrawals = 
CALCULATE(
    SUM(transactions[amount]),
    transactions[type] = "withdrawal"
)
```

**Verify these work** by dragging them to a card visual before proceeding.

---

### Step 2: Create Dependent Measures

**Only create these AFTER the above measures are working:**

```dax
// Measure 3: Net Flow (depends on Total Deposits and Total Withdrawals)
Net Flow = 
[Total Deposits] - [Total Withdrawals]
```

**If you still get an error**, use this alternative syntax:

```dax
Net Flow = 
CALCULATE(SUM(transactions[amount]), transactions[type] = "deposit") - 
CALCULATE(SUM(transactions[amount]), transactions[type] = "withdrawal")
```

---

### Step 3: Additional Measures

```dax
// Risky Transaction Count
Risky Transaction Count = 
CALCULATE(
    COUNTROWS(transactions),
    transactions[risk_flag] = 1
)

// Average Transaction Amount
Avg Transaction Amount = 
AVERAGE(transactions[amount])

// Transaction Count
Transaction Count = 
COUNTROWS(transactions)

// Total Transaction Volume
Total Transaction Volume = 
SUM(transactions[amount])
```

---

### Troubleshooting Common Errors

**Error: "The value for 'Total Deposits' cannot be determined"**

**Solution 1**: Make sure you created `Total Deposits` measure first and it appears in the Fields pane.

**Solution 2**: Check your table name. If Power BI named it differently:
- Look in Fields pane for your transactions table name
- Replace `transactions` in the DAX with your actual table name
- Common variations: `Transactions`, `transactions`, `Transaction`, `transaction`

**Solution 3**: Use explicit table reference in Net Flow:
```dax
Net Flow = 
CALCULATE(SUM(transactions[amount]), transactions[type] = "deposit") - 
CALCULATE(SUM(transactions[amount]), transactions[type] = "withdrawal")
```

**Error: "column doesn't exist"**

- Check column names in your table (they should be lowercase: `amount`, `type`, `risk_flag`)
- In Power BI, go to **Transform Data** → Check column names
- Column names must match exactly (case-sensitive in some contexts)

**Error: "A single value for column 'amount' cannot be determined"**

- Make sure you're creating a **Measure**, not a **Calculated Column**
- Right-click on table → **"New measure"** (not "New column")

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

## Visualization Guides

### 📊 Main Visualization Guide
**[VISUALIZATION_GUIDE.md](VISUALIZATION_GUIDE.md)** - Complete step-by-step instructions for all 3 dashboards:
- **Executive Overview**: KPI cards, trend charts, pie charts, filters
- **Branch Performance**: Rankings, comparisons, maps, metrics tables
- **Risk Monitoring**: Detailed tables, trends, distributions, summary cards

Each section includes:
- Exact visual types to use
- Field mappings
- Formatting specifications
- Color schemes
- Layout recommendations

### 📈 Additional Measures
**[ADDITIONAL_MEASURES.md](ADDITIONAL_MEASURES.md)** - Advanced DAX measures for enhanced analytics:
- Customer & Account measures
- Time-based analysis (MoM, YoY, trends)
- Risk analysis measures
- Branch performance rankings
- Percentage and ratio calculations
- Conditional formatting helpers

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

