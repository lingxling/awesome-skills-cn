#!/usr/bin/env python3
"""
Script to execute all Python programs under "skills" directories with `uv run` and --help flag.
"""

import subprocess
from pathlib import Path

def find_python_files():
    """Find all Python files under skills directories."""
    python_files = []
    
    # Search for skills directories and find Python files
    for skills_dir in Path('.').rglob('../skills'):
        if skills_dir.is_dir():
            python_files.extend(skills_dir.rglob('*.py'))
    
    return sorted(set(python_files))

def run_with_help(python_file):
    """Run a Python file with uv run --help."""
    try:
        print(f"\n{'='*60}")
        print(f"Running: {python_file}")
        print(f"{'='*60}")
        
        result = subprocess.run(
            ['uv', 'run', str(python_file), '--help'],
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        if result.returncode == 0:
            print("SUCCESS - Output:")
            print(result.stdout)
        else:
            print(f"FAILED - Return code: {result.returncode}")
            if result.stderr:
                print("Stderr:")
                print(result.stderr)
            if result.stdout:
                print("Stdout:")
                print(result.stdout)
                
    except subprocess.TimeoutExpired:
        print("TIMEOUT - Command took too long")
    except FileNotFoundError:
        print("ERROR - uv command not found. Please install uv.")
        return False
    except Exception as e:
        print(f"ERROR - {str(e)}")
    
    return True

def main():
    """Main function to find and run all Python files."""
    print("Finding Python files under skills directories...")
    python_files = find_python_files()
    
    if not python_files:
        print("No Python files found under skills directories.")
        return
    
    print(f"Found {len(python_files)} Python files")
    
    success_count = 0
    failed_count = 0
    
    for python_file in python_files:
        if run_with_help(python_file):
            success_count += 1
        else:
            failed_count += 1
    
    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"Total files: {len(python_files)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failed_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
