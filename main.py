from data import vendor_list
from protectionData import protection_cost_data
from intro import show_intro
from protection import run_protection_protocol

import sys
import questionary
import random
import string


# global variable that all created orders are placed into
all_orders = []


# -------------------------------------------------- User Input ---------------------------------------------------


# Retrieve user input for the vendor

def get_vendor_code(vendor_list):
    while True:
        vendor_code = input("Please enter a 4-letter vendor code or 'other' for more options: ").upper()

        if vendor_code == 'OTHER':
            return 'OTHER'

        if len(vendor_code) != 4 or not vendor_code.isalpha():
            print("Vendor code must be exactly 4 letters, no numbers.")
        else:
            vendor_info = vendor_list.get(vendor_code)
            if vendor_info:
                print(f"Vendor Name: {vendor_info['name']}")
                return vendor_code
            else:
                print("Vendor code not found.")

        # Offer choices after handling invalid or unrecognized codes
        action = handle_vendor_error(vendor_list)
        if action == 'Enter a vendor code':
            continue
        elif action == 'Select vendor from list':
            return select_vendor_from_list(vendor_list)





# Function to handle vendor errors

def handle_vendor_error(vendor_list):
    return questionary.select(
        "What would you like to do?",
        choices=["Enter a vendor code", "Select vendor from list"]
    ).ask()




# Provide a list of vendors if user chooses to do so
# Allows for more simplified ui interaction / newer employee success of completing program

def select_vendor_from_list(vendor_list):
    vendor_names = [info['name'] for code, info in vendor_list.items()]
    selected_name = questionary.select(
        "Please select a vendor:",
        choices=vendor_names
    ).ask()

    # Find vendor code corresponding to the selected name
    for code, info in vendor_list.items():
        if info['name'] == selected_name:
           #  print(f"Vendor Name: {vendor_info['name']}")
            print(f"Selected Vendor Code: {code}")
            return code




# Get and return the cost of an item
# - used in process_costs to work on the user input of cost(s)

def get_item_cost():
    while True:
        try:
            cost_input = input("What is the cost of the item? $")
            cost = float(cost_input)
            return cost
        except ValueError:
            print("The cost must be a number.")
            continue_order = questionary.confirm("Would you like to continue with the order?").ask()
            if not continue_order:
                return None





# Handle the overall process of getting costs for items and appending them to the order

def process_costs(vendor_list, vendor_code):
    cost_factor = get_cost_factor(vendor_list, vendor_code)
    if cost_factor in ["restart", "exit"]:
        return None, None, None, cost_factor  # Return the action

    total_costs = get_item_costs()
    if total_costs is None:  # No items added or user chose not to continue
        return None, None, None, "not_confirmed"

    order_confirmed = questionary.confirm(f"You have selected {len(total_costs)} items for the order, is this correct?").ask()
    if not order_confirmed:
        return None, None, None, "not_confirmed"

    cost_total = sum(total_costs)
    price_estimates, _ = calculate_price(total_costs, cost_factor)
    return total_costs, cost_total, price_estimates, "confirmed"



# Function to get costs - used in process_costs

def get_item_costs():
    total_costs = []
    while True:
        cost = get_item_cost()
        if cost is None:  # User chose not to continue during cost input
            return None

        total_costs.append(cost)

        more_items = questionary.confirm("Do you have another item for the order?").ask()
        if not more_items:
            break

    return total_costs




# Function to avoid errors going through the program, allowing restarting or exiting the order when currently in the process

def handle_order_action(action, total_costs, cost_factor):
    if action == "Restart the order":
        return None, None, None  # Signal to restart order
    elif action == "Exit the program":
        return None, None, None  # Signal to exit  program
    else:
        if total_costs:
            cost_total = sum(total_costs)
            price_estimates, total_price = calculate_price(total_costs, cost_factor)
            return total_costs, cost_total, price_estimates
        else:
            return None, None, None  # No items, signal to restart or exit





def handle_order_decision():
    action = questionary.select(
        "How would you like to continue?",
        choices=["Restart the order", "Exit the program"]
    ).ask()

    return action





# Confirm items a proceed with process_cost to avoid errors

def check_order(item_count):
    correct = questionary.confirm(f"You have selected {item_count} items for the order, is this correct?").ask()
    if not correct:
        return handle_order_decision()
    return "Continue"




# ---------------------------------------------------User Input Complete ----------------------------------------------
# ----------------------------------------------------- Calculations ---------------------------------------------------


# Determine the cost of an item
# - multiply the (vendor freight * cost_factor) and return cost of an object
# - if vendor has strict MSRP price listing, return statement saying so to avoid errors

def get_cost_factor(vendor_list, vendor_code):
    vendor_info = vendor_list.get(vendor_code)
    if vendor_info:
        freight = vendor_info.get('freight')
        if isinstance(freight, (int, float)):
            cost_factor = (freight * 2) / 100 + 2
            return cost_factor
        else:
            print("Please refer to MSRP Price Listing")
            action = handle_order_decision()
            if action == "Restart the order":
                return "restart"  # Indicate to restart the order
            elif action == "Exit the program":
                return "exit"  # Indicate to exit the program
    else:
        print("Vendor code not found.")
        return "restart"  # Default to restart if the vendor code is not found




