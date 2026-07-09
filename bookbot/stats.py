def get_book_text(path: string):
    with open(path) as f:
        # do something wiht f (the file) here
        file_content = f.read()
        split_words = file_content.split()
        num_words = len(split_words)
        print(f"Found {len(split_words)} total words")

def get_book_character_count(path: string) -> dict[str, int]:
    with open(path) as f:
        file_content = f.read()
        char_count_dict = {}

        for char in file_content:
            lowercase_char = char.lower()
            if lowercase_char in char_count_dict:
                char_count_dict[lowercase_char] += 1
            else:
                char_count_dict[lowercase_char] = 1

        return char_count_dict

def sort_on(vehicle: tuple[str,int]) -> int:
    return vehicle[1]


def chars_dict_to_sorted_list(char_dict: dict[str, int]) -> list[tuple[str,int]]:
    m_list = [] 

    for key, value in char_dict.items():
        if key.isalpha():
            m_list.append((key, value))

    sorted_list = sorted(m_list, reverse=True, key=sort_on)

    return sorted_list
