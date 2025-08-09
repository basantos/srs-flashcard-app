import csv
import reviewer as r  # contains functions for review page
import datetime

# functions for home page
def print_list(arr):
    """Prints list for the home page
    """
    num = 1
    for item in arr:
        print(str(num) + '. ' + item)
        num += 1

def show_home_page():
    """Prints the home page and takes user input for next action.
    """
    print("\n------------------------------------------\n\tHome – Card Sets List\n------------------------------------------\nCreate and keep your study materials organized, up to date, and all in one place!\n---------------------")
    print_list(sets_list)
    print("---------------------\nPlease enter\n# to select and view a set\n‘a’ to add a new card\n‘aa’ to add multiple cards from a file\n‘h’ for help page\n---------------------")

    while True:
        key = input("What would you like to do?")
        if key.isnumeric():
            show_set(sets_list[int(key) - 1], 0, 4)
        elif key == 'a':
            add_card_page()
            show_home_page()
        elif key == 'aa':
            try:
                file = input("Enter path of your csv file (example: C:\\\\Users\\Bri\\Documents\\Files\\File.csv)")
            except KeyboardInterrupt:
                any_key_to_return("Add cards canceled. Press any key to return to home page.")

            create_cards_from_csv(file)
            any_key_to_return("Cards successfully created!\nEnter any key to return\n")
            show_home_page()
        elif key == 'h':
            show_help_page()
            show_home_page()
        else:
            print('Invalid input. Try again.')

# functions for help page
def show_help_page():
    """Prints help page"""
    print("------------------------------------------\n\tHelp Page\n------------------------------------------\nGet Started:\n1. Add a card by pressing ‘a’ in the home page or set page. "
          "Note: For new users, the only “set” is the “Uncategorized Set.\n2. Enter field information of the card when prompted."
          "Note: When prompted for set name, if you enter a name of a non-existent set, "
          "you will be prompted to confirm the creation of a new set or choose from a list of existing set. "
          "Leaving this field blank will add this card to the “Uncategorized” set. \n3. You have now created a card!\n"
          "What if I want to move a card from a set and into another set?\n1. Select the current set the card is listed in.\n"
          "2. Select the card.\n3. Enter ‘3’ to edit the card’s set field.\n4. Enter the name of the new set."
          "\n5. You have successfully moved a card between sets!\n---------------------\n")
    key = None
    while key != 's' or key != 'ss':
        key = input("Enter 's' to return to previous page or 'ss' to return to home page.")
        if key == 's' or key == 'ss':
            return
        else:
            print("Invalid input. Please try again.")

# functions for adding cards
def add_card_page():
    """Prints add card page and prompts user to enter data for each card field"""
    print("------------------------------------------\n\tAdd Card\n------------------------------------------\nEnter ctrl+c anytime to cancel.\n---------------------")

    try:
        front = input("Enter info for front of card: ")
        back = input("Enter info for back of card: ")
        set = input("Enter name of a set to add card or leave blank: ")
        if set == '':
            set = 'uncategorized'
        # organize set do later
        hint = input("Enter hint: ")
        validate_add_card(front, back, set, hint)
    except KeyboardInterrupt:
        return

def validate_add_card(front, back, set, hint):
    """Asks user to verify if they want to add card. Allows user to validate, update field, or cancel action."""
    print("---------------------\nIs this correct?")
    print('1. Front: ' + front + '\n2. Back: ' + back + '\nSet: ' + set + '\nHint: ' + hint +
          '\nNote: If you left "set" blank, it adds card to "Uncategorized" set.\n---------------------\nPlease enter'
          '\n‘a’ to confirm and add card\n# of field to edit info\n‘ctrl + c’ to cancel\n---------------------')
    while True:
        try:
            key = input()
        except KeyboardInterrupt:
            return

        if key == 'a':
            create_card(front, back, set, hint)
            any_key_to_return('Card successfully added!\nPress any key to continue.')
            return
        else:
            print("Invalid input. Please try again.")

def create_card(front, back, set, hint):
    """Creates new card"""
    if set == '':
        set = sets_list[0]  # uncategorized set
    elif set not in sets_list:
        sets_list.append(set)
        create_new_set(set)

    filename = set.lower() + '.csv'
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([front, back, set, hint, 0, datetime.now()])

def create_cards_from_csv(csv_file):
    """Creates multiple cards from a csv file"""

    with open(csv_file, 'r', newline='') as f:
        reader = csv.reader(f)

        for row in reader:
            create_card(row[0], row[1], row[2].lower(), row[3])

