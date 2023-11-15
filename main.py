from data import vendor_list






def get_vendor_code(vendor_list):
    while True:
        vendor_code = input("Please enter a 4-letter vendor code: ").upper()

        if len(vendor_code) != 4 or not vendor_code.isalpha():
            print("Vendor code must be exactly 4 letters, no numbers.")
            # Don't return; instead, continue to the next iteration of the loop
            continue

        vendor_info = vendor_list.get(vendor_code)
        if vendor_info:
            print(f"Vendor Name: {vendor_info['name']}")
            print(f"Freight %: {vendor_info['freight']}")
            break  # Break out of the loop if the vendor code is found
        else:
            print("Vendor code not found.")
            # Don't return; instead, continue to the next iteration of the loop
            continue

def main():
    get_vendor_code(vendor_list)

main()