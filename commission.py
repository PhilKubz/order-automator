from commissionData import commission_code_data
from vendorData import vendor_list
from commissionProtocolIntro import show_commission_protocol_intro

from prettytable import PrettyTable
import questionary
import sys




# -------------------------------------------------- User Input ---------------------------------------------------


# Retrieve user input for the vendor

def get_vendor_code(vendor_list):
    while True:
        vendor_code = input("Please enter a 4-letter vendor code or 'other' for more options: ").upper()

        if len(vendor_code) == 4 and vendor_code.isalpha():
            vendor_info = vendor_list.get(vendor_code)
            if vendor_info:
                print(f"Vendor Name: {vendor_info['name']}")
                return vendor_code
            else:
                print("Vendor code not found.")
        
        action = handle_vendor_error(vendor_list)
        if action == 'Enter a vendor code':
            continue
        elif action == 'Select vendor from list':
            return select_vendor_from_list(vendor_list)
        elif vendor_code == 'OTHER':
            return None  # User wants to go back to the main menu




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




# Function to check if continuing function

def ask_to_continue(prompt_message):
    continue_decision = questionary.confirm(prompt_message).ask()
    return continue_decision




# Function to get freight percentage based on vendor code
def get_freight_percentage(vendor_code):
    vendor_info = vendor_list.get(vendor_code)
    if vendor_info and 'freight' in vendor_info:
        return vendor_info['freight']
    return 0  # Default to 0 if no freight info is available




# Function to get user input of item's retail sale price
# - return the value

def get_retail_price():
    while True:
        try:
            retail_price_input = input("Please enter the retail sale price of the unit $")
            retail_price = float(retail_price_input)
            return retail_price
        except ValueError:
            print("Retail price must be a number.")
            if not ask_to_continue("Would you like to continue entering the retail price?"):
                return None



# Function to retrieve unit_cost from user

def get_sale_unit_cost():
    while True:
        try:
            unit_cost_input = input("Please enter the cost of the unit $")
            unit_cost = float(unit_cost_input)
            return unit_cost
        except ValueError:
            print("Cost must be a number.")
            if not ask_to_continue("Would you like to continue entering the unit cost?"):
                return None

            



# Function to confirm details of the process
# - Allows user to restart, choose another program, or exit the program as well

def handle_process_decision(item_description, current_function):
    confirmation = questionary.confirm(f"Confirm the following details: {item_description}").ask()
    if not confirmation:
        action = questionary.select(
            "How would you like to continue?",
            choices=["Restart this process", "Choose another program", "Exit the program"]
        ).ask()

        if action == "Restart this process":
            return "restart"
        elif action == "Choose another program":
            return "choose_another"
        elif action == "Exit the program":
            end_program()

    return "confirmed"






# Function to determine user's next steps after completing a process

def handle_post_operation_decision():
    action = questionary.select(
        "What would you like to do next?",
        choices=["Choose another program", "Exit the program"]
    ).ask()

    if action == "Choose another program":
        run_commission_protocol()  # Go back to the main menu
    elif action == "Exit the program":
        end_program()  # Exit the program immediately






# Function to determine user's desired program choice, or exit the program

def user_selection_menu():
    return questionary.select(
        "Choose an option:",
        choices=[
            "Check Commission Code",
            "Find Minimum Retail Price",
            "Exit the Program"
        ]).ask()




# Function to check validity of commission code found

def is_valid_commission(result):
    return result is not None



# Function to end the program

def end_program():
    print("")
    print("Process Completed!")
    input("Please press Enter to exit the program.")
    sys.exit()




# ---------------------------------------------------User Input Complete ----------------------------------------------
# ----------------------------------------------------- Calculations ---------------------------------------------------



# Function to calculate the percentage margin of the sale
# - Return the % value

def calculate_percentage_margin(retail_price, unit_cost, freight_percentage):
    if retail_price <= 0:
        return None 

    total_cost = unit_cost + (unit_cost * freight_percentage / 100)
    profit_margin = ((retail_price - total_cost) / retail_price) * 100
    return profit_margin




# Function to use the % margin of sale calculated and reference the commissionData to the return code from the dictionary
# - Codes will be: A, X, C, H, or Y
# - - Return the commission code value

def find_commission_code(profit_margin, commission_data):
    for code, info in commission_data.items():
        if info["range"][0] <= profit_margin <= info["range"][1]:
            return code, info["percentage"]
    return None  # Return None if no matching range is found




# Function ysed with commission_pricer()
# - determines two values that returned for displaying retail values based on: vendor(frieght %), unit_cost, and desired_profit_margin

