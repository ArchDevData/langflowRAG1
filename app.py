import os
import json

# Define the file path for your flow.json
file_path = "./LangRAG.json"  # Replace with the actual file path

# Function to load flow data from the JSON file
def load_flow_from_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            flow_data = json.load(file)
        return flow_data
    else:
        print(f"File {file_path} not found.")
        return None

if __name__ == "__main__":
    flow = load_flow_from_json(file_path)  # Use the defined file path
    if flow:
        print(f"Loaded flow: {flow}")
    else:
        print("Failed to load flow.")
