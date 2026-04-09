# IARC-SELFIES

Automated conversion of IARC-SMILES data to SELFIES format.

## Overview

This repository contains a CI/CD pipeline that automatically:
1. Clones the `data` folder from [IARC-SMILES](https://github.com/morawskidotmy/IARC-SMILES)
2. Converts all SMILES strings to SELFIES format
3. Commits and pushes the converted data to the `data/` folder in this repository

## File Format

Output SELFIES data uses the [`.sfi` file format](https://github.com/morawskidotmy/.sfi) — the SELFIES equivalent of `.smi`.

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
# One-shot wrapper: clone, convert, cleanup temp files, exit
bash ./run_conversion.sh

# Optional: run converter directly with custom paths
python convert_smiles_to_selfies.py --input-dir ./smiles-data --output-dir ./data --sfi-dir ./data
```

The converted SELFIES data will be saved to `data/`.

## Dependencies

- Python 3.11+
- [selfies](https://github.com/aspuru-guzik-group/selfies) - SMILES to SELFIES conversion
- pandas - Data manipulation
- openpyxl (for Excel files, installed with pandas)

## License

See [LICENSE](LICENSE) file.
