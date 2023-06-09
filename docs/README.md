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

One can simply fork the repo and remove existing recipe and modify configuration by following standard guidance on Material for mkdocs. The main topic to understand is the usage of the Macro which is pretty straightforward. Anywhere in you markdown file you could call it like so:

```
{{"""<your recipe in cooklang notation>""" | parse_recipe()}}
```

It can be seen in action on any of the `.md` files in any of the directories located at `docs/Recipe/` on this repo.

# Explanation of code

- To Do.