import json
import re

# Recursive function to handle both nested and normal JSON and create grok rule
def generate_grok_rule(json_input, parent_key="", indent_level=0, single_line=False):
    grok_patterns = []
    indent_spaces = "\\s+" if not single_line else ""  # Add \s+ for multiline JSON only

    # Function to escape curly braces and square brackets
    def escape_braces(pattern):
        if "%{data:" not in pattern:  # Only escape if it's not a Grok pattern
            pattern = re.sub(r"([\{\}\[\]])", r"\\\1", pattern)
        return pattern

    # Loop through the key-value pairs in the JSON
    for i, (key, value) in enumerate(json_input.items()):
        nested_key_prefix = f"{parent_key}{key}."

        # Check if this is the last key-value pair for handling commas
        is_last = i == len(json_input) - 1

        if isinstance(value, dict):  # Nested JSON handling
            pattern = f'{indent_spaces}"{key}": {{'  # Opening curly brace for nested object
            grok_patterns.append(escape_braces(pattern))
            # Recursively process the nested JSON
            grok_patterns.extend(generate_grok_rule(value, nested_key_prefix, indent_level + 1, single_line))
            # Append closing brace and only add a comma if not the last item
            pattern = f"{indent_spaces}}}{',' if not is_last else ''}"  # Closing curly brace
            grok_patterns.append(escape_braces(pattern))
        elif isinstance(value, list):  # Handle arrays/lists
            pattern = f'{indent_spaces}"{key}": ['
            grok_patterns.append(escape_braces(pattern))
            for j, item in enumerate(value):
                if isinstance(item, dict):  # If the list contains dictionaries
                    grok_patterns.extend(generate_grok_rule(item, nested_key_prefix, indent_level + 1, single_line))
                else:  # For non-dict items in the list (primitive types)
                    grok_patterns.append(f'{indent_spaces}"%{{data:{nested_key_prefix[:-1].lower()}}}"')
                # Handle comma between list items
                if j != len(value) - 1:
                    grok_patterns[-1] += ','
            grok_patterns.append(escape_braces(f'{indent_spaces}]{"," if not is_last else ""}'))
        elif isinstance(value, str):  # Handle normal string values
            pattern = f'{indent_spaces}"{key}": "%{{data:{nested_key_prefix[:-1].lower()}}}"'
            grok_patterns.append(pattern + ("," if not is_last else ""))
        elif isinstance(value, bool):  # Handle boolean values (true/false)
            pattern = f'{indent_spaces}"{key}": %{{data:{nested_key_prefix[:-1].lower()}}}'
            grok_patterns.append(pattern + ("," if not is_last else ""))
        elif value is None:  # Handle null values
            pattern = f'{indent_spaces}"{key}": null'
            grok_patterns.append(pattern + ("," if not is_last else ""))
        else:  # Handle other types (numbers, etc.)
            pattern = f'{indent_spaces}"{key}": %{{data:{nested_key_prefix[:-1].lower()}}}'
            grok_patterns.append(pattern + ("," if not is_last else ""))

    return grok_patterns

# Function to determine if the JSON is on a single line or multiline
def is_single_line_json(json_str):
    return "\n" not in json_str.strip()

# Sample log input with both normal and nested JSON
log_input = r"""
{
  "company": {
    "name": "Tech Corp",
    "location": {
      "city": "New York",
      "country": "USA"
    },
    "employee": {
      "id": "12345",
      "name": "Alice Smith",
      "role": {
        "title": "Software Engineer",
        "department": "Development"
      }
    }
  }
}
"""

# Convert string input to JSON
json_input = json.loads(log_input)

# Detect if JSON is single-line
single_line = is_single_line_json(log_input)

# Generate the grok rule
grok_patterns = generate_grok_rule(json_input, single_line=single_line)
grok_rule = "{\n" + "\n".join(grok_patterns) + "\n}"
print(grok_rule)
