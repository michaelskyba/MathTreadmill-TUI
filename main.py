#!/usr/bin/python

import curses
import time
import datetime
import os
import random
import math

def z(number):
    if number < 0:
        return "({})".format(number)
    else:
        return number

def get_question(skill):
    # List of lines in the file that are for this skill
    skill_lines = []

    # Sample question file line: "2.2 M -10 -2 -10 -2"
    with open("auto_questions") as auto_questions:
        lines = auto_questions.readlines()

        # Find the correct lines for the skill
        for line in lines:
            if line[:3] == skill:
                skill_lines.append(line[4:])

    # Pick a random question type (multi-variable for readability)
    question_id = random.randint(0, len(skill_lines) - 1)
    question_line = skill_lines[question_id]
    question_line = question_line.split()

    x = random.randint(int(question_line[1]), int(question_line[2]))
    y = random.randint(int(question_line[3]), int(question_line[4]))

    # Addition
    if question_line[0] == "A":
        if random.randint(1, 2) == 1:
            question = "{} + {}".format(z(x), z(y))
        else:
            question = "{} + {}".format(z(y), z(x))

        answer = x + y

    # Subtraction
    elif question_line[0] == "S":
        # "AN" is not written
        if len(question_line) == 5:
            if random.randint(1, 2) == 1:
                question = "{} - {}".format(z(x + y), z(y))
                answer = x
            else:
                question = "{} - {}".format(z(x + y), z(x))
                answer = y

        # AN _is_ written (allow negatives)
        else:
            if random.randint(1, 2) == 1:
                question = "{} - {}".format(z(x), z(y))
                answer = x - y
            else:
                question = "{} - {}".format(z(y), z(x))
                answer = y - x


    # Multiplication
    elif question_line[0] == "M":
        if random.randint(1, 2) == 1:
            question = "{} × {}".format(z(x), z(y))
        else:
            question = "{} × {}".format(z(y), z(x))

        answer = x * y

    # Division
    elif question_line[0] == "D":
        if random.randint(1, 2) == 1:
            question = "{} ÷ {}".format(z(x * y), z(y))
            answer = x
        else:
            question = "{} ÷ {}".format(z(x * y), z(x))
            answer = y

    # Exponents
    elif question_line[0] == "E":
        question = "{}^{}".format(x, y)
        answer = x ** y

    # Roots
    elif question_line[0] == "R":
        if y == 2:
            question = "sqrt {}".format(x**y)
        elif y == 3:
            question = "cube root of {}".format(x**y)
        else:
            question = "{}th root of {}".format(y, x**y)

        answer = x

    return {
            "question": question,
            "answer": answer
            }

def configure(skill):
    with open("auto_config") as auto_config:
        lines = auto_config.readlines()

        # Find the correct line for the skill
        # Sample skill config line: "2.3 25 0.75 13"
        for line in lines:
            if line[:3] == skill:
                config = line[3:].split()
                return {
                        "total_time": config[0],
                        "decrement": config[1],
                        "threshold": config[2]
                        }

