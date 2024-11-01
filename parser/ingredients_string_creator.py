import re
import pandas as pd
from parser.helpers import find_ingredients, parse_ingredient
from parser.nutrition_labels_creator import fn_nutrient_label_string

####################################################################################################
#                                                                                                  #
#                  Function to get formatted Ingredients and nutrition labels                      #
#                                                                                                  #
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
    ing_table_var = """
<table><thead>
  <tr>
    <th>S.No</th>
    <th>Ingredient</th>
    <th>Amount</th>
    <th>Step</th>
  </tr></thead>
<tbody>
    """
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
    label_demo_link = "Get the nutrition label and other nutrition details for entire recipe on [this link](https://www.nutritionix.com/natural-demo){target=_blank}. If something is not right, copy the ingredients from below and paste in the box, adjust as needed."
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