import pandas as pd
import json

# Load CSV file into a DataFrame
def load_csv(csv_file):
    df = pd.read_csv(csv_file)
    return df

# Clean the DataFrame
def clean_data(df):
    # Fill missing values (NaNs) with 0
    df.fillna(0, inplace=True)

    # Rename columns for easier access (replace dots with underscores)
    df.columns = [col.replace('.', '_') for col in df.columns]

    # Ensure all numeric columns are converted to integers
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            df[col] = df[col].astype(int)

    return df

# Save the cleaned DataFrame to a JSON file
def save_to_json(df, output_file):
    # Convert the DataFrame to a dictionary and then save it as JSON
    data_dict = df.to_dict(orient='records')  # Convert DataFrame to list of dictionaries
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, indent=2, ensure_ascii=False)
    print(f"Data saved to {output_file}")

def main():
    csv_file = 'reported.csv'
    output_file = 'cleaned_reported.json'
    
    # Load the CSV file into a DataFrame
    df = load_csv(csv_file)
    
    # Clean the data
    df_cleaned = clean_data(df)
    
    # Save the cleaned data to a JSON file
    save_to_json(df_cleaned, output_file)

if __name__ == "__main__":
    main()

