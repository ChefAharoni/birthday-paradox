# In a group of 23 people, there is a 50.7% chance that two people will share a birthday date.
# If we take pairs of people, then one person can pair with 22 other, the second person can pair with 21 other people,
# not including the last person.
from Sources import CommonNames
from colorama import Fore, Back, Style
from Sources import myStyles
from datetime import datetime

CMN_NAMES = list(CommonNames.get_csv_names())  # list of all names in commonNames.csv file; contains 447055 names.
DATE_FORMAT = "%d %B"


def error_invalid_num() -> None:
    """
    Prints error for invalid number.
    @return: None
    """
    print("Error, please enter a valid number: ")


def ran_ppl(num_of_ppl: int) -> set:
    """
    The function receives number of people to run, and selects randomly from the master list.
    @param num_of_ppl: Number of people to be checked.
    @return: a set of n people chosen randomly
    """
    from random import randint
    chosen_ppl = set()  # The returned set of names randomly chosen.
    random_numbers = list()  # A list to keep track of chosen random numbers
    for i in range(num_of_ppl):
        ran_num = randint(0, len(CMN_NAMES) - 1)  # Choose a random number from 0 to the length of the names list.
        while ran_num in random_numbers:  # if this number has been pulled:
            ran_num = randint(0, len(CMN_NAMES) - 1)  # skip and later draw another random number
        else:
            random_numbers.append(ran_num)
            name = CMN_NAMES[ran_num].lower()
            name = name.title()  # style the name to be lowercase and Titled.
            chosen_ppl.add(name)  # adds the fixed name to the set of chosen people.
    # print(chosen_ppl)
    # print(len(chosen_ppl))
    return chosen_ppl


def assign_birthdays(ppl: set) -> dict:
    """
    Assigns a random date (dob) for each man in people list.
    @param ppl: List (or set) of people to assign birthdays to.
    @return: Dict of ppl name as keys and dob as values.
    """
    import datetime
    import random
    # year, month, day
    # print(datetime(1, 12, 31))
    birthdays = dict()
    for dude in ppl:
        month = random.randint(1, 12)
        if month == 2:  # February
            day = random.randint(1, 28)
        elif month in [4, 6, 9, 11]:  # if month has 30 days.
            day = random.randint(1, 30)
        else:  # January, March, May
            day = random.randint(1, 31)
        bd = datetime.date(1600, month, day)  # we assume its a leap year for ease of calculation.
        bd_formatted = datetime.date.strftime(bd, DATE_FORMAT)  # formats the date to words; outputs str
        # print(bd_formatted)
        # print(type(bd_formatted))
        birthdays[dude] = bd_formatted
    print(birthdays)
    return birthdays


def bd_ppl_print(bds: dict) -> None:
    """
    Receives a dict of birthdays, converts to list of dicts, sorts the list by date, prints in tabular format name
    and dob.
    @param bds: Dictionary of name as key and dob as value.
    @return: function's purpose is to print; returns None.
    """
    import datetime
    listed_bds = list()
    for key, value in bds.items():
        listed_bds.append({"Name": key, "DOB": value})  # converting the dict to list of dict for ease of sorting.
    listed_bds.sort(key=lambda x: datetime.datetime.strptime(x['DOB'], DATE_FORMAT))  # sorts the list of dicts by date.
    print(listed_bds)
    # receives the dict from assign_birthdays func and prints the bds in a tabular, clean format.
    print(myStyles.Colors.BOLD + myStyles.Colors.BLUE + f'{"Human Name":<20} |\t {"Birthday":<20} {"|":<20}' +
          myStyles.Colors.END)  # title
    for i in listed_bds:  # for every dict in the ordered listed dictionaries.
        for v in i.values():  # for every value in a dictionary
            print(f'{v:<20}', end=" |\t ")  # prints the name and dob sorted by date, in a tabular format.
        print()  # prints a newline for formatting


def create_pairs(ppl: set) -> dict:
    """
    Function creates pairs of people in ppl list. i.e. for 23 people, the function will pair human 0 with humans 1-23,
    human 1 with humans 2-23, and so on..
    @param ppl: Set of people to create pairs from.
    @return: Dict of people and their pairs.
    """
    pairs = dict()
    # i_pairs = [i for i in range(1, len(ppl))]  # List comprehension in the size of the ppl list.
    ppl_to_pair = list(ppl)  # convert the ppl set to list, so it could be indexed.
    ppl_to_pair = ppl_to_pair[1:]  # choose the list from the second index to the end.
    man_pairs = [man for man in ppl_to_pair]  # List comprehension in the size of the ppl list, minus the first one.
    pairs_sum = 0  # the sum of possible pairs; result should be 253 for 23 ppl.
    for man in ppl:  # for each people in the people's list
        pairs[man] = list(man_pairs)
        pairs_sum += len(pairs[man])
        # print(man, "len is", len(pairs[man]))
        if len(pairs[man]) == 0:
            continue
        man_pairs.pop(0)
    print("\nPairs:", pairs)
    print("There are " + Fore.MAGENTA + str(pairs_sum) + Fore.RESET + " pairs.")
    return pairs


