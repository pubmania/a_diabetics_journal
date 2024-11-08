### Function to get formatted Cookwares was saved in cookware_string_creator.py
"""
from parser.helpers import find_cookware, parse_cookware

####################################################################################################
#                                                                                                  #
#                           Function to get formatted Cookwares-(DELETE)                           #
#                                                                                                  #
####################################################################################################

def fn_cookware_string(input_string):
    cookware_string = ""
    count = 1
    parsed_cookwares = set()
    for cookware in find_cookware(input_string):
        parsed_cookware = parse_cookware(cookware).title()
        parsed_cookwares.add(parsed_cookware)
    for parsed_cookware in parsed_cookwares:
        cookware_string += f"{count}. *{parsed_cookware}*\n"
        count+=1
    return cookware_string
"""

# Function to get formatted Ingredients and nutrition labels was saved in ingredients_string_creator.py
"""
from parser.nutrition_labels_creator import fn_nutrient_label_string

####################################################################################################
#                                                                                                  #
#                  Function to get formatted Ingredients and nutrition labels                      #
#                                         (DELETE)                                                 #
####################################################################################################

def fn_ingredient_string(input_string):
    lines = input_string.splitlines()
    recipe_ingredients = {}
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
            print(f"Serving Size: {serving_size}")

    #print(all_recipe_ingredients)
    recipe_ingredients = {}
    
    # Organize ingredients
    for recipe_ingredient in all_recipe_ingredients:
        ingredient_name = recipe_ingredient['name'].title()
        ingredient_amount = recipe_ingredient['quantity']
        ingredient_unit = recipe_ingredient['units']
        ingredient_step = recipe_ingredient['step']
        ingredient_key = ingredient_name
        
        if ingredient_key not in recipe_ingredients:
            recipe_ingredients[ingredient_key] = {'with_units': [], 'without_units': set()}
        
        if ingredient_unit:
            recipe_ingredients[ingredient_key]['with_units'].append((ingredient_amount, ingredient_unit, ingredient_step))
        else:
            recipe_ingredients[ingredient_key]['without_units'].add(ingredient_amount)
    #print(recipe_ingredients)
    ing_table_var = \"""
<table><thead>
  <tr>
    <th>S.No</th>
    <th>Ingredient</th>
    <th>Amount</th>
    <th>Step</th>
  </tr></thead>
<tbody>
    \"""
    ingredient_string = ''
    ingredient_count = 1
    for recipe_ingredient_key in recipe_ingredients.keys():
        total_entries = len(recipe_ingredients[recipe_ingredient_key]['with_units']) + len(recipe_ingredients[recipe_ingredient_key]['without_units'])
        ing_table_var += f'<tr><td rowspan="{total_entries}"><b>{ingredient_count}.</b></td><td rowspan="{total_entries}"><b><i>{recipe_ingredient_key}</i></b></td>'
        # Start the ingredient line
        #ingredient_string += f"{recipe_ingredient_key}"
        # Add unit-based entries        
        tr_count = 1
        for ingredient_amount, ingredient_unit,ingredient_step in recipe_ingredients[recipe_ingredient_key]['with_units']:
            ing_table_var += f'<td>{ingredient_amount} {ingredient_unit}</td>\n<td>Step {ingredient_step}</td>\n</tr>'
            if tr_count < total_entries:
                tr_count = tr_count + 1
                ing_table_var += "<tr>"
            stripped_ingredient_unit = re.sub(r'\(.*?\)', '', ingredient_unit).upper().strip()
            ingredient_string += f"{recipe_ingredient_key} - {ingredient_amount} {stripped_ingredient_unit}\n"
            #ing_table_var += "</tr><tr>"
        # Add non-unit entries, ensuring uniqueness
        for non_unit_amount in recipe_ingredients[recipe_ingredient_key]['without_units']:
            ingredient_string += f"{recipe_ingredient_key} - {non_unit_amount}\n"
            ing_table_var += f'<td align = "center" colspan="2">{non_unit_amount}</td>\n</tr>'
            if tr_count < total_entries:
                tr_count = tr_count + 1
                ing_table_var += "<tr>"
        #ing_table_var += "<tr>"
        ingredient_count+= 1
        #ingredient_string += "\n"
    
    ing_table_var += f'</tbody>\n</table>'
    
    if not isinstance(serving_size, (int, float)):
    # If it's a string or any other type, set it to 1
        serving_size = 1

    #nutrition_info = fn_nutrition_data(ingredient_string,serving_size)
    nutrition_info = ""

    ###### additional info
    ingredient_string = ingredient_string.replace('\n','\n\t\t')
    label_string = ingredient_string.replace('\n\t\t','%0A').replace(' ','%20').replace('/','%2F')
    nutrition_label_link = f'Get the nutrition label and other nutrition details for entire recipe on [this link](https://www.nutritionix.com/natural-demo?line_delimited&use_raw_foods&q={label_string}&s={serving_size})' + '{target=_blank}. If something is not right, copy the ingredients from below and paste in the box, adjust as needed.'
    nutrition_info_addendum = f'\n\n!!! site-info "Nutritionix Link"\n\t{nutrition_label_link}\n\t??? site-tip "Copy Ingredients"\n\t\t```\n\t\t{ingredient_string}```\n'
    #print(ing_table_var)

    nutrition_info += nutrition_info_addendum

    # Create a DataFrame from all_recipe_ingredients <--- new item added so it can be returned by the function.
    parsed_nutrient_label = fn_nutrient_label_string(pd.DataFrame(all_recipe_ingredients), serving_size)
    #

    # include recipe_ingredients_df and serving_size in items to be returned by this function.
    return ing_table_var,nutrition_info, parsed_nutrient_label
"""

