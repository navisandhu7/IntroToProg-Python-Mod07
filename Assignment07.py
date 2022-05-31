# ---------------------------------------------------------------------------- #
# Title: Assignment 07 - Trying-Its-Best Scheduling Assistant
# Description: Simple bot that will assist in maintaining a schedule, pickled in
#               a file named "MySchedule.dat", via user input;
#               the program utilizes custom error handling
# ChangeLog (Who,When,What):
# NSandhu,5.28.2022,Initialized code
# NSandhu,5.29.2022,Debugging
# ---------------------------------------------------------------------------- #

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% DATA %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
import pickle
import sys
import datetime as dt
fileName = "MySchedule.dat"
scheduleData = []
userChoice = ""
userEvent = ""
userTime = None
userRemove = ""

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PROCESSING %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
class process:
    """Processes data and information"""

    @staticmethod
    def read_pickled_data(file_name = "MySchedule.dat"):
        """ Reads in existing pickled data, else creates new pickle file

        :param file_name: file where stored schedule data is, default is MySchedule.dat. Note that this file needs to
        exist prior to code execution:
        :return: data
        """
        data = []
        try:
            f = open(file_name,"rb")
            while True:
                try:
                    data = pickle.load(f)
                except EOFError as e:
                    IO.error_message(e)
                    break
        except FileNotFoundError as e:
            IO.error_message(e)
        f.close()
        return data

    @staticmethod
    def add_event_to_schedule(event, time, data):
        """ Adds data to a list of dictionary rows

        :param event: (string) with name of event:
        :param time: (datetime object) with time and date of event:
        :param scheduleDAta: (list) with dictionary rows for event and time data:
        :return: scheduleData (list) of dictionary rows of data
        """
        row = {"Event": event, "Time": time}
        data.append(row)
        print("Event added to your schedule.")
        return data

    @staticmethod
    def remove_event(event, data):
        """ Removes data from a list of dictionary rows

        :param event: (string) with name of event to remove:
        :param data: (list) filled with schedule data:
        :return: (list) of dictionary rows of schedule data
        """
        i = 0
        flag = 0
        for row in data:
            if row["Event"].lower() == event.lower().strip():
                flag = 1
                i += 1
                data.remove(row)
                print("Event removed from your schedule.")
            else:
                i += 1
                if i == len(data) and flag == 0:
                    print("Event not found.")
                    print()  # print new line for looks
        return data

    @staticmethod
    def pickle_data(file_name = "MySchedule.dat", data = []):
        """ Writes data from a list of dictionary rows to a File

        :param file_name: (string) with name of file, default is MySchedule.dat:
        :param data: (list) you want filled with file data, default is blank:
        :return: nothing
        """
        f = open(file_name, "ab")
        pickle.dump(data,f)
        f.close()
        print("Data saved!")
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% I/O %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

class IO:
    """ Performs I/O tasks """

    @staticmethod
    def welcome_message():
        """  Display a Welcome message to the user

        :return: nothing
        """

        print("""
        Welcome to the Scheduling Assistant! I will help you
        create and manage a basic schedule in the form of EVENTS
        and TIMES. Please choose from a menu option to get started:\n
        """)

    @staticmethod
    def display_menu():
        """  Display a menu of choices to the user

        :return: nothing
        """
        print('''\n
        Menu of Options
        1) View current Schedule
        2) Add a new Event to Your Schedule
        3) Remove an existing Event
        4) Save Your Schedule        
        5) Exit Program
        ''')
        print()  # Add an extra line for looks

    @staticmethod
    def get_menu_input():
        """  Get user input for any item

         :return: input
            """
        choice = input("Please select a menu option from 1-5: ").strip()
        return choice

    @staticmethod
    def error_message(error):
        """  Displays one of several error messages based on exception raised

        :param e: an exception object:
        :return: nothing
        """
        print()
        if isinstance(error,ValueError):
            print("Please only enter integer values or ensure time formatting is correct!\n")
        elif isinstance(error,EOFError):
            pass
        elif isinstance(error,FileNotFoundError):
            sys.exit("Schedule file does not exist, please create a blank 'MySchedule.dat' file in the local directory "
                  "and try again")
        elif isinstance(error,Exception):
            print(error)

    @staticmethod
    def view_schedule(data):
        """ Shows the current EVENTS in the list of dictionaries rows

                :param data: list of data to be displayed:
                :return: nothing
                """
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("Your Current Schedule shows the Following: ")
        for row in data:
            print(row["Event"] + " happening on " + row["Time"].strftime("%m/%d/%Y, %H:%M"))
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print()

    @staticmethod
    def get_user_event_time():
        """ Gets user input for event and time to add to schedule

        :return: event (user input of event, string)
                time (user input of date and time as datetime object)
        """
        event = input("Please input Event name: ")
        while True:
            try:
                timeMonth,timeDay,timeYear = input("Please enter date of event in MM/DD/YYYY format: ").split(sep="/")
                timeHour, timeMin = input("Please enter time of Event in HH:MM format (24 HOUR FORMAT): ").split(sep=":")
                timeDay = int(timeDay)
                timeMonth = int(timeMonth)
                timeYear = int(timeYear)
                timeHour = int(timeHour)
                timeMin = int(timeMin)
                if timeDay not in range(1,32) or timeMonth not in range(1,13) or timeYear not in range(1,10000) or timeHour not in range(0,24) or timeMin not in range(0,60):
                    print("One of the entered time parameters is out of range, please try again.")
                    continue
                break
            except ValueError as e:
                IO.error_message(e)
                print("Please try again.")
                print()
        time = dt.datetime(year=timeYear, month=timeMonth, day=timeDay, hour=timeHour, minute=timeMin,second=0)
        return event, time

    @staticmethod
    def get_event_to_remove():
        """  Gets the event name to be removed from the list

        :return: (string) with task
        """
        remove_event = input("Please enter name of Event to remove from list: ").strip()
        return remove_event

    @staticmethod
    def exit_message():
        """  Displays a message to the user prior to exiting program

        :return: nothing
        """
        print("Thank you! Program will end upon hitting 'Enter'...")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% MAIN %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

scheduleData = process.read_pickled_data(fileName)

IO.welcome_message()

while True:
    IO.display_menu()
    try:
        userChoice = int(IO.get_menu_input())
        if userChoice not in range(1,6):
            raise Exception("Please only input a value from 1 to 5!")
    except ValueError as e:
        IO.error_message(e)
        continue
    except Exception as e:
        IO.error_message(e)
        continue

    match userChoice:
        case 1:
            IO.view_schedule(scheduleData)
        case 2:
            userEvent, userTime = IO.get_user_event_time()
            scheduleData = process.add_event_to_schedule(userEvent, userTime, scheduleData)
        case 3:
            userRemove = IO.get_event_to_remove()
            scheduleData = process.remove_event(userRemove,scheduleData)
        case 4:
            process.pickle_data(fileName, scheduleData)
        case 5:
            IO.exit_message()
            input()
            break