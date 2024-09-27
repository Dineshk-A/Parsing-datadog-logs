import re

def add_double_backslashes(grok_rule):
    # Replace all single backslashes with double backslashes
    grok_rule = grok_rule.replace('\\', '\\\\')

    # Add backslash before every { except for %{DATA...}
    # This regex looks for `{` that is NOT preceded by `%`
    grok_rule = re.sub(r'(?<!%)\{', '\\\\{', grok_rule)

    return grok_rule

# Example output from the first script
grok_rule = r"""

"""

# Apply the transformation
processed_grok_rule = add_double_backslashes(grok_rule)
print(processed_grok_rule)
