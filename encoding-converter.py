#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV Encoding Converter for Snipe-IT
Convert CSV files to UTF-8 encoding for proper Chinese character support

Author: Manus AI
Date: 2025-07-23
Version: 1.0
"""

import os
import sys
import argparse
import chardet
import csv
from typing import Tuple, Optional

class EncodingConverter:
    """CSV encoding converter for Chinese character support"""
    
    def __init__(self):
        """Initialize encoding converter"""
        self.common_encodings = [
            'utf-8', 'utf-8-sig',  # UTF-8 with and without BOM
            'gbk', 'gb2312', 'gb18030',  # Chinese encodings
            'big5',  # Traditional Chinese
            'cp936',  # Windows Chinese
            'iso-8859-1', 'latin1',  # Western encodings
            'cp1252',  # Windows Western
        ]
    
    def detect_encoding(self, file_path: str) -> Tuple[str, float]:
        """Detect file encoding using chardet and manual testing"""
        # First try chardet
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            detected_encoding = result['encoding']
            confidence = result['confidence']
        
        print(f"Chardet detection: {detected_encoding} (confidence: {confidence:.2f})")
        
        # If confidence is high enough, use detected encoding
        if confidence > 0.8 and detected_encoding:
            return detected_encoding, confidence
        
        # Otherwise, try common encodings manually
        print("Low confidence detection, trying common encodings...")
        
        for encoding in self.common_encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    # Check if content contains Chinese characters
                    has_chinese = any('\u4e00' <= char <= '\u9fff' for char in content)
                    if has_chinese:
                        print(f"Successfully read with {encoding} (contains Chinese characters)")
                        return encoding, 0.9
                    else:
                        print(f"Successfully read with {encoding} (no Chinese characters detected)")
                        return encoding, 0.7
            except (UnicodeDecodeError, UnicodeError):
                continue
            except Exception as e:
                print(f"Error testing {encoding}: {e}")
                continue
        
        # Fallback to detected encoding or utf-8
        return detected_encoding or 'utf-8', confidence or 0.5
    
    def convert_to_utf8(self, input_file: str, output_file: str, source_encoding: Optional[str] = None) -> Tuple[bool, str]:
        """Convert CSV file to UTF-8 encoding"""
        try:
            # Detect source encoding if not provided
            if not source_encoding:
                source_encoding, confidence = self.detect_encoding(input_file)
                if confidence < 0.5:
                    return False, f"Could not reliably detect encoding for {input_file}"
            
            print(f"Converting from {source_encoding} to UTF-8...")
            
            # Read file with source encoding
            with open(input_file, 'r', encoding=source_encoding) as infile:
                content = infile.read()
            
            # Write file with UTF-8 encoding (without BOM)
            with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
                outfile.write(content)
            
            # Verify the conversion
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    f.read()
                
                report = f"Encoding conversion successful!\n"
                report += f"Input file: {input_file}\n"
                report += f"Output file: {output_file}\n"
                report += f"Source encoding: {source_encoding}\n"
                report += f"Target encoding: UTF-8\n"
                
                # Check file sizes
                input_size = os.path.getsize(input_file)
                output_size = os.path.getsize(output_file)
                report += f"Input size: {input_size} bytes\n"
                report += f"Output size: {output_size} bytes\n"
                
                return True, report
                
            except UnicodeDecodeError:
                return False, "Conversion failed: Output file is not valid UTF-8"
            
        except Exception as e:
            return False, f"Error during conversion: {str(e)}"
    
    def validate_utf8(self, file_path: str) -> Tuple[bool, str]:
        """Validate if file is properly encoded in UTF-8"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for BOM
            with open(file_path, 'rb') as f:
                first_bytes = f.read(3)
                has_bom = first_bytes == b'\xef\xbb\xbf'
            
            # Count Chinese characters
            chinese_chars = sum(1 for char in content if '\u4e00' <= char <= '\u9fff')
            
            report = f"UTF-8 Validation Report for: {file_path}\n"
            report += f"File is valid UTF-8: Yes\n"
            report += f"Has BOM: {'Yes' if has_bom else 'No'}\n"
            report += f"Total characters: {len(content)}\n"
            report += f"Chinese characters: {chinese_chars}\n"
            
            if has_bom:
                report += f"\nNote: File has BOM (Byte Order Mark). "
                report += f"Some systems may have issues with BOM in CSV files.\n"
            
            return True, report
            
        except UnicodeDecodeError as e:
            return False, f"File is not valid UTF-8: {str(e)}"
        except Exception as e:
            return False, f"Error validating file: {str(e)}"
    
    def remove_bom(self, file_path: str) -> Tuple[bool, str]:
        """Remove BOM from UTF-8 file"""
        try:
            # Read file as binary
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Check if file has BOM
            if content.startswith(b'\xef\xbb\xbf'):
                # Remove BOM and write back
                content_without_bom = content[3:]
                with open(file_path, 'wb') as f:
                    f.write(content_without_bom)
                return True, f"BOM removed from {file_path}"
            else:
                return True, f"No BOM found in {file_path}"
                
        except Exception as e:
            return False, f"Error removing BOM: {str(e)}"
    
    def fix_csv_encoding(self, input_file: str, output_file: str) -> Tuple[bool, str]:
        """Complete CSV encoding fix process"""
        try:
            # Step 1: Detect and convert encoding
            success, message = self.convert_to_utf8(input_file, output_file)
            if not success:
                return False, message
            
            # Step 2: Remove BOM if present
            success, bom_message = self.remove_bom(output_file)
            if not success:
                return False, bom_message
            
            # Step 3: Validate final result
            is_valid, validation_report = self.validate_utf8(output_file)
            if not is_valid:
                return False, validation_report
            
            # Step 4: Test CSV parsing
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    header = next(reader)
                    row_count = sum(1 for row in reader)
                
                final_report = f"CSV encoding fix completed successfully!\n\n"
                final_report += message + "\n"
                final_report += bom_message + "\n\n"
                final_report += f"CSV Structure:\n"
                final_report += f"Header fields: {len(header)}\n"
                final_report += f"Data rows: {row_count}\n"
                final_report += f"Fields: {', '.join(header[:5])}{'...' if len(header) > 5 else ''}\n\n"
                final_report += "File is ready for Snipe-IT import!\n"
                
                return True, final_report
                
            except Exception as e:
                return False, f"CSV parsing test failed: {str(e)}"
            
        except Exception as e:
            return False, f"Error in encoding fix process: {str(e)}"

