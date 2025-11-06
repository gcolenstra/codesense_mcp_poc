"""
Data Processing Module
Optimized and modernized for Python 3.9+
"""

import pandas as pd
import numpy as np
from datetime import datetime


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV data from specified filepath.
    
    Args:
        filepath: Path to the CSV file to load
        
    Returns:
        DataFrame containing the loaded CSV data
    """
    df = pd.read_csv(filepath)
    return df


def process_sales_data(df: pd.DataFrame) -> dict[str, any]:
    """
    Process sales data efficiently using vectorized operations.
    
    Args:
        df: DataFrame containing sales data with 'amount' and 'product' columns
        
    Returns:
        Dictionary with 'total' (sum of all sales) and 'products' (list of product sales)
    """
    # Efficient: vectorized sum operation
    total_sales = df['amount'].sum()
    
    # Efficient: direct DataFrame to list of dicts conversion
    product_sales = df[['product', 'amount']].rename(
        columns={'amount': 'total'}
    ).to_dict('records')
    
    return {
        'total': total_sales,
        'products': product_sales
    }


def calculate_statistics(data: list[dict]) -> dict[str, float]:
    """
    Calculate statistics using numpy for efficiency.
    
    Args:
        data: List of dictionaries containing 'value' key
        
    Returns:
        Dictionary with 'mean', 'median', and 'count' statistics
    """
    # Extract values efficiently using list comprehension
    values = [item['value'] for item in data]
    
    # Use numpy's built-in optimized functions
    values_array = np.array(values)
    mean = np.mean(values_array)
    median = np.median(values_array)
    
    return {
        'mean': float(mean),
        'median': float(median),
        'count': len(values)
    }


def filter_data(df: pd.DataFrame, min_amount: float, max_amount: float) -> pd.DataFrame:
    """
    Filter DataFrame efficiently using boolean indexing.
    
    Args:
        df: DataFrame to filter
        min_amount: Minimum amount threshold (inclusive)
        max_amount: Maximum amount threshold (inclusive)
        
    Returns:
        Filtered DataFrame containing only rows within the amount range
    """
    # Efficient: vectorized boolean indexing
    return df[(df['amount'] >= min_amount) & (df['amount'] <= max_amount)].copy()


def aggregate_by_category(df: pd.DataFrame) -> dict[str, dict]:
    """
    Aggregate data by category using pandas groupby.
    
    Args:
        df: DataFrame containing 'category', 'amount', and 'product' columns
        
    Returns:
        Dictionary mapping categories to their aggregated statistics
    """
    # Efficient: using groupby and agg for vectorized operations
    grouped = df.groupby('category').agg({
        'amount': ['sum', 'count'],
        'product': lambda x: list(x)
    })
    
    # Transform to desired output format
    categories = {}
    for category in grouped.index:
        categories[category] = {
            'total': grouped.loc[category, ('amount', 'sum')],
            'count': grouped.loc[category, ('amount', 'count')],
            'items': grouped.loc[category, ('product', '<lambda>')]
        }
    
    return categories


def export_report(data: list[dict], filename: str) -> bool:
    """
    Export data to CSV using modern pandas concat method.
    
    Args:
        data: List of dictionaries to export
        filename: Output CSV filename
        
    Returns:
        True if export successful
    """
    df = pd.DataFrame(data)
    # Modern approach: using pd.concat instead of deprecated append
    summary_row = pd.DataFrame([{
        'product': 'TOTAL',
        'amount': sum(item['amount'] for item in data)
    }])
    df = pd.concat([df, summary_row], ignore_index=True)
    df.to_csv(filename, index=False)
    return True


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean data by removing rows with null values efficiently.
    
    Args:
        df: DataFrame to clean
        
    Returns:
        DataFrame with all rows containing null values removed
    """
    # Efficient: using built-in dropna method
    return df.dropna().copy()


if __name__ == "__main__":
    # Example usage
    data = load_data("sales.csv")
    result = process_sales_data(data)
    print("Processed:", result)