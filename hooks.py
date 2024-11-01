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
