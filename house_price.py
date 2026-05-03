import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Create realistic Mumbai housing dataset 
np.random.seed(42)
n = 500  # 500 house records

# Mumbai areas with their base price per sqft (₹)
areas = {
    'Bandra':        45000,
    'Juhu':          40000,
    'Andheri':       25000,
    'Powai':         22000,
    'Borivali':      18000,
    'Thane':         13000,
    'Navi Mumbai':   11000,
    'Mira Road':      9000,
    'Virar':          7000,
    'Panvel':         6500,
}

area_names = list(areas.keys())
area_prices = list(areas.values())

# Randomly assign localities to 500 houses
locality_indices = np.random.randint(0, len(area_names), n)
localities       = [area_names[i] for i in locality_indices]
base_prices      = [area_prices[i] for i in locality_indices]

# Generate realistic features
sqft   = np.random.randint(400, 2500, n)           # 400 to 2500 sqft
bhk    = np.random.randint(1, 5, n)                # 1 to 4 BHK
floor  = np.random.randint(1, 30, n)               # 1 to 30th floor
age    = np.random.randint(0, 30, n)               # 0 to 30 years old

# Calculate price in lakhs
# Base: sqft × price per sqft
# Adjustments: BHK premium, higher floor = more expensive, older = cheaper
price_raw = (
    np.array(base_prices) * sqft                   # base value
    + bhk * 200000                                 # BHK premium
    + floor * 50000                                # floor premium
    - age * 30000                                  # age discount
    + np.random.randint(-500000, 500000, n)        # real-world noise
)

price_lakhs = np.round(price_raw / 100000, 2)      # convert to lakhs
price_lakhs = np.clip(price_lakhs, 10, 50000)      # no negative prices

# Build the DataFrame
df = pd.DataFrame({
    'Locality' : localities,
    'Sqft'     : sqft,
    'BHK'      : bhk,
    'Floor'    : floor,
    'Age_years': age,
    'Price_L'  : price_lakhs                       # L = Lakhs
})

print("✅ Mumbai housing dataset created!")
print(f"   {len(df)} properties\n")
print(df.head(5).to_string(index=False))

# Encode locality as numbers (ML needs numbers) 
df['Locality_code'] = df['Locality'].astype('category').cat.codes

# Show the locality → code mapping
locality_map = dict(enumerate(df['Locality'].astype('category').cat.categories))
reverse_map  = {v: k for k, v in locality_map.items()}
print(f"\n📍 Locality codes: {reverse_map}\n")

# Split features and target 
X = df[['Locality_code', 'Sqft', 'BHK', 'Floor', 'Age_years']]
y = df['Price_L']

# Train / test split 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"📊 Training on {len(X_train)} properties")
print(f"   Testing on  {len(X_test)} properties\n")

# Train the model 
model = LinearRegression()
model.fit(X_train, y_train)
print("🧠 Model trained!\n")

# Accuracy check 
predictions = model.predict(X_test)
error = mean_absolute_error(y_test, predictions)
print(f"📉 Average prediction error: ₹{error:.2f} Lakhs\n")

# Predict your custom property 
print("─" * 40)
print("  🏠  Predict Mumbai Property Price")
print("─" * 40)

print("\nAvailable localities:")
for name, code in sorted(reverse_map.items()):
    print(f"  {code} → {name}  (₹{areas[name]:,}/sqft)")

loc_code = int(input("\nEnter locality code: "))
sqft_in  = int(input("Area in sqft (e.g. 650): "))
bhk_in   = int(input("BHK (1/2/3/4): "))
floor_in = int(input("Floor number (e.g. 5): "))
age_in   = int(input("Age of building in years (e.g. 10): "))

custom = pd.DataFrame([[loc_code, sqft_in, bhk_in, floor_in, age_in]],
                      columns=['Locality_code','Sqft','BHK','Floor','Age_years'])

predicted = model.predict(custom)[0]
loc_name  = locality_map[loc_code]

print(f"\n{'─'*40}")
print(f"  📍 Locality  : {loc_name}")
print(f"  📐 Size      : {sqft_in} sqft | {bhk_in} BHK")
print(f"  🏢 Floor     : {floor_in} | Age: {age_in} yrs")
print(f"  💰 Predicted : ₹{predicted:.2f} Lakhs")
print(f"{'─'*40}\n")