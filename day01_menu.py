while True:

    print("\n===== AI Learning Assistant =====")
    print("1. About Project")
    print("2. Sample Questions")
    print("3. Check Learning Level")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("This project helps students learn AI.")

    elif choice == "2":
        print("1. What is AI?")
        print("2. What is Machine Learning?")
        print("3. What is Generative AI?")

    elif choice == "3":

        level = input("Enter your level: ")

        if level == "beginner":
            print("Start with Python and AI basics.")

        elif level == "intermediate":
            print("Start with Machine Learning.")

        else:
            print("Invalid learning level.")

    elif choice == "0":
        print("Thank you!")
        break

    else:
        print("Invalid choice!")