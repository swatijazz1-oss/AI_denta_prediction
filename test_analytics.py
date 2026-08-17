from database import get_analytics_data


data = get_analytics_data()


print("Analytics query successful!")

print(
    f"Number of assessments: {len(data)}"
)


for row in data[:3]:

    print(row)