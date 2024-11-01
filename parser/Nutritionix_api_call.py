import os
import requests
import json
import pandas as pd

####################################################################################################
#                                                                                                  #
#                Function to convert response from the API into a usable dataframe                 #
#                                                                                                  #
####################################################################################################

def create_nutrient_dataframe(df, ing_str):
    if isinstance(df, pd.DataFrame):
        nutrient_info = {
            208: {'name': 'Calories', 'drv': 2250, 'unit': 'kcal', 'values': []},
            606: {'name': 'Saturated Fat', 'drv': 20, 'unit': 'g', 'values': []},
            204: {'name': 'Total Fat', 'drv': 70, 'unit': 'g', 'values': []},
            205: {'name': 'Carbohydrate', 'drv': 260, 'unit': 'g', 'values': []},
            269: {'name': 'Sugars', 'drv': 30, 'unit': 'g', 'values': []},
            203: {'name': 'Protein', 'drv': 50, 'unit': 'g', 'values': []},
            291: {'name': 'Dietary fiber', 'drv': 30, 'unit': 'g', 'values': []},
            645: {'name': 'Monounsaturated Fat', 'drv': 0.0, 'unit': 'g', 'values': []},
            646: {'name': 'Polyunsaturated Fat', 'drv': 0.0, 'unit': 'g', 'values': []},
            605: {'name': 'Trans Fat', 'drv': 0.0, 'unit': 'g', 'values': []},
            601: {'name': 'Cholesterol', 'drv': 300, 'unit': 'mg', 'values': []},
            307: {'name': 'Sodium', 'drv': 2300, 'unit': 'mg', 'values': []},
            306: {'name': 'Potassium K', 'drv': 3500, 'unit': 'mg', 'values': []},
            301: {'name': 'Calcium', 'drv': 700, 'unit': 'mg', 'values': []},
            303: {'name': 'Iron', 'drv': 11.75, 'unit': 'mg', 'values': []},
            309: {'name': 'Zinc', 'drv': 8.25, 'unit': 'mg', 'values': []},
            317: {'name': 'Selenium', 'drv': 75, 'unit': 'Âµg', 'values': []},
            328: {'name': 'Vitamin D (D2 + D3)', 'drv': 10, 'unit': 'Âµg', 'values': []},
            323: {'name': 'Vitamin E', 'drv': 15, 'unit': 'mg', 'values': []},
            415: {'name': 'Vitamin B-6', 'drv': 1.4, 'unit': 'mg', 'values': []},
            418: {'name': 'Vitamin B-12', 'drv': 2.4, 'unit': 'Âµg', 'values': []},
            262: {'name': 'Caffeine', 'drv': 400, 'unit': 'mg', 'values': []},
        }

        food_names = df['food_name'].tolist()
        
        # Conditional assignment for input_strs
        if len(ing_str) == len(df['food_name']):
            input_strs = ing_str 
        else:
            input_strs = ['Not all ingredients returned'] * len(df['food_name'])

        net_carbs = [round(((row['nf_total_carbohydrate'] - row['nf_dietary_fiber']) / row['serving_weight_grams']) * 100, 2) for _, row in df.iterrows()]

        for _, row in df.iterrows():
            for nutrient_id, nutrient_data in nutrient_info.items():
                nutrient_value = 0
                for entry in row['full_nutrients']:
                    if entry.get('attr_id') == nutrient_id:
                        nutrient_value = entry['value'] if row['serving_weight_grams'] == 100 else round((entry['value'] / row['serving_weight_grams']) * 100, 2)
                        break  # Exit inner loop once nutrient is found
                nutrient_data['values'].append(nutrient_value)

        new_df = pd.DataFrame({
            'input_str': input_strs,
            'source': 'Nutritionix',
            'food_name': food_names,
            'net_carb': net_carbs,
            'serving_unit': 'gms',
            'serving_weight_grams': '100',
        })

        for nutrient_id, nutrient_data in nutrient_info.items():
            nutrient_col_name = nutrient_data['name'].replace(' ', '_')
            new_df[nutrient_col_name] = nutrient_data['values']
            new_df[nutrient_col_name + '_drv'] = nutrient_data['drv']
            # Add unit column for each nutrient
            new_df[nutrient_col_name + '_unit'] = nutrient_data['unit'] 

        return new_df

    else:
        print('Not a dataframe')
        return df

####################################################################################################
#                                                                                                  #
#                            Main Function to call Nutritioninx API                                #
#                                                                                                  #
####################################################################################################

def get_nutritionix_data(ingredients_str):
    # Replace with your actual NutritionX API endpoint, app ID, and app key
    api_url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    app_id = os.environ.get("NUTRITIONIX_APP_ID")
    app_key = os.environ.get("NUTRITIONIX_APP_KEY")

    if not ingredients_str:
        print("Empty ingredient string")
        return None

    payload = {"query": ingredients_str}
    headers = {
        "Content-Type": "application/json",
        "x-app-id": app_id,
        "x-app-key": app_key,
        "line_delimited": "TRUE",
    }

    try:
        response = requests.post(api_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        nutrition_data = response.json()

        if "foods" not in nutrition_data:
            print("Unexpected response format from Nutritionix API")
            return None
        
        df = pd.json_normalize(nutrition_data.get('foods', []))

        df['full_nutrients'] = df['full_nutrients'].apply(
            lambda x: json.loads(x.replace("'", '"')) if not isinstance(x, list) else x
        )

        ingredient_list = [ingredient.split(' -')[0] for ingredient in ingredients_str.splitlines()]

        try:
            new_df = create_nutrient_dataframe(df, ingredient_list)
            return new_df
        except Exception as e:
            print(f"An error occurred during DataFrame creation: {e}")
            return df
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None