# Extract the last two digits of a price
# - used inside of rounded_price

def get_last_two_digits(price_estimates):

    last_two_digits = price_estimates % 100
    return last_two_digits





# Determine a retail suggested price
# - rounds the price_estimate to be used/displayed in the table
# - determine if a price is closer to XX49.95 or XX99.95

def rounded_price(price_estimates):

    last_two_digits = get_last_two_digits(price_estimates)

    if last_two_digits <= 24:
        # Lower the price by 100 and round up to 99.95
        rounded_price = price_estimates - 100 - last_two_digits + 99.95
    elif last_two_digits <= 74:
        # Round to the nearest 49.95
        rounded_price = price_estimates - last_two_digits + 49.95
    else:
        # Round up to the nearest 99.95
        rounded_price = price_estimates - last_two_digits + 99.95

    return rounded_price




# Calculate price estimates for each item in total_costs using the (cost_factor * cost)
# - computes the:
# -- price_estimates &
# -- total_price_estimate (which is the sum of all price_estimates).

def calculate_price(total_costs, cost_factor):
    # Calculate price estimate for each individual cost
    price_estimates = [(cost * cost_factor) for cost in total_costs]

    # Calculate total price estimate
    total_price_estimate = sum(price_estimates)

    return price_estimates, total_price_estimate




# Function to calculate totals to return for printing in table/summary

def calculate_totals(total_costs, cost_factor, protection_choice, protection_cost_data):
    # Calculate price estimates
    price_estimates, _ = calculate_price(total_costs, cost_factor)

    # Calculate total suggested retail
    total_price_estimate = sum(price_estimates)
    total_suggested_retail = rounded_price(total_price_estimate)

    # Calculate total protection cost
    total_protection_cost = calculate_protection_cost(total_suggested_retail, protection_choice, protection_cost_data)

    # Calculate total retail with protection
    total_retail_with_protection = total_suggested_retail + total_protection_cost

    return total_price_estimate, total_suggested_retail, total_protection_cost, total_retail_with_protection




# Function to calculate cost of proteciton plan based on suggested retail and choice of proteciton tier

def calculate_protection_cost(suggested_retail, choice, protection_cost_data):

    if choice is None or choice == 'NONE':
        return 0

    choice = choice.upper()  # Ensure the choice is uppercase to match the keys
    for (lower_bound, upper_bound), cost_info in protection_cost_data.items():
        if lower_bound <= suggested_retail <= upper_bound:
            cost = cost_info.get(choice, 0)
            
            if isinstance(cost, str):
                # Handle percentage-based cost for higher ranges (based on a specific % of sale as stored in the protectionData file)
                if '%' in cost:
                    percentage = float(cost.rstrip('% OF SALE')) / 100
                    return suggested_retail * percentage
                else:
                    # Handle special cases, if any, where cost might be a string but not a percentage
                    pass
            else:
                # Handle fixed cost for lower ranges
                return cost
    return 0



# ------------------------------------------------ Calculations complete -----------------------------------------------------------
# --------------------------------------------------- formatting Data --------------------------------------------------------------


# Table formatted to display the object: order
# - rounded_price() function is used in this function to determine retail costs

def show_pricing_table(order):
    total_costs = [item['Cost'] for item in order['Items']]
    price_estimates = [item['Price Estimate'] for item in order['Items']]
    total_suggested_retail = order['Total Suggested Retail']
    include_protection = order['Protection Plan'] != 'NONE'
    
    header = f"{'Item':<10}{'Cost':>10}{'Price':>15}{'Suggested Retail':>25}"
    if include_protection:
        header += f"{'Retail + Protection':>27}"
    print("")
    print(header)
    print("-" * len(header))

    for i, (cost, price) in enumerate(zip(total_costs, price_estimates), start=1):
        line = f"{'Item ' + str(i):<10}{cost:>10.2f}{price:>15.2f}{rounded_price(price):>20.2f}"
        if include_protection:
            line += f"{'-----':>25}"  # Placeholder for individual item protection cost, as it is not needed
        print(line)

    total_protection_cost = order.get('Total Protection Cost', 0)
    total_retail_with_protection = total_suggested_retail + total_protection_cost

    total_line = f"{'Total':<10}{sum(total_costs):>10.2f}{sum(price_estimates):>15.2f}{total_suggested_retail:>20.2f}"
    if include_protection:
        total_line += f"{total_retail_with_protection:>25.2f}"
    print("-" * len(header))
    print(total_line)





# summary shown in simple format for order

def show_order_summary(order):
    item_count = len(order['Items'])
    total_suggested_retail = order['Total Suggested Retail']
    protection_choice = order['Protection Plan']
    total_protection_cost = order.get('Total Protection Cost', 0)
    total_retail_with_protection = total_suggested_retail + total_protection_cost

    print("")
    print("\nOrder Summary:")
    if protection_choice != 'NONE':
        print(f"The order consisting of {item_count} item(s) with a suggested retail of ${total_suggested_retail:.2f}")
        print(f"The {protection_choice} Protection Plan for this order would cost ${total_protection_cost:.2f}")
        print(f"The total order with protection plan would cost ${total_retail_with_protection:.2f}")
    else:
        print("No protection plan selected.")
        print(f"The order consisting of {item_count} items has a suggested retail of ${total_suggested_retail:.2f}")




