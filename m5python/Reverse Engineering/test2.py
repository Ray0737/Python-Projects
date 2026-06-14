import pandas as pd
import os

# Define the file path
file_path = 'm5python/Aj phoom-my work/work/train.csv'

# Check if the file exists before trying to open it
if os.path.exists(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # 1. Get a summary of how many blanks (nulls) are in each column
    print("--- Count of Blank Entries per Column ---")
    print(df.isnull().sum())
    
    # 2. Find the exact rows that have at least one blank entry
    blanks_only = df[df.isnull().any(axis=1)]
    
    if not blanks_only.empty:
        print(f"\n--- Found {len(blanks_only)} rows with blank entries ---")
        print(blanks_only.head()) # Shows the first few rows with issues
    else:
        print("\nNo blank entries found! Your data is clean.")
else:
    print(f"Error: The file at {file_path} was not found. Please check the directory.")