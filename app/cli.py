from app.records import (
    load_records,
    search,
    count_by,
    get_by_id
)


def main():
    records = load_records()

    while True:
        print("\n===== StartupSetu =====")
        print("1. Show all records")
        print("2. Search records")
        print("3. Count by category")
        print("4. Find record by ID")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            for record in records:
                print(record)

        elif choice == "2":
            keyword = input("Enter keyword: ")
            results = search(records, keyword)

            for record in results:
                print(record)

            if not results:
                print("No records found.")

        elif choice == "3":
            counts = count_by(records, "category")

            for category, total in counts.items():
                print(category, ":", total)

        elif choice == "4":
            record_id = input("Enter record ID: ")
            result = get_by_id(records, record_id)

            if result:
                print(result)
            else:
                print("Record not found.")

        elif choice == "5":
            print("Thank you for using StartupSetu!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()