def main():
    """Main function for command line interface"""
    parser = argparse.ArgumentParser(
        description='Convert CSV files to UTF-8 encoding for Snipe-IT Chinese character support',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python encoding-converter.py convert input.csv output.csv
  python encoding-converter.py convert input.csv output.csv --encoding gbk
  python encoding-converter.py validate input.csv
  python encoding-converter.py detect input.csv
  python encoding-converter.py fix input.csv output.csv
  python encoding-converter.py remove-bom file.csv
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert file encoding to UTF-8')
    convert_parser.add_argument('input', help='Input file path')
    convert_parser.add_argument('output', help='Output file path')
    convert_parser.add_argument('--encoding', help='Source encoding (auto-detect if not specified)')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate UTF-8 encoding')
    validate_parser.add_argument('input', help='Input file path')
    
    # Detect command
    detect_parser = subparsers.add_parser('detect', help='Detect file encoding')
    detect_parser.add_argument('input', help='Input file path')
    
    # Fix command (complete process)
    fix_parser = subparsers.add_parser('fix', help='Complete encoding fix process')
    fix_parser.add_argument('input', help='Input file path')
    fix_parser.add_argument('output', help='Output file path')
    
    # Remove BOM command
    bom_parser = subparsers.add_parser('remove-bom', help='Remove BOM from UTF-8 file')
    bom_parser.add_argument('input', help='Input file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    converter = EncodingConverter()
    
    if args.command == 'convert':
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' not found.")
            return
        
        success, message = converter.convert_to_utf8(args.input, args.output, args.encoding)
        print(message)
    
    elif args.command == 'validate':
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' not found.")
            return
        
        is_valid, report = converter.validate_utf8(args.input)
        print(report)
    
    elif args.command == 'detect':
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' not found.")
            return
        
        encoding, confidence = converter.detect_encoding(args.input)
        print(f"Detected encoding: {encoding}")
        print(f"Confidence: {confidence:.2f}")
    
    elif args.command == 'fix':
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' not found.")
            return
        
        success, message = converter.fix_csv_encoding(args.input, args.output)
        print(message)
    
    elif args.command == 'remove-bom':
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' not found.")
            return
        
        success, message = converter.remove_bom(args.input)
        print(message)

if __name__ == '__main__':
    main()

