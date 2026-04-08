#!/usr/bin/env python3
"""
Convert SMILES data from IARC-SMILES repository to SELFIES format.
"""

import os
import sys
from pathlib import Path
import selfies as sf
import pandas as pd


def convert_smiles_to_selfies(smiles: str) -> str:
    """
    Convert a SMILES string to SELFIES format.
    
    Args:
        smiles: SMILES string
        
    Returns:
        SELFIES string or empty string if conversion fails
    """
    try:
        return sf.encoder(smiles)
    except Exception as e:
        print(f"Warning: Failed to convert SMILES '{smiles}': {e}", file=sys.stderr)
        return ""


def process_file(input_path: Path, output_path: Path):
    """
    Process a single data file, converting SMILES to SELFIES.
    
    Args:
        input_path: Path to input file
        output_path: Path to output file
    """
    print(f"Processing {input_path.name}...")
    
    # Determine file format and read accordingly
    if input_path.suffix == '.csv':
        df = pd.read_csv(input_path)
    elif input_path.suffix in ['.tsv', '.txt']:
        df = pd.read_csv(input_path, sep='\t')
    elif input_path.suffix == '.xlsx':
        df = pd.read_excel(input_path)
    else:
        print(f"Skipping unsupported file format: {input_path.suffix}")
        return
    
    # Find SMILES column (case-insensitive)
    smiles_col = None
    for col in df.columns:
        if col.lower() in ['smiles', 'smile', 'canonical_smiles']:
            smiles_col = col
            break
    
    if smiles_col is None:
        print(f"Warning: No SMILES column found in {input_path.name}, skipping")
        return
    
    # Convert SMILES to SELFIES
    df['SELFIES'] = df[smiles_col].apply(lambda x: convert_smiles_to_selfies(str(x)) if pd.notna(x) else "")
    
    # Save to output file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if output_path.suffix == '.csv':
        df.to_csv(output_path, index=False)
    elif output_path.suffix in ['.tsv', '.txt']:
        df.to_csv(output_path, sep='\t', index=False)
    elif output_path.suffix == '.xlsx':
        df.to_excel(output_path, index=False)
    
    # Count successful conversions
    successful = (df['SELFIES'] != "").sum()
    total = len(df)
    print(f"  Converted {successful}/{total} SMILES to SELFIES")


def main():
    """Main conversion process."""
    smiles_data_dir = Path("smiles-data")
    selfies_data_dir = Path("selfies-data")
    
    if not smiles_data_dir.exists():
        print(f"Error: {smiles_data_dir} directory not found!", file=sys.stderr)
        sys.exit(1)
    
    # Create output directory
    selfies_data_dir.mkdir(exist_ok=True)
    
    # Find all data files
    data_files = []
    for ext in ['*.csv', '*.tsv', '*.txt', '*.xlsx']:
        data_files.extend(smiles_data_dir.glob(f"**/{ext}"))
    
    if not data_files:
        print(f"Warning: No data files found in {smiles_data_dir}")
        sys.exit(0)
    
    print(f"Found {len(data_files)} data file(s) to process\n")
    
    # Process each file
    for input_file in data_files:
        relative_path = input_file.relative_to(smiles_data_dir)
        output_file = selfies_data_dir / relative_path
        
        try:
            process_file(input_file, output_file)
        except Exception as e:
            print(f"Error processing {input_file.name}: {e}", file=sys.stderr)
            continue
    
    print(f"\nConversion complete! SELFIES data saved to {selfies_data_dir}/")


if __name__ == "__main__":
    main()