# Function to create nutrient labels string was saved in nutrition_labels_creator.py
"""
####################################################################################################
#                                                                                                  #
#                          Function to create nutrient labels string                               #
#                                        (DELETE)                                                  #
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
    
        label_string += f\"""
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
\"""
    
    if missing_ingredients_string != "":
        final_label_string = f'<div class = "grid card">{label_string}</div>\n\n!!! warning "Missing Ingredients"\n\t{missing_ingredients_string}'
    else:
        final_label_string = f'<div class = "grid card">{label_string}</div>'

    return final_label_string
"""

# Function to get formatted Nutrition Label was saved in nutrition_labels_creator.py
"""
####################################################################################################
#                                                                                                  #
#                          Function to get formatted Nutrition Label                               #
#                                       (DELETE)                                                   #
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
"""

# Main Function to Parse Cooklang Recipe was saved in parse_recipe.py
"""
####################################################################################################
#                                                                                                  #
#                         Main Function to Parse Cooklang Recipe                                   #
#                                      (DELETE)                                                    #
####################################################################################################

import pandas as pd
from parser.Nutritionix_api_call import get_nutritionix_data
from parser.helpers import find_ingredients, parse_ingredient, replace_amount, replace_unit
from parser.nutrition_labels_creator import calculate_nutrient_summary_per_weight
from parser.steps_creator import fn_steps_string
from parser.ingredients_string_creator import fn_ingredient_string
from parser.cookwares_string_creator import fn_cookware_string
from parser.recipe_metadata_creator import fn_metadata_string

def fn_parse_recipe(recipe_string,image_path):
    recipe_title, cooking_data_string = fn_metadata_string(recipe_string,image_path)
    #ingredient_string = fn_ingredient_string(recipe_string).replace('\n','\n\t\t')
    #ingredient_string, nutrition_info = fn_ingredient_string(recipe_string)
    ingredient_string, nutrition_info, nutrient_labels = fn_ingredient_string(recipe_string)
    ingredient_string = ingredient_string.replace('\n','\n\t')
    ingredient_string = f"<div class=\"grid cards\" markdown>\n\n\n-   ## Ingredients\n\n\t---\n{ingredient_string}\n"
    cookware_string = fn_cookware_string(recipe_string).replace('\n','\n\t')
    cookware_string = f"\n-   ## Cookware\n\n\t---\n\n\t{cookware_string}\n</div>"
    steps_string_new, steps_dia_string = fn_steps_string(recipe_string)
    steps_string_new = f"<div class=\"grid cards\" markdown>\n\n\n-   ## Steps\n\n\t---{steps_string_new}\n"
    style_str = \"""
            !startsub activity
                skinparam activity {
                    $primary_scheme()
                    BarColor #orangered
                    StartColor #orangered
                    EndColor #orangered
                        BorderColor #orangered
                        ArrowColor #orangered
                        ArrowThickness 1.25
                        ArrowFontColor #maroon
                        FontColor #maroon
                        
                        ''
                        DiamondBackgroundColor #darkgreen
                        DiamondLineColor #white
                        DiamondFontColor #white
                }
            !endsub
    \"""
    steps_dia_string = f"\n-   ## Process\n\n\t---\n\n\t```plantuml\n\t@startuml\n\t!theme sketchy-outline\n\t{style_str}\n\tstart\n{steps_dia_string}\tend\n\t@enduml\n\t```\n\n</div>\n\n"
    
    cooklang_block = f'\n??? site-abstract "Recipe in [Cooklang](https://cooklang.org/)' + '{target=_blank' + '}"\n\t```\n\t' + recipe_string.replace("\n","\n\t") + '\n\t```'
    
    combined_recipe_string = f"{cooking_data_string}\n{ingredient_string}{cookware_string}{steps_string_new}{steps_dia_string}\n{nutrient_labels}\n{nutrition_info}\n{cooklang_block}\n"
    
    if recipe_title:
        final_recipe_string = recipe_title + combined_recipe_string.replace('##','###')
    else:
        final_recipe_string = combined_recipe_string

    return final_recipe_string
"""

