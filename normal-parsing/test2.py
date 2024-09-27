import re

# Function to parse the entire string with individual word parsing (first output)
def grok_parse_non_json(text):
    # Define regex patterns for different conditions
    word_pattern = r'\b[A-Za-z]+\b'
    num_pattern = r'\b\d+\b'
    alphanum_pattern = r'\b[A-Za-z0-9]+\b'
    
    # Split the text into tokens
    tokens = text.split()

    # Build parsed result
    parsed_result = []
    for token in tokens:
        if re.match(num_pattern, token):
            parsed_result.append(f"%{{number:num}}")
        elif re.match(alphanum_pattern, token) and any(char.isdigit() for char in token) and any(char.isalpha() for char in token):
            parsed_result.append(f"%{{notSpace}}")
        elif re.match(word_pattern, token):
            parsed_result.append(f"%{{word:{token}}}")
        else:
            parsed_result.append(token)  # For punctuations or unknown formats

    return ' '.join(parsed_result)

# Function to handle comma-separated messages (second output)
def grok_parse_by_commas(text):
    # Split by commas to handle message breaks
    messages = [msg.strip() for msg in text.split(',')]

    parsed_messages = []
    for i, msg in enumerate(messages, 1):
        parsed_messages.append(f"%{{data:message{i}}}")
    
    # Join the parsed messages with commas
    return ', '.join(parsed_messages)

# Function to treat the entire string as one message (third output)
def grok_parse_single_message(text):
    return f"%{{data:message}}"

# Example usage:
text = "my name is dinesh , my age is 24 , my jersey name is din24 ."

# 1. First Output: Grok parsing for individual words
first_output = grok_parse_non_json(text)

# 2. Second Output: Parse each comma-separated segment as separate messages
second_output = grok_parse_by_commas(text)

# 3. Third Output: Treat entire text as one continuous message
third_output = grok_parse_single_message(text)

# Outputs:
print("1. First Output - Grok Parsing for All Words:")
print(first_output)
print("\n2. Second Output - Comma-Separated Messages Parsing:")
print(second_output)
print("\n3. Third Output - Single Message Parsing:")
print(third_output)
