"""Sample Python file for testing"""


def process_data(data: list[int]) -> list[int]:
    """Process some data by doubling positive values.
    
    Args:
        data: List of integers to process
        
    Returns:
        List of doubled positive integers
    """
    return [item * 2 for item in data if item > 0]


def main() -> None:
    """Main entry point for the application."""
    data: list[int] = [1, 2, 3, 4, 5]
    results: list[int] = process_data(data)
    print("Results:", results)


if __name__ == "__main__":
    main()