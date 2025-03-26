# Functions go here
import pandas
import random

def generate_statement(statement, decoration, lines):
    """will make the headings (3 lines), subheadings(2 lines) and emphasised text / mini-heading (1 line).
       Only use emoji for single line statements"""

    middle = f"{decoration * 3} {statement} {decoration * 3}"
    top_bottem = decoration * len(middle)

    if lines == 1:
        print(middle)
    elif lines == 2:
        print(middle)
        print(top_bottem)

    else:
        print(top_bottem)
        print(middle)
        print(top_bottem)


def string_checker(question, valid_ans_list=('yes', 'no'), num_letters=1):
    """checks for users awser and checks it against a walid responce list"""

    while True:

        responce = input(question).lower()

        for item in valid_ans_list:

            if responce == item:
                return item

            # check if it's the first letter
            elif responce == item[:num_letters]:
                return item

        print(f"please choose an option from {valid_ans_list}")


def instruction():
    generate_statement("Instructions", "⚠️", 1)
    print('''

    For each ticket holder enter ...
    -Thier name
    -Thier name
    -The payment method (cash or credit)
    The program will record the ticket sale and calculate the ticket cost
    (and the profit).
    Once you have either sold all of the tickets or entered the
    exit code ('xxx'), the program will display the ticket sales information
    and write the data to a text file.

    It will also choose one lucky ticket holder 
    who wins the draw (their ticket is free).
    ''')


def not_blank(question):
    """checks that the user response is not blank"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("please fill this in. \n to try again")


def int_check(question):
    error = "oops - please enter an integer."

    while True:

        try:

            response = int(input(question))

            return response

        except ValueError:
            print(error)


def currency(x):
    """formats number as currency ($#.##)"""
    return "${:.2f}".format(x)


# main routine
# Initialise ticket numbers

MAX_TICKET = 5
tickets_sold = 0

# intailise variables / non defult opitions
payment_ans = ('cash', 'credit')

# ticket price
CHILD_PRICE = 7.50
ADULT_PRICE = 10.50
SENOIR_PRICE = 6.50

# lists to hold tickets details
all_names = []
all_ticket_costs = []
all_surcharges = []

mini_movie_dict = {
    'Name': all_names,
    'Ticket Price': all_ticket_costs,
    'Surcharge': all_surcharges
}
# credit surcharge 5%
CREDIT_SURCHARGE = 0.05

generate_statement("mini-movie fundraiser program", "😁", 1)

print()
want_instruction = string_checker("do you want to read the instructions")

if want_instruction == "yes":
    instruction()

print()

while tickets_sold < MAX_TICKET:
    name = not_blank("Name: ")

    if name == "xxx":
        break

    # ask for their age and check that there between 12-120 years old
    age = int_check("Age: ")

    # output error message / success message
    if age < 12:
        print(f"{name} is too young")
        continue
    elif age > 120:
        print(f"{name} is too old")
        continue

        # child ticket price
    elif age < 16:
        ticket_price = CHILD_PRICE

    elif age < 65:
        ticket_price = ADULT_PRICE

    elif age < 121:
        ticket_price = SENOIR_PRICE

    else:
        print(f"{name} is too old")
        continue

    pay_method = string_checker("payment method: ", payment_ans, 2)

    if pay_method == "cash":
        surcharge = 0

    # if paying by credit, calculate surcharge
    else:
        surcharge = ticket_price * CREDIT_SURCHARGE

    all_names.append(name)
    all_ticket_costs.append(ticket_price)
    all_surcharges.append(surcharge)

    tickets_sold += 1

# end of ticket loop

# create dataframe / table from dictionary
mini_movie_frame = pandas.DataFrame(mini_movie_dict)

# create dataframe / table from dicionary
mini_movie_frame = pandas.DataFrame(mini_movie_dict)

# Calculate the total payable and profit for each ticket
mini_movie_frame['Total'] = mini_movie_frame['Ticket Price'] + mini_movie_frame['Surcharge']
mini_movie_frame['Profit'] = mini_movie_frame['Ticket Price'] - 5

# work out the total paid and total profit...
total_paid = mini_movie_frame['Total'].sum()
total_profit = mini_movie_frame['Profit'].sum()

# Currency Formatting (uses currency function)
add_dollars = ['Ticket Price', 'Surcharge', 'Total', 'Profit']
for var_item in add_dollars:
    mini_movie_frame[var_item] = mini_movie_frame[var_item].apply(currency)

# output movie frame without index
print(mini_movie_frame.to_string(index=False))
print()
print(f"Total paid: ${total_paid:.2f}")
print(f"Total profit ${total_profit:.2f}")

# choose random winner...
winner = random.choice(all_names)

# find index of the winner(ie: position in lost)
winner_index = all_names.index(winner)
print("winner", winner, "list position", winner_index,)

# retrieve Total won
total_won = mini_movie_frame.at[winner_index, 'Total']

# Winner announcement
print(f"The lucky winner is {winner}. Thier ticket worth ${total_won} is free!")


if tickets_sold == MAX_TICKET:
    print(f"You have sold all the tickets (ie: {MAX_TICKET} tickets")
else:
    print(f"You have sold {tickets_sold} / {MAX_TICKET} tickets")
