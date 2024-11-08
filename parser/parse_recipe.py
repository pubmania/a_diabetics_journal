import re

####################################################################################################
#                                                                                                  #
#                           Function to Extract Cooklang Block                                     #
#                                                                                                  #
####################################################################################################
    
def fn_extract_cooklang_blocks(content):
    # Regular expression to find all occurrences of text between "```cooklang" and "```"
    pattern = r'```cooklang(.*?)```'
    
    # Use re.DOTALL to make '.' match newlines as well
    matches = re.findall(pattern, content, re.DOTALL)
    
    # Strip whitespace from each match and return the list
    return [match.strip() for match in matches]
