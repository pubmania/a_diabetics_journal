import pandas as pd
from parser.helpers import find_ingredients, parse_ingredient, replace_amount, replace_unit
from parser.Nutritionix_api_call import get_nutritionix_data

####################################################################################################
#                                                                                                  #
#                      Function to create nutrient summary dataframe                               #
#                                                                                                  #
####################################################################################################
    
def calculate_nutrient_summary_per_weight(
    df, 
    recipe_weight_in_gms,
    specified_weight,
    nutrient_col_list,
    total_nutrients, 
    average_nutrient_drv,
    average_nutrient_unit,
    nutrient_drv_columns,
    nutrient_unit_columns
):
    # Create a new row for the specified weight
    specified_nutrients = {
        'recipe_weight_in_gms': specified_weight,
        **{f'{nutrient}': [(total_nutrients[nutrient] / recipe_weight_in_gms) * specified_weight] for nutrient in nutrient_col_list},
        **{f'{nutrient_drv}': [average_nutrient_drv[nutrient_drv]] for nutrient_drv in nutrient_drv_columns},
        **{f'{nutrient_unit}': [average_nutrient_unit[nutrient_unit]] for nutrient_unit in nutrient_unit_columns},
    }
    specified_weight_df = pd.DataFrame(specified_nutrients, index=[0])
    return specified_weight_df

####################################################################################################
#                                                                                                  #
#                          Function to create total nutrient weight dict                           #
#                                          (KEEP)                                                  #
####################################################################################################
def fn_total_df_weight(input_string) -> tuple[dict, str, int]:
#def fn_total_df_weight(input_string):
    lines = input_string.splitlines()
    all_recipe_ingredients = []
    step_count = 1
    serving_size = 1
    for line in lines:
        if line.strip() != "" and not line.startswith(">>"):
            step = line.strip()
            for ingredient in find_ingredients(step):
                parsed_ingredient = parse_ingredient(ingredient)
                parsed_ingredient['step'] = step_count
                all_recipe_ingredients.append(parsed_ingredient)
            if step != '':
                if step.startswith('**') and step.endswith('**'):
                    pass
                else:
                    step_count+=1
        elif line.startswith(">> Serving"):
            serving_size_str =  line.lstrip(">> ").strip().split(": ")[1].split(" ")[0]
            # Convert to integer
            try:
                serving_size = int(serving_size_str)  # Convert the string to an integer
            except ValueError:
                serving_size = 1  # Set to 1 if conversion fails
