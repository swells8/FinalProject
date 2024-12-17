import re

'''
references: 
for text color change: https://www.geeksforgeeks.org/print-colors-python-terminal/
'''

class Node:
    def __init__(self,value, details, time_of_day, parent =None):
        self.value = value
        self.details = details
        self.time_of_day = time_of_day
        self.left = None
        self.right = None
        self.parent = parent
        self.height = 1

class Calendar:
    def __init__(self):
        self.head = None

    def add(self, value, details, time_of_day):
        self.head = self.add_recurse(self.head, value, details, time_of_day)
        return self

    def add_recurse(self, current_node, value, details, time_of_day):

        if not current_node:
            return Node(value, details, time_of_day)

        # duplicate handling
        if value == current_node.value:
            return current_node

        if value < current_node.value:
            current_node.left = self.add_recurse(current_node.left, value, details, time_of_day)
            #current_node.left.parent = current_node
        else:
            current_node.right = self.add_recurse(current_node.right, value, details, time_of_day)
            #current_node.right.parent = current_node

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

    def helper(self, node):  # goes through tree to the smallest node
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
            if self.balance_factor(current_node.right) < 0: # right-left case
                #curr = current_node.left
                current_node.right = self.rotate_right(current_node.right)
            return self.rotate_left(current_node)  # rotate left

        # right rotation, left heavy
        if bf < -1:
            if self.balance_factor(current_node.left) > 0: # left-right case
                #curr = current_node.right
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
    """

    def size(self):
        return self.size_recursive(self.head)

    def size_recursive(self, current_node):
        if current_node is None:
            return 0
        return 1 + self.size_recursive(current_node.left) + self.size_recursive(current_node.right)

    """
    Return the BST as a list.
    """

    def time_as_list(self):
        final_list = []
        self.time_as_list_recursive(self.head, final_list)
        return final_list

    def time_as_list_recursive(self, current_node, final_list):
        if current_node is not None:

            # in-order traversal
            self.time_as_list_recursive(current_node.left, final_list)
            final_list.append(current_node.value)
            self.time_as_list_recursive(current_node.right, final_list)

    def all_details_as_list(self):
        final_list = []
        self.all_details_as_list_recursive(self.head, final_list)
        i = 0
        while i < len(final_list):
            print(f"{i + 1}) {final_list[i][1]}")
            i += 1
        return final_list

    def all_details_as_list_recursive(self, current_node, final_list):
        if current_node is not None:

            # in-order traversal
            self.all_details_as_list_recursive(current_node.left, final_list)
            final_list.append((current_node.value, current_node.details, current_node.time_of_day))
            self.all_details_as_list_recursive(current_node.right, final_list)

def print_tree(node, level=0):
    if node:
        print(" " * (level * 4) + f"Node: {node.value}, Details: {node.details} {node.time_of_day}")
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

def make_green(phrase): print("\033[92m {}\033[00m" .format(phrase))
def make_LightGray(phrase): print("\033[97m {}\033[00m" .format(phrase))
def make_Black(phrase): print("\033[98m {}\033[00m" .format(phrase))
def make_Red(phrase): print("\033[91m {}\033[00m".format(phrase))
def make_Yellow(phrase): print("\033[93m {}\033[00m".format(phrase))
def make_LightPurple(phrase): print("\033[94m {}\033[00m".format(phrase))
def make_Purple(phrase): print("\033[95m {}\033[00m".format(phrase))
def make_Cyan(phrase): print("\033[96m {}\033[00m".format(phrase))


def display():
    make_green(f"\n{'*'*3}Daily Calendar{'*'*3}")
    print(f"{'-'*22}")
    make_Yellow(f"Options:")
    print(f"1. Add Event"
          f"\n2. Show Single Event Details"
          f"\n3. Delete Event"
          f"\n4. Display All Events"
          f"\n5. Exit")

def add_event():
    details =[]
    description = input("Event Description: ").strip()
    details.append(description)
    time = input("Start Time of Event (hh:mm): ").strip()
    pattern = "^(0[1-9]|1[0-2]):([0-5][0-9])$"
    while True:
        if re.match(pattern,time):
            hours, minutes = time.split(":")
            hours, minutes = int(hours), int(minutes)
            #print(hours, minutes)
            time_of_day = input("\nAM or PM: ").strip().upper()
            while time_of_day not in ["AM","PM"]:
                time_of_day = input("\nInvalid.\n>> ").strip().upper()
            if time_of_day == "PM" and hours !=12:
                hours+=12 # calculating military time
            elif time_of_day == "AM" and hours == 12:
                hours = 0 # calculating midnight hour
            official_time = hours*100+minutes
            break
        else:
           time = input("Please enter a valid start time (hh:mm): ")

    details.append(official_time)
    details.append(time_of_day)
    #print(official_time)

    return details

def show_single_event(tree):
    while True:
        try:

            event_descriptions_list = tree.all_details_as_list()

            if not event_descriptions_list:
                return False

            option = int(input("\nChoose event: ").strip())

            real_time = change_to_real_time(event_descriptions_list[option-1][0])

            print(f"\nEvent: {event_descriptions_list[option-1][1]}\nStarts at {real_time} {event_descriptions_list[option-1][2]}")
            return True
        except IndexError:
            print("\nChoose a number from the listed options.")
        except ValueError:
            print("\nInvalid option. Please enter a number.")


def change_to_real_time(time):
    real_time = f"{str(time).zfill(4)[:2]}:{str(time).zfill(4)[2:]}"
    return real_time

def delete_event(tree):
    while True:
        try:

            event_descriptions_list = tree.all_details_as_list()

            if not event_descriptions_list:
                return False

            option = int(input("\nChoose event: ").strip())

            time_of_node_to_delete = event_descriptions_list[option - 1][0]
            tree.remove(time_of_node_to_delete)
            print("\nEvent successfully deleted!")

            return True
        except IndexError:
            print("\nChoose a number from the listed options.")
        except ValueError:
            print("\nInvalid option. Please enter a number.")

def display_all(tree):
    event_details_list = tree.all_details_as_list()

    if not event_details_list:
        print("No events available.")
    else:
        print("\nAll Scheduled Events:")
        for time, description, time_of_day in event_details_list:
            real_time = change_to_real_time(time)
            print(f"- {description} at {real_time} {time_of_day}")

def end():
    print("\nCalendar closing. . .")
    exit()

def main():
    calendar = Calendar()


    while True:
        try:

            display()

            option = int(input("\nChoose option: ").strip())

            match option:
                case 1:
                    make_LightGray("\n\nADD EVENT")
                    print(f"{'-' * 10}")

                    event_added_details = add_event()
                    calendar.add(value=event_added_details[1], details=event_added_details[0], time_of_day=event_added_details[2])
                    print("\nEvent successfully added!")
                case 2:
                    make_LightGray(f"\n\nEVENT TIME LOOKUP BY DESCRIPTION")
                    print(f"{'-' * 25}")

                    if show_single_event(calendar):
                            pass
                    else:
                        print("\nNo events available.")

                case 3:
                    make_LightGray(f"\n\nDELETE EVENT\n{'-' * 15}")
                    delete_event(calendar)


                case 4:
                    make_LightGray(f"\n\nDISPLAY ALL EVENTS\n{'-' * 15}")
                    display_all(calendar)

                case 5:
                    end()
                case _:
                    print("Not an option. Please enter a number 1-5.")


        except ValueError:
            print("Invalid option. Please enter a number.")
        except Exception as e:
            end()
            print(f"Error: {e}")

if __name__ == '__main__':
    main()

