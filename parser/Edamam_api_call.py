import os
import requests
import pandas as pd

def get_edamam_data(ingredients_str):
    """
    Queries Edamam's GET /api/nutrition-data endpoint for a list of ingredients,
    standardizes the response into a per-100g nutrient profile, and returns 
    a pandas DataFrame matching the schema of the local database.
    """
    app_id = os.environ.get("EDAMAM_APP_ID")
    app_key = os.environ.get("EDAMAM_API_KEY")

    if not ingredients_str:
        return None

    # Mappings from local DB columns to Edamam response keys and standard DRVs/units
    nutrient_mappings = {
        'Calories': {'key': 'ENERC_KCAL', 'drv': 2250, 'unit': 'kcal'},
        'Saturated_Fat': {'key': 'FASAT', 'drv': 20, 'unit': 'g'},
        'Total_Fat': {'key': 'FAT', 'drv': 70, 'unit': 'g'},
        'Carbohydrate': {'key': 'CHOCDF', 'drv': 260, 'unit': 'g'},
        'Sugars': {'key': 'SUGAR', 'drv': 30, 'unit': 'g'},
        'Protein': {'key': 'PROCNT', 'drv': 50, 'unit': 'g'},
        'Dietary_fiber': {'key': 'FIBTG', 'drv': 30, 'unit': 'g'},
        'Monounsaturated_Fat': {'key': 'FAMS', 'drv': 0.0, 'unit': 'g'},
        'Polyunsaturated_Fat': {'key': 'FAPU', 'drv': 0.0, 'unit': 'g'},
        'Trans_Fat': {'key': 'FATRN', 'drv': 0.0, 'unit': 'g'},
        'Cholesterol': {'key': 'CHOLE', 'drv': 300, 'unit': 'mg'},
        'Sodium': {'key': 'NA', 'drv': 2300, 'unit': 'mg'},
        'Potassium_K': {'key': 'K', 'drv': 3500, 'unit': 'mg'},
        'Calcium': {'key': 'CA', 'drv': 700, 'unit': 'mg'},
        'Iron': {'key': 'FE', 'drv': 11.75, 'unit': 'mg'},
        'Zinc': {'key': 'ZN', 'drv': 8.25, 'unit': 'mg'},
        'Selenium': {'key': 'SE', 'drv': 75, 'unit': 'µg'},
        'Vitamin_D_(D2_+_D3)': {'key': 'VITD', 'drv': 10, 'unit': 'µg'},
        'Vitamin_E': {'key': 'TOCPHA', 'drv': 15, 'unit': 'mg'},
        'Vitamin_B-6': {'key': 'VITB6A', 'drv': 1.4, 'unit': 'mg'},
        'Vitamin_B-12': {'key': 'VITB12', 'drv': 2.4, 'unit': 'µg'},
        'Caffeine': {'key': 'not_in_edamam', 'drv': 400, 'unit': 'mg'}
    }

    rows = []
    url = "https://api.edamam.com/api/nutrition-data"

    for line in ingredients_str.splitlines():
        if not line.strip():
            continue

        # Convert "Ingredient - 100 gms" format to "100 grams Ingredient" for Edamam's natural language parser
        parts = line.split(' - ')
        if len(parts) == 2:
            query = f"{parts[1]} {parts[0]}".replace("gms", "grams")
            input_str = parts[0].upper()
        else:
            query = line.replace("gms", "grams")
            input_str = line.split(' -')[0].upper()

        params = {
            "app_id": app_id,
            "app_key": app_key,
            "ingr": query
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            ingredients = data.get("ingredients", [])
            if not ingredients or "parsed" not in ingredients[0]:
                continue

            parsed = ingredients[0]["parsed"][0]
            weight = parsed.get("weight", 0)
            if weight == 0:
                continue

            nutrients = parsed.get("nutrients", {})

            # Calculate Net Carbs normalized per 100g (Total Carbs - Fiber)
            carbs_g = nutrients.get("CHOCDF", {}).get("quantity", 0)
            fiber_g = nutrients.get("FIBTG", {}).get("quantity", 0)
            net_carbs_100g = round(((carbs_g - fiber_g) / weight) * 100, 2)

            row = {
                'input_str': input_str,
                'source': '[Edamam](https://www.edamam.com)',
                'food_name': parsed.get("food", input_str).upper(),
                'net_carb': net_carbs_100g,
                'serving_unit': 'gms',
                'serving_weight_grams': 100
            }

            for col_name, mapping in nutrient_mappings.items():
                edamam_key = mapping['key']
                drv = mapping['drv']
                unit = mapping['unit']

                raw_value = nutrients.get(edamam_key, {}).get("quantity", 0) if edamam_key in nutrients else 0
                # Normalize values to a per-100g basis
                normalized_val = round((raw_value / weight) * 100, 2)

                row[col_name] = normalized_val
                row[col_name + '_drv'] = drv
                row[col_name + '_unit'] = unit

            rows.append(row)

        except Exception as e:
            print(f"Error querying Edamam for '{query}': {e}")
            continue

    if rows:
        return pd.DataFrame(rows)
    return None
