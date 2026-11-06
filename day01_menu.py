
while True:

    print("\n===== STARTUP RECOGNITION GUIDE =====")
    print("1. About Project")
    print("2. Sample Questions")
    print("3. Business Structure Check")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        print("\nProduct: DPIIT Startup Recognition Guide")
        print("Users: Student Founders")
        print("Example: Agricultural Drone Startup")

    elif choice == "2":

        print("\nSample Questions:")
        print("1. What is DPIIT recognition?")
        print("2. What are the tax benefits?")
        print("3. What is IPR support?")
        print("4. What funding schemes are available?")
        print("5. What Maharashtra incentives are available?")

    elif choice == "3":

        plan = input(
            "Do you plan to raise equity investment? (yes/no): "
        )

        if plan == "yes":
            print("Private Limited Company may be suitable.")

        elif plan == "no":
            print("LLP may be suitable for a flexible partnership.")

        else:
            print("Please enter yes or no.")

    elif choice == "0":

        print("Thank you for using Startup Recognition Guide!")
        break

    else:

        print("Invalid choice. Try again.")
