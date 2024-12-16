import time

'''
Lost in Time

goal: there is one item in each location. find it and collect it to get back home
'''

class Node:
    def __init__(self, value, location, parent=None):
        self.value = value
        self.visited = False
        self.location = location
        self.left = None
        self.right = None
        self.parent = parent
        self.height = 1


class Game:
    def __init__(self):
        self.head = None

    def add(self, value, location):
        self.head = self.add_recurse(self.head, value, location)
        return self

    def add_recurse(self, current_node, value, location):

        if not current_node:
            return Node(value=value, location=location)

        # duplicate handling
        if value == current_node.value:
            return current_node

        if value < current_node.value:
            current_node.left = self.add_recurse(current_node.left, value, location)
            # current_node.left.parent = current_node
        else:
            current_node.right = self.add_recurse(current_node.right, value, location)
            # current_node.right.parent = current_node

        current_node.height = 1 + max(self.height_recurse(current_node.left),
                                      self.height_recurse(current_node.right))

        return self.balance(current_node)

    def remove(self, value):
        self.head = self.remove_recurse(self.head, value)
        return self

    def remove_recurse(self, current_node, value):

        if not current_node:
            return current_node

        if value < current_node.value:
            current_node.left = self.remove_recurse(current_node.left, value)
        elif value > current_node.value:
            current_node.right = self.remove_recurse(current_node.right, value)
        else:
            if not current_node.left:
                return current_node.right
            if not current_node.right:
                return current_node.left

            # Find smallest node in the left subtree
            smallest = self.helper(current_node.right)

            current_node.value = smallest.value
            current_node.right = self.remove_recurse(current_node.right, smallest.value)

        # Update height and re-balance
        current_node.height = 1 + max(self.height_recurse(current_node.left),
                                      self.height_recurse(current_node.right))
        return self.balance(current_node)

    def helper(self, node):  # goes thru tree to smallest node
        while node.left is not None:
            node = node.left
        return node

    """
    Return the height of the tree.
    """

    def height(self):
        return self.height_recurse(self.head)

    def height_recurse(self, current_node):
        if not current_node:
            return 0
        return current_node.height

    def balance_factor(self, current_node):
        if not current_node:
            return 0
        return self.height_recurse(current_node.right) - self.height_recurse(current_node.left)

    def rotate_left(self, imbalanced_node):

        right_child = imbalanced_node.right
        imbalanced_node.right = right_child.left

        if right_child.left:
            right_child.left.parent = imbalanced_node

        # update parents
        right_child.left = imbalanced_node
        right_child.parent = imbalanced_node.parent
        imbalanced_node.parent = right_child

        # Update heights
        imbalanced_node.height = 1 + max(self.height_recurse(imbalanced_node.left),
                                         self.height_recurse(imbalanced_node.right))
        right_child.height = 1 + max(self.height_recurse(right_child.left), self.height_recurse(right_child.right))

        return right_child

    def rotate_right(self, imbalanced_node):

        left_child = imbalanced_node.left
        imbalanced_node.left = left_child.right

        if left_child.right:
            left_child.right.parent = imbalanced_node

        # update parents
        left_child.right = imbalanced_node
        left_child.parent = imbalanced_node.parent
        imbalanced_node.parent = left_child

        # Update heights
        imbalanced_node.height = 1 + max(self.height_recurse(imbalanced_node.left),
                                         self.height_recurse(imbalanced_node.right))
        left_child.height = 1 + max(self.height_recurse(left_child.left), self.height_recurse(left_child.right))

        return left_child

    def balance(self, current_node):
        bf = self.balance_factor(current_node)

        # left rotation, right heavy
        if bf > 1:
            if self.balance_factor(current_node.right) < 0:  # right-left case
                # curr = current_node.left
                current_node.right = self.rotate_right(current_node.right)
            return self.rotate_left(current_node)  # rotate left

        # right rotation, left heavy
        if bf < -1:
            if self.balance_factor(current_node.left) > 0:  # left-right case
                # curr = current_node.right
                current_node.left = self.rotate_left(current_node.left)
            return self.rotate_right(current_node)  # rotate single right

        return current_node

    """
        True if the BST contains the given value, false otherwise.
        You will need to change the return statement
    """

    def contains(self, value):
        return self.contains_recursive(self.head, value)

    def contains_recursive(self, current_node, value):
        if current_node is None:
            return current_node
        if value == current_node.value:
            return current_node
        elif value < current_node.value:
            return self.contains_recursive(current_node.left, value)
        else:
            return self.contains_recursive(current_node.right, value)

    def make_head(self, value):
        node = self.contains(value)
        if not node:
            return self  # Node doesn't exist, return unchanged tree

        all_nodes = self.as_list() # Extract all elements from the tree
        self.head = None # Remove the original tree

        # Rebuild the tree, starting with the desired head
        all_nodes.sort()  # Ensure nodes are sorted (if not already)
        all_nodes.remove((node.value, node.location))
        self.head = self.add(node.value, node.location)

        # Re-add the rest of the nodes
        for value, location in all_nodes:
            self.add(value, location)

        return self

    def find_location_NS_by_action(self, current_node, action):
        if action.lower() == "north" and current_node.left:
            return current_node.left
        elif action.lower() == "south" and current_node.right:
            return current_node.right
        return None

    def find_location_EW_by_action(self, current_node, action):
        if action.lower() == "west" and current_node.left:
            return current_node.left
        elif action.lower() == "east" and current_node.right:
            return current_node.right
        return None

    """
    Return the BST as a list.
    """

    def as_list(self):
        final_list = []
        self.as_list_recursive(self.head, final_list)
        return final_list

    def as_list_recursive(self, current_node, final_list):
        if current_node is not None:
            # in-order traversal
            self.as_list_recursive(current_node.left, final_list)
            final_list.append(current_node.value)
            self.as_list_recursive(current_node.right, final_list)



