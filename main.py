from data import vendor_list

# Function to retrieve input / vendor for user
def get_vendor_code(vendor_list):
    while True:
        vendor_code = input("Please enter a 4-letter vendor code: ").upper()

        if len(vendor_code) != 4 or not vendor_code.isalpha():
            print("Vendor code must be exactly 4 letters, no numbers.")
            continue  # Continue to the next iteration of the loop

        vendor_info = vendor_list.get(vendor_code)
        if vendor_info:
            print(f"Vendor Name: {vendor_info['name']}")
            print(f"Freight %: {vendor_info['freight']}")
            return vendor_code
        else:
            print("Vendor code not found.")
            return None 

# Function to multiply the freight of the input vendor and return cost of an object
def cost_solution(vendor_list, vendor_code):
    if vendor_code is None:
        return  # Exit the function if vendor_code is None

    vendor_info = vendor_list.get(vendor_code)
    if vendor_info:
        freight = vendor_info.get('freight')
        if isinstance(freight, (int, float)):
            result = (freight * 2) / 100 + 2
            print(f"Calculated value: {result}")
            return result
        else:
            print("Please refer to MSRP Price Listing")
            return "Please refer to MSRP Price Listing"
    else:
        print("Vendor code not found.")
        return "Vendor code not found."


# def get_cost(vendor_list):

# def calculate_price(cost, cost_factor):

# def retail_price_suggestion(price, commission):


def main():

    while True:
        vendor_code = get_vendor_code(vendor_list)
        if vendor_code is not None:
            cost_solution(vendor_list, vendor_code)

        continue_search = input("Would you like to input another code? (y/n): ").lower()
        if continue_search != 'y':
            input("Operation complete! Please press Enter to exit the program.")
            break

main()