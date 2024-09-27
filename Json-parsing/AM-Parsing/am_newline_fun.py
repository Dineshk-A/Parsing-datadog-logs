import json

# Recursive function to handle both nested and normal JSON and create grok rule
def generate_grok_rule(json_input, parent_key="", indent_level=0):
    grok_patterns = []
    indent_spaces = "\\s+" * indent_level  # Single \s+ per indent level

    # Loop through the key-value pairs in the JSON
    for i, (key, value) in enumerate(json_input.items()):
        full_key_cleaned = key.replace('\\', '\\\\')  # Handle single backslashes
        nested_key_prefix = f"{parent_key}{key}."

        # Check if this is the last key-value pair for handling commas
        is_last = i == len(json_input) - 1

        if isinstance(value, dict):  # Nested JSON handling
            # Add the rule for the current key and nest it correctly
            pattern = f'{indent_spaces}\\"{full_key_cleaned}\\": \\{{'  # Note the space after colon
            grok_patterns.append(pattern)
            # Recursively process the nested JSON
            grok_patterns.extend(generate_grok_rule(value, nested_key_prefix, indent_level + 1))
            # Append closing brace and only add a comma if not the last item
            grok_patterns.append(f"{indent_spaces}\\}}{',' if not is_last else ''}")
        elif isinstance(value, str):  # Handle normal string values
            pattern = f'{indent_spaces}\\"{full_key_cleaned}\\": \\"%{{data:{nested_key_prefix[:-1].lower()}}}\\"'
            grok_patterns.append(pattern + ("," if not is_last else ""))
        elif isinstance(value, bool):  # Handle boolean values (true/false)
            pattern = f'{indent_spaces}\\"{full_key_cleaned}\\": %{{data:{nested_key_prefix[:-1].lower()}}}'
            grok_patterns.append(pattern + ("," if not is_last else ""))
        elif value is None:  # Handle null values
            pattern = f'{indent_spaces}\\"{full_key_cleaned}\\": %{{data:{nested_key_prefix[:-1].lower()}}}'
            grok_patterns.append(pattern + ("," if not is_last else ""))
        else:  # Handle other types (numbers, etc.)
            pattern = f'{indent_spaces}\\"{full_key_cleaned}\\": %{{data:{nested_key_prefix[:-1].lower()}}}'
            grok_patterns.append(pattern + ("," if not is_last else ""))

    return grok_patterns

# Sample log input with both normal and nested JSON
log_input = r"""

"""

# Convert string input to JSON
json_input = json.loads(log_input.replace('\\"', '"'))

# Generate the grok rule
grok_patterns = generate_grok_rule(json_input)
grok_rule = "{\n" + "\n".join(grok_patterns) + "\n}"
print(grok_rule)
