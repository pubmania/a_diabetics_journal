import os
from jinja2 import Environment, FileSystemLoader
from parser.ingredients_string_creator import fn_recipe_ingredients
from parser.nutrition_labels_creator import fn_total_df_weight
from parser.parse_recipe import fn_extract_cooklang_blocks
from parser.steps_creator import fn_steps_list

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

    #print(relative_path_for_image)

    cooklang_content = fn_extract_cooklang_blocks(markdown)
    if cooklang_content:
        # Create Jinja2 environment, specifying overrides folder as search path
        env = Environment(loader=FileSystemLoader(['parser', '.'])) 
        template = env.get_template('./template/recipe_template.html')
        for content in cooklang_content:
            # Extract data from your functions
            meta_data = {} 
            lines = content.splitlines()
            for line in lines:
                if line.strip() != "" and line.startswith(">>"):
                    key, value = line.lstrip(">> ").strip().split(": ")
                    meta_data[key.strip()] = value.strip()

            steps_list,p_steps_list,cookware = fn_steps_list(content.strip())
            total_weight_dict, missing_ingredients_string, serving_size,net_carbs_table_found_ingredients = fn_total_df_weight(content.strip())
            recipe_ingredients, nutrition_info_addendum = fn_recipe_ingredients(content.strip())
	    
	    # Check if any ingredient contains "gluten"
            contains_gluten = any('wheat gluten' in ingredient.lower() for ingredient in recipe_ingredients.keys())
            
            rendered_html = template.render(
		image_path=relative_path_for_image,
                recipe_ingredients=recipe_ingredients,
		contains_gluten=contains_gluten,
                metadata=meta_data,
                cookware=cookware,
                steps=steps_list,
                process=p_steps_list,
                total_weight_df = total_weight_dict,
                serving_size=serving_size,
		missing_ingredients_string=missing_ingredients_string,
                cooklang_block=content,
                nutrition_info_addendum=nutrition_info_addendum,
		net_carbs_table_found_ingredients=net_carbs_table_found_ingredients,
                page=page
            )
            markdown = markdown.replace(f"```cooklang\n{content}\n```", rendered_html)
    return markdown
