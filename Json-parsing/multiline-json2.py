# Your multiline input string
log_input = r"""
{
\s+"company": \{
\s+"name": "%{data:company.name}",
\s+"location": \{
\s+"city": "%{data:company.location.city}",
\s+"country": "%{data:company.location.country}"
\s+\},
\s+"employee": \{
\s+"id": "%{data:company.employee.id}",
\s+"name": "%{data:company.employee.name}",
\s+"role": \{
\s+"title": "%{data:company.employee.role.title}",
\s+"department": "%{data:company.employee.role.department}"
\s+\}
\s+\}
\s+\}
}
"""

# Remove newline characters while preserving backslashes
single_line_output = log_input.replace("\n", "")

print("Single Line Output:")
print(single_line_output)
