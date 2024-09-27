import re

def convert_double_backslash_to_single(input_string):
    # Use regex to replace \\s+ with \s+
    result = re.sub(r'\\\\s\+', r'\\s+', input_string)
    return result

# Example input with double backslash \\s+
grok_rule_with_double_backslash = r"""

"""

# Convert \\s+ to \s+
cleaned_grok_rule = convert_double_backslash_to_single(grok_rule_with_double_backslash)

# Print the cleaned output
print(cleaned_grok_rule)
