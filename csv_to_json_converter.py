# csv_to_json_converter.py
import csv
import json
import os
import sys
from typing import List, Dict, Any, Optional

class CSVToJSONConverter:
    """
    A class to convert CSV files to JSON format with various options.
    """
    
    def __init__(self, csv_file_path: str, json_file_path: Optional[str] = None):
        """
        Initialize the converter with file paths.
        
        Args:
            csv_file_path: Path to the input CSV file
            json_file_path: Path to the output JSON file (optional)
        """
        self.csv_file_path = csv_file_path
        self.json_file_path = json_file_path or self._generate_output_path()
        self.data: List[Dict[str, Any]] = []
        
    def _generate_output_path(self) -> str:
        """Generate a default JSON file path based on the CSV file name."""
        base_name = os.path.splitext(self.csv_file_path)[0]
        return f"{base_name}.json"
    
    def read_csv(self, delimiter: str = ',', encoding: str = 'utf-8') -> None:
        """
        Read CSV file and convert to list of dictionaries.
        
        Args:
            delimiter: CSV delimiter character (default: ',')
            encoding: File encoding (default: 'utf-8')
        
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            csv.Error: If CSV parsing fails
        """
        if not os.path.exists(self.csv_file_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_file_path}")
        
        try:
            with open(self.csv_file_path, 'r', encoding=encoding) as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
                self.data = list(csv_reader)
                
                # Convert numeric strings to appropriate types
                self._convert_data_types()
                
        except csv.Error as e:
            raise csv.Error(f"Error parsing CSV file: {e}")
    
    def _convert_data_types(self) -> None:
        """
        Automatically convert string values to appropriate types (int, float, bool).
        """
        if not self.data:
            return
            
        # Analyze all rows to determine field types
        field_types = {}
        for row in self.data:
            for key, value in row.items():
                if key not in field_types:
                    field_types[key] = self._detect_type(value)
                else:
                    # If current type is string, try to detect more specific type
                    if field_types[key] == str:
                        detected = self._detect_type(value)
                        if detected != str:
                            field_types[key] = detected
        
        # Convert all values based on detected types
        for row in self.data:
            for key, value in row.items():
                if value.strip() == '':
                    row[key] = None
                elif field_types[key] == int:
                    try:
                        row[key] = int(value)
                    except ValueError:
                        row[key] = value
                elif field_types[key] == float:
                    try:
                        row[key] = float(value)
                    except ValueError:
                        row[key] = value
                elif field_types[key] == bool:
                    row[key] = value.lower() in ('true', 'yes', '1')
                else:
                    row[key] = value.strip()
    
    def _detect_type(self, value: str) -> type:
        """
        Detect the most appropriate type for a string value.
        
        Args:
            value: String value to analyze
        
        Returns:
            Detected type (int, float, bool, or str)
        """
        if not value or value.strip() == '':
            return str
        
        value = value.strip()
        
        # Check for boolean
        if value.lower() in ('true', 'false', 'yes', 'no', '1', '0'):
            return bool
        
        # Check for integer
        try:
            int(value)
            return int
        except ValueError:
            pass
        
        # Check for float
        try:
            float(value)
            return float
        except ValueError:
            pass
        
        return str
    
    def convert_to_json(self, indent: int = 2, ensure_ascii: bool = False) -> None:
        """
        Convert the data to JSON and save to file.
        
        Args:
            indent: Indentation for pretty-printing (default: 2)
            ensure_ascii: If False, allow non-ASCII characters (default: False)
        
        Raises:
            ValueError: If no data is available to convert
        """
        if not self.data:
            raise ValueError("No data to convert. Please read a CSV file first.")
        
        try:
            with open(self.json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(
                    self.data,
                    json_file,
                    indent=indent,
                    ensure_ascii=ensure_ascii,
                    sort_keys=False
                )
            print(f"Successfully converted {len(self.data)} rows to {self.json_file_path}")
        except IOError as e:
            raise IOError(f"Error writing JSON file: {e}")
    
    def get_json_string(self, indent: int = 2, ensure_ascii: bool = False) -> str:
        """
        Get the JSON data as a string without saving to file.
        
        Args:
            indent: Indentation for pretty-printing (default: 2)
            ensure_ascii: If False, allow non-ASCII characters (default: False)
        
        Returns:
            JSON string representation of the data
        
        Raises:
            ValueError: If no data is available
        """
        if not self.data:
            raise ValueError("No data to convert. Please read a CSV file first.")
        
        return json.dumps(
            self.data,
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=False
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the CSV data.
        
        Returns:
            Dictionary with statistics about the data
        """
        if not self.data:
            return {"error": "No data loaded"}
        
        stats = {
            "total_rows": len(self.data),
            "total_columns": len(self.data[0]) if self.data else 0,
            "columns": list(self.data[0].keys()) if self.data else [],
            "empty_values": self._count_empty_values()
        }
        
        return stats
    
    def _count_empty_values(self) -> Dict[str, int]:
        """Count empty values in each column."""
        empty_counts = {}
        for column in self.data[0].keys():
            count = sum(1 for row in self.data if row.get(column) in (None, '', ' ', '  '))
            empty_counts[column] = count
        return empty_counts


def main():
    """
    Main function to run the CSV to JSON converter from command line.
    """
    print("=== CSV to JSON Converter ===")
    
    # Get input file path
    while True:
        csv_path = input("\nEnter the path to your CSV file: ").strip()
        if os.path.exists(csv_path):
            break
        print("File not found. Please try again.")
    
    # Get output file path (optional)
    json_path = input("Enter output JSON path (press Enter for default): ").strip()
    if not json_path:
        json_path = None
    
    # Get delimiter (optional)
    delimiter = input("Enter delimiter (press Enter for comma): ").strip()
    if not delimiter:
        delimiter = ','
    
    try:
        # Create converter instance
        converter = CSVToJSONConverter(csv_path, json_path)
        
        # Read CSV
        print(f"\nReading CSV file: {csv_path}")
        converter.read_csv(delimiter=delimiter)
        
        # Show statistics
        stats = converter.get_statistics()
        print(f"\nFile Statistics:")
        print(f"  - Total rows: {stats['total_rows']}")
        print(f"  - Total columns: {stats['total_columns']}")
        print(f"  - Columns: {', '.join(stats['columns'])}")
        
        # Ask for confirmation
        confirm = input(f"\nConvert to JSON and save to {converter.json_file_path}? (y/n): ").strip().lower()
        if confirm in ('y', 'yes'):
            converter.convert_to_json()
            print("\nConversion completed successfully!")
        
        # Ask if they want to see the JSON
        show = input("\nDisplay JSON output? (y/n): ").strip().lower()
        if show in ('y', 'yes'):
            json_str = converter.get_json_string()
            print("\nJSON Output:")
            print("=" * 50)
            print(json_str[:1000] + ("..." if len(json_str) > 1000 else ""))
            if len(json_str) > 1000:
                print(f"\n(Truncated. Full output saved to {converter.json_file_path})")
        
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
