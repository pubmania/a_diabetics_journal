import re
import pandas as pd
from parser.helpers import find_ingredients, parse_ingredient

###########################################################################################
###                                                                                     ###
###      Function to return recipe ingredients as dict and nutrition_info_addendum      ###
###                                        (KEEP)                                       ###
###########################################################################################

def fn_recipe_ingredients(input_string):
    """
    Function takes cooklang block content as input. 
    1) Parses it to get ingredients, qty and units and returns as a dict. 
    2) Additionally, the function creates a Nutritionix link for all ingredients
    which is returned as an info admonition along with a code block 
    that allows copy of all ingredients.
    """
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
            #print(f"Serving Size: {serving_size}")

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
    ingredient_string = ''
    ingredient_count = 1
    for recipe_ingredient_key in recipe_ingredients.keys():
        for ingredient_amount, ingredient_unit,ingredient_step in recipe_ingredients[recipe_ingredient_key]['with_units']:
            stripped_ingredient_unit = re.sub(r'\(.*?\)', '', ingredient_unit).upper().strip()
            ingredient_string += f"{recipe_ingredient_key} - {ingredient_amount} {stripped_ingredient_unit}\n"
        # Add non-unit entries, ensuring uniqueness
        for non_unit_amount in recipe_ingredients[recipe_ingredient_key]['without_units']:
            ingredient_string += f"{recipe_ingredient_key} - {non_unit_amount}\n"
        #ing_table_var += "<tr>"
        ingredient_count+= 1
        #ingredient_string += "\n"
    
    if not isinstance(serving_size, (int, float)):
    # If it's a string or any other type, set it to 1
        serving_size = 1

    ###### additional info
    ingredient_string = ingredient_string.replace('\n','\n\t\t')
    label_string = ingredient_string.replace('\n\t\t','%0A').replace(' ','%20').replace('/','%2F')
    #nutrition_label_link = f'Get the nutrition label and other nutrition details for entire recipe on [this link](https://www.nutritionix.com/natural-demo?line_delimited&use_raw_foods&q={label_string}&s={serving_size})' + '{target=_blank}. If something is not right, copy the ingredients from below and paste in the box, adjust as needed.'
    nutrition_label_link = f'(https://www.nutritionix.com/natural-demo?line_delimited&use_raw_foods&q={label_string}&s={serving_size})' + '{target=_blank}'
    nutrition_info_addendum = f'\n\n??? site-info "[Nutritionix Link]{nutrition_label_link}"\n\tCopy the ingredients from below and adjust as needed.\n\t??? site-tip "Copy Ingredients"\n\t\t```\n\t\t{ingredient_string}```\n'

    return recipe_ingredients, nutrition_info_addendum
