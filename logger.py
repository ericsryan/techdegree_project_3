"""Write work logs.

This utility allows a user to write a new work log.
"""

import csv

from utils import clear_screen
from utils import get_date


def get_minutes():
    """Validate and return number of minutes."""
    while True:
        try:
            minutes = int(input("Time spent (rounded minutes): "))
            return minutes
        except ValueError:
            clear_screen()
            print("Sorry, you did not enter a number. Please enter the " +
                  "number of minutes you spent on the task."
                  )
            continue
        else:
            break


class Log:
    """Accept logging data from user and write log to csv file."""

    def __init__(self):
        """Accept log info from user."""
        clear_screen()
        self.task_date = get_date("What is the date of the task? " +
                                  "(MM/DD/YYYY): ")
        # Title of the task
        clear_screen()
        self.task_title = input("Title of the task: ")
        if self.task_title == '':
            self.task_title = 'None'
        # Time spent
        clear_screen()
        self.task_time = str(get_minutes())
        # Notes (Optional)
        clear_screen()
        self.task_notes = input("Notes (Optional, you can leave this empty): ")
        if self.task_notes == '':
            self.task_notes = 'None'

    def write_event(self):
        """Write a new work log to the database."""
        with open('log.csv', 'a', newline='') as csv_file:
            fieldnames = ['task_date', 'task_title', 'task_time', 'task_notes']
            taskwriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
            taskwriter.writerow({
                'task_date': self.task_date,
                'task_title': self.task_title,
                'task_time': self.task_time,
                'task_notes': self.task_notes
            })
        clear_screen()
        return_to_menu = input("The entry has been added."
                               " Press enter to return to the main menu. ")
        clear_screen()
