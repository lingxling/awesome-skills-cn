#!/bin/bash

# Link Validation Script
# Validates internal and external links in documentation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DOCS_DIR="$PROJECT_ROOT/docs"
TRANSLATED_DIR="$PROJECT_ROOT/docs_zh-CN"
OUTPUT_FILE="$TRANSLATED_DIR/link-validation-report.txt"

# Create timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Initialize report
{
    echo "Link Validation Report"
    echo "======================="
    echo "Generated: $TIMESTAMP"
    echo ""
    echo "Source Directory: $DOCS_DIR"
    echo "Translated Directory: $TRANSLATED_DIR"
    echo ""
    echo "----------------------------------------"
    echo ""
} > "$OUTPUT_FILE"

# Function to check if a file exists
file_exists() {
    local file="$1"
    if [[ -f "$file" ]]; then
        return 0
    else
        return 1
    fi
}

# Validate Internal Links
{
    echo "INTERNAL LINKS VALIDATION"
    echo "========================="
    echo ""
} >> "$OUTPUT_FILE"

# Find all markdown files and extract links
echo "Scanning for internal links..."

INTERNAL_LINKS=$(grep -rh '\[.*\](.*\.md)' "$DOCS_DIR" --include="*.md" | grep -oE '\([^)]+\.md\)' | sed 's/[(\)]//g' | sort -u)

if [[ -z "$INTERNAL_LINKS" ]]; then
    echo "No internal markdown links found." >> "$OUTPUT_FILE"
else
    echo "Found internal links. Validating..." >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"

    BROKEN_COUNT=0
    VALID_COUNT=0

    while IFS= read -r link; do
        # Handle relative links
        if [[ "$link" != /* ]] && [[ "$link" != http* ]]; then
            # This is a relative link, check if it exists in docs
            # LIMITATION: Currently only checks basename, not full relative path
            # This will report false positives for links like ../../CATALOG.md
            # TODO: Implement proper relative path resolution after more Chinese docs exist
            if find "$DOCS_DIR" -name "$(basename "$link")" -type f | grep -q .; then
                ((VALID_COUNT++))
            else
                echo "BROKEN: $link" >> "$OUTPUT_FILE"
                ((BROKEN_COUNT++))
            fi
        fi
    done <<< "$INTERNAL_LINKS"

    echo "" >> "$OUTPUT_FILE"
    echo "Summary:" >> "$OUTPUT_FILE"
    echo "  Valid Internal Links: $VALID_COUNT" >> "$OUTPUT_FILE"
    echo "  Broken Internal Links: $BROKEN_COUNT" >> "$OUTPUT_FILE"
fi

{
    echo ""
    echo "----------------------------------------"
    echo ""
} >> "$OUTPUT_FILE"

# Sample External Links
{
    echo "EXTERNAL LINKS SAMPLE"
    echo "====================="
    echo ""
    echo "Note: External links are sampled but not validated."
    echo "Run link checker manually to validate external URLs."
    echo ""
} >> "$OUTPUT_FILE"

EXTERNAL_LINKS=$(grep -rh '\[.*\](http' "$DOCS_DIR" --include="*.md" | grep -oE 'https?://[^")\s]+' | sort -u | head -20)

if [[ -z "$EXTERNAL_LINKS" ]]; then
    echo "No external links found." >> "$OUTPUT_FILE"
else
    echo "Sample of external links found:" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "$EXTERNAL_LINKS" >> "$OUTPUT_FILE"
fi

{
    echo ""
    echo "----------------------------------------"
    echo ""
    echo "VALIDATION COMPLETE"
    echo ""
} >> "$OUTPUT_FILE"

echo "Link validation complete. Report saved to:"
echo "  $OUTPUT_FILE"
echo ""
echo "Summary:"
wc -l < "$OUTPUT_FILE" | xargs echo "  Total lines:"
