# Quick Start Guide
## First Capital Bank Insights BI System

Get up and running in 5 minutes!

---

## 🚀 Step-by-Step Setup

### 1. Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### 2. Generate & Clean Data (1 minute)
```bash
python run_pipeline.py
```

This creates:
- ✅ Raw data in `data/raw/` (200 customers, 5 branches, 300 accounts, 3,000 transactions)
- ✅ Cleaned data in `data/clean/` (ready for analysis)

### 3. Load into Database (1 minute)

**Option A: SQLite (Recommended for quick testing)**
```bash
cd sql
python load_to_sqlite.py
```
Creates `data/first_capital_bank.db`

**Option B: Your SQL Database**
- Run `sql/01_create_star_schema.sql` to create tables
- Import CSV files from `data/clean/` using your database's import tool

### 4. Run Analytics Queries (1 minute)
```bash
# Connect to your database and run:
sql/03_kpi_queries.sql
```

### 5. Create Power BI Dashboards (1 minute)
1. Open Power BI Desktop
2. Get Data → Text/CSV → Select files from `data/clean/`
3. Create relationships between tables
4. Follow `powerbi/README.md` for dashboard specifications

---

## 📊 What You Get

- **200 customers** across 5 Malawian cities
- **5 branches**: Lilongwe, Blantyre, Mzuzu, Zomba, Mangochi
- **300 accounts** (savings & current)
- **3,000 transactions** over the past year
- **518 risky transactions** flagged (withdrawals > MWK 500,000)

---

## 🎯 Key Files

| File | Purpose |
|------|---------|
| `run_pipeline.py` | Run complete pipeline (data gen + ETL) |
| `etl/generate_mock_data.py` | Generate mock banking data |
| `etl/etl_pipeline.py` | Clean and transform data |
| `sql/01_create_star_schema.sql` | Create star schema tables |
| `sql/load_to_sqlite.py` | Load data into SQLite (easy testing) |
| `sql/03_kpi_queries.sql` | Business intelligence queries |
| `powerbi/README.md` | Power BI dashboard guide |

---

## ✅ Verification

After running the pipeline, verify:

```bash
# Check data files exist
ls data/raw/*.csv
ls data/clean/*.csv

# Check SQLite database (if using SQLite)
ls data/first_capital_bank.db
```

---

## 🆘 Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'faker'`
- **Fix**: Run `pip install -r requirements.txt`

**Issue**: CSV files not found
- **Fix**: Run `python run_pipeline.py` first

**Issue**: SQLite database not created
- **Fix**: Ensure you're in the `sql/` directory when running `load_to_sqlite.py`

---

## 📚 Next Steps

1. ✅ Data generated and cleaned
2. ✅ Database loaded
3. 📊 Create Power BI dashboards (see `powerbi/README.md`)
4. 📈 Run KPI queries (see `sql/03_kpi_queries.sql`)
5. 🎨 Customize for your portfolio

---

**Total Setup Time**: ~5 minutes

**Ready to build your BI portfolio!** 🎉

