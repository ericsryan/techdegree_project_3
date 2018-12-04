"""Enter work logs and search existing logs.

Users have the option of entering a work log or searching existing logs. They
also have the option of editing or deleteing existing entries.
"""

from finder import search_menu
from logger import Log
from utils import clear_screen


def main_menu():
    """Disply logging options."""
    clear_screen()
    while True:
        print("WORK LOG\n" +
              "What would you like to do?\n" +
              "a) Add new entry\n" +
              "b) Search in existing entries\n" +
              "c) Quit program"
              )
        menu_selection = input("> ")
        if menu_selection.upper() == 'A':
            new_log = Log()
            new_log.write_event()
        elif menu_selection.upper() == 'B':
            search_menu()
        elif menu_selection.upper() == 'C':
            clear_screen()
            print("Thank you for using the logger. Have a nice day!\n\n")
            break
        else:
            clear_screen()
            print("That is not a valid selection. "
                  "Please choose an option from the menu.\n"
                  )


if __name__ == '__main__':
    main_menu()