#            print(f"Serving Size: {serving_size}")
    # Read ingredient and unit csv files
    df_ingredient_db = pd.read_csv('ingredient_nutrient_db.csv')
    df_units_db = pd.read_csv('unit_db.csv')
    # Create a lookup dictionary from df_units_db
    unit_lookup_dict = df_units_db.set_index('Unit')['eq_gms'].to_dict()    
    df_recipe_ingredients = pd.DataFrame(all_recipe_ingredients)
    ##### Code to create nutrition label
    df_recipe_ingredients['cleaned_quantity'] = pd.to_numeric(df_recipe_ingredients['quantity'].apply(replace_amount), errors='coerce')
    df_recipe_ingredients['cleaned_unit'] = df_recipe_ingredients['units'].apply(replace_unit)
    df_recipe_ingredients['quantity_in_gms'] = df_recipe_ingredients['cleaned_quantity'] * df_recipe_ingredients['cleaned_unit'].map(unit_lookup_dict).fillna(0)
    df_recipe_ingredients = df_recipe_ingredients.map(lambda x: x.upper() if isinstance(x, str) else x)
    #print("*******************df_recipe_ingredients***********")
    #print(df_recipe_ingredients)

    # Perform the left merge with ingredient database
    merged_df = df_recipe_ingredients.merge(df_ingredient_db, left_on='name', right_on='input_str', how='left')

    # Filter to get found entries
    found_entries = merged_df[merged_df['input_str'].notna()]
    #print("*******************found_entries***********")
    #print(found_entries)
    #Set nutrient columns
    nutrient_columns = ['net_carb', 'Calories', 'Total_Fat', 'Saturated_Fat', 'Carbohydrate', 'Sugars', 'Protein',
                    'Dietary_fiber', 'Monounsaturated_Fat', 'Polyunsaturated_Fat',
                    'Trans_Fat', 'Cholesterol', 'Sodium', 'Potassium_K',
                    'Calcium', 'Iron', 'Zinc', 'Selenium',
                    'Vitamin_D_(D2_+_D3)', 'Vitamin_E',
                    'Vitamin_B-6', 'Vitamin_B-12', 'Caffeine']

    # found_entries is a slice of another DataFrame so create a copy
    found_entries = found_entries.copy()

    # Cast nutrient columns to float64
    found_entries[nutrient_columns] = found_entries[nutrient_columns].astype('float64')

    # Update nutrient values
    for nutrient in nutrient_columns:
        found_entries.loc[:, nutrient] = (found_entries[nutrient] / found_entries['serving_weight_grams']) * found_entries['quantity_in_gms']
    # Prepare data for calling calculate_nutrient_summary_per_weight function
    total_weight_df = pd.DataFrame()
    # Define the columns for nutrient calculation
    nutrient_drv_columns = []
    nutrient_unit_columns = []
    for nutrient in nutrient_columns:
        if nutrient != 'net_carb':
            nutrient_drv_columns.append(f'{nutrient}_drv')
            nutrient_unit_columns.append(f'{nutrient}_unit')
    # Calculate the total weight of the recipe in grams
    recipe_weight_in_gms = found_entries['quantity_in_gms'].sum()
    # Sum the updated nutrient values for the entire recipe
    total_nutrients = found_entries[nutrient_columns].sum()
    average_nutrient_drv = found_entries[nutrient_drv_columns].mean()
    average_nutrient_unit = found_entries[nutrient_unit_columns].iloc[0]
    #get caluclations for 100gms of recipe
    calculation_weights = [recipe_weight_in_gms,100,recipe_weight_in_gms/serving_size, 2*recipe_weight_in_gms/serving_size]
    #print(calculation_weights)

    for calculation_weight in calculation_weights:
        total_weight_df = pd.concat([total_weight_df,(
            calculate_nutrient_summary_per_weight(
                found_entries, 
                recipe_weight_in_gms,
                calculation_weight,
                nutrient_columns,
                total_nutrients,
                average_nutrient_drv,
                average_nutrient_unit,
                nutrient_drv_columns,
                nutrient_unit_columns
            )
        )], ignore_index=True)

    new_order = ['recipe_weight_in_gms','net_carb']
    for nutrient in nutrient_columns:
        if nutrient != 'net_carb':
            # Check if DRV is 0
            if total_weight_df[f'{nutrient}_drv'].iloc[0] == 0:
                total_weight_df[f'{nutrient}_drv_%'] = ""  # Assign special value
            else:
                total_weight_df[f'{nutrient}_drv_%'] = round((total_weight_df[f'{nutrient}'] / total_weight_df[f'{nutrient}_drv']) * 100,2)
            new_order.append(f'{nutrient}')
            new_order.append(f'{nutrient}_unit')
            new_order.append(f'{nutrient}_drv_%')
            new_order.append(f'{nutrient}_drv')
    # Display the new DataFrame
    #print(new_order)
    total_weight_df = total_weight_df[new_order].round(2)
    # Deal with Not found entries
    not_found_entries = merged_df[merged_df['input_str'].isna()]
    #print("*******************not_found_entries***********")
    #print(not_found_entries)
    if isinstance(not_found_entries,pd.DataFrame):
        # Create the string
        #not_found_string = '\n'.join(not_found_entries['name'] + ' - ' + not_found_entries['quantity_in_gms'].astype(str) + ' gms')
        not_found_string_search = '\n'.join(not_found_entries['name'] + ' - 100 gms')
        #print(not_found_string_search)
        not_found_df = get_nutritionix_data(not_found_string_search)
        if isinstance(not_found_df,pd.DataFrame):
            table_string = not_found_df.to_markdown(index=False).replace('\n','\n\t')
            copy_block_string = not_found_df.to_csv(index=False, header=False,sep=',').replace('\n','\n\t\t')
            missing_ingredients_string = f"Following ingredient was not found on database. It's values from Nutirionix database are as shown in the table below.\n\n\t{table_string}\n\n\tIf these are correct, these can be added to ingredient database simply by copying the code block and pasting in the csv file.\n\n\t??? warning \"Copy for ingredient db\"\n\t\t```\n\t\t{copy_block_string}```"
            #print(missing_ingredients_string)
        else:
            missing_ingredients_string = ""
    # Renaming columns
    found_entries.rename(columns={
        'name': 'Ingredient',
        'quantity': 'Quantity',
        'quantity_in_gms': 'Qty in gms',
        'source': 'Source',
        'cleaned_unit': 'Unit',
        'net_carb': 'Net Carbs (gms)'
    }, inplace=True)
    net_carbs_table_found_ingredients = found_entries[['Ingredient', 'Quantity', 'Unit', 'Qty in gms', 'Source', 'Net Carbs (gms)']].round(2).to_markdown(index=False)
    #nutrient_labels = f"## Nutrition Label\n\n{get_label_string(total_weight_df,missing_ingredients_string,serving_size)}"
    return total_weight_df.to_dict(), missing_ingredients_string, serving_size, net_carbs_table_found_ingredients
