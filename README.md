# IARC-SELFIES

Automated conversion of IARC-SMILES data to SELFIES format.

## Overview

This repository contains a CI/CD pipeline that automatically:
1. Clones the `data` folder from [IARC-SMILES](https://github.com/morawskidotmy/IARC-SMILES)
2. Converts all SMILES strings to SELFIES format
3. Commits and pushes the converted data to the `data/` folder in this repository

## SELFIES Format

SELFIES (Self-Referencing Embedded Strings) is a robust molecular string representation that guarantees 100% validity of generated molecules, unlike SMILES which can produce invalid structures.

## CI/CD Pipeline

The conversion runs automatically on:
- **Monthly schedule** (1st of each month at 2 AM UTC) - checks for updates to IARC-SMILES repository
- Pushes to the `main` branch
- Pull requests
- Manual workflow dispatch

The workflow intelligently checks if IARC-SMILES has been updated and only runs the conversion when there are new changes, avoiding unnecessary processing.

### Workflow Steps

1. **Check for updates**: Compares latest IARC-SMILES commit with last processed version
2. **Clone IARC-SMILES data**: Uses sparse checkout to efficiently clone only the data folder
3. **Install dependencies**: Uses `uv` for fast Python package installation
4. **Convert to SELFIES**: Processes all CSV/TSV/Excel files containing SMILES data
5. **Commit and push**: Saves converted SELFIES data to the `data/` folder and pushes to the repository

## Local Usage

To run the conversion locally:

```bash
# Clone the IARC-SMILES data
git clone --depth 1 --filter=blob:none --sparse https://github.com/morawskidotmy/IARC-SMILES.git temp-smiles
cd temp-smiles
git sparse-checkout set data
cd ..
mv temp-smiles/data ./smiles-data
rm -rf temp-smiles

# Install dependencies with uv
uv pip install selfies pandas

# Run conversion
python convert_smiles_to_selfies.py

# Move to data folder
mkdir -p data
mv selfies-data/* data/
```

The converted SELFIES data will be saved to `data/`.

## Dependencies

- Python 3.11+
- [selfies](https://github.com/aspuru-guzik-group/selfies) - SMILES to SELFIES conversion
- pandas - Data manipulation
- openpyxl (for Excel files, installed with pandas)

## License

See [LICENSE](LICENSE) file.
