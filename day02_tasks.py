
from data.sample_records import RECORDS

# 1. Print all records
print("\n===== ALL STARTUP RECORDS =====")

for record in RECORDS:
    print(record)


# 2. Search records by keyword
print("\n===== SEARCH RECORDS =====")

keyword = input("Enter keyword to search: ").lower()

results = []

for record in RECORDS:
    if keyword in str(record).lower():
        results.append(record)

for record in results:
    print(record)

print("Total matching records:", len(results))


# 3. Count records per category
print("\n===== CATEGORY COUNT =====")

category_count = {}

for record in RECORDS:
    category = record["category"]

    if category in category_count:
        category_count[category] += 1
    else:
        category_count[category] = 1

for category, count in category_count.items():
    print(category, ":", count)
