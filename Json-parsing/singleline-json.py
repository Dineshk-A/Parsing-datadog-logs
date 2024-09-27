import json
import re

# Recursive function to handle both nested and normal JSON and create grok rule
def generate_grok_rule_with_spaces(original_input, json_input, parent_key=""):
    grok_patterns = []

    # Function to escape curly braces and square brackets
    def escape_braces(pattern):
        if "%{data:" not in pattern:  # Only escape if it's not a Grok pattern
            pattern = re.sub(r"([\{\}\[\]])", r"\\\1", pattern)
        return pattern

    # Extract spaces between key-value pairs in the original input
    def extract_spaces_between_key_value_pairs(original_json_str, key):
        # This pattern captures the key and any spaces after the colon
        pattern = rf'("{key}"\s*:\s*)'
        match = re.search(pattern, original_json_str)
        if match:
            return match.group(1)  # Return the key and any spaces after the colon
        return f'"{key}":'  # Default formatting without any extra spaces

    # Loop through the key-value pairs in the JSON
    for key, value in json_input.items():
        nested_key_prefix = f"{parent_key}{key}."

        if isinstance(value, dict):  # Nested JSON handling
            key_with_spaces = extract_spaces_between_key_value_pairs(original_input, key)
            grok_patterns.append(escape_braces(f'{key_with_spaces}{{'))  # Opening brace for object
            grok_patterns.extend(generate_grok_rule_with_spaces(original_input, value, nested_key_prefix))  # Recursive for nested
            grok_patterns.append(escape_braces('}'))  # Closing brace for object
        elif isinstance(value, list):  # Handle arrays/lists
            key_with_spaces = extract_spaces_between_key_value_pairs(original_input, key)
            grok_patterns.append(escape_braces(f'{key_with_spaces}['))  # Opening bracket for array
            for item in value:
                if isinstance(item, dict):
                    grok_patterns.extend(generate_grok_rule_with_spaces(original_input, item, nested_key_prefix))
                else:
                    grok_patterns.append(f'"%{{data:{nested_key_prefix[:-1].lower()}}}"')
            grok_patterns.append(escape_braces(']'))  # Closing bracket for array
        elif isinstance(value, str):  # Handle normal string values
            key_with_spaces = extract_spaces_between_key_value_pairs(original_input, key)
            grok_patterns.append(f'{key_with_spaces}"%{{data:{nested_key_prefix[:-1].lower()}}}"')
        elif isinstance(value, bool):  # Handle boolean values (true/false)
            key_with_spaces = extract_spaces_between_key_value_pairs(original_input, key)
            grok_patterns.append(f'{key_with_spaces}%{{data:{nested_key_prefix[:-1].lower()}}}')
        elif value is None:  # Handle null values
            key_with_spaces = extract_spaces_between_key_value_pairs(original_input, key)
            grok_patterns.append(f'{key_with_spaces}null')
        else:  # Handle other types (numbers, etc.)
            key_with_spaces = extract_spaces_between_key_value_pairs(original_input, key)
            grok_patterns.append(f'{key_with_spaces}%{{data:{nested_key_prefix[:-1].lower()}}}')

    return grok_patterns

# Sample log input with or without spaces after colons
log_input = r"""{"company":{"name": "Tech Corp","location":{"city": "New York","country": "USA"},"employee":{"id": "12345","name": "Alice Smith","role":{"title": "Software Engineer","department":"Development"}}}}"""

# Convert the string input to JSON
json_input = json.loads(log_input)

# Generate the grok rule based on the single user input
grok_patterns = generate_grok_rule_with_spaces(log_input, json_input)

# Output the final Grok rule
grok_rule = "".join(grok_patterns)

print("Generated Grok Rule:")
print(grok_rule)
