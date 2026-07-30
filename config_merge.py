import yaml
import os

# Define the list of YAML files
file_list = [
    "callhome.yaml",
    "com.yaml",
    "database_config.yaml",
    "factory_setting.yaml",
    "logging.yaml",
    "mqtt.yaml",
    "oee.yaml",
    "redis.yaml",
    "software_version.yaml"
]

# Define the output file name
output_file = "config/system_config.yaml"

# Initialize an empty dictionary to store merged data
merged_data = {}

# Function to load and merge data from a YAML file
def merge_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        name = os.path.splitext(os.path.basename(file_path))[0]
        merged_data[name] = data

# Iterate through the list of files and merge data
for file_name in file_list:
    merge_yaml(f'config/{file_name}')

# Write the merged data to the output file
with open(output_file, 'w') as outfile:
    yaml.dump(merged_data, outfile, default_flow_style=False)

print(f"Data merged successfully and saved to {output_file}")
