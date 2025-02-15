

import json

# Paste JSON Data here
data = {
  "assets": {
    "name": "ASSETS",
    "value": "13318970.87",
    "items": [
      {
        "account_id": None,
        "name": "Current Assets",
        "value": "13300233.24",
        "items": [
          {
            "account_id": None,
            "name": "Bank Accounts",
            "value": "-513160.89",
            "items": [
              {"account_id": "6c9790a2-0800-46cc-8c50-e29e69d8015c", "name": "Flex Cash", "value": "806291.61"},
              {"account_id": "b58e60f6-fe20-451e-9fc2-87eb58bcb297", "name": "Flex Checking", "value": "-1272375.00"},
              {"account_id": "c7a7a89e-cc40-40b0-90dd-60f0dadedc41", "name": "Flex 2761", "value": "-47077.50"}
            ]
          },
          {
            "account_id": None,
            "name": "Accounts Receivable",
            "value": "13788410.16",
            "items": [
              {"account_id": "bdd4df93-54ac-420c-8a9b-897a24f79c9c", "name": "Accounts Receivable", "value": "13788410.16"}
            ]
          }
        ]
      },
      {
        "account_id": None,
        "name": "Fixed Assets",
        "value": "18737.63",
        "items": [
          {
            "account_id": None,
            "name": "Property, Plant, and Equipment",
            "value": "18737.63",
            "items": [
              {"account_id": "47c124b7-efcb-4225-95b8-7b85e2dcb977", "name": "Office Equipment", "value": "14855.91"},
              {"account_id": "3073b7ee-8d38-48e8-b2cc-a422ffb2d20f", "name": "Furniture", "value": "1017.08"},
              {"account_id": "6450bea2-bafc-40a5-9faa-0a069669f758", "name": "Computers and Accessories", "value": "2864.64"}
            ]
          }
        ]
      }
    ]
  },
  "liabilities": {
    "name": "Liabilities",
    "value": "1025016.99",
    "items": [
      {
        "account_id": None,
        "name": "Current Liabilities",
        "value": "1014525.75",
        "items": [
          {
            "account_id": None,
            "name": "Accounts Payable",
            "value": "83086.72",
            "items": [
              {"account_id": "09342b42-bfa9-459c-997b-f7dac52d32a6", "name": "Accrued Rent", "value": "69723.08"},
              {"account_id": "1cf73166-6064-4e55-875a-ede915e5f0cb", "name": "Payable to Character", "value": "9313.64"}
            ]
          }
        ]
      }
    ]
  },
  "equity": {
    "name": "Equity",
    "value": "12399101.55",
    "items": [
      {
        "account_id": None,
        "name": "Owners Equity",
        "value": "-95000.00",
        "items": [
          {"account_id": "831b6852-6f82-4ce1-b07b-88601d16457d", "name": "Owner's Equity", "value": "-95000.00"}
        ]
      },
      {"account_id": "b1ba5fb3-5d54-4806-ad8d-e78bd2187e13", "name": "Retained Earnings", "value": "11881707.50"},
      {"account_id": "49862dbf-e470-479e-98ae-c1e172bd86a3", "name": "Balance Adjustments", "value": "122453.09"},
      {"account_id": None, "name": "Net Income", "value": "489940.96"}
    ]
  }
}

def validate_rollup(node, level=0):
    """ Recursively validate that each parent node's value equals the sum of its children. """
    parent_name = node["name"]
    parent_value = float(node["value"])

    # If no children exist, return the node's own value
    if "items" not in node or not isinstance(node["items"], list) or len(node["items"]) == 0:
        print(f"{'  ' * level}🔹 {parent_name}: Expected = {parent_value}, Calculated = {parent_value} ✅")
        return parent_value  

    # Compute child sum
    child_values = [validate_rollup(child, level + 1) for child in node["items"]]
    child_sum = sum(child_values)

    # Debugging: Print sum details at critical nodes
    if parent_name in ["Current Assets", "ASSETS", "Current Liabilities", "Liabilities"]:
        print(f"\n🔍 Debug: {parent_name} Child Breakdown:")
        for idx, child in enumerate(node["items"]):
            print(f"    ➜ {child['name']}: {child_values[idx]}")
        print(f"    Total: {child_sum}, Expected: {parent_value}\n")

    # Check for missing children
    if parent_value != child_sum:
        missing_amount = parent_value - child_sum
        print(f"🚨 MISMATCH in '{parent_name}': Expected {parent_value}, Calculated {child_sum}, Missing {missing_amount}")
        print(f"    🔎 Possible Missing Child in '{parent_name}' → Check JSON for values around {missing_amount}\n")

    return child_sum  # Return calculated child sum

# Validate each top-level category
for key in data:
    print(f"\n🔍 Checking: {data[key]['name']}")
    validate_rollup(data[key])
    print("✅ Check completed.\n")