def intro(name):
    print(f"\nWelcome to Lost in Time, {name}\nActions: north, south, east, west, quit\n{'-' * 30}"
          f"\nYou are walking home from school only to stumble upon a strange device."
          f"\nYou pick it up, wipe the mud off, and to your surprise you find the words "
          f"\n\'Time Traveling Machine\' etched on."
          f"\nYou walk inside your house but slip on your dog\'s wet puddle from the rain"
          f"\nand the device goes flying out of your hand."
          f"\nWhen you go to pick it up, your thumb accidentally presses a button labeled \'Rome\'"
          f"\nSuddenly, your surroundings start spinning and everything goes dark...")

    #time.sleep(10)
    #for i in range(5):
        #print(f"{'***'}")
        #time.sleep(1)


def egypt_intro(name): # at a pharaoh's palace
    print(f'1500 BC - EGYPT'
          f'\n{'-' * 10}'
          f'\nYou wake up confused, hot, and thirsty.'
          f'\n"Where am I?" you mutter to yourself. '
          f'\nA Pharaoh dressed in a wraparound white linen robe with gold jewelry approaches you'
          f'\n"Welcome to Egypt! I hope you had a safe travel, {name}."'
          f'\nWhile I would accommodate you in my kingdom. I have no room currently.'
          f'\nI suggest you head East for some water first.')
    #time.sleep(5)


def rome_intro(name): # with Leonardo da Vinci
    print(f'YEAR 1503 - ROME'
          f'\n{'-' * 10}'
          f'\n"Benvenuto!"'
          f'\nYou look around to see someone painting the Mona Lisa.'
          f'\n"SHHHH...I\'m working on a piece be quiet. Now that you\'re up, '
          f'\ngo north and bring my brush from the Basilica.')
    #time.sleep(5)


def giza():

    print(f'\nWelcome to the Great Pyramids of Giza!'
          f'\nYou enter the base of the pyramid and the door shuts behind you.'
          f'\nA man appears. . . "Answer this correct and I will let you out')

    tries = 0
    answer = 'Leonardo da Vinci'
    response = input("Who painted the Mona Lisa? ")
    a = True

    while response != answer:
        if tries > 4:
            print("\nHINT: It\'s 3 words")
        elif tries > 7:
            print("\nHINT: L.. d.. V..")
        elif tries > 15:
            a=False
            break
        response = input("\n>> ").strip()
        tries+=1

    return a

def nile():
    print('\nWelcome to the Nile River!'
          '\nQuick, you are thirsty. Answer this riddle before it\'s too late!!')
    tries = 0
    answers = ['X','x','ten','Ten','10']
    a = True

    response = input("What number can be written in both Roman numerals and Arabic numerals and still be the same? ")

    while response not in answers:
        if tries > 4:
            print("\nHINT: It\'s a number")
        elif tries > 7:
            print("\nHINT: It\'s below 15")
        if tries > 10:
            a = False
            break
        response = input("\n>> ").strip()
        tries += 1

    return a