def match_bds(bds: dict, pairs: dict) -> dict:
    """
    Finds people with the same dob from dict of pairs.
    Function wasn't tested if 3 or more people share a dob, probably will not find well since it works with pairs, and
    it is not the idea behind the birthday paradox.
    @param bds: Dict of people and their dob (suggested from assign_birthdays func).
    @param pairs: Dict of people and their pairs (suggested from create_pairs func).
    @return: Prints results and returns dict of people and their matches; dob as key and list of people sharing the dob
    in a list; If three people are sharing a bd, value of key dob will show only the last people sharing the date, and
    not all people sharing.
    """
    s_cyan = myStyles.Colors.CYAN
    s_yellow = myStyles.Colors.YELLOW
    s_green = myStyles.Colors.GREEN
    s_end = myStyles.Colors.END
    matching_bds = dict()
    for human in pairs.items():
        for pair in human[1]:  # for each pair in the list of the pairs;
            if bds[human[0]] == bds[pair]:  # if the birthday of the first human is paired with the second human's bd.
                print(f'{s_cyan}{human[0]}{s_end} is sharing a birthday with {s_yellow}{pair}{s_end} on '
                      f'{s_green}{bds[human[0]]}{s_end}.')
                print(f'{human[0]}\'s birthday is on {bds[human[0]]}.')
                print(f'{pair}\'s birthday is on {bds[pair]}.')
                matching_bds[bds[human[0]]] = [human[0], pair]
    return matching_bds


def successful_pairs(matching_bds: dict, num_of_ppl: int) -> None:
    """
    If matching birthdays were found, function prints how much were found out of total number of people checked.
    @param matching_bds: Dict of matching bds (suggested from match_bds func).
    @param num_of_ppl: Number of people in ppl list (known as n in computations).
    @return: Currently just prints, might add statistical data in the future.
    """
    # function should see how many values are in the successful pairs' dictionary, and justify the statistics.
    num_results = len(matching_bds.keys())
    if num_results == 1:
        print(f'I have found {num_results} shared date from a list of {num_of_ppl} people.')
    elif num_results > 1:
        print(f'I have found {num_results} shared dates from a list of {num_of_ppl} people.')
    # add statistics data


def probability(total_days=365, precision=3, num_of_ppl=23) -> float or None:
    """
    Function calculates the probability of finding a pair of two people with a birthday.
    @param total_days: Total days in a year, could be a constant, but kept anyway for other future possible options.
    @param precision: Precision of result in percentage, default set to 3.
    @param num_of_ppl: Number of people in the list / people to check.
    @return: P(B) = The chances that two people will share a birthday.
    """
    s_bold = myStyles.Colors.BOLD
    s_end = myStyles.Colors.END
    import math
    n = total_days
    k = num_of_ppl
    try:
        v_nr = (math.factorial(n)) / (math.factorial(n - k))
    except OverflowError:  # If number is too large for python to calculate.
        return None  # Cannot calculate due to large number.
    except ValueError:  # factorial() not defined for negative values
        return None  # Cannot calculate due to negative factorial.
    v_t = n ** k
    p_a = v_nr / v_t
    p_b = 1 - p_a
    # print("Chances two pairs will" + style.Colors.BOLD + " not " + style.Colors.END + "share a birthday: ", end="")
    print(f'{Back.BLACK}Chances two pairs will {s_bold} not {s_end}{Back.BLACK} share a birthday: ', end="")
    print(f'{p_a:.{precision}%}{Style.RESET_ALL}')
    print(f'{Back.BLACK}Chances two pairs will share a birthday: ', end="")
    print(f'{p_b:.{precision}%}{Style.RESET_ALL}')
    return p_b


def num_ppl() -> int:
    """
    Checks from user number of people to get checked; returns 23 if user doesn't enter anything.
    @return: int of number of people.
    """
    while True:
        try:
            num_of_ppl = int(input(">>> "))
        except ValueError:  # if num entered isn't int
            error_invalid_num()
            continue
        if num_of_ppl <= 0:  # if num equal/less than 0.
            error_invalid_num()
            continue
        else:
            break
    return num_of_ppl


