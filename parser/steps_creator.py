from parser.helpers import find_cookware, parse_cookware, parse_timer, find_timers, find_ingredients, parse_ingredient 
from parser.plantuml_steps_creator import puml

####################################################################################################
#                                                                                                  #
#                              Function to get formatted steps                                     #
#                                                                                                  #
####################################################################################################

def fn_steps_string(input_string):
    lines = input_string.splitlines()
    steps_string_new = ""
    p_step_string = ""
    step_count = 1
    p_step = ""
    #Remove metadata of cooklang that starts with >> and store it in variable inp_step
    for line in lines:
        if line.strip() != "" and not line.startswith(">>"):
            step = line.strip()
            for cookware in find_cookware(step):
                parsed_cookware = parse_cookware(cookware)
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
                    step = step.replace(ingredient,f'==*{ingredient_quantity} {ingredient_unit}* **{ingredient_name}**==')
                else:
                    step = step.replace(ingredient,f'==**{ingredient_name}**== ({ingredient_quantity})')
            p_step = puml(step.replace(':material-timer-sand-full:','')\
                          .replace('**==','</b>')\
                          .replace('==**','<b>')\
                          .replace('*==','</i>')
                          .replace('==*','<i>')\
                          .replace('* **','</i> <b>')
                          )
            if step != '':
                if step.startswith('**') and step.endswith('**'):
                    step = f"\n\n\t### {step.replace('**','')}\n\n"
             #       p_step = f"{p_step}"
                else:
                    step = f"\n\t* [ ] **{step_count}**: {step.strip()}"
                    step_count+=1
            steps_string_new += step
            p_step_string += p_step
    p_step_string = f"{p_step_string}\n"
    steps_string_new = f"{steps_string_new}\n"
    return steps_string_new,p_step_string