import re

def parse_date_time_only(date_str):
    # Define regex patterns to match different date and time formats
    date_formats = {
        # Patterns for datetime with milliseconds (1 to 3 digits) with and without 'T' separator
        r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}\.(\d{1,3}))Z?$': lambda m: f'%{{date("yyyy-MM-dd{"\'T\'" if "T" in m.group(0) else " "}HH:mm:ss.{"SSS" if len(m.group(2)) == 3 else "SS" if len(m.group(2)) == 2 else "S"}{"Z" if "Z" in date_str else ""}"):date}}',
        r'(\d{4}/\d{2}/\d{2}[T ]\d{2}:\d{2}:\d{2}\.(\d{1,3}))Z?$': lambda m: f'%{{date("yyyy/MM/dd{"\'T\'" if "T" in m.group(0) else " "}HH:mm:ss.{"SSS" if len(m.group(2)) == 3 else "SS" if len(m.group(2)) == 2 else "S"}{"Z" if "Z" in date_str else ""}"):date}}',

        # Patterns for datetime without milliseconds, with and without 'T' separator
        r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})Z?$': lambda m: f'%{{date("yyyy-MM-dd{"\'T\'" if "T" in m.group(0) else " "}HH:mm:ss{"Z" if "Z" in date_str else ""}"):date}}',
        r'(\d{4}/\d{2}/\d{2}[T ]\d{2}:\d{2}:\d{2})Z?$': lambda m: f'%{{date("yyyy/MM/dd{"\'T\'" if "T" in m.group(0) else " "}HH:mm:ss{"Z" if "Z" in date_str else ""}"):date}}',

        # Patterns for dd/MM/yyyy and dd-MM-yyyy with time and optional milliseconds
        r'(\d{2}/\d{2}/\d{4}[T ]\d{2}:\d{2}:\d{2}\.(\d{1,3}))Z?$': lambda m: f'%{{date("dd/MM/yyyy{"\'T\'" if "T" in m.group(0) else " "}HH:mm:ss.{"SSS" if len(m.group(2)) == 3 else "SS" if len(m.group(2)) == 2 else "S"}{"Z" if "Z" in date_str else ""}"):date}}',
        r'(\d{2}-\d{2}-\d{4}[T ]\d{2}:\d{2}:\d{2}\.(\d{1,3}))Z?$': lambda m: f'%{{date("dd-MM-yyyy{"\'T\'" if "T" in m.group(0) else " "}HH:mm:ss.{"SSS" if len(m.group(2)) == 3 else "SS" if len(m.group(2)) == 2 else "S"}{"Z" if "Z" in date_str else ""}"):date}}',

        # Patterns for datetime without milliseconds in dd/MM/yyyy and dd-MM-yyyy
        r'(\d{2}/\d{2}/\d{4}[T ]\d{2}:\d{2}:\d{2})Z?$': lambda m: f'%{{date("dd/MM/yyyy{"\'T\'" if "T" in m.group(0) else " "}HH:mm:ss{"Z" if "Z" in date_str else ""}"):date}}',
        r'(\d{2}-\d{2}-\d{4}[T ]\d{2}:\d{2}:\d{2})Z?$': lambda m: f'%{{date("dd-MM-yyyy{"\'T\'" if "T" in m.group(0) else " "}HH:mm:ss{"Z" if "Z" in date_str else ""}"):date}}',

        # Patterns for dates without time
        r'(\d{4}-\d{2}-\d{2})': '%{date("yyyy-MM-dd"):date}',  # For yyyy-MM-dd format without time
        r'(\d{4}/\d{2}/\d{2})': '%{date("yyyy/MM/dd"):date}',  # For yyyy/MM/dd format without time
        r'(\d{2}/\d{2}/\d{4})': '%{date("dd/MM/yyyy"):date}',  # For dd/MM/yyyy format without time
        r'(\d{2}-\d{2}-\d{4})': '%{date("dd-MM-yyyy"):date}',  # For dd-MM-yyyy format without time
    }

    for pattern, grok_format in date_formats.items():
        match = re.match(pattern, date_str)
        if match:
            if callable(grok_format):  # If grok_format is a function (lambda)
                return grok_format(match)  # Call the lambda function with the match object
            return grok_format  # Otherwise, return the static format
    return "No valid date-time format found."

# Test the function with a single input
test_input = "2024/06/06 10:12:12"  # Example input

# Output the parsed Grok format
parsed_date_time_output = parse_date_time_only(test_input)
print(f"{parsed_date_time_output}")
