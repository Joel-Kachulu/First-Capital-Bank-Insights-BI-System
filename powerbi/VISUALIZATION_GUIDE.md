# Power BI Visualization Guide
## First Capital Bank Insights BI System

Step-by-step guide to create all dashboard visualizations.

---

## 📊 Dashboard 1: Executive Overview

**Purpose**: High-level KPIs and trends for senior management

### Step 1: Create the Page
1. In Power BI Desktop, create a new page: **"Executive Overview"**
2. Set page size: **16:9** (1920 x 1080) or **Standard (16:9)**

### Step 2: Add KPI Cards (Top Row)

**Card 1: Total Deposits**
1. Click **Card** visual from Visualizations pane
2. Drag **Total Deposits** measure to the card
3. Format:
   - Title: "Total Deposits"
   - Value: Format as **Currency** → **MWK** (or custom: "MWK #,##0")
   - Background: Light blue (#E3F2FD)
   - Position: Top-left

**Card 2: Total Withdrawals**
1. Add another Card visual
2. Drag **Total Withdrawals** measure
3. Format: Similar to above, use light orange background (#FFF3E0)
4. Position: Next to Total Deposits

**Card 3: Net Flow**
1. Add Card visual
2. Drag **Net Flow** measure
3. Format: Use green if positive, red if negative (conditional formatting)
4. Position: Next to Total Withdrawals

**Card 4: Transaction Count**
1. Add Card visual
2. Drag **Transaction Count** measure
3. Format: Number format with thousands separator
4. Position: Top-right

**Card 5: Risky Transaction Count**
1. Add Card visual
2. Drag **Risky Transaction Count** measure
3. Format: Red accent color (#F44336) for attention
4. Position: Next to Transaction Count

### Step 3: Transaction Trend Line Chart

**Monthly Transaction Trends**
1. Click **Line chart** visual
2. Drag fields:
   - **Axis**: `transactions[transaction_month]` (or create a date hierarchy)
   - **Values**: 
     - `Total Deposits` (blue line)
     - `Total Withdrawals` (orange line)
3. Format:
   - Title: "Monthly Transaction Trends"
   - Legend: Position at top
   - Colors: Blue for deposits, Orange for withdrawals
   - Y-axis: Format as Currency (MWK)
4. Position: Below KPI cards, full width

**Alternative**: Use **Area chart** for filled area visualization

### Step 4: Transaction Volume by Type (Pie/Donut Chart)

1. Click **Donut chart** visual
2. Drag fields:
   - **Legend**: `transactions[type]`
   - **Values**: `Total Transaction Volume` measure (or create: `SUM(transactions[amount])`)
3. Format:
   - Title: "Transaction Volume by Type"
   - Colors: 
     - Deposit: Green (#4CAF50)
     - Withdrawal: Red (#F44336)
     - Transfer: Blue (#2196F3)
4. Position: Right side, below cards

### Step 5: Daily Transaction Trend (Last 30 Days)

1. Click **Line chart** or **Area chart**
2. Drag fields:
   - **Axis**: `transactions[date]` (filter to last 30 days)
   - **Values**: `Transaction Count` measure
3. Format:
   - Title: "Daily Transaction Count (Last 30 Days)"
   - X-axis: Date format (MMM DD)
4. Position: Bottom section

### Step 6: Add Filters

1. Add **Slicer** visual for Date Range
   - Field: `transactions[date]`
   - Type: **Between** or **Date range**
2. Add **Slicer** for Branch (optional)
   - Field: `branches[branch_name]`
   - Type: **Dropdown** or **List**

### Step 7: Format the Page

- Background: Light gray (#F5F5F5)
- Add page title: "Executive Overview" (Text box)
- Align all visuals neatly
- Use consistent spacing

---

## 📊 Dashboard 2: Branch Performance

**Purpose**: Compare branch performance and identify top performers

### Step 1: Create the Page
1. Create new page: **"Branch Performance"**
2. Set page size: **16:9**

### Step 2: Branch Performance Ranking (Horizontal Bar Chart)

1. Click **Bar chart** visual (horizontal)
2. Drag fields:
   - **Axis**: `branches[branch_name]`
   - **Values**: `Total Transaction Volume` measure
3. Sort: **Descending** (highest to lowest)
4. Format:
   - Title: "Branch Performance Ranking"
   - Data colors: Gradient (green to blue)
   - Y-axis: Show branch names
   - X-axis: Format as Currency (MWK)
5. Position: Top-left, large size

### Step 3: Branch Comparison Table

1. Click **Table** visual
2. Drag fields (in order):
   - `branches[branch_name]`
   - `branches[city]`
   - `Total Deposits` measure
   - `Total Withdrawals` measure
   - `Net Flow` measure
   - `Transaction Count` measure
   - `Risky Transaction Count` measure
3. Format:
   - Title: "Branch Performance Metrics"
   - Conditional formatting: 
     - Net Flow: Green if positive, Red if negative
     - Risky Transaction Count: Red background if > 10
4. Position: Right side of bar chart

### Step 4: Deposits vs Withdrawals by Branch (Clustered Bar Chart)

1. Click **Clustered bar chart** visual
2. Drag fields:
   - **Axis**: `branches[branch_name]`
   - **Legend**: Create calculated column or use transaction type
   - **Values**: 
     - `Total Deposits` measure
     - `Total Withdrawals` measure
3. Format:
   - Title: "Deposits vs Withdrawals by Branch"
   - Colors: Green for deposits, Red for withdrawals
4. Position: Below bar chart ranking

**Alternative approach**: Use two separate bar charts side by side

### Step 5: Customer Count by Branch

1. Click **Bar chart** visual
2. Drag fields:
   - **Axis**: `branches[branch_name]`
   - **Values**: Create measure: `Customer Count = DISTINCTCOUNT(accounts[customer_id])`
3. Format:
   - Title: "Customer Count by Branch"
   - Color: Purple (#9C27B0)
4. Position: Right side, below comparison table

### Step 6: Account Count by Branch

1. Click **Bar chart** visual
2. Drag fields:
   - **Axis**: `branches[branch_name]`
   - **Values**: Create measure: `Account Count = COUNTROWS(accounts)`
3. Format:
   - Title: "Account Count by Branch"
   - Color: Teal (#009688)
4. Position: Next to Customer Count

### Step 7: Branch Map (Optional - if coordinates available)

1. Click **Map** visual
2. Drag fields:
   - **Location**: `branches[city]` (or add latitude/longitude if available)
   - **Size**: `Total Transaction Volume` measure
3. Format:
   - Title: "Branch Locations"
   - Bubble size based on transaction volume
4. Position: Bottom section

**Note**: If map doesn't work, use a **Matrix** visual showing city and metrics instead

### Step 8: Add Filters

1. **Date Range Slicer**: `transactions[date]`
2. **Branch Multi-select**: `branches[branch_name]` (allows comparing specific branches)

---

## 📊 Dashboard 3: Risk Monitoring

**Purpose**: Monitor and analyze risky transactions

### Step 1: Create the Page
1. Create new page: **"Risk Monitoring"**
2. Set page size: **16:9**
3. Background: Slightly darker to emphasize importance

### Step 2: Risky Transactions Table (Detailed)

1. Click **Table** visual
2. Drag fields (in order):
   - `transactions[transaction_id]`
   - `transactions[date]`
   - `customers[name]` (via relationship)
   - `branches[branch_name]` (via relationship)
   - `branches[city]`
   - `transactions[type]`
   - `transactions[amount]`
3. Add filter: `transactions[risk_flag] = 1`
4. Format:
   - Title: "Risky Transactions Detail"
   - Conditional formatting on amount: Red background if > 750,000 MWK
   - Sort: By amount descending
   - Enable drill-through if needed
5. Position: Top section, full width

### Step 3: Risky Transactions by Branch (Bar Chart)

1. Click **Bar chart** visual
2. Drag fields:
   - **Axis**: `branches[branch_name]`
   - **Values**: `Risky Transaction Count` measure
3. Format:
   - Title: "Risky Transactions by Branch"
   - Color: Red gradient (darker = more risky)
   - Data labels: Show values
4. Position: Top-right, above table

### Step 4: Risky Transaction Trend (Line Chart)

1. Click **Line chart** visual
2. Drag fields:
   - **Axis**: `transactions[transaction_month]`
   - **Values**: `Risky Transaction Count` measure
3. Format:
   - Title: "Risky Transaction Trend Over Time"
   - Color: Red line
   - Markers: Show data points
   - Y-axis: Integer format
4. Position: Below branch chart

### Step 5: Top Risky Customers (Table)

1. Click **Table** visual
2. Create measure: 
   ```dax
   Risky Transaction Amount = 
   CALCULATE(
       SUM(transactions[amount]),
       transactions[risk_flag] = 1
   )
   ```
3. Drag fields:
   - `customers[name]`
   - `customers[city]`
   - `Risky Transaction Count` measure (filtered by customer)
   - `Risky Transaction Amount` measure (filtered by customer)
4. Format:
   - Title: "Top 10 Customers by Risky Transactions"
   - Sort: By Risky Transaction Count descending
   - Limit: Top 10 (use visual-level filter)
5. Position: Right side, below trend chart

### Step 6: Risk Amount Distribution (Histogram)

1. Click **Column chart** visual
2. Create calculated column for amount bins:
   - In Power Query or DAX, create bins: 500K-600K, 600K-700K, etc.
   - Or use automatic binning in Power BI
3. Drag fields:
   - **Axis**: Amount bins
   - **Values**: `Risky Transaction Count` measure
4. Format:
   - Title: "Distribution of Risky Transaction Amounts"
   - Color: Red shades
5. Position: Bottom section

**Alternative**: Use **Box and Whisker** chart if available in your Power BI version

### Step 7: Risk Summary Cards

1. Add **Card** visuals:
   - Total Risky Transactions: `Risky Transaction Count`
   - Total Risky Amount: Create measure `SUM(transactions[amount])` filtered by risk_flag = 1
   - Average Risky Amount: Create measure `AVERAGE(transactions[amount])` filtered by risk_flag = 1
   - Max Risky Amount: Create measure `MAX(transactions[amount])` filtered by risk_flag = 1
2. Format: Red accent colors
3. Position: Top row, above all other visuals

### Step 8: Add Filters

1. **Date Range Slicer**: `transactions[date]`
2. **Branch Slicer**: `branches[branch_name]`
3. **Amount Threshold Slicer**: Create parameter for custom threshold
4. **Customer Slicer** (optional): `customers[name]`

---

## 🎨 General Formatting Tips

### Color Scheme
- **Primary Blue**: #1E88E5 (trust, stability)
- **Success Green**: #43A047 (deposits, positive)
- **Warning Orange**: #FB8C00 (withdrawals, caution)
- **Danger Red**: #F44336 (risk, negative)
- **Accent Purple**: #7B1FA2 (premium, special)

### Typography
- **Page Titles**: Bold, 24-28pt
- **Visual Titles**: Bold, 14-16pt
- **Axis Labels**: 10-12pt
- **Data Labels**: 9-11pt

### Layout
- Use consistent spacing (10-20px between visuals)
- Align visuals to grid
- Group related visuals together
- Use white backgrounds for visual containers

### Currency Formatting
- Format: **MWK #,##0** or **MWK #,##0.00**
- Use thousands separators
- Consistent across all visuals

---

## ✅ Checklist for Each Dashboard

- [ ] All measures created and working
- [ ] Relationships between tables established
- [ ] Visuals properly formatted
- [ ] Filters added and functional
- [ ] Titles and labels clear
- [ ] Colors consistent with scheme
- [ ] Currency formatted correctly
- [ ] Page layout clean and organized
- [ ] Data refreshes correctly
- [ ] Tooltips enabled (optional but recommended)

---

## 🔗 Data Relationships Required

Make sure these relationships exist:

```
transactions[account_id] → accounts[account_id] (Many-to-One)
accounts[customer_id] → customers[customer_id] (Many-to-One)
accounts[branch_id] → branches[branch_id] (Many-to-One)
```

**To create relationships**:
1. Go to **Model** view (left sidebar)
2. Drag `account_id` from transactions to accounts
3. Repeat for other relationships
4. Ensure cardinality is correct (Many-to-One)

---

## 📸 Final Steps

1. **Test all filters** - Make sure they work correctly
2. **Check data refresh** - Refresh data and verify visuals update
3. **Add tooltips** - Hover information for better UX
4. **Take screenshots** - Save as PNG for portfolio
5. **Export to PDF** - For documentation

---

**Need help?** Refer to the main `powerbi/README.md` for data connection and measure setup.

