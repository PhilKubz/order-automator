from data import vendor_list





# Function to retrieve input / vendor for user
def get_vendor_code(vendor_list):
    while True:
        vendor_code = input("Please enter a 4-letter vendor code: ").upper()

        if len(vendor_code) != 4 or not vendor_code.isalpha():
            print("Vendor code must be exactly 4 letters, no numbers.")
            continue

        vendor_info = vendor_list.get(vendor_code)
        if vendor_info:
            if isinstance(vendor_info['freight'], str) and vendor_info['freight'] == "Refer to the MSRP Price Listing":
                print("Please refer to the MSRP Price Listing, the order automator is not necessary for your order pricing.")
                return None
            else:
                print(f"Vendor Name: {vendor_info['name']}")
                print(f"Freight %: {vendor_info['freight']}")
                return vendor_code
        else:
            print("Vendor code not found.")
            return None




# Function to multiply the freight of the input vendor and return cost of an object
def get_cost_factor(vendor_list, vendor_code):
    if vendor_code is None:
        return  # Exit the function if vendor_code is None

    vendor_info = vendor_list.get(vendor_code)
    if vendor_info:
        freight = vendor_info.get('freight')
        if isinstance(freight, (int, float)):
            cost_factor = (freight * 2) / 100 + 2
            print(f"Calculated value: {cost_factor}")
            return cost_factor
        else:
            print("Please refer to MSRP Price Listing")
            return "Please refer to MSRP Price Listing"
    else:
        print("Vendor code not found.")
        return "Vendor code not found."







# Function to get and return the cost of a single item
def get_item_cost():
    cost = float(input("What is the cost of the item? $"))
    return cost





# Function to handle the overall process of getting costs for items
def process_costs(vendor_list, vendor_code):
    total_costs = []
    cost_factor = get_cost_factor(vendor_list, vendor_code)  # Assuming get_cost_factor is defined

    cost = get_item_cost()
    total_costs.append(cost)

    while True:
        more_items = input("Do you have another item for the order? (y/n): ").lower()
        if more_items != 'y':
            cost_total = sum(total_costs)
            price_estimates, total_price = calculate_price(total_costs, cost_factor)
            show_pricing_table(total_costs, cost_total, price_estimates)
            return False 

        cost = get_item_cost()
        total_costs.append(cost)






# This function takes in total_costs and cost_total, and displays them in a table format
def show_pricing_table(total_costs, cost_total, price_estimates):
    # header
    print(f"{'Item':<10}{'Cost':>10}{'Price':>15}{'Suggested Retail':>20}")
    print("-" * 56)

    # cost, price, and suggested retail price 
    for i, (cost, price) in enumerate(zip(total_costs, price_estimates), start=1):
        suggested_retail = rounded_price(price)
        print(f"{'Item ' + str(i):<10}{cost:>10.2f}{price:>15.2f}{suggested_retail:>20.2f}")

    # Calculate the total suggested retail price based on the total of price_estimates
    total_suggested_retail = rounded_price(sum(price_estimates))

    # Divider and totals row
    print("-" * 56)
    print(f"{'Total':<10}{cost_total:>10.2f}{sum(price_estimates):>15.2f}{total_suggested_retail:>20.2f}")





# Calculate price estimates for each item in total_costs using the cost_factor,
# and compute the total price estimate.



def calculate_price(total_costs, cost_factor):
    
    # Calculate price estimate for each individual cost
    price_estimates = [cost * cost_factor for cost in total_costs]

    # Calculate total price estimate
    total_price_estimate = sum(price_estimates)

    return price_estimates, total_price_estimate





# Function -- def retail_price_suggestion(price, commission):

# Find algorithm to determine if a price is closer to XX49.95 or XX99.95
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



def get_last_two_digits(price_estimates):

    last_two_digits = price_estimates % 100
    return last_two_digits

# Function -- def find_lowest_price(price, commission{A}):

# find lowest amount A code sale price for full commission





# Seperate Function -- : check_commission_code

#  take sale price and find out what the commission code is (using commission dictionary in data.py)








def main():
    while True:
        vendor_code = get_vendor_code(vendor_list)
        if vendor_code is not None:
            continue_program = process_costs(vendor_list, vendor_code)

            if not continue_program:
                input("Operation complete! Please press Enter to exit the program.")
                break 

        # Ask if the user wants to continue with a new vendor code
        continue_search = input("Would you like to input another vendor code? (y/n): ").lower()
        if continue_search != 'y':
            input("Operation complete! Please press Enter to exit the program.")
            break

main()