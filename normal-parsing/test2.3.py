import re

def extract_date_format(date_str):
    # Define regex patterns to match different date and time formats
    date_formats = {
        r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}': '%{date("yyyy-MM-dd HH:mm:ss")}',
        r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}': '%{date("yyyy/MM/dd HH:mm:ss")}',
        r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}': '%{date("MM/dd/yyyy HH:mm:ss")}',
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}': '%{date("yyyy-MM-dd\'T\'HH:mm:ss")}',
        r'\d{4}-\d{2}-\d{2}': '%{date("yyyy-MM-dd")}',  # For dates without time
        r'\d{4}/\d{2}/\d{2}': '%{date("yyyy/MM/dd")}',  # For dates without time
    }
    
    for pattern, grok_format in date_formats.items():
        if re.match(pattern, date_str):
            return grok_format
    return None

def grok_parse_non_json(text):
    # Define regex patterns for different conditions
    word_pattern = r'\b[A-Za-z]+\b'
    num_pattern = r'\b\d+\b'
    alphanum_pattern = r'\b[A-Za-z0-9]+\b'
    
    # Split the text into tokens
    tokens = re.findall(r'\S+', text)  # Use regex to keep special characters
    parsed_result = []
    word_count = {}  # Track occurrences of each word
    date_found = False  # Track if date has been found

    for token in tokens:
        # Check if the token is part of a date and time
        if not date_found:
            # Check for date format
            date_grok = extract_date_format(token)
            if date_grok:
                parsed_result.append(date_grok)
                date_found = True  # Mark date as found
                continue  # Skip to the next token

        # Process other tokens after checking for a date
        if re.match(num_pattern, token):
            parsed_result.append(f"%{{number:num}}")
        elif re.match(alphanum_pattern, token) and any(char.isdigit() for char in token) and any(char.isalpha() for char in token):
            parsed_result.append(f"%{{notSpace:alphanumeric}}")  # Named notSpace as alphanumeric
        elif re.match(word_pattern, token):
            # Track occurrences of the word
            if token in word_count:
                word_count[token] += 1
                parsed_result.append(f"%{{word:{token}{word_count[token]}}}")
            else:
                word_count[token] = 1
                parsed_result.append(f"%{{word:{token}}}")
        else:
            # Keep special characters as they are
            parsed_result.append(token)

    return ' '.join(parsed_result)

# Example usage:
text = "The event is on 2024-06-24 11:22:59. my name is dinesh."

# Output:
first_output = grok_parse_non_json(text)

print("Output - Grok Parsing for All Words:")
print(first_output)