def auto_num_ppl() -> int:
    """
    Chooses num of people to run auto check. Translates no response (enter) to 23.
    @return: number (int) of people to run the check.
    """
    num_of_ppl = input(">>> ")
    if num_of_ppl == "":
        return 23
    else:
        try:  # try to convert to int
            num_of_ppl = int(num_of_ppl)
        except ValueError:  # if num entered isn't int
            error_invalid_num()
            ERROR_VALID_NUM
            while True:
                try:
                    num_of_ppl = int(input(">>> "))
                except ValueError:  # if num entered isn't int
                    error_invalid_num()
                    continue
                else:
                    break
                # type(num_of_ppl) != int or num_of_ppl <= 0:
        return num_of_ppl


def choose_name() -> str:
    """
    Checks and asks for name input from user.
    @return: Name formatted.
    """
    # should choose 1 people each time
    name = input('Choose human name: ')
    name = name.lower().title()  # format the name to be lower cased and titled.
    # check input?
    return name


def choose_bdd() -> datetime.date:
    """
    Manually input from user for man bd.
    @return: Formatted date.
    """
    print("Enter the date of birth in DD MMMM format.")
    print("For example, 02 February")
    bdd = input(">>> ")  # bdd = birthday date
    # write a check for input; check if input is in format. If not - convert it or give error.
    bd_formatted = convert_str_to_date(bdd=bdd)  # convert inout to date time format
    return bd_formatted


def convert_str_to_date(bdd: str) -> str:
    """
    Receives birthdate as str and converts to datetime format.
    @param bdd: Birthdate as str
    @return: Str in Date format.
    """
    import datetime
    bd = datetime.datetime.strptime(bdd, DATE_FORMAT)  # convert input to datetime format
    # the datetime.strptime() class method creates a datetime object from a string representing a date and time
    # and a corresponding format string.
    bd_formatted = datetime.date.strftime(bd, DATE_FORMAT)  # formats the date to words; outputs str
    return bd_formatted


def choose_people(num_of_ppl: int) -> dict:
    """
    For n people in num_of_ppl chooses name manually from choose_name and bd from choose_bdd.
    @param num_of_ppl: Number of people to run the check.
    @return: dict of people and their bd.
    """
    ppl = dict()
    for man in range(num_of_ppl):
        name = choose_name()
        bdd = choose_bdd()
        ppl[name] = bdd
    return ppl


def choose_mode() -> dict:
    """
    Checks with user for his chosen mode of operation for running the program.
    @return: Dict of people and bds to perform the birthday pairs check.
    """
    print('Please choose code running mode, with a number between 1 and 3.')
    print('1. Auto Mode - the machine chooses random people and assigns random birthdays.')
    print('2. Manual Mode - you will choose 23 people and assign their birthdays; csv file can be chosen as well.')
    print('3. Semi Mode - you will choose a number of people, the machine will choose the rest.')

    while True:
        try:  # tries to ask for valid input from user
            mode = int(input('>>> '))
        except ValueError:  # if num isn't int
            error_invalid_num()
            continue
        if mode not in [1, 2, 3]:  # if num isn't in answer
            print("Error, please choose a number from the mode options - a number between 1 and 3.")
            continue
        else:
            break

    if mode == 1:  # Auto mode
        print("You've chosen Automatic Mode.\n")
        print("Enter the amount of people you'd like the machine to automatically check, or press enter for checking "
              "23 people: \n")
        num_of_ppl = auto_num_ppl()
        print(f'Running check on {num_of_ppl} people.\n---------------------------------------')
        ppl = ran_ppl(num_of_ppl=num_of_ppl)  # draw a random set of people.
        bds = assign_birthdays(ppl)  # assign to rand ppl random birthdays.
        return bds  # run the auto function with 23 people.
    elif mode == 2:  # Manual mode
        print("You've chosen Manual Mode.")
        return manual_check()
    elif mode == 3:  # Semi mode
        bold = myStyles.Colors.BOLD
        end = myStyles.Colors.END
        print("You've chosen Semi Mode.")
        print("You will enter the number of people you'd like to check in total and the number of manually checks;"
              "\n For the manual checks, you will manually enter their data, in program or from csv file, and the "
              "program will complete all other people from the total of all people.\n")
        print("For example: total checks - 50, manual - 10; you will enter manually 10, and the program will complete"
              "the other 40.\n--------------------------------------------------------")
        print(f'Enter the {bold}total amount{end} of people you\'d like to check: ')
        num_of_total_ppl = num_ppl()  # number of total people to check
        manual_ppl = manual_check()
        num_of_manual_ppl = len(manual_ppl.keys())  # number of manual people to check
        auto_runs = num_of_total_ppl - num_of_manual_ppl  # num of total people minus num of manually entered ppl.
        auto_ppl = ran_ppl(num_of_ppl=auto_runs)  # draw random ppl for the rest of the people (all-manual).
        auto_bds = assign_birthdays(auto_ppl)  # assign bds to auto people; returns dict of ppl and their bds.
        manual_ppl.update(auto_bds)  # merge the manual dict and the auto dict; auto_bds is pushed to the end.
        all_ppl = dict(manual_ppl)  # creates a new dict of the updated dict just for ease of reading and understanding.
        return all_ppl


