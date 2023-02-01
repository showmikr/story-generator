
import random
import io

# master_dict stores the hashed data structure for the markov madel. Words are linked by nesting dictionaries.
# Ultimately, master_dict will have two nested dictionaries within an outer dictionary.
# The outer dictionary has first words as keys and dictionaries
# (representing the set of all second words that come after a given first word) as values.
# The second layer nested dictionary stores second words as keys and dictionaries (representing
# the set of all third words that come after a given first and second word) as values. The third layer nested dictionary
# contains third words as keys and a frequency of how often the whole three-word sequence appears in our text sample.
# This data structure was used because it can access elements in constant runtime which is far faster than the linear
# runtime access of linked lists. At the end of the day, it still properly represents each layer of the markov chain.

master_dict = {}


def remove_punctuations(string: str):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for x in string.lower():
        if x in punctuations:
            string = string.replace(x, "")
    return string


# Cleans up and processes a text for use in our data structure
# This method is specific to the AI assignment text files. You'll have to implement
# your own line processing function to clean up general text.
def get_processed_lines(text: str):
    file = io.StringIO(text)
    lines = []
    line = file.readline()
    while line:
        if line != '\n':
            if line.isupper():  # remove line if it's all uppercase b/c that indicates it's a chapter/title
                file.readline()  # skip next line b/c it's a chapter name
            else:
                line = remove_punctuations(line.strip().lower())
                lines.append(line)
        line = file.readline()
    lines.pop(0)  # removes author's name from list of lines
    return lines


# Takes a list of lines of text and converts it into a list of words
def get_word_list(lines: list):
    w_list = []
    for line in lines:
        words = line.split()
        w_list.extend(words)
    return w_list


# Takes a list of words (our text sample) and places them into a markov model data structure (i.e master_dict)
def fill_master_dict(list_of_words: list):
    master_dict.clear() # empty master_dict. This is for AWS lambda: if we're calling the same container again with new text, we want to make sure we're working with an empty master_dict
    for i in range(len(list_of_words) - 2):
        first_word = list_of_words[i]
        if first_word not in master_dict:
            master_dict[first_word] = {}
        second_word = list_of_words[i + 1]
        if second_word not in master_dict[first_word]:
            master_dict[first_word][second_word] = {}
        third_word = list_of_words[i + 2]
        if third_word not in master_dict[first_word][second_word]:
            master_dict[first_word][second_word][third_word] = 1
        else:
            master_dict[first_word][second_word][third_word] += 1


# Gets the most likely second word in a two word sequence given the first word
def get_second_word(first_word: str):
    # store second words mapped to how frequently they appear given the first word
    second_word_dict = {}
    for word in master_dict[first_word]:
        second_word_dict[word] = sum(master_dict[first_word][word].values())
    # grab the most frequent second word given the first word
    modal_second_word = max(second_word_dict, key=second_word_dict.get)
    return modal_second_word


# Gets the most likely third word in a three word sequence given the first and second word
def get_third_word(first_word: str, second_word: str):
    modal_third_word = max(master_dict[first_word][second_word], key=master_dict[first_word][second_word].get)
    return modal_third_word


# Generates a story from our markov model data structure (i.e master_dict)
# Keep in mind, this method prints to console - it doesn't return a generated story.
# If you want this method to return
def generate_story():
    story_sequence = list()

    # first_word_set's purpose: every third word is checked against this set to see if it
    # has been used as a first word. Essentially, if a third word has been used as a first word, it will
    # end up repeating a sequence of words of variable length over and over again. To prevent this repetition
    # the first_word_set is checked to see if we are about to repeat said sequence.
    first_word_set = set()

    first_word = random.choice(list(master_dict))

    for i in range(0, 500, 2):
        second_word = get_second_word(first_word)
        story_sequence.append(first_word)
        story_sequence.append(second_word)
        third_word = get_third_word(first_word, second_word)

        if third_word in first_word_set:    # Checks if we are about to repeat a sequence
            first_word_set.remove(third_word)  # Since we've prevented a repeat sequence, we can let the third word be reused as a first word, hence why it is freed from the set.
            if len(master_dict[first_word][second_word]) > 1:  # Try grabbing another possible relevant third word from the same two word sequence if there are more than one possible third words
                new_word = third_word
                while third_word == new_word:  # this is to make sure we don't randomly select the same word we want to replace
                    third_word = random.choice(list(master_dict[first_word][second_word]))
            else:  # if all else fails, just select a completely random word
                third_word = random.choice(list(master_dict))

        first_word = third_word  # Update the end of our three word sequence as the new first word

        if first_word not in master_dict:  # Handles an edge case where text file is less than 2000 words long. Just resets first word if text file is too short (< 2000 words i.e our for loop limit)
            first_word = random.choice(list(master_dict))
        first_word_set.add(first_word)  # Update our first_word_set to prevent repeating sequences

    return story_sequence # output story is a list of the sequence of words in the story


# Converts a story sequence into a giant string.
# You'll probably want to return this method's output for the AWS service
def stringify_story(story_sequence):
    separator = ' '
    return separator.join(story_sequence) # separator.join() simply converts our story sequence (list) into a giant string


# Pretty prints a story to console. By "pretty" print, I just mean that we're not printing one giant line.
def pretty_print_story(story_sequence):
    max_words_per_line = 20
    line_word_count = 0
    for i in range(0, 500, 2):
        print(story_sequence[i], story_sequence[i+1], end=" ")
        line_word_count += 2
        if line_word_count >= max_words_per_line:  # skip line once we print too many words in a single line
            print()
            line_word_count = 0
