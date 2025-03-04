import nltk
import sys
from nltk.tokenize import word_tokenize


TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP

NP -> Det N | Det Adj N | N | NP PP | Det N PP | Adj N | N P N | Det Adj Adj N
VP -> V | V NP | V PP | V NP PP | Adv V | Adv V NP | Adv V PP | V Adv | V Adv NP | V NP Adv
PP -> P NP

N -> N N
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = word_tokenize(sentence)   #用word tokenize进行分词（需要提前导入）
    words = [word.lower() for word in words]
    filtered_words = [word for word in words if any(char.isalpha() for char in word)]  #去除非字母的字符串
    return filtered_words



def is_np_tree(tree: nltk.Tree) -> bool:  #检查是否是 np树
    return tree.label() == "NP"


def is_np_chunk(tree: nltk.Tree) -> bool:  #返回是否是np块
    if not is_np_tree(tree):  #首先需要是np树
        return False

    for subtree in tree.subtrees(): #遍历np树的子树
        if tree == subtree:
            continue

        if is_np_tree(subtree): #如果子树有np树，则返回 false
            return False
    return True


def np_chunk(tree: nltk.Tree):
    np_chunks = [
        np_subtree
        for np_subtree in tree.subtrees(is_np_tree)  #遍历所有符合 np 树条件的子树
        if is_np_chunk(np_subtree)  #且这个子树应该是np块
    ]
    return np_chunks


if __name__ == "__main__":
    main()
