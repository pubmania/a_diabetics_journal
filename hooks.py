import os
import re
import markdown
from parser.parse_recipe import fn_extract_cooklang_blocks, fn_parse_recipe

def on_page_markdown(markdown, page, **kwargs):
    cooklang_content = fn_extract_cooklang_blocks(markdown)
    if cooklang_content:
        for content in cooklang_content:
            processed_output = fn_parse_recipe(content.strip())
            #replace codeblock in markdown with processd_output in the content
            markdown = markdown.replace(f"```cooklang\n{content}\n```",processed_output)
        #print(f"------------------\n{md_content}\n-------------------")
    return markdown