def manual_check() -> dict:
    """
    If csv file is wished to be uploaded, returns data from csv; else runs choose people for n times (num_of_ppl).
    @return: Dict of people and their bds.
    """
    usr_csv = use_csv()  # Checks if user has a csv to upload
    if usr_csv:  # if user have a csv file
        print(usr_csv)
        return usr_csv  # return the dictionary from the csv.
    else:  # if user doesnt have csv file
        print("Enter the amount of people you'd like to manually enter: \n")
        num_of_ppl = num_ppl()  # choose how many ppl to run the test
        ppl_bds = choose_people(num_of_ppl)
        print(ppl_bds)
        return ppl_bds


def bdd_csv() -> dict:
    """
    Function checks if header is in csv table and returns a dictionary of people and their bds.
    @return: Dict of name as key and birthday as value from csv file.
    """
    import csv
    print("Please make sure your first column is people's name and the second column is their birthdate, "
          "in the following format: ")
    print("DD MMMM; i.e. - 02 February.\n\n")  # later this should be removed and a cleanup for the date format should
    # be entered.
    print("Please move the CSV file to the same folder with this code.")
    f_name = input("Please enter the file name without extension: ")
    # run check here for extension
    f_name += ".csv"  # adds csv extension to name of file.
    print("Is there a header in your file?")
    print("Enter 1 if there is a header.\nEnter 0 if there is no header.\n")
    hdr = int(input(">>> "))  # hdr = header
    while type(hdr) != int or hdr not in [0, 1]:  # if hdr isn't int or answer isn't 0 or 1.
        hdr = int(input("Please enter a valid answer, between 0 and 1: "))
    with open(f_name) as f_manual_names:
        f_reader = csv.reader(f_manual_names, delimiter=',')
        line = 0  # indicator for line in loop.
        f_ppl = dict()
        for row in f_reader:
            name = row[0].lower().title()  # converts the name to lowercase and first letter uppercase.
            bdd = convert_str_to_date(row[1])
            if row[0] == '':  # if name in csv is empty
                continue
            if hdr == 1 and line == 0:  # if the first line is header
                # print(f'Header: {", ".join(row)}')  # if header is needed to be printed.
                line += 1  # ignore the header by adding 1 to line count.
            elif hdr == 1 and line != 0:
                f_ppl[name] = bdd
            else:  # if there is no header
                f_ppl[name] = bdd  # adds name as key and bdd as value to dict
                line += 1

    return f_ppl


def use_csv():
    """
    Function to check if user wants to use a csv file for bds checks.
    @return: False for no use of file; calls csv function if True (bdd_csv).
    """
    print("Do you want to upload a csv file?")
    print("Enter 0 for No, and 1 for Yes.")
    csv_exist = int(input(">>> "))
    while type(csv_exist) != int or csv_exist not in [0, 1]:
        csv_exist = int(input("Please enter a valid answer, between 0 and 1: "))
    if csv_exist == 0:  # if there is no csv file
        return False
    elif csv_exist == 1:  # if there is a csv file
        return bdd_csv()


def main():
    ppl_bds = choose_mode()  # dict of names and birthdays
    bd_ppl_print(ppl_bds)
    pairs = create_pairs(set(ppl_bds.keys()))
    matching_bds = match_bds(bds=ppl_bds, pairs=pairs)
    probability(num_of_ppl=len(ppl_bds), precision=8)
    print("\n\n-----------------------------------")
    successful_pairs(matching_bds=matching_bds, num_of_ppl=len(ppl_bds))

    # aharonisbds  - name of my csv file for checks
    # write a function that writes some of the data to a csv file.
    # clean csv file data; if date is entered in wrong format.
    # complete flow chart
    # complete documentation


if __name__ == "__main__":
    main()
    # convert_str_to_date("29 October")
