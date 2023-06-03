"""
Basic example of a Mkdocs-macros module
"""

import math
import re

def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    - filter: a function with one of more arguments,
        used to perform a transformation
    """

    # add to the dictionary of variables available to markdown pages:
    env.variables['baz'] = "John Doe"

    # NOTE: you may also treat env.variables as a namespace,
    #       with the dot notation:
    env.variables.baz = "John Doe"

    @env.macro
    def bar(x):
        return (2.3 * x) + 7

    # If you wish, you can  declare a macro with a different name:
    def f(x):
        return x * x
    env.macro(f, 'barbaz')

    # or to export some predefined function
    env.macro(math.floor) # will be exported as 'floor'


    # create a jinja2 filter
    @env.filter
    def parse_recipe(input_string):
        ingredient_pattern = r'@([\w\s]+)\(([\d.]+)%(\w+)\)'
        matches = re.findall(ingredient_pattern, input_string)
        cookware_pattern = r'{#([\w\s]+)}'
        cookware_matches = re.findall(cookware_pattern, input_string)
        ingredients = {}
        cookwares = set()
        steps = []
        cooking_data = {}
        
        for match in matches:
            ingredient_name = match[0].capitalize()
            amount = float(match[1])
            unit = match[2]
            
            ingredient_key = ingredient_name
            if ingredient_key in ingredients:
                ingredients[ingredient_key].append((amount, unit))
            else:
                ingredients[ingredient_key] = [(amount, unit)]
            
        for cookware_match in cookware_matches:
            cookware_name = cookware_match.capitalize()
            cookwares.add(cookware_name)
        
        lines = input_string.replace("@", "").replace("%", " ").replace("{#", '').replace("}", '').splitlines()

        ingredient_string = ""
        for line in lines:
            if line.strip() != "" and line.startswith("-"):
                key, value = line.lstrip("- ").strip().split(":")
                cooking_data[key.strip()] = value.strip()
            elif line.strip() != "":
                steps.append(line.strip())
        
        ingredient_string += "\n-   ## Ingredients\n\n\t---\n"
        ingredient_count = 1
        for ingredient_name, amounts in ingredients.items():
            ingredient_line = f"\t\t{ingredient_count}. {ingredient_name}:"
            ingredient_string += ingredient_line + "\n"
            for amount, unit in amounts:
                ingredient_line = f"\t\t\t- {amount} {unit}"
                ingredient_string += ingredient_line + "\n"
            ingredient_string += "\n\n"
            ingredient_count += 1
        if cookwares:
            cookware_string = "\n-   ## Cookwares\n\n\t---\n"
            cookware_count = 1
            for cookware in cookwares:
                cookware_line = f"\t{cookware_count}. {cookware}"
                cookware_count += 1
                cookware_string += cookware_line + "\n"
        else:
            cookware_string = ''
        
        steps_string = "\n-   ## Steps\n\n\t---"
        dia_string = "\n-   ## Process\n\n\t---\n\t```plantuml\n\t@startuml\n\t!theme cerulean\n\tstart\n"
        for step in steps:
            dia_string += "\t:" + step + ";\n"
            step_line = f"\n\t* {step}"
            steps_string += step_line
                
        dia_string += "\tend\n\t@enduml\n\t```\n</div>"
        
        if "Title" in cooking_data:
            title = cooking_data["Title"]
            del cooking_data["Title"]
            cooking_data_string = f"# {title}\n\n"
        else:
            cooking_data_string = ""
        
        cooking_data_string += "<div class=\"grid cards\" markdown>\n\n"
        for key, value in cooking_data.items():
            cooking_data_string += f"- **{key}**:*{value}*\n"
        
        final_output_string = cooking_data_string + "\n" + ingredient_string + "\n" + cookware_string + "\n" + steps_string + "\n" + dia_string
        return final_output_string