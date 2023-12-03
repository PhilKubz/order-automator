# File to display intro text and version

from version import version_data

def show_intro():
    version_info = version_data["version"]

    print(r"                                                                       ")
    print(r"    ____         __         ___       __                  __           ")
    print(r"   / __ \_______/ /______  / _ |__ __/ /____  __ _  ___ _/ /____  ____ ")
    print(r"  / /_/ / __/ _  / -_ __/ / __ / // / __/ _ \/  ' \/ _ `/ __/ _ \/ __/ ")
    print(r"  \____/_/  \_,_/\__/_/  /_/ |_\_,_/\__/\___/_/_/_/\_,_/\__/\___/_/    ")   
    print(r"                                                                       ")
    print(r"                                                                       ")
    print(r"                                                                       ")

    print("                      Welcome to Order Automator")
    print("-----------------------------------------------------------------------")
    print(f"                         Beta Version: {version_info['number']}")
    print(f"                     Latest data updated: {version_info['update_data']}")
    print(f"                        Creator: {version_info['creator']}")
    print("-----------------------------------------------------------------------")

