class Node:
    def __init__(self,value, location, parent =None):
        self.value = value
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

        def remove(self, value, location):
            self.head = self.remove_recurse(self.head, value, location)
            return self

        def remove_recurse(self, current_node, value, location):

            if not current_node:
                return current_node

            if value < current_node.value:
                current_node.left = self.remove_recurse(current_node.left, value, location)
            elif value > current_node.value:
                current_node.right = self.remove_recurse(current_node.right, value, location)
            else:
                if not current_node.left:
                    return current_node.right
                if not current_node.right:
                    return current_node.left

                # Find smallest node in the left subtree
                smallest = self.helper(current_node.right)

                current_node.value = smallest.value
                current_node.right = self.remove_recurse(current_node.right, smallest.value, location)

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
                return False
            if value == current_node.value:
                return True
            elif value < current_node.value:
                return self.contains_recursive(current_node.left, value)
            else:
                return self.contains_recursive(current_node.right, value)

        """
        Return the number of values in the BST.
        You will need to change the return statement.
        

        def size(self):
            return self.size_recursive(self.head)

        def size_recursive(self, current_node):
            if current_node is None:
                return 0
            return 1 + self.size_recursive(current_node.left) + self.size_recursive(current_node.right)
        """
        """
        Return the BST as a list.
        

        def as_list(self):
            final_list = []
            self.as_list_recursive(self.head, final_list)
            return final_list

        def as_list_recursive(self, current_node, final_list):
            if current_node is not None:
                # pre-order traversal
                final_list.append(current_node.value)
                self.as_list_recursive(current_node.left, final_list)
                self.as_list_recursive(current_node.right, final_list)
        """

def intro(name):

    print(f"\nWelcome to Lost in Time, {name}\nActions: north, south, east, west, quit\n{'-'*30}"
          f"\nYou are walking home from school only to stumble upon a strange device."
          f"\nYou pick it up, wipe the mud off, and to your surprise you find the words "
          f"\n\'Time Traveling Machine\' etched on."
          f"\nYou walk inside your house but slip on your dog\'s wet puddle from the rain"
          f"\nand the device goes flying out of your hand."
          f"\nWhen you go to pick it up, your thumb accidentally presses a button labeled \'Rome (west)\'"
          f"\nSuddenly, your surroundings start spinning and everything goes dark...")

def rome_intro(name):
    print(f'1500 BC - ROME'
          f'\nYou wake up confused, hot, and thirsty.'
          f'\n"Where am I?" you mutter to yourself. '
          f'\nA Pharaoh dressed in a wraparound white linen robe with gold jewelry approaches you'
          f'\n"Welcome to Egypt! I hope you had a safe travel, {name}.'
          f'\nWhile I would accommodate you in my kingdom. I have no room currently.'
          f'\nI suggest you head East for some water first.')

def get_action():
    choice = input('Where would you like to go? ').strip().lower().capitalize()
    return choice

def end():
    print('Thanks for playing Lost in Time!')
    exit()


def main():

    # player actions
    directions = ['north', 'south', 'east', 'west', 'quit']
    places = {

        # Home - 2024
        'Home': {'North': 'Egypt', 'South': 'Hyper Train Station', 'West': 'Rome, Italy' },

        # Egypt - 1500 BC
        'Egypt': {'North':'Pyramid of Giza', 'South':'Home', 'East':'Nile River','West':'Cleopatra\'s Tomb'},

        # Rome, Italy - 1800
        'Rome' : {'North':'Basilica di San Pietro', 'South':'Catacombs', 'East':'Home'},

        # Hyper Train Station - 3000
        'Hypertrain Station' : {'North':'Home', 'South':'Underwater Research Colony', 'East':'Virtual City of Oma','West':'Floating City of Ha'}

                }

    # player inventory
    inventory = []

    player_name = input("What is your name? ").strip()

    intro(player_name)

    place = Game()
    place.add(value=10, location='Rome')
    place.add(value=20, location='Egypt')
    place.add(value=30, location='Rome')
    place.add(value=40, location='HyperTrain Station') # after these 4 are added, Rome is at the top of AVl balanced tree ( home is on left)

    # starting location
    current_location = game.get_current_location
    rome_intro(player_name) # game starts in Rome

    while True: # game loop

        action = get_action()

        if action in directions:
            if action == 'Quit':
                end()
            if action in places[current_location]:
                current_location = places[current_location][action]
                if current_location == 'Egypt':
                    match action:
                        case 'north': #pyramid of Giza
                            current_location = 'Pyramid of Giza'
                        case 'south': #Home
                            current_location = 'Home'

                        case 'east': #Nile River
                            current_location = 'Nile River'

                        case 'west': #Celopatra's Tomb
                            current_location = 'Cleopatra\'s Tomb'


                elif current_location == 'Rome':
                    match action:
                        case 'north': #basilica di san pietro
                            current_location = 'Basilica di San Pietro'

                        case 'south': #catacombs
                            current_location = 'Catacombs'

                        case 'east': #Home
                            current_location = 'Home'

                elif current_location == 'Home':
                    match action:
                        case 'north': # Egypt
                            current_location = 'Egypt'

                        case 'south': # hypertrain station
                            current_location = 'HyperTrain Station'

                        case 'east':
                            current_location = 'Home'

                        case 'west': # Rome
                            current_location = 'Rome'

                elif current_location == 'HyperTrain Station':
                    match action:
                        case 'north': #home
                            current_location = 'Home'

                        case 'south': #underwater research colony
                            current_location = 'Underwater Research Colony'

                        case 'east': #virtual city of Oma
                            current_location = 'Virtual City of Oma'

                        case 'west': #floating city of Ha
                            current_location = 'Floating City of Ha'


            else:
                print("You can\'t go that way.")

        else:
            print("Invalid choice. Try again.")


if __name__ == '__main__':
    main()

    # TODO
    # change all quotes to be double (consistency)