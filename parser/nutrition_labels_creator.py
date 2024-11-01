import pandas as pd
from parser.helpers import replace_amount, replace_unit
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
#                          Function to create nutrient labels string                               #
#                                                                                                  #
####################################################################################################
def get_label_string(total_weight_df,missing_ingredients_string,serving_size):
    label_string = ""
    for i in range(len(total_weight_df)):
        if i == 1:
            amount_per = 'Amount Per 100gms'
        elif i == 2:
            amount_per = f'Amount Per Serving (Total Servings: {serving_size})'
        elif i == 3:
            amount_per = f'Amount in 2 Servings (Total Servings: {serving_size})'
        else:
            amount_per = f"Amount In Whole Recipe ({total_weight_df['recipe_weight_in_gms'][i]}gms)"
        #print(amount_per)
    
        label_string += f"""
<div class="grid card">
<div id="nutrition_label"><div itemscope="" class="nf" role="region" aria-label="nutrition label" style=" width: 300px;">
<div class="nf-title" tabindex="0">Nutrition Facts</div>
<div class="nf-line">
<div class="nf-serving">
<div class="nf-amount-per-serving" align="right" tabindex="0"><b>{amount_per}</b></div>
</div><!-- end of class="nf-serving" -->

</div><!-- end of class="nf-line" -->

<div class="nf-bar2"></div>
<div class="nf-netcarbs" tabindex="0">
<span class="">Net Carbs</span>
<span class="nf-pr" itemprop="net_carbs">{total_weight_df['net_carb'][i]} g</span>
</div>
<div class="nf-bar1"></div>
<div class="nf-calories" tabindex="0">
<span class="">Calories</span>
<span class="nf-pr" itemprop="calories">{total_weight_df['Calories'][i]} Kcal</span>
</div>
<div class="nf-bar1"></div>
<div class="nf-line nf-text-right">
<span class="nf-highlight nf-percent-dv">% Daily Value*</span>
</div>
<div class="nf-line" tabindex="0">
<span class="nf-highlight">Total Fat</span>
<span class="" itemprop="fatContent">{total_weight_df['Total_Fat'][i]}<span aria-hidden="true">g</span><span class="sr-only"> grams</span></span>
<span class="nf-highlight nf-pr">{total_weight_df['Total_Fat_drv_%'][i]}% <span class="sr-only">Daily Value</span></span>
</div>
<div class="nf-line nf-indent" tabindex="0">
<span class="">Saturated Fat</span>
<span class="" itemprop="saturatedFatContent">{total_weight_df['Saturated_Fat'][i]}<span aria-hidden="true">g</span><span class="sr-only"> grams</span></span>
<span class="nf-highlight nf-pr">{total_weight_df['Saturated_Fat_drv_%'][i]}% <span class="sr-only">Daily Value</span></span>
</div>
<div class="nf-line nf-indent" tabindex="0">
<span class=""><em>Trans</em> Fat</span>
<span class="" itemprop="transFatContent">{total_weight_df['Trans_Fat'][i]}<span aria-hidden="true">g</span><span class="sr-only"> grams</span></span>
</div>
<div class="nf-line nf-indent" tabindex="0">
<span class="">Polyunsaturated Fat</span>
<span class="" itemprop="">{total_weight_df['Polyunsaturated_Fat'][i]}<span aria-hidden="true">g</span><span class="sr-only"> grams</span></span>
</div>
<div class="nf-line nf-indent" tabindex="0">
<span class="">Monounsaturated Fat</span>
<span class="" itemprop="">{total_weight_df['Monounsaturated_Fat'][i]}<span aria-hidden="true">g</span><span class="sr-only"> grams</span></span>
</div>
<div class="nf-line" tabindex="0">
<span class="nf-highlight">Cholesterol</span>
<span class="" itemprop="cholesterolContent">{total_weight_df['Cholesterol'][i]}<span aria-hidden="true">mg</span><span class="sr-only"> milligrams</span></span>
<span class="nf-highlight nf-pr">{total_weight_df['Cholesterol_drv_%'][i]}% <span class="sr-only">Daily Value</span></span>
</div>
<div class="nf-line" tabindex="0">
<span class="nf-highlight">Sodium</span>
<span class="" itemprop="sodiumContent">{total_weight_df['Sodium'][i]}<span aria-hidden="true">mg</span><span class="sr-only"> milligrams</span></span>
<span class="nf-highlight nf-pr">{total_weight_df['Sodium_drv_%'][i]}% <span class="sr-only">Daily Value</span></span>
</div>
<div class="nf-line" tabindex="0">
<span class="nf-highlight">Total Carbohydrates</span>
<span class="" itemprop="carbohydrateContent">{total_weight_df['Carbohydrate'][i]}<span aria-hidden="true">g</span><span class="sr-only"> grams</span></span>
<span class="nf-highlight nf-pr">{total_weight_df['Carbohydrate_drv_%'][i]}% <span class="sr-only">Daily Value</span></span>
</div>
<div class="nf-line nf-indent" tabindex="0">
<span class="">Dietary Fiber</span>
<span class="" itemprop="fiberContent">{total_weight_df['Dietary_fiber'][i]}<span aria-hidden="true">g</span><span class="sr-only"> grams</span></span>
<span class="nf-highlight nf-pr">{total_weight_df['Dietary_fiber_drv_%'][i]}% <span class="sr-only">Daily Value</span></span>
</div>
<div class="nf-line nf-indent" tabindex="0">
<span class="">Sugars</span>
<span class="" itemprop="sugarContent">{total_weight_df['Sugars'][i]}<span aria-hidden="true">g</span><span class="sr-only"> grams</span></span>
</div>
<div class="nf-line" tabindex="0">
<span class="nf-highlight">Protein</span>
<span class="" itemprop="proteinContent">{total_weight_df['Protein'][i]}<span aria-hidden="true">g</span><span class="sr-only"> grams</span></span>
</div>
<div class="nf-bar2"></div>
<div class="nf-vitamins">
<div class="nf-vitamins">
<div class="" tabindex="0">
<span class="">Vitamin D</span>
<span class="" itemprop="vitaminDContent">{total_weight_df['Vitamin_D_(D2_+_D3)'][i]}<span aria-hidden="true">mcg</span><span class="sr-only"> micrograms</span></span>
<span class="nf-highlight nf-pr">{total_weight_df['Vitamin_D_(D2_+_D3)_drv_%'][i]}% <span class="sr-only">Daily Value</span></span>
</div>
<div class="nf-line" tabindex="0">
<span class="">Calcium</span>
<span class="" itemprop="calciumContent">{total_weight_df['Calcium'][i]}<span aria-hidden="true">mg</span><span class="sr-only"> milligrams</span></span>
<span class="nf-highlight nf-pr">{total_weight_df['Calcium_drv_%'][i]}% <span class="sr-only">Daily Value</span></span>
</div>
<div class="nf-line" tabindex="0">
<span class="">Iron</span>
<span class="" itemprop="ironContent">{total_weight_df['Iron'][i]}<span aria-hidden="true">mg</span><span class="sr-only"> milligrams</span></span>
<span class="nf-highlight nf-pr">{total_weight_df['Iron_drv_%'][i]}% <span class="sr-only">Daily Value</span></span>
</div>
<div class="nf-line" tabindex="0">
<span class="">Potassium</span>
<span class="" itemprop="potassiumContent">{total_weight_df['Potassium_K'][i]}<span aria-hidden="true">mg</span><span class="sr-only"> milligrams</span></span>
<span class="nf-highlight nf-pr">{total_weight_df['Potassium_K_drv_%'][i]}% <span class="sr-only">Daily Value</span></span>
</div>
<div class="nf-line" tabindex="0">
<span class="">Zinc</span>
<span class="" itemprop="zincContent">{total_weight_df['Zinc'][i]}<span aria-hidden="true">mg</span><span class="sr-only"> milligrams</span></span>
<span class="nf-highlight nf-pr">{total_weight_df['Zinc_drv_%'][i]}% <span class="sr-only">Daily Value</span></span>
</div>
</div>
</div>
<div class="nf-bar2"></div>
<div class="" tabindex="0">
<span class="nf-highlight">Caffeine</span>
<span class="" itemprop="caffeineContent">{total_weight_df['Caffeine'][i]}mg</span>
</div>
<div class="nf-bar1"></div>
<div class="nf-vitamins">
<div class="nf-footnote">
<span tabindex="0">The % Daily Value (DV) tells you how much a nutrient in a serving of food contributes to a daily diet. 2000 calories a day is used for general nutrition advice.</span>
</div>
<div class="naTooltip">Data not available</div>
</div><!-- closing class="nf" -->
</div></div>
</div>
"""
    
    if missing_ingredients_string != "":
        final_label_string = f'<div class = "grid card">{label_string}</div>\n\n!!! warning "Missing Ingredients"\n\t{missing_ingredients_string}'
    else:
        final_label_string = f'<div class = "grid card">{label_string}</div>'

    return final_label_string

