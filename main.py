import sys
from stats import get_book_text, get_book_character_count,chars_dict_to_sorted_list


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <path_to_book>")
        sys.exit(1)

    path = sys.argv[1]
    print(f"""============ BOOKBOT ============ \nAnalyzing book found at {path}...""")
    print("----------- Word Count ----------")
    get_book_text(path)
    print("--------- Character Count -------")
    char_count = get_book_character_count(path)
    sorted_char_count_list = chars_dict_to_sorted_list(char_count)
    
    for value in sorted_char_count_list:
        print(f"{value[0]}: {value[1]}")

    print("============= END ===============")


main()

