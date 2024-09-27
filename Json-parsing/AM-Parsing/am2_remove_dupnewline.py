import re

def remove_consecutive_spaces(input_string):
    # Use regex to replace any occurrences of multiple \s+ with just one \s+
    result = re.sub(r'(\\s\+){2,}', r'\\s+', input_string)
    return result

# Example input with multiple consecutive \s+
grok_rule_with_multiple_spaces = r"""

"""

# Remove consecutive \s+ occurrences
cleaned_grok_rule = remove_consecutive_spaces(grok_rule_with_multiple_spaces)

# Print the cleaned output
print(cleaned_grok_rule)
