"""
Main pipeline runner for First Capital Bank Insights BI System
Runs data generation and ETL pipeline in sequence
"""

import os
import sys
import subprocess

def main():
    """Run the complete data pipeline"""
    print("=" * 60)
    print("FIRST CAPITAL BANK INSIGHTS BI SYSTEM")
    print("Complete Pipeline Runner")
    print("=" * 60)
    print()
    
    # Change to etl directory
    os.chdir('etl')
    
    # Step 1: Generate mock data
    print("STEP 1: Generating mock data...")
    print("-" * 60)
    try:
        subprocess.run([sys.executable, 'generate_mock_data.py'], check=True)
        print()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating mock data: {e}")
        return 1
    
    # Step 2: Run ETL pipeline
    print("STEP 2: Running ETL pipeline...")
    print("-" * 60)
    try:
        subprocess.run([sys.executable, 'etl_pipeline.py'], check=True)
        print()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running ETL pipeline: {e}")
        return 1
    
    # Return to root directory
    os.chdir('..')
    
    print("=" * 60)
    print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Review cleaned data in: data/clean/")
    print("2. Load data into your SQL database using: sql/01_create_star_schema.sql")
    print("3. Run KPI queries: sql/03_kpi_queries.sql")
    print("4. Create Power BI dashboards (see: powerbi/README.md)")
    print()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

