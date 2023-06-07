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
        def parse_cookware(item: str) -> dict[str, str]:
            """Parse cookware item
            e.g. #pot or #potato masher{}
            """
            if item[0] != "#":
                raise ValueError("Cookware should start with #")
            item = item.replace("{}", "")
            return item[1:]


        def parse_quantity(item: str) -> list[str, str]:
            """Parse the quantity portion of an ingredient
            e.g. 2%kg
            """
            if "%" not in item:
                return [item, ""]
            return item.split("%", maxsplit=1)


        def parse_ingredient(item: str) -> dict[str, str]:
            """Parse an ingredient string
            eg. @salt or @milk{4%cup}
            """
            if item[0] != "@":
                raise ValueError("Ingredients should start with @")
            if item[-1] != "}":
                return {
                    "type": "ingredient",
                    "name": item[1:],
                    "quantity": "some",
                    "units": "",
                }
            name, quantity = item.split("{", maxsplit=1)
            val, units = parse_quantity(quantity[0:-1])
            return {
                "type": "ingredient",
                "name": name[1:],
                "quantity": val or "some",
                "units": units,
            }


        def parse_timer(item: str) -> dict[str, str]:
            """Parse timer string
            e.g. ~eggs{3%minutes} or ~{25%minutes}
            """
            if item[0] != "~":
                raise ValueError("Timer should start with ~")
            name, quantity = item.split("{", maxsplit=1)
            val, units = parse_quantity(quantity[0:-1])
            return {
                "type": "timer",
                "name": name[1:],
                "quantity": val,
                "units": units,
            }

        def find_specials(step: str, start_char="#") -> list[str]:
            matches = []
            item = ""
            matching: bool = False
            specials = ["~", "@", "#"]
            for i, x in enumerate(step):
                if x == start_char:
                    if start_char == "~" and step[i - 1] == "{":
                        continue  # Skip - approx value in ingredient
                    matching = True
                    item += x
                    continue
                if matching and x in specials:
                    if " " in item:
                        item = item.split(" ")[0]
                    elif "." in item:
                        item = item.split(".")[0]
                    matches.append(item)
                    matching = False
                    item = ""
                if matching and x == "}":
                    item += x
                    matches.append(item)
                    matching = False
                    item = ""
                if matching:
                    item += x

            if matching:
                if " " in item:
                    item = item.split(" ")[0]
                elif "." in item:
                    item = item.split(".")[0]
                matches.append(item)
            return matches

        def find_cookware(step: str) -> list[str]:
            """Find cookware items in a recipe step"""
            return find_specials(step, "#")


        def find_ingredients(step: str) -> list[str]:
            """Find ingredients in a recipe step"""
            return find_specials(step, "@")


        def find_timers(step: str) -> list[str]:
            """Find timers in a recipe step"""
            return find_specials(step, "~")
        
        def insert_newlines(input_string, chars_per_line):
            mod = ""    
            for i,x in enumerate(input_string):
                if x in ('`','*'):
                    x = ''
                elif x ==' ' and i >= chars_per_line:
                    x = "\n"
                    chars_per_line += chars_per_line
                mod += x    
            return mod
        cooklang_block = f'\n??? abstract "Recipe in [Cooklang](https://cooklang.org/)' + '{target=_blank' + '}"\n\t```\n\t' + input_string.replace("\n","\n\t") + '```'
        matches = []
        for item in find_ingredients(input_string):
            matches.append(parse_ingredient(item))
        cookware_matches = find_cookware(input_string)
        ingredients = {}
        cookwares = set()
        steps = []
        cooking_data = {}

        for match in matches:
            ingredient_name = match['name'].capitalize()
            amount = match['quantity']
            unit = match['units']

            ingredient_key = ingredient_name
            if ingredient_key in ingredients:
                ingredients[ingredient_key].append((amount, unit))
            else:
                ingredients[ingredient_key] = [(amount, unit)]

        for cookware_match in cookware_matches:
            cookware_name = parse_cookware(cookware_match).capitalize()
            cookwares.add(cookware_name)

        #Remove individual timer notation ~{25%minutes}
        input_string = re.sub(r'~{(\d+)%([^}]+)}', lambda match: f"{match.group(1)} {match.group(2)}",input_string)
        
        lines = input_string.replace("{}", '').\
        replace("@", "").\
        replace("%", " ").\
        replace("#", '').\
        replace("~", '').\
        replace("{", ' (').replace("}", ')').splitlines()

        ingredient_string = ""
        for line in lines:
            if line.strip() != "" and line.startswith(">>"):
                key, value = line.lstrip(">> ").strip().split(": ")
                cooking_data[key.strip()] = value.strip()
            elif line.strip() != "":
                steps.append(line.strip())

        ingredient_string += "<div class=\"grid cards\" markdown>\n\n\n-   ## Ingredients\n\n\t---\n"
        #ingredient_string += "\n## Ingredients\n\n\t---\n"
        ingredient_count = 1
        for ingredient_name in ingredients.keys():
            if len(ingredients[ingredient_name]) > 1:
                ingredient_line = f"\t\t{ingredient_count}. {ingredient_name}:"
                ingredient_string += ingredient_line + "\n"
                for amount, unit in ingredients[ingredient_name]:
                    ingredient_line = f"\t\t\t- {amount} {unit}"
                    ingredient_string += ingredient_line + "\n"
            else:
                ingredient_line = ""
                for amount, unit in ingredients[ingredient_name]:
                    ingredient_line += f"\t\t{ingredient_count}. {ingredient_name}: {amount} {unit}"
                ingredient_string += ingredient_line + "\n"
            ingredient_count += 1
        if cookwares:
            cookware_string = "\n-   ## Cookwares\n\n\t---\n"
            cookware_count = 1
            for cookware in cookwares:
                cookware_line = f"\t{cookware_count}. *{cookware}*"
                cookware_count += 1
                cookware_string += cookware_line + "\n"
        else:
            cookware_string = ''
        cookware_string += '\n\n</div>\n\n'
        steps_string = "<div class=\"grid cards\" markdown>\n\n\n-   ## Steps\n\n\t---"
        dia_string = "\n-   ## Process\n\n\t---\n\t```plantuml\n\t@startuml\n\t!theme cerulean\n\tstart\n"
        for step in steps:
            dia_string += "\t:" + insert_newlines(step,30) + ";\n"
            step_line = f"\n\t* {step}"
            steps_string += step_line
        #steps_string += "\n</div>\n\n"
        dia_string += "\tend\n\t@enduml\n\t```\n\n</div>\n\n"

        if "Title" in cooking_data:
            title = cooking_data["Title"]
            del cooking_data["Title"]
            cooking_data_string = f"## {title}\n\n"
        else:
            cooking_data_string = ""
        if "Image" in cooking_data:
            if "Image-Caption" in cooking_data:
                image_data_string = f"## Image\n\n<figure markdown>\n![image](../../assets/images/"+cooking_data["Image"]+")\n<figcaption>" + cooking_data["Image-Caption"] + "</figcaption>\n</figure>\n\n"
                del cooking_data["Image-Caption"]
                del cooking_data["Image"]
            else:
                image_data_string = f"## Image\n\n<figure markdown>\n![image](../../assets/images/"+cooking_data["Image"]+")\n</figure>\n\n"
                del cooking_data["Image"]
        else:
            image_data_string = ""
        #cooking_data_string += "<div class=\"grid cards\" markdown>\n\n"
        temp_cooking_data_string = ""
        one_cooking_data_string = ""
        two_cooking_data_string = ""
        three_cooking_data_string = ""
        four_cooking_data_string = ""
        for key, value in cooking_data.items():
            if key in ('Cooking Time','Serving Size','Type', 'Source'):
                if key == 'Cooking Time':
                    one_cooking_data_string = f":material-timer: *{value}*"
                elif key == 'Serving Size':
                    two_cooking_data_string = f", :fontawesome-solid-chart-pie: *{value}*"
                elif key == 'Type':
                    if value == 'Vegetarian':
                        three_cooking_data_string = f", **{key}**: :leafy_green:"
                    elif value == 'Vegetarian with Egg':
                        three_cooking_data_string = f", **{key}**: :leafy_green::egg:"
                    else:
                        three_cooking_data_string = f", **{key}**: :cut_of_meat:"
                elif key == 'Source':
                    four_cooking_data_string = f", **{key}**: [:material-origin:]({value})"                
            else:
                cooking_data_string += f", **{key}**: *{value}*"
        if one_cooking_data_string != "":
            temp_cooking_data_string = one_cooking_data_string 
        if two_cooking_data_string != "":
            temp_cooking_data_string += two_cooking_data_string
        if three_cooking_data_string != "":
            temp_cooking_data_string += three_cooking_data_string
        if four_cooking_data_string != "":
            temp_cooking_data_string += four_cooking_data_string + "{target=_blank}"
        cooking_data_string = f'<div class=\"grid cards\" align = \"center\" markdown>\n\n-   ' + temp_cooking_data_string + cooking_data_string + '\n\n</div>\n\n'

        final_output_string = image_data_string + cooking_data_string + "\n" + ingredient_string + "\n" + cookware_string + "\n" + steps_string + "\n" + dia_string + cooklang_block
        return final_output_string