def cleo():
    print('\nCleopatra\'s Tomb. . .'
          '\nYou hear movement in the darkness ahead. '
          '\nDo you want to check it out? (y/n) ')

    a = False
    while not a:
        if input() == 'y':
            for i in range(5):
                print(f"{'***'}")
                time.sleep(1)
            print('\n\nLuckily it\'s only Tivali, Cleopatra\'s cat. '
                  '\nAround her neck is a rolled paper. You take it.'
                  '\nIt reads:'
                  '\n\t\tThe only way to escape is to gather everything.')
            a=True
        elif input() == 'n':
            print('Suddenly you feel the tile beneath your feet begins to shake...')

            break
        else:
            print('\nInvalid answer. Try Again\n>>')

    return a

def basilica():
    print('\nYou walk into the Basilica di San Pietro and find the pen.'
          '\nWould you like to get it? (y/n) ')
    a = False
    while not a:
        if input().lower() == 'y':
            print('\nYou put it in your pocket and head back to the painter.')
            a=True
        elif input().lower() == 'n':
            print('\n\nYou continue to walk through the Basilica and return back'
                  '\nto the painter without the pen.')
        else:
            print('\nInvalid answer. Try again\n>>')
    return a

def no_pen():
    answer='siren'
    response=''
    tries = 0
    a=True
    print("\nWhat is the name of the mythical creature known to lure sailors to their death"
        "\nby singing enchanting songs? ")
    while response != answer:
        if tries > 4:
            print("\nHINT: They are 1/2 woman and 1/2 bird")
        elif tries > 7:
            print("\nGood luck. . .")
            a = False
            break
        response = input('\n>> ').strip()
        tries += 1
    return a

def catacombs():
    print("\nYou hear angelic singing come from behind you."
          "\nDo you want to check it out? (y/n) ")
    a = False
    while not a:
        if input().lower() == 'y':
            print('\nYou slowly turn back and the singing gets louder. . .')
            break
        elif input().lower() == 'n':
            print('\nYou continue forward with the singing fading in the distance.')
            a=True
        else:
            print('\nInvalid answer. Try again\n>>')
    return a


def get_action():
    choice = input('\n\nWhere would you like to go? ').strip()
    choice = choice.lower()
    return choice


def end():
    print('\nThanks for playing Lost in Time!\n')
    exit()


def print_tree(node, level=0):
    if node:
        print(" " * (level * 4) + f"Node: {node.value}, Location: {node.location}")
        if node.left:
            print(" " * (level * 4) + f"  Left: {node.left.value}")
        else:
            print(" " * (level * 4) + "  Left: None")
        if node.right:
            print(" " * (level * 4) + f"  Right: {node.right.value}")
        else:
            print(" " * (level * 4) + "  Right: None")

        # Recursively print children
        print_tree(node.left, level + 1)
        print_tree(node.right, level + 1)


