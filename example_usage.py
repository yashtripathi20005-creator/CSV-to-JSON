# example_usage.py
"""
Example usage of the CSV to JSON converter.
This file demonstrates various ways to use the converter programmatically.
"""

from csv_to_json_converter import CSVToJSONConverter
import os

def example_basic_usage():
    """Example of basic usage with a sample CSV file."""
    print("=== Example: Basic Usage ===\n")
    
    # Sample CSV data as a string (we'll create a file from it)
    sample_csv_content = """name,age,city,employed
John Doe,30,New York,true
Jane Smith,25,Los Angeles,false
Bob Johnson,35,Chicago,true
Alice Brown,28,Houston,true
"""
    
    # Create a sample CSV file
    csv_file = "sample_data.csv"
    with open(csv_file, 'w') as f:
        f.write(sample_csv_content)
    
    # Convert to JSON
    converter = CSVToJSONConverter(csv_file)
    converter.read_csv()
    converter.convert_to_json()
    
    # Display the results
    json_str = converter.get_json_string()
    print("Converted JSON:")
    print(json_str)
    
    # Clean up
    os.remove(csv_file)
    os.remove("sample_data.json")


def example_custom_delimiters():
    """Example using different delimiters."""
    print("\n=== Example: Custom Delimiter ===\n")
    
    # Sample CSV with semicolon delimiter
    sample_csv_content = """name;age;city;employed
Alice;30;New York;true
Bob;25;Los Angeles;false
"""
    
    csv_file = "semicolon_data.csv"
    with open(csv_file, 'w') as f:
        f.write(sample_csv_content)
    
    # Use semicolon delimiter
    converter = CSVToJSONConverter(csv_file)
    converter.read_csv(delimiter=';')
    json_str = converter.get_json_string()
    print("CSV with semicolon delimiter converted to JSON:")
    print(json_str)
    
    # Clean up
    os.remove(csv_file)
    os.remove("semicolon_data.json")


def example_get_statistics():
    """Example of getting data statistics."""
    print("\n=== Example: Get Statistics ===\n")
    
    sample_csv_content = """product,price,quantity,in_stock
Apple,0.99,50,true
Banana,0.59,100,true
Orange,0.79,0,false
Grape,2.99,25,true
"""
    
    csv_file = "products.csv"
    with open(csv_file, 'w') as f:
        f.write(sample_csv_content)
    
    converter = CSVToJSONConverter(csv_file)
    converter.read_csv()
    
    # Get statistics
    stats = converter.get_statistics()
    print("Data Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Clean up
    os.remove(csv_file)
    os.remove("products.json")


if __name__ == "__main__":
    example_basic_usage()
    example_custom_delimiters()
    example_get_statistics()
    print("\nAll examples completed!")
