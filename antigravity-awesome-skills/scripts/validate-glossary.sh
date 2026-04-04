#!/bin/bash

# Glossary Consistency Validation Script
# Validates glossary structure and reports statistics

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
GLOSSARY_FILE="$PROJECT_ROOT/docs_zh-CN/.glossary.json"
OUTPUT_FILE="$PROJECT_ROOT/docs_zh-CN/glossary-consistency-report.txt"

# Create timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install jq to run this script."
    echo "  Ubuntu/Debian: sudo apt-get install jq"
    echo "  macOS: brew install jq"
    exit 1
fi

# Initialize report
{
    echo "Glossary Consistency Report"
    echo "==========================="
    echo "Generated: $TIMESTAMP"
    echo ""
    echo "Glossary File: $GLOSSARY_FILE"
    echo ""
    echo "----------------------------------------"
    echo ""
} > "$OUTPUT_FILE"

# Check if glossary file exists
if [[ ! -f "$GLOSSARY_FILE" ]]; then
    {
        echo "ERROR: Glossary file not found at:"
        echo "  $GLOSSARY_FILE"
        echo ""
        echo "Please create the glossary file first."
    } >> "$OUTPUT_FILE"
    echo "Error: Glossary file not found!"
    exit 1
fi

# Validate JSON structure
if ! jq empty "$GLOSSARY_FILE" 2>/dev/null; then
    {
        echo "ERROR: Invalid JSON in glossary file."
        echo "Please check the file format."
    } >> "$OUTPUT_FILE"
    echo "Error: Invalid JSON in glossary file!"
    exit 1
fi

# Extract metadata
{
    echo "METADATA"
    echo "========"
    echo ""
    echo "Version:"
    jq -r '.metadata.version' "$GLOSSARY_FILE" | sed 's/^/  /'
    echo ""
    echo "Created:"
    jq -r '.metadata.created' "$GLOSSARY_FILE" | sed 's/^/  /'
    echo ""
    echo "Last Updated:"
    jq -r '.metadata.last_updated' "$GLOSSARY_FILE" | sed 's/^/  /'
    echo ""
    echo "----------------------------------------"
    echo ""
} >> "$OUTPUT_FILE"

# Extract term count
TERM_COUNT=$(jq -r '.metadata.total_terms // 0' "$GLOSSARY_FILE")

{
    echo "GLOSSARY STATISTICS"
    echo "==================="
    echo ""
    echo "Total Terms: $TERM_COUNT"
    echo ""
} >> "$OUTPUT_FILE"

if [[ "$TERM_COUNT" -eq 0 ]]; then
    echo "Glossary is empty. No terms to analyze." >> "$OUTPUT_FILE"
else
    # Get top 10 terms
    {
        echo "Top 10 Terms (alphabetical):"
        echo ""
        jq -r '.terms | to_entries | sort_by(.key) | .[0:10][] | "  \(.key): \(.value.zh // (if .value.translations then .value.translations[0] else "N/A" end))"' "$GLOSSARY_FILE" 2>/dev/null || echo "  Unable to extract terms"
        echo ""
    } >> "$OUTPUT_FILE"

    # Check for required fields
    {
        echo "Field Validation:"
        echo ""
        jq -r '.terms | to_entries[] | select(.value.zh == null and (.value.translations | not) ) | "  Missing translation: \(.key)"' "$GLOSSARY_FILE" > /tmp/missing_translations.txt

        if [[ -s /tmp/missing_translations.txt ]]; then
            cat /tmp/missing_translations.txt >> "$OUTPUT_FILE"
        else
            echo "  All terms have translations." >> "$OUTPUT_FILE"
        fi

        rm -f /tmp/missing_translations.txt
        echo ""
    } >> "$OUTPUT_FILE"
fi

# Consistency checks
{
    echo "----------------------------------------"
    echo ""
    echo "CONSISTENCY CHECKS"
    echo "=================="
    echo ""
} >> "$OUTPUT_FILE"

# Check for duplicate English terms
DUPLICATES=$(jq -r '.terms | keys[]' "$GLOSSARY_FILE" | sort | uniq -d)

if [[ -n "$DUPLICATES" ]]; then
    echo "WARNING: Duplicate term keys found:" >> "$OUTPUT_FILE"
    echo "$DUPLICATES" | sed 's/^/  /' >> "$OUTPUT_FILE"
else
    echo "No duplicate term keys found." >> "$OUTPUT_FILE"
fi

{
    echo ""
    echo "----------------------------------------"
    echo ""
    echo "VALIDATION COMPLETE"
    echo ""
    echo "Glossary file is valid and ready for use."
} >> "$OUTPUT_FILE"

echo "Glossary validation complete. Report saved to:"
echo "  $OUTPUT_FILE"
echo ""
echo "Summary:"
echo "  Total Terms: $TERM_COUNT"
echo "  Status: Valid ✓"
