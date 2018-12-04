"""Utilities to be used in the Work Log program."""

import csv
import datetime
import os


def clear_screen():
    """Clear the screen for better readability."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_date(question):
    """Validate and return date input."""
    while True:
        # Format date_input for consistancy and flexibility
        # Validate date input
        formatted_date = ''
        try:
            date_input = input(question)
            for character in date_input:
                if character == '-':
                    formatted_date += '/'
                else:
                    formatted_date += character
            formatted_date = datetime.datetime.strptime(formatted_date,
                                                        '%m/%d/%Y')
        except ValueError:
            clear_screen()
            print("The date was not formatted correctly. Please try again.")
        else:
            break
    return datetime.datetime.strftime(formatted_date, '%m/%d/%Y')


def nav_bar(options):
    """Generate a navigation bar to be used while viewing logs."""
    d = '[D]elete'
    e = '[E]dit'
    m = '[M]ain Menu'
    n = '[N]ext'
    p = '[P]revious'
    s = '[S]earch Menu'
    bar = []
    for letter in options:
        bar.append(eval(letter))
        bar.append(' | ')
    del bar[-1]
    print(''.join(bar))


def order_logs():
    """Order the work logs by date."""
    logs = []
    with open('log.csv', 'r', newline='') as csv_file:
        log_reader = csv.reader(csv_file)
        for line in log_reader:
            logs.append(line)
    del logs[0]
    for line in logs:
        line[0] = datetime.datetime.strptime(line[0], '%m/%d/%Y')
    logs.sort()
    for line in logs:
        line[0] = datetime.datetime.strftime(line[0], '%m/%d/%Y')
    with open('log.csv', 'w', newline='') as csv_file:
        log_writer = csv.writer(csv_file)
        fieldnames = ['task_date', 'task_title', 'task_time', 'task_notes']
        log_writer.writerow(fieldnames)
        for line in logs:
            log_writer.writerow(line)


def store_logs():
    """Retrieve logs from the database to be used by the search program."""
    order_logs()
    logs = []
    with open('log.csv', 'r', newline='') as csv_file:
        log_reader = csv.DictReader(csv_file)
        for line in log_reader:
            logs.append(line)
    return logs
