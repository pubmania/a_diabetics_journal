# About
This repo is created using Material for mkdocs theme and the main addition is the macro defined in `main.py` in root of this repo, specifically the function called `parse_recipe`.

This function parses a recipe written in [Cooklang](https://cooklang.org/) and generates markdown from it to then display the recipes in a consistent manner.

# Driver
One of the main driver in the way I present recipe on screen is my frustration with how recipes in general are presented across the web where one has to keep jumping between `Ingredients` and `Steps`. I think one of the reason it is done that way is because author has to make a choice between presenting all ingredients at one place or just in the steps. Using cooklang with this macro takes that problem away because author (me in this case) just has to write steps and ingredients in one place and then macro written in python does it's bit and extracts ingredients from recipe and presents in one place and not only that if an ingredient is used twice it provides quantities twice so when am cooking I know for my prep using ingredient list I can keep both measures ready and can use those while following the steps.

Now as an added bonus and just because I like using plantuml, I have included in macro the plantuml generator. It is not very fancy and basically just presents steps in boxes and arrows. Although, I have included the logic which allows parsing a basic if then else statement during steps. For example the step `If it's too spicy then add a little bit of @erythritol{as needed}.` is parsed for plantuml to present the if loop by breaking this statement to:

```
if (It's too spicy?) then (yes)
    :Add a little bit of erythritol (as needed).;
else (no)
endif
```

# Usage:

One can simply fork the repo and remove existing recipe and modify configuration by following standard guidance on Material for mkdocs. Only minor addition would be to copy the `custom css` from path `docs\assets\stylesheets\main.css`. The main topic to understand is the usage of the Macro which is pretty straightforward. Anywhere in you markdown file you could call it like so:

```
{{"""<your recipe in cooklang notation>""" | parse_recipe()}}
```

It can be seen in action on any of the `.md` files in any of the directories located at `docs/Recipes/` on this repo.

# Explanation of code behind the `Macros Filter`

First important thing is that for the macro to work, we must ensure [`mkdocs-macros-plugin`](https://mkdocs-macros-plugin.readthedocs.io/en/latest/) has been installed and activated.

Plugin can be installed by `pip install mkdocs-macros-plugin`. Then it should be enabled under plugins on `mkdocs.yml`. Check the `mkdocs.yml` in this repo for a working example.

Now, with that out of the way, one can start creating filters to use by first creating a `main.py` file in the root directory which is what I did. In that file is located the function `parse_recipe`.

Let's break down various functions within this function and what they do and how they do it.

Details about each function and how it works are as explained below:

1. `parse_cookware(item: str) -> dict[str, str]`:
   - This function takes a cookware item as input, which is a string starting with the '#' character, such as "#pot" or "#potato masher{}".
   - It checks if the item starts with '#'. If not, it raises a `ValueError` with the message "Cookware should start with #".
   - The function removes the '{}' characters from the item and returns a dictionary with the cookware name as the value.

2. `parse_quantity(item: str) -> list[str, str]`:
   - This function parses the quantity portion of an ingredient. The input is a string like "2%kg".
   - It checks if the '%' character is present in the item. If not, it returns a list with the item itself and an empty string as the quantity and units, respectively.
   - If '%' is present, the function splits the item at '%' and returns a list with the quantity and units as separate elements.

3. `parse_ingredient(item: str) -> dict[str, str]`:
   - This function parses an ingredient string. The input is a string starting with the '@' character, such as "@salt" or "@milk{4%cup}".
   - It checks if the item starts with '@'. If not, it raises a `ValueError` with the message "Ingredients should start with @".
   - If the item does not end with '}', it returns a dictionary with the ingredient name, a default quantity of "some", and an empty string as the units.
   - If the item ends with '}', it splits the item at '{' and calls the `parse_quantity` function to parse the quantity portion.
   - The function then returns a dictionary with the ingredient name, the parsed quantity (or "as needed" if no quantity is specified), and the units.

4. `parse_timer(item: str) -> dict[str, str]`:
   - This function parses a timer string. The input is a string starting with the '~' character, such as "~eggs{3%minutes}" or "~{25%minutes}".
   - It checks if the item starts with '~'. If not, it raises a `ValueError` with the message "Timer should start with ~".
   - The function splits the item at '{' and calls the `parse_quantity` function to parse the quantity portion.
   - It returns a dictionary with the timer name, the parsed quantity, and the units.

5. `find_specials(step: str, start_char="#") -> list[str]`:
   - This function finds special items (cookware, ingredients, timers) in a recipe step based on the specified start character.
   - It takes a step string and a start character as input.
   - The function iterates over each character in the step string and identifies special items by checking if the current character matches the start character.
   - When a special item is found, it removes any trailing whitespace or punctuation characters ('.', ' ') and appends the item to the matches list.
   - The function returns a list of all the special items found.

6. `find_cookware(step: str) -> list[str]`:
   - This function finds cookware items in a recipe step. It calls the `find_specials` function with the start character set as '#'.

7. `find_ingredients(step: str) -> list[str]`:
   - This function finds ingredients in a recipe step. It calls the `find_specials` function with the start character set as '@'.

8. `find_timers(step: str) -> list[str]`:
   - This function finds timers in a recipe step. It calls the `find_specials` function with the start character set as '~'.

9. `insert_newlines(input_string, chars_per_line)`:
   - This function inserts newlines in the input string to limit the number of characters per line.
   - It takes an input string and a maximum number of characters per line as input.
   - The function splits the input string into words and iteratively joins them with spaces until the character count exceeds the limit.
   - When the limit is exceeded, it adds a newline character and continues the process.
   - The function returns the modified string with newlines.

10. `parse_recipe(input_string)`:
    - This is the main function that processes the input recipe string, extracts the ingredients, cookware, timers, and steps, and returns a formatted string representing the processed recipe.
    - It splits the input string into lines and uses the insert_newlines function to limit the number of characters per line.
    - The function iterates over each line and checks if it contains cookware, ingredients, or timers by calling the corresponding find functions.
    - It then constructs a formatted string by combining the extracted information and returns the final processed recipe string.

These functions work together to parse the input recipe string, extract relevant information, and format it into a more structured representation.

## Example

Let's take a recipe for example and the output it generates.

If you were to run following code block in Jupter Notebook:

```python
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
                "quantity": val or "as needed",
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
                    x = "\n\t"
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
            ingredient_name = match['name'].title()
            amount = match['quantity']
            unit = match['units']

            ingredient_key = ingredient_name
            if ingredient_key in ingredients:
                ingredients[ingredient_key].append((amount, unit))
            else:
                ingredients[ingredient_key] = [(amount, unit)]

        for cookware_match in cookware_matches:
            cookware_name = parse_cookware(cookware_match).title()
            cookwares.add(cookware_name)


        #Remove individual timer notation ~{25%minutes} or ~{25-30%minutes}
        pattern = r'~{(\d+)(?:-(\d+))?%([^}]+)}'
        replacement = lambda match: f"{match.group(1)}-{match.group(2)} {match.group(3)}" if match.group(2) else f"{match.group(1)} {match.group(3)}"
        input_string = re.sub(pattern, replacement,input_string)

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
            if step.startswith('**') and step.endswith('**'):
                dia_step = step[:-2].replace('**','#Black:')
                dia_string += "\t" + insert_newlines(dia_step,50) + "|\n"
            else:
                if step.upper().startswith("IF") and "THEN" in step.upper():
                    dia_if_s = ""
                    condition = step.upper().split("THEN")[0].strip().replace("IF ", "").replace(" ELSE", "")
                    true_action = step.upper().split("THEN")[1].split("ELSE")[0].strip()
                    dia_if_s += f"\tif ({insert_newlines(condition.capitalize(),20)}?) then (yes)\n"
                    dia_if_s += f"\t\t:{insert_newlines(true_action.capitalize(),20)};\n"
                    if "ELSE" in step.upper():
                        false_action = step.upper().split("ELSE")[1].strip()
                        dia_if_s += f"\telse (no)\n"
                        dia_if_s += f"\t\t:{insert_newlines(false_action.capitalize(),20)};\n\tendif\n" 
                    else:
                        dia_if_s += f"\telse (no)\n\tendif\n"
                    dia_string += dia_if_s
                else:    
                    dia_string += "\t:" + insert_newlines(step,50) + ";\n"
            if step.startswith('**') and step.endswith('**'):
                step_line = f"\n\t### {step.replace('**','')}"
            else:    
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
                image_data_string = f"## Image\n\n<figure markdown>\n![image](../../assets/images/"+cooking_data["Image"]+"){: style=\"width: 920px;height: 430px;object-fit: contain;\"}\n<figcaption>" + cooking_data["Image-Caption"] + "</figcaption>\n</figure>\n\n"
                del cooking_data["Image-Caption"]
                del cooking_data["Image"]
            else:
                image_data_string = f"## Image\n\n<figure markdown>\n![image](../../assets/images/"+cooking_data["Image"]+"){: style=\"width: 920px;height: 430px;object-fit: contain;\"}\n</figure>\n\n"
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

input_string = """
>> Serving Size: 4 portions
>> Cooking Time: 10 minutes (Prep Time - 5 minutes)
>> Category: Indian Chutney
>> Type: Vegetarian
Take #smallest mixer jar{}.
Add @fresh mint leaves{1/2%of mixer jar}.
Add @fresh corriander leaves{1/2%of mixer jar}, @green chillies{2-3%medium} and @garlic{1%clove}.
Add @Baby Spinach{7-10%leaves} and @Apple cider vinegar{1%tbsp}, @ginger{1%inch}.
Add @vine tomatoes{4%medium}, @virgin olive oil{1.5%tbsp}, @red Capsicum{1/6%chopped}.
Finally add @Pink Himalayan Salt{to taste}.
Grind on #mixer grinder{}.
If it's too spicy then add a little bit of @erythritol{as needed}.
Serve it with snack dishes.
"""
output_string = parse_recipe(input_string)
print(output_string)
```

The output will be as shown below:

```markdown
<div class="grid cards" align = "center" markdown>

-   :material-timer: *10 minutes (Prep Time - 5 minutes)*, :fontawesome-solid-chart-pie: *4 portions*, **Type**: :leafy_green:, **Category**: *Indian Chutney*

</div>


<div class="grid cards" markdown>


-   ## Ingredients

	---
		1. Fresh Mint Leaves: 1/2 of mixer jar
		2. Fresh Corriander Leaves: 1/2 of mixer jar
		3. Green Chillies: 2-3 medium
		4. Garlic: 1 clove
		5. Baby Spinach: 7-10 leaves
		6. Apple Cider Vinegar: 1 tbsp
		7. Ginger: 1 inch
		8. Vine Tomatoes: 4 medium
		9. Virgin Olive Oil: 1.5 tbsp
		10. Red Capsicum: 1/6 chopped
		11. Pink Himalayan Salt: to taste 
		12. Erythritol: as needed 


-   ## Cookwares

	---
	1. *Smallest Mixer Jar*
	2. *Mixer Grinder*


</div>


<div class="grid cards" markdown>


-   ## Steps

	---
	* Take smallest mixer jar.
	* Add fresh mint leaves (1/2 of mixer jar).
	* Add fresh corriander leaves (1/2 of mixer jar), green chillies (2-3 medium) and garlic (1 clove).
	* Add Baby Spinach (7-10 leaves) and Apple cider vinegar (1 tbsp), ginger (1 inch).
	* Add vine tomatoes (4 medium), virgin olive oil (1.5 tbsp), red Capsicum (1/6 chopped).
	* Finally add Pink Himalayan Salt (to taste).
	* Grind on mixer grinder.
	* If it's too spicy then add a little bit of erythritol (as needed).
	* Serve it with snack dishes.

-   ## Process

	---
	```plantuml
	@startuml
	!theme cerulean
	start
	:Take smallest mixer jar.;
	:Add fresh mint leaves (1/2 of mixer jar).;
	:Add fresh corriander leaves (1/2 of mixer jar), green
	chillies (2-3 medium) and garlic (1 clove).;
	:Add Baby Spinach (7-10 leaves) and Apple cider vinegar
	(1 tbsp), ginger (1 inch).;
	:Add vine tomatoes (4 medium), virgin olive oil (1.5
	tbsp), red Capsicum (1/6 chopped).;
	:Finally add Pink Himalayan Salt (to taste).;
	:Grind on mixer grinder.;
	if (It's too spicy?) then (yes)
		:Add a little bit of erythritol (as needed).;
	else (no)
	endif
	:Serve it with snack dishes.;
	end
	@enduml
	```

</div>


??? abstract "Recipe in [Cooklang](https://cooklang.org/){target=_blank}"
	```
	
	>> Serving Size: 4 portions
	>> Cooking Time: 10 minutes (Prep Time - 5 minutes)
	>> Category: Indian Chutney
	>> Type: Vegetarian
	Take #smallest mixer jar{}.
	Add @fresh mint leaves{1/2%of mixer jar}.
	Add @fresh corriander leaves{1/2%of mixer jar}, @green chillies{2-3%medium} and @garlic{1%clove}.
	Add @Baby Spinach{7-10%leaves} and @Apple cider vinegar{1%tbsp}, @ginger{1%inch}.
	Add @vine tomatoes{4%medium}, @virgin olive oil{1.5%tbsp}, @red Capsicum{1/6%chopped}.
	Finally add @Pink Himalayan Salt{to taste}.
	Grind on #mixer grinder{}.
	If it's too spicy then add a little bit of @erythritol{as needed}.
	Serve it with snack dishes.
	```
```

This output is what the macro passes to mkdocs to generate the output which is displayed on site.