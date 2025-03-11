import sqlite3
import random
import datetime

# Create a connection to SQLite database
conn = sqlite3.connect('manufacturing_qc.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS QualityControl (
    Product_ID TEXT,
    Batch_Number TEXT,
    Temperature REAL,
    Pressure REAL,
    Defect_Rate REAL,
    Production_Date TEXT,
    Factory_Location TEXT
)
''')

# Generate dummy data
def generate_dummy_data(n=100):
    factory_locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
    data = []
    for _ in range(n):
        product_id = f"P{random.randint(1000, 9999)}"
        batch_number = f"B{random.randint(100, 999)}"
        temperature = round(random.uniform(20, 100), 2)
        pressure = round(random.uniform(1, 10), 2)
        defect_rate = round(random.uniform(0, 5), 2)
        production_date = (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        factory_location = random.choice(factory_locations)
        data.append((product_id, batch_number, temperature, pressure, defect_rate, production_date, factory_location))
    return data

# Insert dummy data
data = generate_dummy_data(100)
cursor.executemany('''INSERT INTO QualityControl VALUES (?, ?, ?, ?, ?, ?, ?)''', data)

# Commit and close connection
conn.commit()
conn.close()

print("Dummy data inserted into manufacturing_qc.db")