# Function to get formatted metadata was saved in recipe_metadata_creator.py
"""
import os

####################################################################################################
#                                                                                                  #
#                           Function to get formatted metadata                                     #
#                                                                                                  #
####################################################################################################

def fn_metadata_string(input_string,image_path):
    #print(image_path)
    meta_data = {}
    meta_data_string_title = ""
    meta_data_string = ""
    image_data_string = ""
    lines = input_string.splitlines()

    for line in lines:
        if line.strip() != "" and line.startswith(">>"):
            key, value = line.lstrip(">> ").strip().split(": ")
            meta_data[key.strip()] = value.strip()
    if "Title" in meta_data:
        title = meta_data["Title"]
        del meta_data["Title"]
        meta_data_string_title = f"## {title}\n\n"
    else:
        meta_data_string = ""
    if "Image" in meta_data:
        final_image_path = os.path.join(image_path,meta_data["Image"])
        print(final_image_path)
        if "Image-Caption" in meta_data:
            #image_data_string += f"<figure markdown>![image]({image_path}"+meta_data["Image"]+"){: style=\"width: 920px;height: 430px;object-fit: contain;\"}<figcaption>" + meta_data["Image-Caption"] + "</figcaption></figure>"
            image_data_string += f\"""
<figure class = "card">
<p><img alt="image" src="{final_image_path}" style="width: 920px;height: 430px;object-fit: contain;"></p>
<figcaption>{meta_data["Image-Caption"]}</figcaption>
</figure>
\"""
            del meta_data["Image-Caption"]
            del meta_data["Image"]
        else:
            #image_data_string += f"<figure markdown>![image]({image_path}"+meta_data["Image"]+"){: style=\"width: 920px;height: 430px;object-fit: contain;\"}</figure>"
            image_data_string += f\"""
<figure class = "card" >
<p><img alt="image" src="{image_path}/{meta_data["Image"]}" style="width: 920px;height: 430px;object-fit: contain;"></p>
</figure>
\"""
            del meta_data["Image"]

    #cooking_data_string += "<div class=\"grid cards\" markdown>\n\n"
    temp_meta_data_string = ""
    other_meta_data_string = ""
    one_meta_data_string = ""
    two_meta_data_string = ""
    three_meta_data_string = ""
    four_meta_data_string = ""
    for key, value in meta_data.items():
        if key in ('Cooking Time','Serving Size','Type', 'Source'):
            if key == 'Cooking Time':
                one_meta_data_string = f":material-timer: *{value}*"
            elif key == 'Serving Size':
                two_meta_data_string = f":fontawesome-solid-chart-pie: *{value}*"
            elif key == 'Type':
                if value == 'Vegetarian':
                    three_meta_data_string = f"**{key}**: :leafy_green:"
                elif value == 'Vegetarian with Egg':
                    three_meta_data_string = f"**{key}**: :leafy_green::egg:"
                else:
                    three_meta_data_string = f"**{key}**: :cut_of_meat:"
            elif key == 'Source':
                four_meta_data_string = f"**{key}**: [:material-origin:]({value})"                
        else:
            other_meta_data_string += f"**{key}**: *{value}*" + '\n{ .card }\n\n'
    if one_meta_data_string != "":
        temp_meta_data_string = one_meta_data_string + '\n{ .card }\n\n'
    if two_meta_data_string != "":
        temp_meta_data_string += two_meta_data_string + '\n{ .card }\n\n'
    if three_meta_data_string != "":
        temp_meta_data_string += three_meta_data_string + '\n{ .card }\n\n'
    if four_meta_data_string != "":
        temp_meta_data_string += four_meta_data_string+"{target=_blank}" + '\n{ .card }\n\n'
    
    if image_data_string != "":
        meta_data_string += f'## Key Stats\n<div class="grid" markdown><div class="grid" markdown>{image_data_string}</div>\n\n<div align="center" class="grid" markdown>\n\n {temp_meta_data_string}{other_meta_data_string}\n</div></div>'
    else:
        meta_data_string += f'## Key Stats\n<div class="grid" markdown><div align="center" class="grid" markdown>\n\n {temp_meta_data_string}{other_meta_data_string}\n</div></div>'

    #print(meta_data_string.replace('\n{ .card }\n\n','\n'))
    return meta_data_string_title, meta_data_string
"""    

