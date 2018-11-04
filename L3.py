#Jebel Macias
#  11/4/2018
#Lab 3 option(B)
import time

#Used to construct AVL Trees
class AVLNode:
    def __init__(self, word):
        self.word = word
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0

    #Determines current node balance factor
    def get_balance(self):
        left_height = -1

        #If height is not none, get current height of left subtree
        if self.left is not None:
            left_height = self.left.height

        right_height = -1

        #If height is not none, get current height of right subtree
        if self.right is not None:
            right_height = self.right.height

        #current balance factor
        return left_height - right_height

    #Recalculates height, executed after tree has been modified
    def update_height(self):
        left_height = -1
        if self.left is not None:
            left_height = self.left.height

        right_height = -1
        if self.right is not None:
            right_height = self.right.height

        #Assign height to the greatest node depth
        self.height = max(left_height, right_height) + 1

    #Assigns new child to either a right or left subtree
    #return false if child is not inserted, true otherwise
    def set_child(self, which_child, child):
        if which_child != "left" and which_child != "right":
            return False

        #Right or left subtree
        if which_child == "left":
            self.left = child
        else:
            self.right = child
        if child is not None:
            child.parent = self
        self.update_height()
        return True

    #Assings new child to the old child, returns False
    #if child is not inserted
    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)
        return False

#AVL balanced binary search tree
class AVLTree:
    def __init__(self):
        self.root = None

    #Left rotation on node, returns new root
    def rotate_left(self, node):

        #Changes pointer according to rotation
        right_left_child = node.right.left

        if node.parent is not None:
            node.parent.replace_child(node, node.right)
        else:
            self.root = node.right
            self.root.parent = None

        node.right.set_child('left', node)
        node.set_child('right', right_left_child)
        return node.parent

    #Right rotation on node, returns new root
    def rotate_right(self, node):

        #Changes pointer according to rotation
        left_right_child = node.left.right
        if node.parent is not None:
            node.parent.replace_child(node, node.left)
        else:
            self.root = node.left
            self.root.parent = None
        node.left.set_child('right', node)
        node.set_child('left', left_right_child)
        return node.parent

    #Used to perform rotations as necessary.
    #Update tree height. Returns new root
    def rebalance(self, node):
        node.update_height()
        if node.get_balance() == -2:
            if node.right.get_balance() == 1:
                self.rotate_right(node.right)
            return self.rotate_left(node)

        elif node.get_balance() == 2:
            if node.left.get_balance() == -1:
                self.rotate_left(node.left)
            return self.rotate_right(node)
        return node

    #Used to insert new nodes into tree
    def insert(self, node):

        #Set root to node, if root is empty
        if self.root is None:
            self.root = node
            node.parent = None
        else:

            #Regular binary search
            current_node = self.root
            while current_node is not None:
                if node.word.lower() < current_node.word.lower():
                    if current_node.left is None:
                        current_node.left = node
                        node.parent = current_node
                        current_node = None
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.right = node
                        node.parent = current_node
                        current_node = None
                    else:
                        current_node = current_node.right

            #To maintain a BBST, rebalance tree
            node = node.parent
            while node is not None:
                self.rebalance(node)
                node = node.parent

    #Used to find given word, in a tree
    #Returns node if word is found in tree
    def search(self, word):
        current_node = self.root
        while current_node is not None:
            if current_node.word.lower() == word.lower():
                return current_node
            elif current_node.word.lower() < word.lower():
                current_node = current_node.right
            else:
                current_node = current_node.left

    #The method read_from_dictionary, populates a
    #avltree by taking words from each line the file
    #given
    def read_from_dictionary(self, file_name):
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    self.insert(AVLNode(line.split()[0]))
        except Exception as e:
            print("Failed to load file " + file_name + " in method readFromFile, in class AVLtree")
            return
        return

# Node used to construct Red and black trees
class RBTNode:
    def __init__(self, word, parent, is_red = False, left = None, right = None, mark = None):
        self.word = word
        self.left = left
        self.right = right
        self.parent = parent
        self.mark = None

        if is_red:
            self.color = "red"
        else:
            self.color = "black"

    #Checks if right and left subtree are black, returns
    #false otherwise.
    def are_both_children_black(self):
        if self.left != None and self.left.is_red():
            return False
        if self.right != None and self.right.is_red():
            return False
        return True

    def count(self):
        count = 1
        if self.left != None:
            count = count + self.left.count()
        if self.right != None:
            count = count + self.right.count()
        return count

    def get_grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    def get_predecessor(self):
        node = self.left
        while node.right is not None:
            node = node.right
        return node

    def get_sibling(self):
        if self.parent is not None:
            if self is self.parent.left:
                return self.parent.right
            return self.parent.left
        return None

    def get_uncle(self):
        grandparent = self.get_grandparent()
        if grandparent is None:
            return None
        if grandparent.left is self.parent:
            return grandparent.right
        return grandparent.left

    def is_black(self):
        return self.color == "black"

    def is_red(self):
        return self.color == "red"

    #Replaces old child with new child.
    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)
        return False

    #Sets new child, returns false if unable to insert child
    def set_child(self, which_child, child):
        if which_child != "left" and which_child != "right":
            return False

        if which_child == "left":
            self.left = child
        else:
            self.right = child

        if child != None:
            child.parent = self

        return True

