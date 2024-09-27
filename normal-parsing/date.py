import re

def extract_date_format(date_str):
    # Define regex patterns to match different date and time formats
    date_formats = {
        # Patterns for datetime with milliseconds (1 to 3 digits)
        r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.(\d{1,3}))Z?$': lambda m: f'%{{date("yyyy-MM-dd HH:mm:ss.{"SSS" if len(m.group(2)) == 3 else "SS" if len(m.group(2)) == 2 else "S"}{"Z" if "Z" in date_str else ""}"):date}}',  # With milliseconds and optional Z
        r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}\.(\d{1,3}))Z?$': lambda m: f'%{{date("yyyy/MM/dd HH:mm:ss.{"SSS" if len(m.group(2)) == 3 else "SS" if len(m.group(2)) == 2 else "S"}{"Z" if "Z" in date_str else ""}"):date}}',  # With milliseconds and optional Z
        r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}\.(\d{1,3}))Z?$': lambda m: f'%{{date("MM/dd/yyyy HH:mm:ss.{"SSS" if len(m.group(2)) == 3 else "SS" if len(m.group(2)) == 2 else "S"}{"Z" if "Z" in date_str else ""}"):date}}',  # With milliseconds and optional Z
        r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.(\d{1,3}))Z?$': lambda m: f'%{{date("yyyy-MM-dd\'T\'HH:mm:ss.{"SSS" if len(m.group(2)) == 3 else "SS" if len(m.group(2)) == 2 else "S"}{"Z" if "Z" in date_str else ""}"):date}}',  # With milliseconds and optional Z
        
        # Patterns for datetime with UTC indicator (without milliseconds)
        r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})Z$': lambda m: '%{date("yyyy-MM-dd HH:mm:ssZ"):date}',  # UTC time without milliseconds
        r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})Z$': lambda m: '%{date("yyyy/MM/dd HH:mm:ssZ"):date}',  # UTC time without milliseconds
        r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})Z$': lambda m: '%{date("MM/dd/yyyy HH:mm:ssZ"):date}',  # UTC time without milliseconds
        r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})Z$': lambda m: '%{date("yyyy-MM-dd\'T\'HH:mm:ssZ"):date}',  # UTC time without milliseconds and T separator
        
        # Patterns for datetime without milliseconds
        r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})': '%{date("yyyy-MM-dd HH:mm:ss"):date}',  # Without milliseconds
        r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})': '%{date("yyyy/MM/dd HH:mm:ss"):date}',  # Without milliseconds
        r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})': '%{date("MM/dd/yyyy HH:mm:ss"):date}',  # Without milliseconds
        r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})': '%{date("yyyy-MM-dd\'T\'HH:mm:ss"):date}',  # Without milliseconds and T separator

        # Patterns for dates without time
        r'(\d{4}-\d{2}-\d{2})': '%{date("yyyy-MM-dd"):date}',  # For dates without time
        r'(\d{4}/\d{2}/\d{2})': '%{date("yyyy/MM/dd"):date}',  # For dates without time
    }

    for pattern, grok_format in date_formats.items():
        match = re.match(pattern, date_str)
        if match:
            if callable(grok_format):  # If grok_format is a function (lambda)
                return grok_format(match)  # Call the lambda function with the match object
            return grok_format  # Otherwise, return the static format
    return None

def parse_date_time_only(text):
    # Check if the text matches any date-time format
    date_grok = extract_date_format(text)
    if date_grok:
        return date_grok
    else:
        return "No valid date-time format found."

# Replace this with your single test input
test_input = "2024/06/24 11:22:59.234Z"  # Input date-time string

# Output
parsed_date_time_output = parse_date_time_only(test_input)
print(parsed_date_time_output)
