#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch CSV Converter for Snipe-IT Chinese Import
Process multiple CSV files in batch mode

Author: Manus AI
Date: 2025-07-23
Version: 1.0
"""

import os
import sys
import argparse
import glob
from pathlib import Path
import subprocess
import json
from typing import List, Dict, Tuple

class BatchConverter:
    """Batch converter for multiple CSV files"""
    
    def __init__(self, encoding_tool: str = "encoding-converter.py", 
                 field_tool: str = "csv-field-converter.py"):
        """Initialize batch converter"""
        self.encoding_tool = encoding_tool
        self.field_tool = field_tool
        self.results = []
    
    def find_csv_files(self, directory: str, pattern: str = "*.csv") -> List[str]:
        """Find all CSV files in directory"""
        search_pattern = os.path.join(directory, pattern)
        files = glob.glob(search_pattern)
        return sorted(files)
    
    def process_file(self, input_file: str, output_dir: str, asset_type: str = "assets") -> Dict:
        """Process a single CSV file"""
        filename = os.path.basename(input_file)
        name_without_ext = os.path.splitext(filename)[0]
        
        # Create output filenames
        temp_file = os.path.join(output_dir, f"{name_without_ext}_temp.csv")
        final_file = os.path.join(output_dir, f"{name_without_ext}_converted.csv")
        
        result = {
            "input_file": input_file,
            "temp_file": temp_file,
            "output_file": final_file,
            "asset_type": asset_type,
            "encoding_success": False,
            "field_success": False,
            "encoding_message": "",
            "field_message": "",
            "overall_success": False
        }
        
        try:
            # Step 1: Fix encoding
            print(f"Processing {filename}...")
            print("  Step 1: Fixing encoding...")
            
            encoding_cmd = [
                "python", self.encoding_tool, "fix", 
                input_file, temp_file
            ]
            
            encoding_result = subprocess.run(
                encoding_cmd, 
                capture_output=True, 
                text=True, 
                encoding='utf-8'
            )
            
            if encoding_result.returncode == 0:
                result["encoding_success"] = True
                result["encoding_message"] = "Encoding fixed successfully"
                print("    ✓ Encoding fixed")
            else:
                result["encoding_message"] = encoding_result.stderr
                print(f"    ✗ Encoding failed: {encoding_result.stderr}")
                return result
            
            # Step 2: Convert field names
            print("  Step 2: Converting field names...")
            
            field_cmd = [
                "python", self.field_tool, "convert",
                temp_file, final_file,
                "--type", asset_type
            ]
            
            field_result = subprocess.run(
                field_cmd,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if field_result.returncode == 0:
                result["field_success"] = True
                result["field_message"] = "Field names converted successfully"
                result["overall_success"] = True
                print("    ✓ Field names converted")
                
                # Clean up temp file
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    
            else:
                result["field_message"] = field_result.stderr
                print(f"    ✗ Field conversion failed: {field_result.stderr}")
            
        except Exception as e:
            result["encoding_message"] = f"Exception during processing: {str(e)}"
            print(f"    ✗ Exception: {str(e)}")
        
        return result
    
    def process_directory(self, input_dir: str, output_dir: str, 
                         asset_type: str = "assets", pattern: str = "*.csv") -> List[Dict]:
        """Process all CSV files in a directory"""
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Find all CSV files
        csv_files = self.find_csv_files(input_dir, pattern)
        
        if not csv_files:
            print(f"No CSV files found in {input_dir} matching pattern {pattern}")
            return []
        
        print(f"Found {len(csv_files)} CSV files to process:")
        for file in csv_files:
            print(f"  - {os.path.basename(file)}")
        print()
        
        # Process each file
        results = []
        for csv_file in csv_files:
            result = self.process_file(csv_file, output_dir, asset_type)
            results.append(result)
            self.results.append(result)
        
        return results
    
    def generate_report(self, results: List[Dict], output_file: str = None) -> str:
        """Generate processing report"""
        total_files = len(results)
        successful_files = sum(1 for r in results if r["overall_success"])
        failed_files = total_files - successful_files
        
        report = f"Batch Conversion Report\n"
        report += f"=" * 50 + "\n\n"
        report += f"Total files processed: {total_files}\n"
        report += f"Successful conversions: {successful_files}\n"
        report += f"Failed conversions: {failed_files}\n"
        report += f"Success rate: {(successful_files/total_files*100):.1f}%\n\n"
        
        # Successful files
        if successful_files > 0:
            report += f"Successfully Converted Files:\n"
            report += f"-" * 30 + "\n"
            for result in results:
                if result["overall_success"]:
                    filename = os.path.basename(result["input_file"])
                    output_filename = os.path.basename(result["output_file"])
                    report += f"✓ {filename} → {output_filename}\n"
            report += "\n"
        
        # Failed files
        if failed_files > 0:
            report += f"Failed Conversions:\n"
            report += f"-" * 20 + "\n"
            for result in results:
                if not result["overall_success"]:
                    filename = os.path.basename(result["input_file"])
                    report += f"✗ {filename}\n"
                    if not result["encoding_success"]:
                        report += f"  Encoding error: {result['encoding_message']}\n"
                    elif not result["field_success"]:
                        report += f"  Field conversion error: {result['field_message']}\n"
            report += "\n"
        
        # Next steps
        report += f"Next Steps:\n"
        report += f"-" * 10 + "\n"
        if successful_files > 0:
            report += f"1. Review converted files in the output directory\n"
            report += f"2. Validate the converted CSV files before importing\n"
            report += f"3. Import the files to Snipe-IT using web interface or command line\n"
        
        if failed_files > 0:
            report += f"4. Review and fix the failed conversions manually\n"
            report += f"5. Check the error messages for specific issues\n"
        
        # Save report to file if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to: {output_file}")
        
        return report
    
    def validate_converted_files(self, results: List[Dict]) -> Dict:
        """Validate all converted files"""
        validation_results = {
            "total_files": 0,
            "valid_files": 0,
            "invalid_files": 0,
            "details": []
        }
        
        for result in results:
            if not result["overall_success"]:
                continue
                
            output_file = result["output_file"]
            if not os.path.exists(output_file):
                continue
            
            validation_results["total_files"] += 1
            
            # Validate using the field converter tool
            try:
                validate_cmd = [
                    "python", self.field_tool, "validate", output_file
                ]
                
                validate_result = subprocess.run(
                    validate_cmd,
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                
                if validate_result.returncode == 0:
                    validation_results["valid_files"] += 1
                    status = "Valid"
                else:
                    validation_results["invalid_files"] += 1
                    status = "Invalid"
                
                validation_results["details"].append({
                    "file": os.path.basename(output_file),
                    "status": status,
                    "message": validate_result.stdout or validate_result.stderr
                })
                
            except Exception as e:
                validation_results["invalid_files"] += 1
                validation_results["details"].append({
                    "file": os.path.basename(output_file),
                    "status": "Error",
                    "message": str(e)
                })
        
        return validation_results

def main():
    """Main function for command line interface"""
    parser = argparse.ArgumentParser(
        description='Batch convert multiple CSV files for Snipe-IT Chinese import',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python batch-convert.py process input_dir output_dir
  python batch-convert.py process input_dir output_dir --type users
  python batch-convert.py process input_dir output_dir --pattern "*assets*.csv"
  python batch-convert.py validate output_dir
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Process CSV files in batch')
    process_parser.add_argument('input_dir', help='Input directory containing CSV files')
    process_parser.add_argument('output_dir', help='Output directory for converted files')
    process_parser.add_argument('--type', choices=['assets', 'users', 'accessories', 'consumables', 'licenses', 'components'],
                               default='assets', help='Asset type (default: assets)')
    process_parser.add_argument('--pattern', default='*.csv', help='File pattern to match (default: *.csv)')
    process_parser.add_argument('--report', help='Output file for processing report')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate converted files')
    validate_parser.add_argument('directory', help='Directory containing converted CSV files')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    converter = BatchConverter()
    
    if args.command == 'process':
        if not os.path.exists(args.input_dir):
            print(f"Error: Input directory '{args.input_dir}' not found.")
            return
        
        print(f"Starting batch conversion...")
        print(f"Input directory: {args.input_dir}")
        print(f"Output directory: {args.output_dir}")
        print(f"Asset type: {args.type}")
        print(f"File pattern: {args.pattern}")
        print()
        
        # Process files
        results = converter.process_directory(
            args.input_dir, 
            args.output_dir, 
            args.type, 
            args.pattern
        )
        
        # Generate report
        report_file = args.report or os.path.join(args.output_dir, "conversion_report.txt")
        report = converter.generate_report(results, report_file)
        print(report)
        
        # Validate converted files
        print("Validating converted files...")
        validation_results = converter.validate_converted_files(results)
        
        print(f"\nValidation Results:")
        print(f"Total files validated: {validation_results['total_files']}")
        print(f"Valid files: {validation_results['valid_files']}")
        print(f"Invalid files: {validation_results['invalid_files']}")
        
        if validation_results['invalid_files'] > 0:
            print("\nInvalid files:")
            for detail in validation_results['details']:
                if detail['status'] != 'Valid':
                    print(f"  ✗ {detail['file']}: {detail['status']}")
    
    elif args.command == 'validate':
        if not os.path.exists(args.directory):
            print(f"Error: Directory '{args.directory}' not found.")
            return
        
        # Find converted CSV files
        csv_files = converter.find_csv_files(args.directory, "*_converted.csv")
        
        if not csv_files:
            print(f"No converted CSV files found in {args.directory}")
            return
        
        print(f"Validating {len(csv_files)} converted files...")
        
        # Create fake results for validation
        fake_results = []
        for csv_file in csv_files:
            fake_results.append({
                "overall_success": True,
                "output_file": csv_file
            })
        
        validation_results = converter.validate_converted_files(fake_results)
        
        print(f"\nValidation Results:")
        print(f"Total files: {validation_results['total_files']}")
        print(f"Valid files: {validation_results['valid_files']}")
        print(f"Invalid files: {validation_results['invalid_files']}")
        
        for detail in validation_results['details']:
            status_icon = "✓" if detail['status'] == 'Valid' else "✗"
            print(f"  {status_icon} {detail['file']}: {detail['status']}")

if __name__ == '__main__':
    main()

