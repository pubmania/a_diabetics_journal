from parser.helpers import find_cookware, parse_cookware, parse_timer, find_timers, find_ingredients, parse_ingredient 
from parser.plantuml_steps_creator import puml

####################################################################################################
#                                                                                                  #
#                  Function to get formatted steps and plantuml steps in list                      #
#                                                                                                  #
####################################################################################################

def fn_steps_list(input_str):
    parsed_cookwares = set()
    steps_list = []
    p_steps_list = []
    multiline_note = []
    multiline_flag = False
    lines = input_str.splitlines()
    step_count = 1
    p_step = ""
    for line in lines:
        if line.strip() != "" and not line.startswith(">>"):
            step = line.strip()
            p_step = line.strip()
            for cookware in find_cookware(step):
                parsed_cookware = parse_cookware(cookware)
                parsed_cookwares.add(parsed_cookware.title())
                p_step = step.replace(cookware, f"{parsed_cookware}")
                step = step.replace(cookware, f"{parsed_cookware}")
            for timer in find_timers(step):
                parsed_timer = parse_timer(timer)['quantity'] + ' ' + parse_timer(timer)['units']
                p_step = step.replace(timer, parsed_timer)
                step = step.replace(timer, f':material-timer-sand-full: {parsed_timer}')
            for ingredient in find_ingredients(step):
                parsed_ingredient = parse_ingredient(ingredient)
                ingredient_name = parsed_ingredient['name']
                ingredient_quantity = parsed_ingredient['quantity']
                ingredient_unit = parsed_ingredient['units']
                if ingredient_unit != '':
                    if ingredient_unit != 'Number':
                        p_step = p_step.replace(ingredient, f'<i>{ingredient_quantity} {ingredient_unit}</i> <b> {ingredient_name}</b>')
                        step = step.replace(ingredient, f'<cookmark><em>{ingredient_quantity} {ingredient_unit}</em> <strong> {ingredient_name}</strong></cookmark>')
                    else:
                        p_step = p_step.replace(ingredient, f'<i>{ingredient_quantity}</i> <b> {ingredient_name}</b>')
                        step = step.replace(ingredient, f'<cookmark><em>{ingredient_quantity}</em> <strong> {ingredient_name}</strong></cookmark>')
                else:
                    p_step = p_step.replace(ingredient, f'<b>{ingredient_name}</b> ({ingredient_quantity})')
                    step = step.replace(ingredient, f'<cookmark><strong>{ingredient_name}</strong></cookmark> ({ingredient_quantity})')
            if step.startswith('[-'):
                multiline_note.append(step)
                multiline_flag = True
            else:
                if step.endswith('-]'):
                    multiline_note.append(step)
                    multiline_step = '\n\t'.join(multiline_note).replace('[- ','<multiline>\n\t').replace(' -]','\n</multiline>').replace('[-','<multiline>\n\t').replace('-]','\n</multiline>')
                    multiline_flag = False
                    steps_list.append(multiline_step)
                    p_multiline_step = puml('\n'.join(multiline_note)).replace('[- ','note right\n\t').replace(' -]','\n\tend note').replace('[-','note right\n\t').replace('-]','\nend note')
                    p_steps_list.append(p_multiline_step)
                    multiline_note = []
                elif multiline_flag:
                    multiline_note.append(step)
                else:
                    if step.startswith('**') and step.endswith('**'):
                        p_steps_list.append(puml(step))
                        step_section = f"<strong>{step.replace('**', '')}</strong>"
                        steps_list.append(step_section)
                    else:
                        if step.startswith('--'):
                            p_note = puml(step).replace('-- ','note right\n\t').replace('--','note right\n\t')
                            p_steps_list.append(f"{p_note}\n\tendnote\n")
                            step_note = step.replace('--','<note>')
                            steps_list.append(f"{step_note}</note>")
                        else:
                            p_steps_list.append(f"{puml(p_step).replace(':', f':<b>Step {step_count}</b>: ', 1)}")
                            steps_list.append(f"<strong id='Step{step_count}'>Step {step_count}</strong>: {step}")
                            step_count+= 1
    return steps_list, p_steps_list, parsed_cookwares
