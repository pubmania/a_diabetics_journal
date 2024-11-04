import re
####################################################################################################
#                                                                                                  #
#                                      Helper Functions                                            #
#                                                                                                  #
#################################################################################################### 

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


def find_ingredients(step: str) -> list[str]:
    """Find ingredients in a recipe step"""
    return find_specials(step, "@")

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

def parse_quantity(item: str) -> list[str, str]:
    """Parse the quantity portion of an ingredient
    e.g. 2%kg
    """
    if "%" not in item:
        if " " not in item: #in case the ingredient is just specified as a number with no unit
            return [item, "number"]
        else:
            return [item, ""]
    return item.split("%", maxsplit=1)
    
def find_cookware(step: str) -> list[str]:
    """Find ingredients in a recipe step"""
    return find_specials(step, "#")

def parse_cookware(item: str) -> dict[str, str]:
        """Parse cookware item
        e.g. #pot or #potato masher{}
        """
        if item[0] != "#":
            raise ValueError("Cookware should start with #")
        item = item.replace("{}", "")
        return item[1:] 

def find_timers(step: str) -> list[str]:
        """Find timers in a recipe step"""
        return find_specials(step, "~")

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

def replace_amount(value):
    # Replace fractions with decimals
    if '/' in value:
        numerator, denominator = value.split('/')
        try:
            value = str(float(numerator) / float(denominator))
        except ZeroDivisionError:
            value = '0'

    # Replace ranges with the highest value
    if '-' in value:
        value = value.split('-')[-1]

    # Replace worded items with 0
    if value.isalpha() or re.match(r'^[a-zA-Z\s]+$', value):
        value = '0'

    # Additional replacements
    value = value.lower().strip()
    if value == 'as needed' or value == 'to taste' or value == 'to taste (optional)':
        value = '0'
    elif value.endswith('l') or value.endswith('ml'):
        value = value[:-1]

    return value

def replace_unit(unit):
    # Remove information in brackets
    unit = re.sub(r'\(.*?\)', '', unit)

    # Remove trailing whitespace
    unit = unit.upper().strip()

    return unit
