# File to display intro text and version for commission protocol

from version import version_data

def show_commission_protocol_intro():
    version_info = version_data["version"]

    print(r"                                                                                                              ")
    print(r"                                                                                                              ")
    print(r"        ______                          _           _                ____             __                   __ ")
    print(r"       / ____/___  ____ ___  ____ ___  (_)_________(_)___  ____     / __ \_________  / /_____  _________  / / ")
    print(r"      / /   / __ \/ __ `__ \/ __ `__ \/ / ___/ ___/ / __ \/ __ \   / /_/ / ___/ __ \/ __/ __ \/ ___/ __ \/ /  ")
    print(r"     / /___/ /_/ / / / / / / / / / / / (__  |__  ) / /_/ / / / /  / ____/ /  / /_/ / /_/ /_/ / /__/ /_/ / /   ")
    print(r"     \____/\____/_/ /_/ /_/_/ /_/ /_/_/____/____/_/\____/_/ /_/  /_/   /_/   \____/\__/\____/\___/\____/_/    ")
    print(r"                                                                                                              ")
    print(r"                                                                                                              ")
    print(r"                                                                                                              ")

    print("                                            Welcome to Commission Protocol")
    print("---------------------------------------------------------------------------------------------------------------")
    print(f"                                      Beta Version: {version_info['number']}")
    print(f"                                     Latest data update: {version_info['update_data']}")
    print(f"                                         Creator: {version_info['creator']}")
    print("---------------------------------------------------------------------------------------------------------------")