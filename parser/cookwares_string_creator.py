from parser.helpers import find_cookware, parse_cookware

####################################################################################################
#                                                                                                  #
#                           Function to get formatted Cookwares                                    #
#                                                                                                  #
####################################################################################################

def fn_cookware_string(input_string):
    cookware_string = ""
    count = 1
    parsed_cookwares = set()
    for cookware in find_cookware(input_string):
        parsed_cookware = parse_cookware(cookware).title()
        parsed_cookwares.add(parsed_cookware)
    for parsed_cookware in parsed_cookwares:
        cookware_string += f"{count}. *{parsed_cookware}*\n"
        count+=1
    return cookware_string
