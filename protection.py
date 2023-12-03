import questionary

def get_user_choice():
    return questionary.select(
        "Please select a protection plan:",
        choices=['BRONZE', 'SILVER', 'GOLD', 'GOLD + PET', 'NONE']
    ).ask()

def process_choice(choice):
    if choice != 'NONE':
        print(f"{choice} protection plan has been selected.")
        return choice
    else:
        print("Returning to the previous question.")




def choose_protection_plan():
    while True:
        choice = get_user_choice()
        if choice == 'NONE':
            return 'NONE'  # Explicitly return 'NONE' if selected
        else:
            return choice  # Return the selected choice





def get_protection_plan():
    add_protection = questionary.confirm("Would you like to add a protection plan?").ask()
    if add_protection:
        return choose_protection_plan()
    else:
        return 'NONE'





# Overall protection function to export to main/other files


def run_protection_protocol():
    return get_protection_plan()


