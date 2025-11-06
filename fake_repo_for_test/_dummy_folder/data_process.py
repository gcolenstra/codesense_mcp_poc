"""
Data Processing Module
Needs optimization and modernization
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_data(filepath):
    """Load CSV data"""
    df = pd.read_csv(filepath)
    return df

def process_sales_data(df):
    """Process sales data - inefficient!"""
    # Inefficient: iterating over DataFrame
    total_sales = 0
    for index, row in df.iterrows():
        total_sales = total_sales + row['amount']
    
    # Inefficient: creating list then converting
    product_sales = []
    for index, row in df.iterrows():
        product_sales.append({
            'product': row['product'],
            'total': row['amount']
        })
    
    return {
        'total': total_sales,
        'products': product_sales
    }

def calculate_statistics(data):
    """Calculate statistics - could use numpy better"""
    values = []
    for item in data:
        values.append(item['value'])
    
    # Manual calculations instead of using numpy
    mean = sum(values) / len(values)
    
    sorted_values = sorted(values)
    n = len(sorted_values)
    if n % 2 == 0:
        median = (sorted_values[n//2-1] + sorted_values[n//2]) / 2
    else:
        median = sorted_values[n//2]
    
    return {
        'mean': mean,
        'median': median,
        'count': len(values)
    }

def filter_data(df, min_amount, max_amount):
    """Filter DataFrame - inefficient"""
    filtered_rows = []
    for index, row in df.iterrows():
        if row['amount'] >= min_amount and row['amount'] <= max_amount:
            filtered_rows.append(row)
    
    return pd.DataFrame(filtered_rows)

def aggregate_by_category(df):
    """Aggregate data by category - verbose"""
    categories = {}
    for index, row in df.iterrows():
        category = row['category']
        if category not in categories:
            categories[category] = {
                'total': 0,
                'count': 0,
                'items': []
            }
        categories[category]['total'] = categories[category]['total'] + row['amount']
        categories[category]['count'] = categories[category]['count'] + 1
        categories[category]['items'].append(row['product'])
    
    return categories

def export_report(data, filename):
    """Export data to CSV - deprecated method"""
    df = pd.DataFrame(data)
    # Using deprecated .append() method
    summary_row = pd.Series({
        'product': 'TOTAL',
        'amount': sum(item['amount'] for item in data)
    })
    df = df.append(summary_row, ignore_index=True)
    df.to_csv(filename, index=False)
    return True

def clean_data(df):
    """Clean data - inefficient null handling"""
    clean_rows = []
    for index, row in df.iterrows():
        is_valid = True
        for col in df.columns:
            if pd.isna(row[col]):
                is_valid = False
                break
        if is_valid:
            clean_rows.append(row)
    
    return pd.DataFrame(clean_rows)

if __name__ == "__main__":
    # Example usage
    data = load_data("sales.csv")
    result = process_sales_data(data)
    print("Processed:", result)