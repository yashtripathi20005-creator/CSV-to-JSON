# test_converter.py
"""
Unit tests for the CSV to JSON converter.
Run with: python -m unittest test_converter.py
"""

import unittest
import json
import os
import tempfile
from csv_to_json_converter import CSVToJSONConverter


class TestCSVToJSONConverter(unittest.TestCase):
    """Test cases for CSVToJSONConverter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_csv_content = """name,age,city,employed
John Doe,30,New York,true
Jane Smith,25,Los Angeles,false
Bob Johnson,35,Chicago,true
"""
        self.temp_dir = tempfile.mkdtemp()
        self.csv_file = os.path.join(self.temp_dir, "test.csv")
        self.json_file = os.path.join(self.temp_dir, "test.json")
        
        with open(self.csv_file, 'w') as f:
            f.write(self.test_csv_content)
    
    def tearDown(self):
        """Clean up test fixtures."""
        for file in [self.csv_file, self.json_file]:
            if os.path.exists(file):
                os.remove(file)
        os.rmdir(self.temp_dir)
    
    def test_initialization(self):
        """Test converter initialization."""
        converter = CSVToJSONConverter(self.csv_file)
        self.assertEqual(converter.csv_file_path, self.csv_file)
        self.assertIsNotNone(converter.json_file_path)
    
    def test_read_csv(self):
        """Test reading CSV file."""
        converter = CSVToJSONConverter(self.csv_file)
        converter.read_csv()
        self.assertEqual(len(converter.data), 3)
        self.assertEqual(converter.data[0]['name'], 'John Doe')
        self.assertEqual(converter.data[0]['age'], 30)
        self.assertEqual(converter.data[0]['employed'], True)
    
    def test_type_conversion(self):
        """Test automatic type conversion."""
        converter = CSVToJSONConverter(self.csv_file)
        converter.read_csv()
        
        # Check types
        self.assertIsInstance(converter.data[0]['age'], int)
        self.assertIsInstance(converter.data[0]['employed'], bool)
        self.assertIsInstance(converter.data[0]['name'], str)
    
    def test_convert_to_json(self):
        """Test converting to JSON and saving to file."""
        converter = CSVToJSONConverter(self.csv_file, self.json_file)
        converter.read_csv()
        converter.convert_to_json()
        
        self.assertTrue(os.path.exists(self.json_file))
        
        with open(self.json_file, 'r') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['name'], 'John Doe')
    
    def test_get_json_string(self):
        """Test getting JSON as string."""
        converter = CSVToJSONConverter(self.csv_file)
        converter.read_csv()
        json_str = converter.get_json_string()
        
        self.assertIsInstance(json_str, str)
        data = json.loads(json_str)
        self.assertEqual(len(data), 3)
    
    def test_empty_file(self):
        """Test handling of empty CSV file."""
        empty_csv = os.path.join(self.temp_dir, "empty.csv")
        with open(empty_csv, 'w') as f:
            f.write("")
        
        converter = CSVToJSONConverter(empty_csv)
        with self.assertRaises(csv.Error):
            converter.read_csv()
    
    def test_custom_delimiter(self):
        """Test reading with custom delimiter."""
        semicolon_content = """name;age;city
Alice;30;New York
Bob;25;Los Angeles
"""
        csv_file = os.path.join(self.temp_dir, "semicolon.csv")
        with open(csv_file, 'w') as f:
            f.write(semicolon_content)
        
        converter = CSVToJSONConverter(csv_file)
        converter.read_csv(delimiter=';')
        self.assertEqual(len(converter.data), 2)
        self.assertEqual(converter.data[0]['name'], 'Alice')
        self.assertEqual(converter.data[0]['age'], 30)
    
    def test_missing_file(self):
        """Test handling of missing file."""
        converter = CSVToJSONConverter("nonexistent.csv")
        with self.assertRaises(FileNotFoundError):
            converter.read_csv()
    
    def test_statistics(self):
        """Test statistics generation."""
        converter = CSVToJSONConverter(self.csv_file)
        converter.read_csv()
        stats = converter.get_statistics()
        
        self.assertEqual(stats['total_rows'], 3)
        self.assertEqual(stats['total_columns'], 4)
        self.assertIn('name', stats['columns'])
        self.assertIn('age', stats['columns'])
        
        # Check empty values (none should be empty)
        for count in stats['empty_values'].values():
            self.assertEqual(count, 0)


if __name__ == '__main__':
    unittest.main()