# Function to handle action of user after a successful order completion

def handle_post_order_decision():
    print("")
    action = questionary.select(
        "What would you like to do next?",
        choices=["Begin a new order", "View orders", "Exit the program"]
    ).ask()

    return action




# Function to generate a random id for successfully created orders

def generate_order_id(vendor_code):
    # Generate a random sequence of 6 characters (both letters and numbers)
    random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    # ID will always be vendor code + 6 randomized characters
    return f"{vendor_code}-{random_id}"




# Function to create an object named Order upon successfull order completion

def create_order(total_costs, price_estimates, total_price, total_suggested_retail, total_protection_cost, protection_choice, vendor_code):
    order_id = generate_order_id(vendor_code)
    if protection_choice == 'NONE':
        total_protection_cost = 0
        total_retail_with_protection = total_suggested_retail
    else:
        total_retail_with_protection = total_suggested_retail + total_protection_cost

    order = {
        "Order ID": order_id,
        "Items": [{"Cost": cost, "Price Estimate": price, "Suggested Retail": rounded_price(price)} for cost, price in zip(total_costs, price_estimates)],
        "Total Price": total_price,
        "Total Suggested Retail": total_suggested_retail,
        "Protection Plan": protection_choice,
        "Total Protection Cost": total_protection_cost,
        "Total Retail with Protection": total_retail_with_protection
    }
    all_orders.append(order)
    return order




# Function to view orders created 

def view_orders():
    if not all_orders:
        print("No orders available to view.")
        return

    order_ids = [order['Order ID'] for order in all_orders] + ["Exit"]
    selected_order_id = questionary.select(
        "Select an order to view or 'Exit' to go back:",
        choices=order_ids
    ).ask()

    if selected_order_id == "Exit":
        return

    selected_order = next((order for order in all_orders if order['Order ID'] == selected_order_id), None)
    if selected_order:
        # Show order details using the selected order object
        show_pricing_table(selected_order)
        show_order_summary(selected_order)
    else:
        print("Order not found.")




# Function to end the program

def end_program():
    print("")
    print("Order Completed!")
    input("Please press Enter to exit the program.")
    sys.exit()



# ----------------------------------------------------- Main Function ----------------------------------------------


# Runs the program

def main():
    show_intro()

    while True:
        vendor_code = get_vendor_code(vendor_list)

        if vendor_code == 'OTHER':
            post_order_action = handle_post_order_decision()
            if post_order_action == "Begin a new order":
                continue  # Restart the program from the beginning
            elif post_order_action == "View orders":
                if not all_orders:
                    print("No orders available to view.")
                else:
                    view_orders()  # View existing orders
                continue  # After viewing orders, prompt for next action
            elif post_order_action == "Exit the program":
                end_program()  # Exit the program
                break
            continue  # Go back to the start of the loop

        if vendor_code is None:
            end_program()  # Exit if 'exit' is entered or end the program
            break

        cost_factor = get_cost_factor(vendor_list, vendor_code)
        if cost_factor in ["restart", "exit"]:
            continue  # Restart the order process from the beginning or exit

        total_costs, cost_total, price_estimates, order_status = process_costs(vendor_list, vendor_code)

        if order_status == "confirmed":
            protection_choice = run_protection_protocol()
            total_price, total_suggested_retail, total_protection_cost, total_retail_with_protection = calculate_totals(
                total_costs, cost_factor, protection_choice, protection_cost_data
            )

            # Create the order object
            order = create_order(
                total_costs, price_estimates, total_price, total_suggested_retail, total_protection_cost, protection_choice, vendor_code
            )

            # Print table and summary to CLI
            show_pricing_table(order)
            show_order_summary(order)

            print(f"Order ID: {order['Order ID']} has been successfully created.")

        while True:
            post_order_action = handle_post_order_decision()
            if post_order_action == "Begin a new order":
                break  # Exit the loop to restart the program from the beginning
            elif post_order_action == "View orders":
                if not all_orders:
                    print("No orders available to view.")
                else:
                    view_orders()  # View existing orders
                continue  # After viewing orders, prompt for next action
            elif post_order_action == "Exit the program":
                end_program()  # Exit the program
                return  # Return to exit the main function

        if order_status in ["restart", "exit", "not_confirmed"]:
            continue  # Restart the order process, exit, or handle unconfirmed order

    end_program()  # Ensure program ends gracefully after the loop

main()











# ------------------------------------------------------ Ideas ---------------------------------------------------------------


# Function -- def find_lowest_price(price, commission{A}):

# find lowest amount A code sale price for full commission





# Seperate Function -- : check_commission_code

#  take sale price and find out what the commission code is (using commission dictionary in data.py)





