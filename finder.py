"""Search the work log by exact date, date range, text match, or regex pattern.

These utilities allow a user to search the work log datebase. The search can be
made by matching an exact date, by viewing work logs within a date range, by
matching exact text in the title or notes of the work log, or by matching a
regex pattern.
"""

import csv
import datetime
import re

from utils import clear_screen
from utils import get_date
from utils import nav_bar
from utils import store_logs


def search_menu():
    """Give user search options."""
    clear_screen()
    while True:
        log_length = store_logs()
        if len(log_length) == 0:
            clear_screen()
            return_to_menu = input("There are no logs in the system. " +
                                   "Press 'Enter' to return to the " +
                                   "main menu.")
            clear_screen()
            break
        print("Do you want to search by:\n"
              "a) Exact Date\n" +
              "b) Range of Dates\n" +
              "c) Time Spent\n" +
              "d) Exact Search\n" +
              "e) Regex Pattern\n\n" +
              "[M]ain Menu\n"
              )
        search_selection = input("> ")
        if search_selection.upper() == 'A':
            search_date()
        elif search_selection.upper() == 'B':
            search_range()
        elif search_selection.upper() == 'C':
            time_search()
        elif search_selection.upper() == 'D':
            exact_search()
        elif search_selection.upper() == 'E':
            search_regex()
        elif search_selection.upper() == 'M':
            clear_screen()
            break
        else:
            clear_screen()
            print("That is not a valid selection. "
                  "Please choose an option from the menu.\n"
                  )
            continue

####################
# SEARCH FUNCTIONS #
####################


def search_date():
    """Search work logs by exact date."""
    logs = store_logs()
    date_log_list = []
    date_list = []
    for line in logs:
        if line['task_date'] not in date_list:
            date_list.append(line['task_date'])
    # Order the list of dates
    dt_list = []
    for date in date_list:
        dt_list.append(datetime.datetime.strptime(date, '%m/%d/%Y'))
    dt_list.sort(reverse=True)
    ordered_dates = []
    for date in dt_list:
        ordered_dates.append(datetime.datetime.strftime(date, '%m/%d/%Y'))
    # Create strings of numbered dates
    counter = 1
    num_date_list = []
    for date in ordered_dates:
        num_date_list.append("{}) {}".format(str(counter), date))
        counter += 1
    # Select date to view logs
    clear_screen()
    while True:
        try:
            print("For which date would you like to see the work logs?\n")
            for date in num_date_list:
                print("  " + date)
            date_selection = int(input("\n> "))
        except ValueError:
                clear_screen()
                print("Sorry, that is not a valid selection.")
                continue
        if date_selection not in range(1, (len(num_date_list) + 1)):
            clear_screen()
            print("Sorry, that is not a valid selection.")
            continue
        else:
            # Create a list of selected logs
            for line in logs:
                if line['task_date'] == (ordered_dates[(int(date_selection) -
                                         1)]):
                    date_log_list.append(line)
            # Display work logs for the selected date
            show_logs(date_log_list)
            break


def search_range():
    """Search work logs by date range."""
    logs = store_logs()
    range_log_list = []
    clear_screen()
    print("What beggining date would you like to use for the range? " +
          "(MM/DD/YYYY)\n")
    begin_range = get_date("> ")
    clear_screen()
    while True:
        print("What ending date would you like to use for the range? " +
              "(MM/DD/YYYY)\n")
        end_range = get_date("> ")
        if (datetime.datetime.strptime(begin_range, '%m/%d/%Y') >
            datetime.datetime.strptime(end_range, '%m/%d/%Y')):
            clear_screen()
            print("The ending date must be after {}.".format(begin_range))
        else:
            break
    for line in logs:
        if (datetime.datetime.strptime(line['task_date'], '%m/%d/%Y') >=
            datetime.datetime.strptime(begin_range, '%m/%d/%Y') and
            datetime.datetime.strptime(line['task_date'], '%m/%d/%Y') <=
            datetime.datetime.strptime(end_range, '%m/%d/%Y')):
            range_log_list.append(line)
    if len(range_log_list) < 1:
        clear_screen()
        return_to_menu = input("There are no logs in that date range.\n" +
                               "You will be returned to the search menu.\n" +
                               "Press 'Enter' to continue.")
        clear_screen()
    else:
        show_logs(range_log_list)


def time_search():
    """Search work logs by time."""
    logs = store_logs()
    time_list = []
    clear_screen()
    print("Enter the amount of time for the " +
          "logs that you would like to see.\n")
    time = input("> ")
    for line in logs:
        if str(time) == line['task_time']:
            time_list.append(line)
    if len(time_list) == 0:
        clear_screen()
        return_to_menu = input("There are no matches for " +
                               "that amouht of time.\n" +
                               "You will be returned to the search menu.\n" +
                               "Press 'Enter' to continue.")
        clear_screen()
    else:
        show_logs(time_list)


def exact_search():
    """Search work logs by exact match."""
    logs = store_logs()
    exact_log_list = []
    clear_screen()
    print("Enter the search term that you would like to use.\n")
    term = input("> ")
    for line in logs:
        if (term.lower() in line['task_date'].lower() or
            term.lower() in line['task_title'].lower() or
            term.lower() in line['task_time'].lower() or
            term.lower() in line['task_notes'].lower()):
            exact_log_list.append(line)
    if len(exact_log_list) < 1:
        clear_screen()
        return_to_menu = input("There are no matches for that term.\n" +
                               "You will be returned to the search menu.\n" +
                               "Press 'Enter' to continue.")
        clear_screen()
    else:
        show_logs(exact_log_list)


