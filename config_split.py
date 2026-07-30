import yaml
import os

# Define the input merged file
input_file = "config/system_config.yaml"

# Read the merged data from the input file
with open(input_file, 'r') as file:
    merged_data = yaml.safe_load(file)

# Function to write data to individual YAML files
def write_to_yaml(file_name, data):
    with open(file_name, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

# Iterate through the merged data and write to individual files
for name, data in merged_data.items():
    output_file = f"config/{name}.yaml"
    write_to_yaml(output_file, data)

print("Data split successfully.")
