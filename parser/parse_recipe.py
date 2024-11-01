import re
from parser.steps_creator import fn_steps_string
from parser.ingredients_string_creator import fn_ingredient_string
from parser.cookwares_string_creator import fn_cookware_string
from parser.recipe_metadata_creator import fn_metadata_string

####################################################################################################
#                                                                                                  #
#                         Main Function to Parse Cooklang Recipe                                   #
#                                                                                                  #
####################################################################################################

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
    style_str = """
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
    """
    steps_dia_string = f"\n-   ## Process\n\n\t---\n\n\t```plantuml\n\t@startuml\n\t!theme sketchy-outline\n\t{style_str}\n\tstart\n{steps_dia_string}\tend\n\t@enduml\n\t```\n\n</div>\n\n"
    
    cooklang_block = f'\n??? site-abstract "Recipe in [Cooklang](https://cooklang.org/)' + '{target=_blank' + '}"\n\t```\n\t' + recipe_string.replace("\n","\n\t") + '\n\t```'
    
    combined_recipe_string = f"{cooking_data_string}\n{ingredient_string}{cookware_string}{steps_string_new}{steps_dia_string}\n{nutrient_labels}\n{nutrition_info}\n{cooklang_block}\n"
    
    if recipe_title:
        final_recipe_string = recipe_title + combined_recipe_string.replace('##','###')
    else:
        final_recipe_string = combined_recipe_string

    return final_recipe_string

####################################################################################################
#                                                                                                  #
#                           Function to Extract Cooklang Block                                     #
#                                                                                                  #
####################################################################################################
    
def fn_extract_cooklang_blocks(content):
    # Regular expression to find all occurrences of text between "```cooklang" and "```"
    pattern = r'```cooklang(.*?)```'
    
    # Use re.DOTALL to make '.' match newlines as well
    matches = re.findall(pattern, content, re.DOTALL)
    
    # Strip whitespace from each match and return the list
    return [match.strip() for match in matches]
