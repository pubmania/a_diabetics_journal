from parser.helpers import find_cookware, parse_cookware, parse_timer, find_timers, find_ingredients, parse_ingredient 
from parser.plantuml_steps_creator import puml

####################################################################################################
#                                                                                                  #
#                  Function to get formatted steps and plantuml steps in list                      #
#                                                                                                  #
####################################################################################################

def fn_steps_list(input_string):
    lines = input_string.splitlines()
    steps_list = []
    p_step_list = []
    step_count = 1
    p_step = ""
    parsed_cookwares = set()
    for line in lines:
        if line.strip() != "" and not line.startswith(">>"):
            step = line.strip()
            for cookware in find_cookware(step):
                parsed_cookware = parse_cookware(cookware)
                parsed_cookwares.add(parsed_cookware.title())
                step = step.replace(cookware,f"{parsed_cookware}")
            for timer in find_timers(step):
                parsed_timer = parse_timer(timer)['quantity'] + ' ' + parse_timer(timer)['units']
                step = step.replace(timer,f':material-timer-sand-full: {parsed_timer}')
            for ingredient in find_ingredients(step):
                parsed_ingredient = parse_ingredient(ingredient)
                ingredient_name = parsed_ingredient['name']
                ingredient_quantity = parsed_ingredient['quantity']
                ingredient_unit = parsed_ingredient['units']
                if ingredient_unit !='':
                    if ingredient_unit !='Number':
                        step = step.replace(ingredient,f'<cookmark><em>{ingredient_quantity} {ingredient_unit}</em> <strong> {ingredient_name}</strong></cookmark>')
                    else:
                        step = step.replace(ingredient,f'<cookmark><em>{ingredient_quantity}</em> <strong> {ingredient_name}</strong></cookmark>')
                else:
                    step = step.replace(ingredient,f'<cookmark><strong>{ingredient_name}</strong></cookmark> ({ingredient_quantity})')
            p_step = puml(step.replace(':material-timer-sand-full:','')\
                          .replace('<cookmark>','')\
                          .replace('</cookmark>','')\
                          .replace('<strong>','<b>')\
                          .replace('</strong>','</b>')\
                          .replace('<em>','<i>')\
                          .replace('</em>','</i>')
                          )
            if step != '':
                if step.startswith('**') and step.endswith('**'):
                    step = f"<strong>{step.replace('**','')}</strong>"
                else:
                    step = f"<strong>{step_count}</strong>: {step.strip()}"
                    step_count+=1
            steps_list.append(step)
            p_step_list.append(p_step)
    return steps_list,p_step_list,parsed_cookwares