# Function to get formatted steps was saved in steps_creator.py
"""
####################################################################################################
#                                                                                                  #
#                              Function to get formatted steps                            #
#                                                                                                  #
####################################################################################################

def fn_steps_string(input_string):
    lines = input_string.splitlines()
    steps_string_new = ""
    p_step_string = ""
    step_count = 1
    p_step = ""
    #Remove metadata of cooklang that starts with >> and store it in variable inp_step
    for line in lines:
        if line.strip() != "" and not line.startswith(">>"):
            step = line.strip()
            for cookware in find_cookware(step):
                parsed_cookware = parse_cookware(cookware)
                step = step.replace(cookware,f"{parsed_cookware}")
            for timer in find_timers(step):
                parsed_timer = parse_timer(timer)['quantity'] + ' ' + parse_timer(timer)['units']
                step = step.replace(timer,f':material-timer-sand-full: {parsed_timer}')
            for ingredient in find_ingredients(step):
                parsed_ingredient = parse_ingredient(ingredient)
                ingredient_name = parsed_ingredient['name']
                ingredient_quantity = parsed_ingredient['quantity']
                ingredient_unit = parsed_ingredient['units']
                if ingredient_unit !='':
                    if ingredient_unit !='Number':
                        step = step.replace(ingredient,f'<mark><em>{ingredient_quantity} {ingredient_unit}</em> <strong> {ingredient_name}</strong></mark>')
                    else:
                        step = step.replace(ingredient,f'<mark><em>{ingredient_quantity}</em> <strong> {ingredient_name}</strong></mark>')
                else:
                    step = step.replace(ingredient,f'<mark><strong>{ingredient_name}</strong></mark> ({ingredient_quantity})')
            p_step = puml(step.replace(':material-timer-sand-full:','')\
                          .replace('<mark>','')\
                          .replace('</mark>','')\
                          .replace('<strong>','<b>')\
                          .replace('</strong>','</b>')\
                          .replace('<em>','<i>')\
                          .replace('</em>','</i>')
                          )
            if step != '':
                if step.startswith('**') and step.endswith('**'):
                    step = f"<strong>{step.replace('**','')}</strong>\n"
             #       p_step = f"{p_step}"
                else:
                    #step = f"\n\t* [ ] **{step_count}**: {step.strip()}"
                    step = f"<strong>{step_count}</strong>: {step.strip()}\n"
                    #<strong>1</strong>: Cut the <mark><em>160 gms (4 medium)</em> <strong>tomatoes</strong></mark> using knife into small pieces.
                    step_count+=1
            steps_string_new += step
            p_step_string += p_step
    p_step_string = f"{p_step_string}\n"
    steps_string_new = f"{steps_string_new}\n"
    return steps_string_new,p_step_string
"""

# Hooks.py function that was changed to utilise the recipe template
"""
import os
import re
import markdown
from parser.parse_recipe import fn_extract_cooklang_blocks, fn_parse_recipe

def on_page_markdown(markdown, page, **kwargs):
    current_page_path = page.file.src_path
    current_dir = os.path.dirname(current_page_path)
     # Define the base image path
    base_image_path = 'assets/images/'
    # Check if the current directory is within the Recipes directory
    recipes_dir = os.path.abspath('Recipes')  # Get the absolute path of the Recipes directory
    current_dir_abs = os.path.abspath(current_dir)  # Get the absolute path of the current directory

    # Determine the relative path to the images
    if os.path.commonpath([recipes_dir, current_dir_abs]) == recipes_dir:
        # If current_dir is a subdirectory of Recipes, calculate how many levels to go up
        relative_path_for_image = os.path.relpath(base_image_path, current_dir_abs)
    else:
        # Default to the base image path if not in Recipes
        relative_path_for_image = base_image_path

    print(relative_path_for_image)

    cooklang_content = fn_extract_cooklang_blocks(markdown)
    if cooklang_content:
        for content in cooklang_content:
            processed_output = fn_parse_recipe(content.strip(),relative_path_for_image)
            #replace codeblock in markdown with processd_output in the content
            markdown = markdown.replace(f"```cooklang\n{content}\n```",processed_output)
        #print(f"------------------\n{md_content}\n-------------------")
    return markdown
"""