####################################################################################################
#                                                                                                  #
#                          Function to get formatted Nutrition Label                               #
#                                                                                                  #
####################################################################################################

def fn_nutrient_label_string(df_recipe_ingredients, serving_size):
    # Read ingredient and unit csv files
    df_ingredient_db = pd.read_csv('ingredient_nutrient_db.csv')
    df_units_db = pd.read_csv('unit_db.csv')
    # Create a lookup dictionary from df_units_db
    unit_lookup_dict = df_units_db.set_index('Unit')['eq_gms'].to_dict()    
    ##### Code to create nutrition label
    df_recipe_ingredients['cleaned_quantity'] = pd.to_numeric(df_recipe_ingredients['quantity'].apply(replace_amount), errors='coerce')
    df_recipe_ingredients['cleaned_unit'] = df_recipe_ingredients['units'].apply(replace_unit)
    df_recipe_ingredients['quantity_in_gms'] = df_recipe_ingredients['cleaned_quantity'] * df_recipe_ingredients['cleaned_unit'].map(unit_lookup_dict).fillna(0)
    df_recipe_ingredients = df_recipe_ingredients.map(lambda x: x.upper() if isinstance(x, str) else x)

    # Perform the left merge with ingredient database
    merged_df = df_recipe_ingredients.merge(df_ingredient_db, left_on='name', right_on='input_str', how='left')

    # Filter to get found entries
    found_entries = merged_df[merged_df['input_str'].notna()]
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
    if isinstance(not_found_entries,pd.DataFrame):
        # Create the string
        #not_found_string = '\n'.join(not_found_entries['name'] + ' - ' + not_found_entries['quantity_in_gms'].astype(str) + ' gms')
        not_found_string_search = '\n'.join(not_found_entries['name'] + ' - 100 gms')
        #print(not_found_string)
        not_found_df = get_nutritionix_data(not_found_string_search)
        if isinstance(not_found_df,pd.DataFrame):
            table_string = not_found_df.to_markdown(index=False).replace('\n','\n\t')
            copy_block_string = not_found_df.to_csv(index=False, header=False,sep=',').replace('\n','\n\t\t')
            missing_ingredients_string = f"Following ingredient was not found on database. It's values from Nutirionix database are as shown in the table below.\n\n\t{table_string}\n\n\tIf these are correct, these can be added to ingredient database simply by copying the code block and pasting in the csv file.\n\n\t??? warning \"Copy for ingredient db\"\n\t\t```\n\t\t{copy_block_string}```"
            #print(missing_ingredients_string)
        else:
            missing_ingredients_string = ""
    nutrient_labels = f"## Nutrition Label\n\n{get_label_string(total_weight_df,missing_ingredients_string,serving_size)}"
    return nutrient_labels