import re

####################################################################################################
#                                                                                                  #
#             Newlines in the input_string after specified number of characters-(KEEP)             #
#                                                                                                  #
####################################################################################################

def insert_newlines(input_string: str, chars_per_line: int):
    """Inserts newline in the input_string after specified number of characters from char_per_line"""
    # Use regex to find HTML tags, PlantUML links [[url label]], and words as individual tokens
    words = re.findall(r'<[^>]+>.*?</[^>]+>|\[\[.*?\]\]|[^<\s]+', input_string)
    mod = ""
    count = 0
    for word in words:
        if count + len(word) > chars_per_line:
            mod += "\n\t"
            count = 0
        mod += word + " "
        count += len(word) + 1
    return mod.strip() 

####################################################################################################
#                                                                                                  #
#                         Function to return Plantuml compliant String-(KEEP)                      #
#                                                                                                  #
####################################################################################################

def puml(step: str):
    """
    This function takes a single step and checks for any If statements and transforms the string for if loop where needed.
    It removes some of the markdown formatting, from the stringy, applies some formatting specific to plantuml 
    and calls insert_newline function to ensure plantuml boxes don't overflow before returning the string.
    """
    # 1. Extract markdown links [label](url) and replace them with placeholders
    # so they don't get messed up during case conversions.
    links = []
    def link_replacer(match):
        label = match.group(1)
        url = match.group(2)
        links.append((label, url))
        return f"___LINK_PLACEHOLDER_{len(links) - 1}___"
    
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    step_with_placeholders = re.sub(pattern, link_replacer, step)

    # Convert to uppercase for structural/keyword checks (like IF/THEN)
    p_step = step_with_placeholders.upper().strip()

    # Function to restore links after formatting
    def restore_links(text: str) -> str:
        for i, (label, url) in enumerate(links):
            placeholder_upper = f"___LINK_PLACEHOLDER_{i}___"
            placeholder_lower = f"___link_placeholder_{i}___"
            # Convert .md extension in the URL to .html to reference the built pages
            html_url = url.replace('.md', '.html')
            text = text.replace(placeholder_upper, f"[[{html_url} {label}]]")
            text = text.replace(placeholder_lower, f"[[{html_url} {label}]]")
        return text

    out = ""

    # Check if step starts with IF and contains a THEN 
    # If so, it is a candidate for If Then Else syntax of plantuml
    if p_step.startswith('IF') and 'THEN' in p_step:
        # Replace 'ELSE IF' with 'ELSEIF' so there is no clash with final ELSE statement
        if 'ELSE IF' in p_step:
            p_step = p_step.replace('ELSE IF','ELSEIF')
        # Create a variable to first remove just IF from the step
        if_removed = ''.join(re.split(r"\bIF\b", p_step)).strip()
        # Using above, remove 'ELSE'. This will be a list with two items
        else_removed_l = re.split(r"\bELSE\b", if_removed)
        # Now with If and Else removed, break the sentence first item from above list
        # at ELSEIF and store in another list below
        elif_removed_l = re.split(r"\bELSEIF\b", else_removed_l[0])
        # For every item in above list, break it down at THEN and store in a new list
        then_removed_l = []
        for elif_removed in elif_removed_l:
            then_removed_l += re.split(r"\bTHEN\b", elif_removed)
        # Initiate if loop parsing
        i = 0
        while i < len(then_removed_l): 
            if i==0:
                # The very first entry in then_removed_l is condition for if statement 
                # and second entry is then statement
                cond = restore_links(insert_newlines(then_removed_l[i].strip(), 20))
                val = restore_links(insert_newlines(then_removed_l[i+1].strip().capitalize(), 30))
                out += f'\tif ({cond}?) then (yes)\n\t\t:{val};\n'
                i = i+2
            elif i % 2 == 0:
                # Add elseif condition 
                cond = restore_links(insert_newlines(then_removed_l[i].strip().capitalize(), 20))
                out+= f'\t(no) elseif ({cond}?) then (yes)\n'
                i = i+1
            else:
                # Every odd entry is a then statement
                val = restore_links(insert_newlines(then_removed_l[i].strip().capitalize(), 30))
                out+=f'\t\t:{val};\n'
                i = i + 1
        # Check if ELSE exists in the step
        if len(else_removed_l)>1:
            val = restore_links(insert_newlines(else_removed_l[1].strip().capitalize(), 30))
            out += f'\telse (no)\n\t\t:{val};\n'
        else:
            out += f'\telse (no)\n\t\t\n'
        out += f'\tendif\n'
    elif step != '':
        if step.startswith('**') and step.endswith('**'):
            # If the step starts with ** and ends with **, apply different formatting and remove **
            raw_content = p_step.replace("**","").replace("`","").strip()
            raw_content = restore_links(raw_content)
            out += f'\t:<color: white>{insert_newlines(raw_content, 50)}</color>; <<#Maroon>>\n'
        elif step.startswith('--'):
            # If step starts with -- then its a single line comment
            raw_content = p_step.replace("`","").strip().capitalize()
            raw_content = restore_links(raw_content)
            out += f'\t{insert_newlines(raw_content, 50)}'
        elif step.startswith('[-'):
            # If step starts with [- then it is a string of multiline comments with newline in it
            p_steps_split = p_step.splitlines()
            for p_step_split in p_steps_split:
                raw_content = p_step_split.replace("`","").strip().capitalize()
                raw_content = restore_links(raw_content)
                out += f'\n\t{insert_newlines(raw_content, 50)}'
            out = f"{out}\n"
        else:
            # If the step does not start with ** and ends with **, apply standard formatting
            raw_content = p_step.replace("`","").strip().capitalize()
            raw_content = restore_links(raw_content)
            out += f'\t:{insert_newlines(raw_content, 50)};\n'
    return out
    #out = f'{steps_string}\n\n{out}'
    # Return final markdown for plantuml step
    return out