# Print some text
def text(text, y, stdscr):
    # Find the middle of the screen
    mx = stdscr.getmaxyx()[1]//2
    my = stdscr.getmaxyx()[0]//2

    # Subtract len(text)//2 to adjust for the length of the text
    stdscr.addstr(my + y, mx - len(text)//2, text)
    stdscr.refresh()

# The main selection menu
def main_menu(stdscr, sel_row):
    options = [{
                "text": "Welcome to MathTreadmill",
                "y": -5
            },
            {
                "text": "Auto Mode",
                "y": 1
            },
            {
                "text": "Custom Mode",
                "y": 2
            }]

    for index, option in enumerate(options):
        if sel_row == index:
            # This reverses the background colour for the selected option
            stdscr.attron(curses.color_pair(1))
            text(option["text"], option["y"], stdscr)
            stdscr.attroff(curses.color_pair(1))

        else:
            text(option["text"], option["y"], stdscr)


def main(stdscr):
    # Set up colours
    curses.use_default_colors()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    stdscr.nodelay(True)

    skills = ["1.1", "1.2", "1.3", "1.4", "2.1", "2.2", "2.3", "2.4", "3.1", "3.2", "3.3", "3.4", "4.1", "4.2", "4.3", "4.4", "5.1", "5.2", "5.3", "5.4", "SSS"]
    skill = 0

    # Starting screen
    state = "main_menu"
    sel_row = 1
    main_menu(stdscr, sel_row)

    # Main loop
    while 1:
        # Get the pressed key
        key = stdscr.getch()

        # Quit with "q"
        if key == 113:
            break

        # Main menu
        elif state == "main_menu":
            # Pressing 'up' or 'k' selects the "Auto Mode" option
            if key in [curses.KEY_UP, 107]:
                sel_row = 1
                main_menu(stdscr, sel_row)

            # Pressing 'down' or 'j' selects the "Custom Mode" option
            elif key in [curses.KEY_DOWN, 106]:
                sel_row = 2
                main_menu(stdscr, sel_row)

            # Pressing enter goes into the option
            elif key in [curses.KEY_ENTER, 10, 13]:
                stdscr.clear()

                if sel_row == 1:
                    state = "auto"

                    question_object = get_question(skills[skill])
                    question = question_object["question"]
                    answer = question_object["answer"]

                    config_object = configure(skills[skill])
                    sec_total = int(config_object["total_time"])
                    sec_rem = sec_total
                    decrement = config_object["decrement"]
                    threshold = config_object["threshold"]

                    wrong = 0

                    current_value = ""

                    question_start = datetime.datetime.now()

                    bars = round(sec_total / sec_rem * 20)

                else:
                    state = "custom"
                    text("What would you like..?", 0, stdscr)

        # Auto Mode
        elif state == "auto":
            # Calculate bar numbers
            sec_rem = sec_total - (datetime.datetime.now() - question_start).seconds
            sec_rem -= wrong # Split the bar in half every time you get it wrong
            bars = round(sec_rem / sec_total * 20)

            # Clear old number
            if sec_rem < 10:
                sec_rem = " {}".format(sec_rem)

            # Skill
            text(str(skills[skill]), -5, stdscr)

            # Question
            text("{} = ?".format(question), -1, stdscr)

            # Respose
            text("{}> {}_{}".format(" "*12, current_value, " "*12), 0, stdscr)

            # Time bar
            text("|{bar}{space}|".format(bar="█"*bars, space=" "*(20-bars)), 3, stdscr)

            # Time text
            text("{sec}s left".format(sec=sec_rem), 4, stdscr)

            # 0-9
            if key in range(48, 58):
                current_value += str(key - 48)

                # Make sure value doesn't exceed space
                if len(current_value) > 6:
                    current_value = current_value[:-1]

            # Input negative numbers
            if key == 45:
                current_value += "-"

                # Make sure value doesn't exceed space
                if len(current_value) > 6:
                    current_value = current_value[:-1]

            # Backspace
            elif key in [8, curses.KEY_BACKSPACE]:
                current_value = current_value[:-1]

            # Enter, to submit an answer
            elif key in [curses.KEY_ENTER, 10, 13]:
                if len(current_value) > 0 and int(current_value) == answer:
                    # Update to next question
                    stdscr.clear()
                    skill += 1

                    question_object = get_question(skills[skill])
                    question = question_object["question"]
                    answer = question_object["answer"]

                    config_object = configure(skills[skill])
                    sec_total = int(config_object["total_time"])
                    sec_rem = sec_total
                    decrement = config_object["decrement"]
                    threshold = config_object["threshold"]

                    wrong = 0

                    current_value = ""

                    question_start = datetime.datetime.now()

                    bars = round(sec_total / sec_rem * 20)

                elif len(current_value) > 0:
                    # First get the remaining seconds (it's currently a string)
                    sec_rem = sec_total - (datetime.datetime.now() - question_start).seconds
                    sec_rem -= wrong
                    wrong += math.floor(sec_rem / 2)

                    # Clear typed answer
                    current_value = ""

curses.wrapper(main)
