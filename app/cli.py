
from app.records import (
    load_records,
    search,
    count_by,
    get_by_id
)


def main():

    # Load records from records.json
    try:
        records = load_records()
    except (FileNotFoundError, ValueError) as error:
        print("Error loading records:", error)
        print("Please run: python -m app.ingest")
        return

    while True:

        print("\n========== StartupSetu ==========")
        print("1. Show all records")
        print("2. Search records")
        print("3. Count records by category")
        print("4. Find record by ID")
        print("5. Exit")
        print("=================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            print("\nAll Startup Records:")

            for record in records:
                print("\n", record)

        elif choice == "2":

            keyword = input("Enter search keyword: ").strip()

            results = search(records, keyword)

            if results:
                print("\nSearch Results:")

                for record in results:
                    print("\n", record)
            else:
                print("No records found.")

        elif choice == "3":

            counts = count_by(records, "category")

            print("\nCategory-wise Record Count:")

            for category, total in counts.items():
                print(category, ":", total)

        elif choice == "4":

            record_id = input("Enter record ID: ").strip()

            result = get_by_id(records, record_id)

            if result:
                print("\nRecord Found:")
                print(result)
            else:
                print("Record not found.")

        elif choice == "5":

            print("Thank you for using StartupSetu!")
            break

        else:

            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