def search_regex():
    """Search work logs using REGEX match."""
    logs = store_logs()
    regex_log_list = []
    clear_screen()
    print("Enter the REGEX pattern that you would like to use to search.")
    regex = input("> ")
    for line in logs:
        if (re.search(regex, line['task_date']) or
            re.search(regex, line['task_title']) or
            re.search(regex, line['task_time']) or
            re.search(regex, line['task_notes'])):
            regex_log_list.append(line)
    if len(regex_log_list) < 1:
        clear_screen()
        return_to_menu = input("There are no matches for that term.\n" +
                               "You will be returned to the search menu.\n" +
                               "Press 'Enter' to continue.")
        clear_screen()
    else:
        show_logs(regex_log_list)

###############
# LOG DISPLAY #
###############


def show_logs(log_list):
    """Display the logs that have been selected by the user."""
    show_list = log_list
    counter = 1
    index = 0
    clear_screen()
    while True:
        print("Date: {}\n".format(show_list[index]['task_date']) +
              "Title: {}\n".format(show_list[index]['task_title']) +
              "Time Spent: {}\n".format(show_list[index]['task_time']) +
              "Notes: {}\n\n".format(show_list[index]['task_notes']) +
              "Result {} of {}".format(counter, len(show_list))
              )
        if len(show_list) == 1:
            nav_options = 'des'
        elif counter <= 1:
            nav_options = 'neds'
        elif counter > 1 and counter < len(show_list):
            nav_options = 'pneds'
        elif counter == len(show_list):
            nav_options = 'peds'
        nav_bar(nav_options)
        menu_option = input("> ")
        if menu_option.upper() not in nav_options.upper() or menu_option == '':
            clear_screen()
            print("Sorry, that is not a valid selection.\n")
        elif menu_option.upper() == 'N':
            clear_screen()
            counter += 1
            index += 1
        elif menu_option.upper() == 'P':
            clear_screen()
            counter -= 1
            index -= 1
        elif menu_option.upper() == 'D':
            show_list = delete_log(show_list, index)
            index = 0
            counter = 1
            clear_screen()
            next = input("The log has been deleted. " +
                         "Press 'Enter' to continue.")
            clear_screen()
            if len(show_list) == 0:
                index = 0
                counter = 1
                clear_screen()
                break
        elif menu_option.upper() == 'E':
            show_list = edit_log(show_list, index)
            index = 0
            counter = 1
            clear_screen()
            next = input("The log has been edited. " +
                         "Press 'Enter' to continue.")
            clear_screen()
            break
        elif menu_option.upper() == 'S':
            clear_screen()
            break

##############
# ALTER LOGS #
##############


def delete_log(log_list, index):
    """Delete the selected work log."""
    logs = store_logs()
    for line in logs:
        if line == log_list[index]:
            logs.remove(line)
            log_list.remove(line)
            break
    with open('log.csv', 'w') as csv_file:
        fieldnames = ['task_date', 'task_title', 'task_time', 'task_notes']
        taskwriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
        headerwriter = csv.writer(csv_file)
        headerwriter.writerow(fieldnames)
        for line in logs:
            taskwriter.writerow(line)
    return log_list


def edit_log(log_list, index):
    """Edit the selected work log."""
    logs = store_logs()
    for line in logs:
        if line == log_list[index]:
            while True:
                clear_screen()
                print("Which field would you like to edit?\n\n" +
                      "  a) Date\n" +
                      "  b) Title\n" +
                      "  c) Time\n" +
                      "  d) Notes\n")
                selection = input("> ")
                if selection not in 'abcd':
                    print("That is not a valid selection.\n")
                    continue
                elif selection.upper() == 'A':
                    clear_screen()
                    print("Original Date: " + line['task_date'] +
                          "\n\nWhat would you like the date to be?\n")
                    new_date = get_date("> ")
                    line['task_date'] = new_date
                    log_list[index] = new_date
                elif selection.upper() == 'B':
                    clear_screen()
                    print("Original Title: " + line['task_title'] +
                          "\n\nWhat would you like the title to be?\n")
                    new_title = input("> ")
                    line['task_title'] = new_title
                    log_list[index] = new_title
                elif selection.upper() == 'C':
                    clear_screen()
                    print("Original Time: " + line['task_time'] +
                          "\n\nWhat would you like the time to be?\n")
                    new_time = input("> ")
                    line['task_time'] = new_time
                    log_list[index] = new_time
                elif selection.upper() == 'D':
                    clear_screen()
                    print("Original Notes: " + line['task_notes'] +
                          "\n\nWhat would you like the notes to be?\n")
                    new_notes = input("> ")
                    line['task_notes'] = new_notes
                    log_list[index] = new_notes
                break
    with open('log.csv', 'w') as csv_file:
        fieldnames = ['task_date', 'task_title', 'task_time', 'task_notes']
        taskwriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
        headerwriter = csv.writer(csv_file)
        headerwriter.writerow(fieldnames)
        for line in logs:
            taskwriter.writerow(line)
    return log_list
