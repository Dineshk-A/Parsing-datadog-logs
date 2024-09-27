import re

def grok_parse_non_json(text):
    # Define regex patterns for words, numbers, and alphanumeric (no spaces)
    word_pattern = r'\b[A-Za-z]+\b'
    num_pattern = r'\b\d+\b'
    alphanumeric_pattern = r'\b[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\b'

    # Mappings for log levels and environments
    log_level_words = ['info', 'information']
    env_words = ['prod', 'production', 'stage', 'staging', 'dev', 'development']

    # Function to escape special characters like [] and {}
    def escape_special_chars(token):
        special_chars = r'([\[\]\{\}])'  # Escaping only brackets and braces for now
        return re.sub(special_chars, r'\\\g<1>', token)  # Add backslash before special chars

    # Function to check if token matches any log level
    def is_log_level(token):
        return token.lower() in log_level_words

    # Function to check if token matches any environment
    def is_environment(token):
        return token.lower() in env_words

    # Split the text into tokens, keeping spaces and special characters
    tokens = re.split(r'(\s+|[\[\]\{\}:,])', text)

    # Build parsed result
    parsed_result = []
    word_count = 1  # Counter for numbering generic word tokens
    num_count = 1   # Counter for numbering generic number tokens

    for token in tokens:
        # Escape special characters first
        escaped_token = escape_special_chars(token)

        # Now check for specific mappings first
        if is_log_level(token):
            parsed_result.append(f"%{{word:LogLevel}}")
        elif is_environment(token):
            parsed_result.append(f"%{{word:Environment}}")
        # Check for numbers, words, and alphanumeric patterns
        elif re.match(num_pattern, token):
            parsed_result.append(f"%{{number:num{num_count}}}")  # Use numX format
            num_count += 1  # Increment counter for next number
        elif re.match(word_pattern, token):
            # This is where we fix the generic word pattern to use "word" with a number
            parsed_result.append(f"%{{word:word{word_count}}}")
            word_count += 1  # Increment counter for next word
        elif re.match(alphanumeric_pattern, token):
            parsed_result.append(f"%{{notspace:alphanumeric}}")
        else:
            # If no pattern matches, just use the escaped version
            parsed_result.append(escaped_token)

    return ''.join(parsed_result)

# Example usage
text = 'my env is : [info] , {log level} is INFO , dev server running 27 33. asdre4-sukagd'
parsed_text = grok_parse_non_json(text)
print(parsed_text)
