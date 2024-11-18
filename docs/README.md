# About
This repo is created using Material for mkdocs theme and the main addition is the directory called `parser`. It has several functions that are called at the time of build through the python function defined in `hooks.py`.

The functions together parse a recipe written in [Cooklang](https://cooklang.org/) so long as it is presented between codeblock as shown below:

<pre>```cooklang
Recipe in cooklang here...
```</pre>

The string is parsed through the functions for ingredients, cookware, steps, nutritional information etc that are then passed as dictionaroes and strings to the jinja2 template called `recipe_template.html` in the same directory. This template places the information in in a consistent manner to then be displayed with various sections on the website.

# Driver
One of the main driver in the way I present recipe on screen is my frustration with how recipes in general are presented across the web where one has to keep jumping between `Ingredients` and `Steps`. I think one of the reason it is done that way is because author has to make a choice between presenting all ingredients at one place or just in the steps. 

Using cooklang with this parser takes that problem away because author (me in this case) just has to write steps and ingredients in one place and then hook written in python does it's bit and extracts ingredients from recipe and presents in one place and not only that if an ingredient is used twice it provides quantities twice so when am cooking, I know for my prep using ingredient list I can keep both measures ready and can use those while following the steps.

Now as an added bonus and just because I like using plantuml, I have included a plantuml generator - `/parser/plantuml_steps_creator.py`. It is not very fancy and basically just presents steps in boxes and arrows. Although, I have included the logic which allows parsing a basic if then else statement during steps. For example the step `If it's too spicy then add a little bit of @erythritol{as needed}.` is parsed for plantuml to present the if loop by breaking this statement to:

```
if (It's too spicy?) then (yes)
    :Add a little bit of erythritol (as needed).;
else (no)
endif
```

# Usage:

One can simply fork the repo and remove existing recipe and modify configuration by following standard guidance on Material for mkdocs. Only minor addition would be to copy the `custom css` from path `docs\assets\stylesheets\extra.css`. The main topic to understand is the usage of the hook and associated function in parser which is pretty straightforward. Anywhere in your markdown file it can be invoked like so:

<pre>```cooklang
Recipe in cooklang here...
```</pre>

It can be seen in action on any of the `.md` files in any of the directories located at `docs/Recipes/` on this repo.

# Explanation of code behind the `Hook`

> __Note__
> The code was recently refactored significantly to change look and feel as well as include more nutrient information and to utilise the Nutrionix API at build time for new ingredients for which information is not on my csv file.

Let's break down various functions in the helpers.py first:

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

10. `puml(input_string)`:
    - This function takes the input recipe string and converts it into PlantUML code and Steps.
    - It is also able to do basic parsing for `if then else`, `if then elseif then else` type statements so long as the step starts with the word If and has the word then in it.
    - Look at the function code on [Jupyter File](../Cooklang%20Parser.ipynb) as it is documented to explain the flow.

I will be updating the documentation but the [new Jupyter file]{https://github.com/pubmania/a_diabetics_journal/blob/main/Cooklang%20on%20material%20for%20mkdocs.ipynb} is already uploaded and I think it allows better understanding of the flow.
