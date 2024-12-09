import csv
import webbrowser

def open_links_from_csv(file_path, column_name = "Link"):
    """
    Opens links from a specified column in a CSV file in Chrome tabs.

    Parameters:
        file_path (str): Path to the CSV file.
        column_name (str): The name of the column containing the links.
    """
    try:
        # Open the CSV file
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)

            # Check if the column exists
            if column_name not in reader.fieldnames:
                print(f"Error: Column '{column_name}' not found in the CSV file.")
                return

            # Open each link in a new tab
            for row in reader:
                link = row[column_name].strip()
                if link:
                    webbrowser.open_new_tab(link)
            print("Links have been opened in Chrome.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example Usage
# Provide the path to your CSV file and the column name containing the links
def showcarsmain(csv_file_path = 'Autotrader_Listings_Filtered_Cleaned_DeepSearchPerformance.csv'):
    # Replace with the path to your CSV file
    link_column_name = 'Link'  # Replace with the actual column name in your CSV
    open_links_from_csv(csv_file_path, link_column_name)


# if True:
#     showcarsmain()