#Red and black trees
class RBTree:
    def __init__(self):
        self.root = None

    def __len__(self):
        if self.root is None:
            return 0
        return self.root.count()

    #Constructs new node to be inserted into the tree
    def insert(self, word):
        new_node = RBTNode(word, None, True, None, None)
        self.insert_node(new_node)

    #Inserts new node into the tree
    def insert_node(self, node):

        #Sets node to root, if root is empty
        if self.root is None:
            self.root = node
        else:

            #Regular Binary Search
            current_node = self.root
            while current_node is not None:
                if node.word.lower() < current_node.word.lower():
                    if current_node.left is None:
                        current_node.set_child("left", node)
                        break
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.set_child("right", node)
                        break
                    else:
                        current_node = current_node.right
        node.color = "red"
        self.insertion_balance(node)

    #Balances heigh factor of the red and black tree
    #after an insertion
    def insertion_balance(self, node):
        if node.parent is None:
            node.color = "black"
            return

        if node.parent.is_black():
            return
        parent = node.parent
        grandparent = node.get_grandparent()
        uncle = node.get_uncle()

        if uncle is not None and uncle.is_red():
            parent.color = uncle.color = "black"
            grandparent.color = "red"
            self.insertion_balance(grandparent)
            return

        #Left rotation
        if node is parent.right and parent is grandparent.left:
            self.rotate_left(parent)
            node = parent
            parent = node.parent

        #Right rotation
        elif node is parent.left and parent is grandparent.right:
            self.rotate_right(parent)
            node = parent
            parent = node.parent

        parent.color = "black"
        grandparent.color = "red"

        if node is parent.left:
            self.rotate_right(grandparent)
        else:
            self.rotate_left(grandparent)

    #Performs a left rotation on the node
    def rotate_left(self, node):
        right_left_child = node.right.left
        if node.parent != None:
            node.parent.replace_child(node, node.right)
        else:
            self.root = node.right
            self.root.parent = None
        node.right.set_child("left", node)
        node.set_child("right", right_left_child)

    #Performs a right rotation on the node
    def rotate_right(self, node):
        left_right_child = node.left.right
        if node.parent != None:
            node.parent.replace_child(node, node.left)
        else:
            self.root = node.left
            self.root.parent = None
        node.left.set_child("right", node)
        node.set_child("left", left_right_child)

    #Takes a given word and checks if the gicen word
    #is in the tree.
    def search(self, word):
        current_node = self.root
        while current_node is not None:
            if current_node.word.lower() == word.lower():
                return current_node

            elif word.lower() < current_node.word.lower():
                current_node = current_node.left
            else:
                current_node = current_node.right
        return None

    #The method read_from_dictionary, populates a
    #rbtree by taking words from each line the file
    #given
    def read_from_dictionary(self, file_name):
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    self.insert(line.split()[0]) # Ignore whitespace
        except Exception as e:
            print("Failed to load file " + file_name + " in method readFromFile, in class RedBlackTree.")
            return
        return

#The function print_Anagrams determines
#if a word is in the binary search tree
def print_anagrams(dict, count, word, prefix=""):
    if len(word) <= 1:
        str = prefix + word

        #If in tree, print string, and append to counter
        if dict.search(str) != None:
            print(str)
            count.append(str)
    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i] # letters before cur
            after = word[i + 1:] # letters after cur

            if cur not in before:
                print_anagrams(dict, count, before + after, prefix + cur)

def max_in_list(list):
    """The funcion max_in_list is used to
    determine the word in any given list
    with the greatest number of anagrams
    The run time of this function is O(n)
    """

    max = list[0] # Takes first item to avoid none error below
    for i in range(1, len(list)):
        if int(list[i].split()[0]) > int(max.split()[0]):
            max = list[i]
    return max

def read_from_file(file_name, dict):
    """The fucntion read_from_file takes any given
    file containing a list of words, and determines
    how many anagarams each word has.
    """

    try:
        most_anagrams = []
        with open(file_name, 'r') as file:
            for line in file:
                count = [] # Stores word and count of angrams
                word = line.split()[0]
                print("---Anagrams for " + word.upper() + "---")
                print_anagrams(dict, count, word)
                most_anagrams.append(str(len(count)) + " " + word) # Appends words, and amount of anagrams
                print("Total Anagrams: " + str(len(count)) +"\n")
        max = max_in_list(most_anagrams) # Which word contains the most anagrams
        print("The word with the most anagrams:" + max.split()[1])
    except Exception as e:
        print("Failed to load file " + file_name + " in read_From_File.")
        return
    return


def begin():
    again = True
    while again:
        dict_name = input("What is the name of the file containing the list of english words?\n") # File containing englishword
        file_name = input("What is the name of the file containing the list of words you want to check for anagrams?\n") # File containing word used to check for anagrams
        balanced_tree = input("Which tree do you want to use to store the list of english words? RBT(Red-Black tree), or AVL\n")

        english_words = None
        if balanced_tree.lower() == "avl":
            english_words = AVLTree()
        else:
            english_words = RBTree()

        english_words.read_from_dictionary(dict_name)
        read_from_file(file_name, english_words)

        again = True if input("Would you like to try a different list of words? Type y or n: ") == "y" else False

begin()
