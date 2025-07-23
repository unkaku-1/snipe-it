#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Snipe-IT CSV Field Converter
Convert Chinese field names to English field names for Snipe-IT import

Author: Manus AI
Date: 2025-07-23
Version: 1.0
"""

import csv
import json
import os
import sys
import argparse
import chardet
from typing import Dict, List, Optional, Tuple

class CSVFieldConverter:
    """CSV field converter for Snipe-IT Chinese field names"""
    
    def __init__(self, mapping_file: str = "chinese-field-mapping.json"):
        """Initialize converter with field mapping configuration"""
        self.mapping_file = mapping_file
        self.field_mappings = {}
        self.load_mappings()
    
    def load_mappings(self) -> None:
        """Load field mappings from JSON configuration file"""
        try:
            with open(self.mapping_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.field_mappings = data.get('field_mappings', {})
                self.status_mappings = data.get('status_mappings', {})
                self.category_mappings = data.get('category_mappings', {})
                self.manufacturer_mappings = data.get('manufacturer_mappings', {})
        except FileNotFoundError:
            print(f"Error: Mapping file '{self.mapping_file}' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in mapping file: {e}")
            sys.exit(1)
    
    def detect_encoding(self, file_path: str) -> str:
        """Detect file encoding using chardet"""
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            confidence = result['confidence']
            
            print(f"Detected encoding: {encoding} (confidence: {confidence:.2f})")
            
            # If confidence is low, try common encodings
            if confidence < 0.7:
                for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5']:
                    try:
                        with open(file_path, 'r', encoding=enc) as test_file:
                            test_file.read()
                        print(f"Successfully read file with {enc} encoding")
                        return enc
                    except UnicodeDecodeError:
                        continue
            
            return encoding or 'utf-8'
    
    def convert_field_name(self, field_name: str, asset_type: str = 'assets') -> str:
        """Convert Chinese field name to English field name"""
        # Remove leading/trailing whitespace
        field_name = field_name.strip()
        
        # Check if field is already in English
        if field_name in self.get_all_english_fields():
            return field_name
        
        # Look up in mappings
        mappings = self.field_mappings.get(asset_type, {})
        if field_name in mappings:
            return mappings[field_name]
        
        # Check in other asset types if not found
        for other_type, other_mappings in self.field_mappings.items():
            if field_name in other_mappings:
                return other_mappings[field_name]
        
        # Return original if no mapping found
        print(f"Warning: No mapping found for field '{field_name}'")
        return field_name
    
    def convert_field_value(self, field_name: str, value: str) -> str:
        """Convert Chinese field values to English equivalents"""
        if not value or not isinstance(value, str):
            return value
        
        value = value.strip()
        
        # Convert status values
        if field_name.lower() in ['status', '状态', '设备状态']:
            return self.status_mappings.get(value, value)
        
        # Convert category values
        if field_name.lower() in ['category', '类别', '分类', '设备类型']:
            return self.category_mappings.get(value, value)
        
        # Convert manufacturer values
        if field_name.lower() in ['manufacturer', '制造商', '厂商', '生产商', '品牌']:
            return self.manufacturer_mappings.get(value, value)
        
        return value
    
    def get_all_english_fields(self) -> List[str]:
        """Get all English field names from mappings"""
        english_fields = set()
        for asset_type, mappings in self.field_mappings.items():
            english_fields.update(mappings.values())
        return list(english_fields)
    
    def convert_csv(self, input_file: str, output_file: str, asset_type: str = 'assets') -> Tuple[bool, str]:
        """Convert CSV file from Chinese fields to English fields"""
        try:
            # Detect file encoding
            encoding = self.detect_encoding(input_file)
            
            # Read input CSV
            with open(input_file, 'r', encoding=encoding) as infile:
                # Try to detect delimiter
                sample = infile.read(1024)
                infile.seek(0)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                
                reader = csv.reader(infile, delimiter=delimiter)
                rows = list(reader)
            
            if not rows:
                return False, "Input file is empty"
            
            # Convert header row
            header = rows[0]
            converted_header = []
            field_mapping_log = []
            
            for field in header:
                original_field = field
                converted_field = self.convert_field_name(field, asset_type)
                converted_header.append(converted_field)
                
                if original_field != converted_field:
                    field_mapping_log.append(f"'{original_field}' -> '{converted_field}'")
            
            # Convert data rows
            converted_rows = [converted_header]
            for row in rows[1:]:
                converted_row = []
                for i, value in enumerate(row):
                    if i < len(converted_header):
                        field_name = converted_header[i]
                        converted_value = self.convert_field_value(field_name, value)
                        converted_row.append(converted_value)
                    else:
                        converted_row.append(value)
                converted_rows.append(converted_row)
            
            # Write output CSV with UTF-8 encoding
            with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(converted_rows)
            
            # Generate conversion report
            report = f"Conversion completed successfully!\n"
            report += f"Input file: {input_file}\n"
            report += f"Output file: {output_file}\n"
            report += f"Asset type: {asset_type}\n"
            report += f"Total rows: {len(converted_rows)}\n"
            report += f"Field mappings applied:\n"
            
            if field_mapping_log:
                for mapping in field_mapping_log:
                    report += f"  - {mapping}\n"
            else:
                report += "  - No field mappings needed (all fields already in English)\n"
            
            return True, report
            
        except Exception as e:
            return False, f"Error converting CSV: {str(e)}"
    
    def validate_csv(self, file_path: str) -> Tuple[bool, str]:
        """Validate CSV file for Snipe-IT import"""
        try:
            encoding = self.detect_encoding(file_path)
            
            with open(file_path, 'r', encoding=encoding) as f:
                reader = csv.reader(f)
                header = next(reader)
                
                # Check for required fields (varies by asset type)
                required_fields = ['Category']  # Category is always required
                missing_fields = []
                
                for field in required_fields:
                    if field not in header:
                        missing_fields.append(field)
                
                # Check for common issues
                issues = []
                
                # Check for empty header fields
                for i, field in enumerate(header):
                    if not field.strip():
                        issues.append(f"Empty field name at column {i+1}")
                
                # Check for duplicate header fields
                seen_fields = set()
                for field in header:
                    if field in seen_fields:
                        issues.append(f"Duplicate field name: '{field}'")
                    seen_fields.add(field)
                
                # Generate validation report
                report = f"CSV Validation Report for: {file_path}\n"
                report += f"Encoding: {encoding}\n"
                report += f"Total fields: {len(header)}\n"
                report += f"Fields: {', '.join(header)}\n\n"
                
                if missing_fields:
                    report += f"Missing required fields: {', '.join(missing_fields)}\n"
                
                if issues:
                    report += f"Issues found:\n"
                    for issue in issues:
                        report += f"  - {issue}\n"
                else:
                    report += "No issues found.\n"
                
                is_valid = len(missing_fields) == 0 and len(issues) == 0
                return is_valid, report
                
        except Exception as e:
            return False, f"Error validating CSV: {str(e)}"
    
    def generate_template(self, asset_type: str, output_file: str) -> bool:
        """Generate CSV template with Chinese and English field names"""
        try:
            mappings = self.field_mappings.get(asset_type, {})
            
            if not mappings:
                print(f"No mappings found for asset type: {asset_type}")
                return False
            
            # Create header with both Chinese and English names
            chinese_header = list(mappings.keys())
            english_header = [mappings[field] for field in chinese_header]
            
            # Add sample data row
            sample_data = []
            for field in english_header:
                if field == 'Category':
                    sample_data.append('笔记本电脑')
                elif field == 'Item Name':
                    sample_data.append('示例设备名称')
                elif field == 'Company':
                    sample_data.append('示例公司')
                elif field == 'Location':
                    sample_data.append('办公室')
                elif field == 'Manufacturer':
                    sample_data.append('戴尔')
                elif field == 'Status':
                    sample_data.append('可部署')
                else:
                    sample_data.append('示例数据')
            
            # Write template file
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(chinese_header)  # Chinese field names
                writer.writerow(sample_data)     # Sample data
            
            print(f"Template generated: {output_file}")
            print(f"Chinese fields: {', '.join(chinese_header)}")
            print(f"English equivalents: {', '.join(english_header)}")
            
            return True
            
        except Exception as e:
            print(f"Error generating template: {str(e)}")
            return False

def main():
    """Main function for command line interface"""
    parser = argparse.ArgumentParser(
        description='Convert Snipe-IT CSV files from Chinese to English field names',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python csv-field-converter.py convert input.csv output.csv
  python csv-field-converter.py convert input.csv output.csv --type users
  python csv-field-converter.py validate input.csv
  python csv-field-converter.py template assets template.csv
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert CSV file')
    convert_parser.add_argument('input', help='Input CSV file path')
    convert_parser.add_argument('output', help='Output CSV file path')
    convert_parser.add_argument('--type', choices=['assets', 'users', 'accessories', 'consumables', 'licenses', 'components'],
                               default='assets', help='Asset type (default: assets)')
    convert_parser.add_argument('--mapping', help='Custom mapping file path')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate CSV file')
    validate_parser.add_argument('input', help='Input CSV file path')
    
    # Template command
    template_parser = subparsers.add_parser('template', help='Generate CSV template')
    template_parser.add_argument('type', choices=['assets', 'users', 'accessories', 'consumables', 'licenses', 'components'],
                                help='Asset type')
    template_parser.add_argument('output', help='Output template file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize converter
    mapping_file = args.mapping if hasattr(args, 'mapping') and args.mapping else 'chinese-field-mapping.json'
    converter = CSVFieldConverter(mapping_file)
    
    if args.command == 'convert':
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' not found.")
            return
        
        success, message = converter.convert_csv(args.input, args.output, args.type)
        print(message)
        
        if success:
            print(f"\nValidating converted file...")
            is_valid, validation_report = converter.validate_csv(args.output)
            print(validation_report)
    
    elif args.command == 'validate':
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' not found.")
            return
        
        is_valid, report = converter.validate_csv(args.input)
        print(report)
    
    elif args.command == 'template':
        success = converter.generate_template(args.type, args.output)
        if not success:
            sys.exit(1)

if __name__ == '__main__':
    main()

