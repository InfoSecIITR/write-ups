def remove_special_characters(input_list):
    # Define the set of characters to be removed
    special_characters = "',!;|()=+:><*&$@[\\]{}?/."

    # Create a translation table
    translation_table = str.maketrans('', '', special_characters)

    # Ensure input_list is a list
    if not isinstance(input_list, list):
        raise ValueError("Input must be a list of characters")

    # Convert the list of integers to a string and use translate to remove the specified characters
    input_string = ''.join(map(chr, input_list))
    result_string = input_string.translate(translation_table)

    return result_string

# Example usage:
with open('code.txt', 'rb') as key_file:
    key_list = list(key_file.read())

result = remove_special_characters(key_list)
print(result)
