# AMFI NAV Data Extractor

A shell script that extracts Scheme Name and Net Asset Value data from the AMFI (Association of Mutual Funds in India) daily NAV file and saves it in both TSV and JSON formats.

## Features

- Downloads the latest NAV data file from AMFI's website
- Extracts scheme names and their corresponding NAV values
- Saves data in tab-separated values (TSV) format
- Also converts and saves data in JSON format
- Provides a format comparison and recommendations

## Requirements

- Bash shell (compatible with Linux, macOS, and Windows with WSL or Git Bash)
- Basic Unix utilities: `curl`, `awk`, `grep`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/amfi-data-extractor.git
cd amfi-data-extractor
```

2. Make the script executable:
```bash
chmod +x extract_amfi_data.sh
```

## Usage

Run the script with no arguments:

```bash
./extract_amfi_data.sh
```

The script will:
1. Download the latest NAV data from https://www.amfiindia.com/spages/NAVAll.txt
2. Extract Scheme Name and Net Asset Value
3. Save data in both TSV and JSON formats
4. Provide a summary and format recommendations

## Output Files

The script generates two output files:

1. `amfi_nav_data.tsv` - Tab-separated values format
   - Simple two-column format with headers
   - Easy to open in Excel, Google Sheets, or other spreadsheet applications

2. `amfi_nav_data.json` - JSON format
   - Array of objects, each with "scheme_name" and "nav" fields
   - Suitable for programmatic access and web applications

## Example Output

### TSV Format
```
Scheme Name	Net Asset Value
Aditya Birla Sun Life Overnight Fund-Direct Plan-Growth	1176.5232
Aditya Birla Sun Life Overnight Fund-Regular Plan-Growth	1175.0325
...
```

### JSON Format
```json
[
  {
    "scheme_name": "Aditya Birla Sun Life Overnight Fund-Direct Plan-Growth",
    "nav": "1176.5232"
  },
  {
    "scheme_name": "Aditya Birla Sun Life Overnight Fund-Regular Plan-Growth",
    "nav": "1175.0325"
  },
  ...
]
```

## Format Comparison: TSV vs JSON

### TSV (Tab-Separated Values)
- **Pros:**
  - Simple, lightweight format
  - Human-readable
  - Easy to open in spreadsheet applications
  - Better for large datasets with simple structure
- **Cons:**
  - Limited support for complex data structures
  - Less standardized than JSON

### JSON (JavaScript Object Notation)
- **Pros:**
  - Industry standard for data interchange
  - Support for complex, nested data structures
  - Native integration with JavaScript and web applications
  - Better type support
- **Cons:**
  - More verbose for simple data
  - Slightly harder to read for non-technical users

### Recommendation
For this specific AMFI NAV data with just two columns:
- Use **TSV** if primarily working with spreadsheets or basic data analysis
- Use **JSON** if integrating with web applications or need programmatic access

## Customization

You can modify the script to:
- Extract additional fields from the AMFI data
- Change output file names
- Customize the data processing logic

Simply edit the `extract_amfi_data.sh` file with your preferred text editor.

## Error Handling

The script includes basic error handling for:
- Missing dependencies
- Failed downloads
- Data processing issues

## License

MIT License