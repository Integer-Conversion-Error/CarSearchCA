import csv
import KeywordCleanup


def remove_duplicates_from_row(row):
    """
    Removes duplicates within a single row. If an item appears in one column, it will not appear in others.
    """
    # Gather all unique values from all columns
    unique_values = set()
    for col in row:
        if col:
            unique_values.update(col.split("; "))

    # Remove duplicates from each column
    seen_values = set()
    cleaned_row = []
    for col in row:
        if col:
            items = col.split("; ")
            filtered_items = [item for item in items if item not in seen_values]
            seen_values.update(filtered_items)
            cleaned_row.append("; ".join(filtered_items))
        else:
            cleaned_row.append("")
    return cleaned_row


def clean_csv(input_file, output_file):
    """
    Cleans the CSV file by removing duplicates from each row's columns.
    """
    KeywordCleanup.remove_duplicates_and_clean_trim(input_file, output_file)
    with open(output_file, mode="r", newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        headers = next(reader)  # Read the headers
        rows = list(reader)

    cleaned_rows = [headers]  # Start with headers

    for row in rows:
        cleaned_row = remove_duplicates_from_row(row)
        cleaned_rows.append(cleaned_row)

    with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(cleaned_rows)


def csvmain(input_filename = "Autotrader_Listings_Updated.csv"):  # Input file name):
    
    output_csv = input_filename.split(".")[0]+"_Cleaned.csv"  # Output file name

    print("Cleaning CSV file...")
    clean_csv(input_filename, output_csv)
    
    print(f"Cleaned CSV file saved as {output_csv}")
    return output_csv


# if __name__ == "__main__":
#     csvmain()