# functions for viewing cards
def view_card(set, row_num):
    """Prints card page and prompts for user action"""
    print("------------------------------------------\n\tCard Page\n------------------------------------------\n")
    filename = set.lower() + '.csv'

    with open(filename, mode='r', newline='') as f:
        reader = csv.reader(f)
        index = 0
        for row in reader:
            if index == int(row_num) -1:
                print("1. Front: " + row[0] + "\n2. Back: " + row[1] + "\n3. Set: " + row[2] + "\n4. Hint: " + row[3])
            index += 1

    print("---------------------\nPlease enter\n# to edit field info\n‘d’ to delete card\n'h' to show help page"
          "\n‘s’ to return to set page\n'ss' to return to home/sets list page\n---------------------\n")
    while True:
        key = input("What would you like to do?")
        if key.isnumeric() and int(key) >= 1 and int(key) <= 4:
            edit_field(set, int(row_num), int(key))
            view_card(set, row_num)
        elif key == 'd':
            delete_card(set, int(row_num)-1)
            show_set(set)
        elif key == 'h':
            show_help_page()
            view_card(set, row_num)
        elif key == 's':
            show_set(set)
        elif key == 'ss':
            show_home_page()
        else:
            print("Invalid input. Please try again.")

# functions for deleting cards
def delete_card(set, row_num):
    """Asks user to verify if they want to delete a card then deletes the card. Also allows cancelling of action."""
    print("Deleting a card loses all data associated with the card.\nWould you like to continue to delete card?"
          "Press ‘d’ to delete or ctrl+c to cancel")
    try:
        while True:
            key = input()
            if key == 'd':
                filename = set.lower() + '.csv'
                with open(filename, 'r', newline='') as f:
                    reader = csv.reader(f)
                    rows = []
                    index = 0
                    for row in reader:
                        if index != row_num:
                            rows.append(row)
                        index += 1

                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(rows)
                any_key_to_return("Card successfully deleted. Press any key to continue.")
                return
            else:
                print("Invalid input. Please try again.")
    except KeyboardInterrupt:
        return

# functions for editing cards
def edit_field(set, row_num, field_num):
    """Allows user to edit field on a card."""
    row_num = int(row_num)
    field_num = int(field_num)

    print("By editing this field, previous info will be overwritten. Enter ctrl+c to cancel.\n---------------------\n")
    try:
        new_info = input("Enter new info: ")
    except KeyboardInterrupt:
        return

    filename = set.lower() + '.csv'
    rows = []
    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f)
        index = 0
        for row in reader:
            if index == row_num-1:
                try:
                    print("Previous data will be overwritten. Proceed?\n\tOld info: "
                          + row[field_num-1] + "\n\tNew info: " + new_info + '\n')
                    key = input("Press any key to overwrite data or ctrl+c to cancel.")
                except KeyboardInterrupt:
                    view_card(set, row_num)
                new_row = []
                for i in range(4):
                    if i != field_num-1:
                        new_row.append(row[i])
                    else:
                        new_row.append(new_info)
                rows.append(new_row)
            else:
                rows.append(row)
            index += 1

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

# functions for sets
def show_set(set, start=0, end=4):
    """Prints a list of cards from a set 5 cards at a time. Prompts user to move to next page or perform an action."""
    print("------------------------------------------\n\t" + set + "\n------------------------------------------")

    filename = set.lower() + '.csv'

    with open(filename, mode='r', newline='') as f:
        reader = csv.reader(f)
        csv_length = sum(1 for row in reader)

    with open(filename, mode='r', newline='') as f:
        reader = csv.reader(f)
        csv_row = 0
        for row in reader:
            if csv_row >= start and csv_row <= end and csv_row < csv_length:
                print(str(csv_row+1) + '. ' + row[0])
            elif csv_row > end:
                break
            csv_row += 1
    print("---------------------\nPlease enter:\n# to select and view card\n‘n’ to view next 5 cards\n‘p’ to view previous 5 cards"
          "\n‘a’ to add a new card\n'r' to start review\n'h' to show help page\n‘s’ or 'ss' to return to home/set lists page\n---------------------\n")
    while True:
        key = input("What would you like to do?")
        if key.isnumeric():
            view_card(set, key)
            return
        elif key == 'n':
            start = end + 1
            if start < csv_length:
                show_set(set, start, start+4)
            else:
                show_set(set, 0, 4)
        elif key == 'p':
            if start == 0:
                start = csv_length - (csv_length % 5) # keeps list in intervals of 5 so if set is 7 cards, previous from start 0 is card 6 and 7
                show_set(set, start, start+4)
            else:
                start -= 5
                show_set(set, start, start + 4)
            return
        elif key == 'a':
            add_card_page()
            show_set(set, start, end)
        elif key == 'r':
            r.start_review(set)
            show_set(set, start, end)
        elif key == 'h':
            show_help_page()
            show_set(set, start, end)
        elif key == 's' or key =='ss':
            show_home_page()
        else:
            print("Invalid input. Please try again.")

def create_new_set(set):
    """Adds a new set to the sets csv file"""
    with open('sets.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([set])

# misc functions
def any_key_to_return(prompt):
    """Allows user to hit any key to return."""
    input(prompt)

if __name__ == "__main__":
    sets_list = []
    with open('sets.csv', 'r') as f:
        reader = csv.reader(f)

        for category in reader:
            sets_list.append(category[0])

    while True:
        show_home_page()