def calculate_minimum_retail_price(unit_cost, freight_percentage, desired_profit_margin):
    if unit_cost <= 0 or desired_profit_margin <= 0:
        return None, None

    total_cost = unit_cost + (unit_cost * freight_percentage / 100)
    minimum_retail_price = total_cost / (1 - (desired_profit_margin / 100))
    minimum_retail_price_rounded_up = round_up_price(minimum_retail_price)

    return minimum_retail_price, minimum_retail_price_rounded_up




# Function to round minimum retail up to a xx9.95 price

def round_up_price(price):
    # Extract the part of the price after the tens place
    decimal_part = price % 10

    # If the decimal part is already over 9.95, round up to the next tenth's 9.95
    if decimal_part > 9.95:
        return price + (10 - decimal_part) + 9.95 - 10
    else:
        # Otherwise, round up to the current tenth's 9.95
        return price - decimal_part + 9.95






# ------------------------------------------------ Calculations complete -----------------------------------------------------------
# --------------------------------------------------- formatting Data --------------------------------------------------------------



# Function to display the data of the commission_check process
# - take in the necessary values to then format in a PrettyTable for clean result viewing

def display_commission_results(vendor_code, profit_margin, retail_price, unit_cost, commission_code, commission_percentage):
    table = PrettyTable()
    table.field_names = ["Vendor", "Retail Price", "Unit Cost", "Profit Margin", "Commission Code", "Commission %"]
    table.add_row([vendor_code, f"{retail_price:.2f}%", f"{unit_cost}", f"{profit_margin:.2f}%", commission_code, f"{commission_percentage}%"])
    
    print("\nCommission Check Results:")
    print(table)



# Function to display the data of the commission_pricer process
# - take in the necessary values to then format in a PrettyTable for clean result viewing

def display_pricing_results(vendor, unit_cost, desired_profit_margin, minimum_retail_price, minimum_retail_price_rounded_up):
    table = PrettyTable()
    table.field_names = ["Vendor", "Unit Cost", "Profit Margin %", "Minimum Retail Price", "Rounded Up Price" ]
    table.add_row([vendor, f"{unit_cost}", f"{desired_profit_margin}", f"{minimum_retail_price:.2f}", f"{minimum_retail_price_rounded_up}"])

    print("\nMinimum Retail Price Results:")
    print(table)




# ------------------------------------------------ Formatting data complete -----------------------------------------------------------
# --------------------------------------------------- Major Functions --------------------------------------------------------------


# Function to determine the commission code of an item being sold

def run_commission_check():
    vendor_code = get_vendor_code(vendor_list)
    if vendor_code is None:
        return  # Go back to the main menu

    freight_percentage = get_freight_percentage(vendor_code)
    retail_price = get_retail_price()
    unit_cost = get_sale_unit_cost()

    decision = handle_process_decision(f"Vendor: {vendor_code}, Retail Price: ${retail_price}, Unit Cost: ${unit_cost}", run_commission_check)
    if decision == "restart":
        return run_commission_check()
    elif decision == "choose_another":
        return
    elif decision != "confirmed":
        return  # Go back based on the user's choice

    profit_margin = calculate_percentage_margin(retail_price, unit_cost, freight_percentage)
    commission_result = find_commission_code(profit_margin, commission_code_data)
    
    if is_valid_commission(commission_result):
        commission_code, commission_percentage = commission_result
    else:
        commission_code, commission_percentage = None, None
        print("No matching commission code found.")

    display_commission_results(vendor_code, profit_margin, retail_price, unit_cost, commission_code, commission_percentage)




# Function to determine minimum retail price in a desired commission code range

def run_commission_pricer():
    vendor_code = get_vendor_code(vendor_list)
    if vendor_code is None:
        return  # Go back to the main menu

    freight_percentage = get_freight_percentage(vendor_code)
    unit_cost = get_sale_unit_cost()

    decision = handle_process_decision(f"Vendor: {vendor_code}, Unit Cost: ${unit_cost}", run_commission_pricer)
    if decision == "restart":
        return run_commission_pricer()
    elif decision == "choose_another":
        return
    elif decision != "confirmed":
        return  # Go back based on the user's choice

    desired_profit_margin = 47  
    minimum_retail_price, minimum_retail_price_rounded_up = calculate_minimum_retail_price(unit_cost, freight_percentage, desired_profit_margin)
    
    display_pricing_results(vendor_code, unit_cost, desired_profit_margin, minimum_retail_price, minimum_retail_price_rounded_up)



# ------------------------------------------------ Major Functions complete -----------------------------------------------------------
# ----------------------------------------------  Primary Program application ---------------------------------------------------------


# Main Function

def run_commission_protocol():

    show_commission_protocol_intro()

    while True:
        choice = user_selection_menu()
        
        if choice == "Check Commission Code":
            run_commission_check()
        elif choice == "Find Minimum Retail Price":
            run_commission_pricer()
        elif choice == "Exit the Program":
            end_program()
            break

run_commission_protocol()