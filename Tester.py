from Markov import *

# Make sure to include the text files you want to read inside the same directory as this code


if __name__ == '__main__':
    text_file = 'houn.txt'  # Feel free to change the filename to test different text samples
    processed_lines = get_processed_lines(text_file)
    word_list = get_word_list(processed_lines)
    fill_master_dict(word_list)
    story_sequence = generate_story()    # prints out a 2000-word story based on the text sample provided
    print("STORY DUPLICATE")
    pretty_print_story(story_sequence)
