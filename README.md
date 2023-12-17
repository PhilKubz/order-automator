# order-automator

![Order Automator screenshot2](https://github.com/PhilKubz/order-automator/assets/122698773/50c05a2f-748b-453b-9cc4-ff76affc3e86)



Order Automator is designed to expedite the special order writing process so that users spend less time figuring out pricing on orders, and more time working with the customer.

Speed, accurarcy of pricing, and up-to-date vendor information are the key focus in this program that provides a simple UI experience for users through an application that is easily naviagted through the order cration process in the console terminal.

Simply start the program and follow inputs until you finish the order creation, where you may: create another order, view orders, or exit the program.

A secondary program, Commission Protocol, also would allow for the ability to check commission codes of an item on sale, as well as find a minimum retail price that will keep the sale at highest commission percentage obtainable. This program would provide high value prices for a customer while ensuring the salesperson does not undercut their pay.



## Table of Contents

[Details](#details)

[Demo](#demo)

[Future Features](future-features)

[Installation](#installation)

[Patch Log](#patch-log)

[Contact](#contact)




## Details

In an effort to simplify/expedite the special order process, this application allows users to minmize downtime during a sale in adition to providing accurate information that can be useful for quicker purchase order writing as well. The data that is used will always be the most up-to-date for vendor information and pricing, thus providing accurate, instant pricing on the orders as well.

A large importance of this program is making it easy to navigate. Many users for this program will not be rather 'tech-savy', so it is crucial to design a program that is straightforward and does not allow users to be lost or misunderstand the process at any given step of the program use.

Program 1: Order Automator
- Designed to automatically price/quote a special order based on criteria that a user inputs.

Program 2: Commission Protocol
1. Check the commission on any given item based on its retail sale and unit cost
2. Determine the lowest retail price possible while maintaining full commission
- Designed in order to allow for proper pricing ranges for special orders to not undercut the company or salesperson



## Demo

v 0.12 Demo:

![Order Automator gif](https://github.com/PhilKubz/order-automator/assets/122698773/6dbf1d46-0c15-4097-858f-c1aecd9bb09f)


## Future Features

- Write unit tests to ensure stability and speed up error catches when implementating new features
- Improved order numbering to display code referencing the date of order
- Storing orders on a server for future reference
- Refactoring code for more scalability/flexibility
- Creating other functionality in different programs, turning all programs into one larger application for more varied usage


## Installation

The application can be made into a .exe application with the use of a pyinstaller command:

- In this application, it is named Order Automator and will make use of any files related to that main.py file that are needed to function

```
pyinstaller --onefile --name "Order Automator" main.py
```


For use of this on the work network, it may be distributed via public access networks for computers on the company file system, hosted for download online, or manually distributed.

Most important is that this application is easily updated when vendor freight changes take place. The current set-up allows for easy data updates to not affect the performance quality of the application, simply update values.
Note: Orders are only stored for a per session usage, currently they are created for simplicity and not stored on any hosted server/database.


## Patch Log

v 0.13: Commission Protocol program created
        This program allows for two programs to be run inside of it:
        - Check commission codes based on vendor, retail price, and unit cost
        - Check minimum retail sale price while staying in proper commission range
        -- Program is functional and reusable in a single session, but will be further updated for storing completed process data
        Introduce package to improvide displaying results

v 0.12: Further improvements with order creation
        Functions refactored to clean-up code
        Slight bux fixes

v 0.11: Improved looping to minmize potential errors running program
        Protection plan implementation
        questionary library used to simplify process
        Intro added
        Bug fixes

v 0.1: Application functions and provides pricing for custom orders with minimal ui involvement


## Contact

GitHub:   [https://github.com/PhilKubz](https://github.com/PhilKubz)

Email:    [philip.kubisz#gmail.com](philip.kubisz#gmail.com)

LinkedIn: [https://www.linkedin.com/in/philipkubisz/](https://www.linkedin.com/in/philipkubisz/)

-- This is a project to both help in the current work environment, as well as learn Python and further my understanding in software engineering. So anything unusual with file structure or usage of Python is purely as a novice learning Python. All skills will be refined, and code improved as I continue work on the project.