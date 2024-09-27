# Your multiline input string
log_input = r"""

"""

# Remove newline characters while preserving backslashes
single_line_output = log_input.replace("\n", "")

print("Single Line Output:")
print(single_line_output)
