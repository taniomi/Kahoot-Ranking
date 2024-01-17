from unidecode import unidecode
import re

def clean_string(input_string):
    # Use a regular expression to remove spaces and numbers
    cleaned_string = re.sub(r'[\s\d]', '', input_string)

    # Remove accents using unidecode
    no_accents_string = unidecode(cleaned_string)

    # Convert the cleaned string to lowercase
    lowercased_string = no_accents_string.lower()

    return lowercased_string