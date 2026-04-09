#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP_DIR="$(mktemp -d "${REPO_ROOT}/.tmp-iarc-smiles-XXXXXX")"
DATA_DIR="${REPO_ROOT}/data"

cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

echo "Cloning IARC-SMILES data..."
git clone --depth 1 --filter=blob:none --sparse https://github.com/morawskidotmy/IARC-SMILES.git "${TMP_DIR}/repo"
git -C "${TMP_DIR}/repo" sparse-checkout set data

echo "Installing Python dependencies..."
python3 -m pip install --quiet selfies pandas openpyxl

echo "Cleaning legacy output folders..."
rm -rf "${REPO_ROOT}/selfies-data" "${REPO_ROOT}/selfies-sfi"
mkdir -p "${DATA_DIR}"

echo "Converting SMILES to SELFIES..."
python3 "${REPO_ROOT}/convert_smiles_to_selfies.py" \
  --input-dir "${TMP_DIR}/repo/data" \
  --output-dir "${DATA_DIR}" \
  --sfi-dir "${DATA_DIR}"

echo "Done."
echo "Converted tables and .sfi files: ${DATA_DIR}"
