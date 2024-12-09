import csv, re

def filter_rows_with_keyword_and_add_trim(input_file, output_file, keyword="null"):
    # Compile a regular expression for a whole-word match (case-insensitive)
    keyword_pattern = re.compile(rf'\b{re.escape(keyword)}\b', re.IGNORECASE)
    trim_pattern = re.compile(r'Trim:\s*([^;]+)')  # Extract text after "Trim:" up to the next semicolon
    
    matches_found = 0  # Counter for debugging
    seen_links = set()  # Set to track unique links
    
    # Open the input CSV file
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        # Define new fieldnames with the added "Trim" column
        fieldnames = reader.fieldnames[:4] + ["Trim"] + reader.fieldnames[4:]
        
        # Prepare the output CSV file
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            # Write the header to the output CSV
            writer.writeheader()
            
            # Process each row in the input CSV
            for row in reader:
                print(f"DEBUG: Checking row: {row}")  # Debug: print row content
                
                # Normalize values and check if the keyword matches as a full word
                if any(keyword_pattern.search(str(value).strip() or "") for value in row.values()):
                    link = row.get("Link", "").strip()  # Get the Link column value
                    if link and link not in seen_links:  # Check if link is unique
                        # Extract "Trim" value from the Specifications field
                        specifications = row.get("Specifications", "")
                        trim_match = trim_pattern.search(specifications)
                        trim_value = trim_match.group(1).strip() if trim_match else "Unknown"
                        
                        # Insert the "Trim" value into the row
                        row["Trim"] = trim_value
                        
                        print(f"DEBUG: Match found, trim extracted: {trim_value}, row: {row}")  # Debug: print matching row
                        writer.writerow(row)
                        seen_links.add(link)  # Mark the link as seen
                        matches_found += 1
                    else:
                        print(f"DEBUG: Duplicate link found, skipping row: {row}")

    print(f"DEBUG: Total matches found (unique links): {matches_found}")

def remove_duplicates_and_clean_trim(input_file, output_file):
    trim_pattern = re.compile(r'Trim:\s*([^;]+)')  # Regex to extract Trim value
    seen_links = set()  # Set to track unique links
    
    # Mapping of common trims to standardized values
    trim_replacements = {
        "performance": "Performance",
        "long range": "Long Range",
        "standard range plus": "Standard Range Plus",
    }
    
    # Function to clean and standardize trim values
    def clean_trim(trim, specifications):
        trim_lower = trim.lower()
        for key, replacement in trim_replacements.items():
            if key in trim_lower:
                return replacement
        
        # Handle cases where trim is not recognized
        if "awd" in specifications.lower():
            return "Long Range"
        elif "rwd" in specifications.lower():
            return "Standard Range Plus"
        return trim  # If no match and no AWD/RWD, leave it as-is
    
    # Open the input CSV file
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        # Define new fieldnames with the added "Trim" column
        fieldnames = reader.fieldnames[:4] + ["Trim"] + reader.fieldnames[4:]
        
        # Prepare the output CSV file
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            # Write the header to the output CSV
            writer.writeheader()
            
            # Process each row in the input CSV
            for row in reader:
                link = row.get("Link", "").strip()  # Get the Link column value
                if link and link not in seen_links:  # Check if link is unique
                    # Extract "Trim" value from the Specifications field
                    specifications = row.get("Specifications", "")
                    trim_match = trim_pattern.search(specifications)
                    raw_trim = trim_match.group(1).strip() if trim_match else "Unknown"
                    
                    # Clean and standardize the Trim value
                    clean_trim_value = clean_trim(raw_trim, specifications)
                    row["Trim"] = clean_trim_value
                    
                    # Write the row to the output file
                    writer.writerow(row)
                    seen_links.add(link)  # Mark the link as seen
                else:
                    print(f"DEBUG: Duplicate link found, skipping row: {row}")

    print(f"DEBUG: Processed file, removed duplicates, and standardized trims.")


def keycleanup(keyword = "Performance",input_csv = "Autotrader_Listings_Updated.csv"):
    

    # Define input and output file paths
    
    output_csv = input_csv.split(".")[0]+"_"+keyword+".csv"

    # Run the function
    filter_rows_with_keyword_and_add_trim(input_csv, output_csv,keyword)

    print(f"Filtered rows have been saved to {output_csv}")
    return output_csv
