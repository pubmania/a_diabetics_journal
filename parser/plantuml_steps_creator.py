import re

####################################################################################################
#                                                                                                  #
#             Newlines in the input_string after specified number of characters-(KEEP)             #
#                                                                                                  #
####################################################################################################

def insert_newlines(input_string: str, chars_per_line: int):
    """Inserts newline in the input_string after specified number of characters from char_per_line"""
    # Use regex to find words and HTML elements
    words = re.findall(r'<[^>]+>.*?</[^>]+>|[^<\s]+', input_string)
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
    and calls insert_newline ffunction to ensure plantuml boxes don't overflow before returning the string.
    """
    out = ""

    # Convert step into uppercase for uniform comparison
    p_step = step.upper().strip()
    # Check if step starts with IF and contains a THEN 
    # If so, it is a candidate for If Then Else syntax of plantuml
    # If not treat it as normal step
    if p_step.startswith('IF') and 'THEN' in p_step:
        # Replace 'ELSE IF' with 'ELSEIF' so there is no clash with final ELSE statement
        if 'ELSE IF' in p_step:
            p_step = p_step.replace('ELSE IF','ELSEIF')
        # Create a variable to first remove just IF from the step
        if_removed = ''.join(re.split(r"\bIF\b", p_step)).strip()
        # Using above, remove 'ELSE'. This will be a list with two items
        else_removed_l = re.split(r"\bELSE\b", if_removed)
        # Now will If and Else removed, break the sentencefirst item from above list
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
                out += f'\tif ({insert_newlines(then_removed_l[i].strip(),20)}?) then (yes)\n\t\t:{insert_newlines(then_removed_l[i+1].strip().capitalize(),30)};\n'
                i = i+2
            elif i % 2 == 0:
                # Add elseif condition 
                #Logic is that variable then_removed_l has every even item as an elseif condition 
                # and every odd item as then statement
                out+= f'\t(no) elseif ({insert_newlines(then_removed_l[i].strip().capitalize(),20)}?) then (yes)\n'
                i = i+1
            else:
                #Every odd entry is a then statement so use it to create the then statement
                out+=f'\t\t:{insert_newlines(then_removed_l[i].strip().capitalize(),30)};\n'
                i = i + 1
        # Check if ELSE exists in the step and if it does include the final else statement
        if len(else_removed_l)>1:
            out += f'\telse (no)\n\t\t:{insert_newlines(else_removed_l[1].strip().capitalize(),30)};\n'
        else:
            out += f'\telse (no)\n\t\t\n'
        out += f'\tendif\n'
    elif step != '':
        if step.startswith('**') and step.endswith('**'):
            # If the step starts with ** and ends with **, apply different formatting and remove **
            step = step.replace("**","")
            out += f'\t#Maroon:<color: white>{insert_newlines(p_step.replace("`","").strip(),50)}</color>/\n'
        elif step.startswith('--'):
            # If step starts with -- then its a single line comment
            out += f'\t{insert_newlines(p_step.replace("`","").strip().capitalize(),50)}'
        elif step.startswith('[-'):
            # If step starts with [- then it is a string of multiline comments with newline in it
            # break each new line and then break it further based on number of characters.
            p_steps_split = p_step.splitlines()
            for p_step_split in p_steps_split:
                out += f'\n\t{insert_newlines(p_step_split.replace("`","").strip().capitalize(),50)}'
            out = f"{out}\n"
        else:
            # If the step does not start with ** and ends with **, apply standard formatting
            out += f'\t:{insert_newlines(p_step.replace("`","").strip().capitalize(),50)};\n'
    #out = f'{steps_string}\n\n{out}'
    # Return final markdown for plantuml step
    return out