def main():

    try:
        # player actions
        directions = ['north', 'south', 'east', 'west', 'quit']
        places = {

            # Home - 2024
            'Home': {'North': 'Egypt', 'South': 'Hyper Train Station', 'West': 'Rome, Italy'},

            # Egypt - 1500 BC
            'Egypt': {'North': 'Pyramid of Giza', 'East': 'Nile River', 'West': 'Cleopatra\'s Tomb'},

            #Cleopatra's Tomb (Egypt)
            #'Cleopatra\'s Tomb': {'Item': 'Ancient Hieroglyph'},

            # Rome, Italy - 1800
            'Rome': {'North': 'Basilica di San Pietro', 'South': 'Catacombs'},


            # Hyper Train Station - 3000
            'Hypertrain Station': {'South': 'Underwater Research Colony', 'East': 'Virtual City of Oma',
                                   'West': 'Floating City of Ha'}

        }

        # player places visited inventory, can only visit a place once
        #inventory = {'Home': False, 'Egypt': False, 'Pyramid of Giza': False, 'Nile River':False,'Cleopatra\'s Tomb':False,'Rome':False,'Basilica di San Pietro':False,
                     #'Catacombs':False,'Underwater Research Colony':False,'Virtual City of Oma':False,'Floating City of Ha':False}

        player_name = input("What is your name? ").strip()

        mainTree = Game()
        mainTree.add(value=50, location='Home')
        mainTree.add(value=30, location='Rome')
        mainTree.add(value=70, location='Egypt')
        mainTree.add(value=80, location='HyperTrain Station')  # after these 4 are added, Rome is at the top of AVl balanced tree
        #print(mainTree.as_list())

        # starting location - Home
        current_location = mainTree.head
        intro(player_name) # show game intro

        print_tree(current_location)
        print(f'\nTEST {current_location.location}\n')

        rome_intro(player_name) # game starts in Rome
        mainTree.make_head(30) # makes Rome head (
        current_location = mainTree.find_location_NS_by_action(current_location,'north')

        print(f'\nTEST {current_location.head.location}\n')

        #print_tree(current_location)

        while True:  # game loop

            #location_node = mainTree.contains_recursive(mainTree.head, )
            #if location_node:
                #current_location = location_node.location
                #print(f"\nYou are now in {current_location}.\n{'-'*20}")

            action = get_action()
            print(f'\nTEST {action.capitalize()}')

            if action in directions:
                if action.capitalize() == 'Quit':
                    end()
                if action.capitalize() in places[current_location]:
                    temp_current_location = places[current_location][action.capitalize()]
                    print(current_location)
                    print(temp_current_location)
                    #mainTree.make_head(20)
                    if current_location == 'Egypt':
                        #inventory[current_location] = True
                        egypt_intro(player_name)
                        match action:
                            case 'north':  # pyramid of Giza
                                temp_current_location = 'Pyramid of Giza'
                                if giza():
                                    print('\nYou got it! You\'re back at the palace.')
                                    #inventory[temp_current_location] = True
                                else:
                                    print('\nToo bad you got trapped. Maybe next time!')
                                    end()

                            case 'east':  # Nile River
                                temp_current_location = 'Nile River'
                                if nile():
                                    print('\nYou got it!  You\'re back at the palace.')
                                    #inventory[temp_current_location] = True
                                else:
                                    print('\nToo bad you died of thirst. Maybe next time!')
                                    end()

                            case 'west':  # Celopatra's Tomb
                                temp_current_location = 'Cleopatra\'s Tomb'
                                if cleo():
                                    print('\nYou got it! You\'re back at the palace.')
                                    #inventory[temp_current_location] = True
                                else:
                                    print('\nToo bad you fall in a death trap. Maybe next time!')
                                    end()

                    elif current_location == 'Rome':

                        match action:
                            case 'north':  # basilica di san pietro
                                temp_current_location = 'Basilica di San Pietro'
                                if basilica():
                                    print('\nThe painter thanks you for retrieving his pen.'
                                          '\nAs a parting gift, he gives you a piece of advice:'
                                          '\n\t"There is a rumor that there is a secret passage through the catacombs.'
                                          '\n\tBut beware, the sirens are not to be trusted."')
                                    #inventory[temp_current_location] = True

                                else:
                                    if no_pen():
                                        print("\nNice! You are back with the painter now.")
                                    else:
                                        print('\nYou are back with the painter now.')
                                        # continues but doesn't get info ab sirens

                            case 'south':  # catacombs
                                temp_current_location = 'Catacombs'
                                #inventory[temp_current_location] = True
                                if catacombs():
                                    pass
                                else:
                                    print("\nYou fell for the sirens trap. Better luck next time.")
                                    end()


                    elif current_location == 'Home':
                        #inventory[current_location] = True
                        match action:
                            case 'north':  # Egypt
                                current_location = 'Egypt'

                            case 'south':  # hypertrain station
                                current_location = 'HyperTrain Station'

                            case 'east':
                                current_location = 'Home'

                            case 'west':  # Rome
                                current_location = 'Rome'

                    elif current_location == 'HyperTrain Station':
                        #inventory[current_location] = True
                        match action:
                            case 'north':  # home
                                current_location = 'Home'

                            case 'south':  # underwater research colony
                                current_location = 'Underwater Research Colony'

                            case 'east':  # virtual city of Oma
                                current_location = 'Virtual City of Oma'

                            case 'west':  # floating city of Ha
                                current_location = 'Floating City of Ha'


                else:
                    print("\n\nYou can\'t go that way.")

            else:
                print("\n\nInvalid choice. Try again.")
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Exiting...")
        end()
    except Exception as e:
        print(f"ERROR: {e}")
        end()


if __name__ == '__main__':
    main()

    # TODO
    # change all quotes to be double (consistency)