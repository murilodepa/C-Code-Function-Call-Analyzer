# csv_display.py
"""
This script provides a utility function to load and display a sample of a CSV file.
It displays the first few rows, a preview of the content, and the total number of rows.
Author: [Your Name]
Date: [Today's Date]
"""

import pandas as pd

# Set Pandas options for a large display limit if needed
pd.options.display.max_rows = 10000

def display_csv(file_path, max_rows=10):
    """
    Load and display a sample of the content of a CSV file.
    
    Parameters:
    file_path (str): The path to the CSV file.
    max_rows (int): The maximum number of rows to display from the start of the file.
                    Defaults to 10.
    """
    try:
        # Load the CSV file with header detection and error handling for malformed lines
        df = pd.read_csv(file_path, on_bad_lines='warn')

        # Display a sample of rows from the beginning and end
        print("CSV File Content (sample):")
        print(df.head(max_rows))  # Display the first max_rows rows
        
        # Display total number of rows in the DataFrame
        print(f"\nTotal rows: {df.shape[0]}")

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except pd.errors.EmptyDataError:
        print(f"The file '{file_path}' is empty.")
    except pd.errors.ParserError:
        print(f"Error parsing '{file_path}'. Check for malformed rows.")
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")

# Example usage
# display_csv('example.csv')
