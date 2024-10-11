from anytree import Node, RenderTree
from collections import defaultdict, Counter
# Function to add a word to the tree
def add_word(root, word):
    current_node = root
    for letter in word:
        # Check if a child with this letter already exists
        child_node = next((child for child in current_node.children if child.name == letter), None)
        if not child_node:
            child_node = Node(letter, parent=current_node)
        current_node = child_node
    # Mark the end of the word
    Node(word, parent=current_node)

# Function to read words from a file and build the tree
def build_tree_from_file(file_path):
    root = Node("root")
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()
            add_word(root, word)
    return root

# Function to display the tree
def display_tree(root):
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))

def tree_search(node, a, b, c, d):
    words = []
    for child in node.children:
        if (len(child.name) > 1):
            words = words + [child.name]
        if (child.name in a):
            words = words + tree_search(child, b, c, d, a)
        if (child.name in b):
            words = words + tree_search(child, c, d, a, b)
        if (child.name in c):
            words = words + tree_search(child, b, d, a, c)

    return words

def find_words(node, a, b, c, d):
    words = []
    for child in node.children:
        if (child.name in a):
            words = words + tree_search(child, b, c, d, a)
        if (child.name in b):
            words = words + tree_search(child, c, d, a, b)
        if (child.name in c):
            words = words + tree_search(child, b, d, a, c)
        if (child.name in d):
            words = words + tree_search(child, b, c, a, d)
    
    return [ word for word in words if len(word) >= 3 ]

def find_combos(word_list, letters):
    # Create a dictionary where keys are first letters and values are lists of words
    first_letter_dict = defaultdict(list)
    for w in word_list:
        if w:
            first_letter_dict[w[0]].append(w)
    
    results = []
    letters_set = set(letters)

    def search(sentence, depth, used_letters):
        if len(used_letters) == len(letters_set):
            results.append(sentence)
            return

        if depth <= 0:
            return
        
        last_letter = sentence[-1]
        if last_letter in first_letter_dict:
            for w in first_letter_dict[last_letter]:
                new_used_letters = used_letters | set(w)
                if len(new_used_letters) <= len(letters_set):
                    search(sentence + " " + w, depth - 1, new_used_letters)
        
    # Initialize search with each word in the word_list
    for w in word_list:
        search(w, max_itterations - 1, set(w))
    
    return results

max_itterations = 4
# Main function
if __name__ == "__main__":
    top = ['b', 'w', 'h']
    right = ['v', 'c', 'm']
    bottom = ['e', 'l', 'a']
    left = ['r', 'o', 'n']
    file_path = "1000-most-common-words.txt"  
    #file_path = "google-10000-english.txt"  
    #file_path = "Oxford 5000.txt"  
    root = build_tree_from_file(file_path)
    print("Tree built")
    words = find_words(root, top, right, bottom, left)
    print("Words found:")
    print(words)
    set = find_combos(words, top + right + bottom + left)
    print("Output:")
    print(set)