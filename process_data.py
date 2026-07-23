import glob
import os
import pandas as pd

# 1. Find all .xlsx files in the 'data/' folder (or root) dynamically
data_folder = "data"
excel_files = glob.glob(os.path.join(data_folder, "*.xlsx"))

if not excel_files:
    print(f"No Excel files found in '{data_folder}/'. Checking root repository...")
    excel_files = glob.glob("*.xlsx")

print(f"Found {len(excel_files)} sensor file(s): {excel_files}")

all_sensor_data = []

# 2. Iterate through whatever files exist without depending on fixed names
for file_path in excel_files:
    print(f"Processing: {file_path}")
    try:
        # Read Excel file (reads first sheet by default, or specify sheet_name=None for all)
        df = pd.read_excel(file_path)
        
        # Add metadata if needed (e.g., track source filename or sensor ID)
        sensor_id = os.path.basename(file_path).replace(".xlsx", "")
        df['Sensor_Source'] = sensor_id
        
        all_sensor_data.append(df)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# 3. Merge all parsed sensor data together
if all_sensor_data:
    combined_df = pd.concat(all_sensor_data, ignore_index=True)
    
    # Save output for your JSON dashboard / web host
    output_path = "processed_data.json"
    combined_df.to_json(output_path, orient="records", date_format="iso")
    print(f"Successfully generated {output_path}")
else:
    print("No data was processed.")
