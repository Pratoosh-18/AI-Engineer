set -e

AMFI_URL="https://www.amfiindia.com/spages/NAVAll.txt"
OUTPUT_TSV="amfi_nav_data.tsv"
OUTPUT_JSON="amfi_nav_data.json"

echo "===================================="
echo "AMFI NAV Data Extraction Tool"
echo "===================================="
echo "Fetching data from: $AMFI_URL"

check_requirements() {
    for cmd in curl awk grep; do
        if ! command -v $cmd &> /dev/null; then
            echo "Error: $cmd is required but not installed."
            exit 1
        fi
    done
}

download_data() {
    echo "Downloading data..."
    local temp_file="amfi_data_temp.txt"
    
    if curl -s --retry 3 --retry-delay 2 -o "$temp_file" "$AMFI_URL"; then
        echo "Download completed successfully."
        echo "$(wc -l < "$temp_file") lines of data retrieved."
        echo
    else
        echo "Error: Failed to download data from $AMFI_URL"
        exit 1
    fi
    
    echo "$temp_file"
}

extract_to_tsv() {
    local input_file=$1
    local output_file=$2
    
    echo "Extracting Scheme Name and Asset Value to TSV..."
    
    echo -e "Scheme Name\tNet Asset Value" > "$output_file"
    
    awk -F';' '
        # Skip header lines and empty lines
        NF >= 5 && $4 != "" && $5 != "" {
            # Print Scheme Name and Net Asset Value separated by tab
            print $4 "\t" $5
        }
    ' "$input_file" >> "$output_file"
    
    local count=$(wc -l < "$output_file")
    echo "Extraction complete. $((count-1)) records extracted to $output_file"
}

convert_to_json() {
    local input_file=$1
    local output_file=$2
    
    echo "Converting data to JSON format..."
    
    echo "[" > "$output_file"
    
    awk -F'\t' 'NR > 1 {
        # Remove any quotes that might cause JSON parsing issues
        gsub(/"/, "\"", $1);
        gsub(/"/, "\"", $2);
        
        # Print JSON object for each entry, with comma except for last line
        printf "  {\n    \"scheme_name\": \"%s\",\n    \"nav\": \"%s\"\n  }%s\n", 
               $1, $2, (NR==FNR ? "" : ",")
    }' "$input_file" | sed '$ s/,$//' >> "$output_file"
    
    echo "]" >> "$output_file"
    
    echo "JSON conversion complete. Data saved to $output_file"
}

main() {
    check_requirements
    
    local data_file=$(download_data)
    
    extract_to_tsv "$data_file" "$OUTPUT_TSV"
    convert_to_json "$OUTPUT_TSV" "$OUTPUT_JSON"
    
    echo
    echo "Summary:"
    echo "- TSV data saved to: $OUTPUT_TSV"
    echo "- JSON data saved to: $OUTPUT_JSON"
    echo
    echo "Data format comparison:"
    echo "- TSV: Simpler format, easy to read in spreadsheet applications"
    echo "- JSON: More structured, better for programmatic access, supports nested data"
    echo
    echo "Recommendation for this data:"
    echo "For this specific AMFI NAV data with just two columns, both formats work well."
    echo "- Use TSV if primarily working with spreadsheets or basic data analysis"
    echo "- Use JSON if integrating with web applications or need programmatic access"
    
    echo
    echo "Cleaning up temporary files..."
    rm -f "$data_file"
    echo "Done!"
}

main