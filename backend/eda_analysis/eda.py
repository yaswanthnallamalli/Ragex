import pandas as pd
import json
import os
 
def process_files(files):
    try:
        # Load and merge data from multiple files
        dfs = []
        for file in files:
            if file.content_type not in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
                return {"error": f"Invalid file type: {file.filename}"}
            dfs.append(pd.read_excel(file))
       
        combined_df = pd.concat(dfs, ignore_index=True)
 
        # Convert data types to standard Python types
        combined_df = combined_df.astype(object).where(pd.notnull(combined_df), None)
 
        # Filter numeric columns for summary statistics
        numeric_df = combined_df.select_dtypes(include=['number'])
 
        # Perform data analysis
        data_info = {
            "num_rows": int(combined_df.shape[0]),
            "num_columns": int(combined_df.shape[1]),
            "columns": {col: str(dtype) for col, dtype in combined_df.dtypes.items()},
            "summary_statistics": numeric_df.describe().applymap(lambda x: float(x) if pd.notnull(x) else None).to_dict() if not numeric_df.empty else "No numeric columns found",
            "missing_values": combined_df.isnull().sum().to_dict()
        }
 
        # Save JSON data to data folder in eda_analysis directory
        output_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'data_info.json')
       
        with open(output_file, 'w') as f:
            json.dump(data_info, f, indent=4)
       
        print(f"Data saved to {output_file}")  # Confirm the file path
 
        # Save the DataFrame as a CSV file instead of saving the Excel files
        csv_file_path = os.path.join(output_dir, 'data.csv')
        combined_df.to_csv(csv_file_path, index=False)
       
        print(f"Combined data saved to {csv_file_path} as data.csv")
 
        return data_info
    except Exception as e:
        return {"error": str(e)}