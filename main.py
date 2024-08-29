"""
Basic example of a Mkdocs-macros module
"""

import math
import re
import os
import pandas as pd
from fractions import Fraction
import requests
from thefuzz import fuzz, process

def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    - filter: a function with one of more arguments,
        used to perform a transformation
    """

    def read_upload(obj_file,str_sheetname,col_list=None, date_col_list=False, file_type='xlsx', file_name=''):
        dataframe=""    
        try:
            if obj_file is not None:
                if file_type == 'csv':
                    dataframe = pd.read_csv(obj_file, usecols=col_list, parse_dates = date_col_list).applymap(lambda s: s.upper() if type(s) == str else s).fillna('')
                else:
                    dataframe = pd.read_excel(obj_file,sheet_name = str_sheetname, usecols=col_list, parse_dates = date_col_list).applymap(lambda s: s.upper() if type(s) == str else s).fillna('')
            else:
                dataframe= file_name+" is Empty - Provide a file name first"
                #print(dataframe)
        except ValueError as e:
            print("Problem: "+ e.args[0])
        finally:
            return dataframe

    def get_indian_db_nutrient_information(ingredients):
        """ runs a fuzzy search on provided ingredient dataframe against indian_db"""
        #get data from csv file into a dataframe
        obj_file = 'indian_db.csv'
        str_sheetname = 'indian_db'
        col_list = ['Food Name; name', 'Energy; enerc',	'Total Fat; fatce',	'Dietary Fiber; fibtg',	'Carbohydrate; choavldf', 'Protein; protcnt']
        df_in_food_db = read_upload(obj_file,str_sheetname,col_list, date_col_list=False, file_type='csv', file_name='indian_db.csv')
        #rename columns
        df_in_food_db.rename(columns = { 'Food Name; name' : 'Food Name', \
                                        'Carbohydrate; choavldf' : 'Carbohydrate (g)', \
                                        'Protein; protcnt' : 'Protein (g)', \
                                        'Total Fat; fatce' : 'Fat (g)', \
                                        'Dietary Fiber; fibtg' : 'Fibre',
                                        'Energy; enerc' : 'Energy'}, inplace=True)
        #print(df_in_food_db.head(5))
        df_in_options_inner = pd.DataFrame()
        choices = df_in_food_db['Food Name'].unique()
        for item in ingredients:
            ingredient = item.upper()
            comp_var = process.extract(ingredient, choices, limit=6)
            #print(comp_var)
            #print(item)
            if comp_var:
                for i in range(len(comp_var)):
                    if comp_var[i][1] >=90:
                        df_filtered = df_in_food_db[df_in_food_db['Food Name'] == comp_var[i][0]][['Food Name','Carbohydrate (g)', 'Protein (g)','Fat (g)','Energy','Fibre']]
                        df_filtered['Searched Ingredient'] = ingredient
                        df_in_options_inner = pd.concat([df_in_options_inner, df_filtered])
                        # if match was 100% then break from this for loop to get next item from outer for loop.
                        if comp_var[i][1] == 100:
                            break
        
        return df_in_options_inner


    def get_nccdb_nutrient_information(api_key, ingredients, nutrient_ids=[1008, 1005, 1079, 1003, 1004]):
        #print(f'get_nccdb_nutrient_information --- {ingredients}')
        url = "https://api.nal.usda.gov/fdc/v1/foods/search"
        headers = {"Content-Type": "application/json"}
        nutrient_data = []  # List to store the extracted nutrient information
        df_options_nccdb_inner = pd.DataFrame()
        for ingredient in ingredients:
            #print(ingredient)
            params = {
                "query": ingredient,
                "pageSize": 10,
                "api_key": api_key
            }

            response = requests.get(url, headers=headers, params=params)
            response_json = response.json()

            foods = response_json.get('foods', [])
            #print(len(foods))
            if foods:
                for i in range(len(foods)):
                    food = foods[i]
                    #print(food['description'])
                    nutrient_info = {
                        'Food Name': ''.join(food['description'].upper().split(','))
                    }
                    for nutrient in food.get('foodNutrients', []):
                        if nutrient['nutrientId'] in nutrient_ids:
                            nutrient_info[nutrient['nutrientName']] = nutrient['value']
                    nutrient_data.append(nutrient_info)
                df_nccdb = pd.DataFrame(nutrient_data)
                patterns = ['RECIPE', 'CANS', 'BISCUIT', 'NO FRUIT PIECES', \
            'FLAVOURS','BEEF','DISH','LAMB','PIE','DESSERT','INCLUDING',\
            'SAMPLES','MANUFACTURER','CURRY','BRAMLEY','CLOVER','LIGHT MEAT','COOKED',\
           'LEAN AND','EDIBLE PORTION OF','EDIBLE CONVERSION FACTOR','BOILED','STEAMED',\
           'JARS','FISH','ROAST','FRIED','GRILLED', 'MEAT AND','JUICE DRINK', 'CARBONATED',\
           'KEBAB','CRAB','WEIGHT LOSS','FILLETS','CAKE','SALTED', 'SMOKED','GOOSE','HARE',\
            'HAM','BAKED','TURKEY','PUNJABI','TONGUE','SABJI','OX','TUNA','HOMEMADE','WITH SUGAR',\
            'STEWED','FAT FREE','PUDDING','SAUSAGE','PORK','PASTRY','RETAIL','SOUP','SQUID','STEAK',\
            'STEW','WEDGES','SWEETS','BOILED','JAM','INFUSION','BURGER','TOFFEE','TRIFLE','TOPPING',\
           'TURKEY','CASSEROLE','DIP','PICKLED','SAUCE']
                pattern = '|'.join(patterns)  # Combine multiple patterns with the OR operator

                df_nccdb = df_nccdb[~(df_nccdb['Food Name'].str.contains(pattern, flags=re.IGNORECASE))]
                choices = df_nccdb['Food Name'].unique()
                comp_var = process.extract(ingredient, choices, limit=6)
             #   print(comp_var)
              #  print(len(comp_var))

                if comp_var:
                    for i in range(len(comp_var)):
                        if comp_var[i][1] >=90:
                            df_filtered = df_nccdb[df_nccdb['Food Name'] == comp_var[i][0]].reset_index(drop=True)
                            df_filtered['Searched Ingredient'] = ingredient
                            df_options_nccdb_inner = pd.concat([df_options_nccdb_inner, df_filtered])
                            if comp_var[i][1] == 100:
                                break
                    #df_options_nccdb_inner['Searched Ingredient'] = ingredient

        #df = pd.DataFrame(nutrient_data)
        #print(df_options_nccdb_inner.keys())
        if not df_options_nccdb_inner.empty:
            df_options_nccdb_inner['Net Carbs'] = df_options_nccdb_inner['Carbohydrate, by difference'] - df_options_nccdb_inner['Fiber, total dietary'].fillna(0)
            #df_options_nccdb_inner.rename(columns = { 'Carbohydrate, by difference' : 'Carbohydrate (g)','Protein' : 'Protein (g)', 'Total lipid (fat)' : 'Fat (g)', 'Energy' : 'Energy (kcal) (kcal)'}, inplace=True)
        #Total lipid (fat) |   Carbohydrate, by difference |   Energy |   Fiber, total dietary
        #df = df_options_nccdb_inner[['Searched Ingredient','Food Name', 'Carbohydrate (g)', 'Fiber, total dietary', 'Net Carbs', 'Protein (g)', 'Fat (g)', 'Energy (kcal) (kcal)']]
        #print(df)
        return df_options_nccdb_inner     
    
    def get_matches(df):
        """ runs a fuzzy search on provided dataframe """
        #from rapidfuzz import process
        obj_file = './docs/assets/tables/McCance_Widdowsons_Composition_of_Foods_Integrated_Dataset_2021.xlsx'
        str_sheetname = '1.3 Proximates'
        col_list = ['Food Name','Description','Carbohydrate (g)', 'Protein (g)','Fat (g)','Energy (kcal) (kcal)','AOAC fibre (g)']
        df_uk_food_db = read_upload(obj_file,str_sheetname,col_list, date_col_list=False, file_type='xlsx', file_name='McCance_Widdowsons_Composition_of_Foods_Integrated_Dataset_2021.xlsx')
        #print(df_uk_food_db.shape)
        #df_uk_food_db = df_uk_food_db[~[df_uk_food_db['Description'] contains ['Recipe']]]
        patterns = ['RECIPE', 'CANS', 'BISCUIT', 'NO FRUIT PIECES', \
            'FLAVOURS','BEEF','DISH','LAMB','PIE','DESSERT','INCLUDING',\
            'SAMPLES','MANUFACTURER','CURRY','BRAMLEY','CLOVER','LIGHT MEAT','COOKED',\
           'LEAN AND','EDIBLE PORTION OF','EDIBLE CONVERSION FACTOR','BOILED','STEAMED',\
           'JARS','FISH','ROAST','FRIED','GRILLED', 'MEAT AND','JUICE DRINK', 'CARBONATED',\
           'KEBAB','CRAB','WEIGHT LOSS','FILLETS','CAKE','SALTED', 'SMOKED','GOOSE','HARE',\
            'HAM','BAKED','TURKEY','PUNJABI','TONGUE','SABJI','OX','TUNA','HOMEMADE','WITH SUGAR',\
            'STEWED','FAT FREE','PUDDING','SAUSAGE','PORK','PASTRY','RETAIL','SOUP','SQUID','STEAK',\
            'STEW','WEDGES','SWEETS','BOILED','JAM','INFUSION','BURGER','TOFFEE','TRIFLE','TOPPING',\
           'TURKEY','CASSEROLE','DIP','PICKLED','SAUCE']
        pattern = '|'.join(patterns)  # Combine multiple patterns with the OR operator

        df_uk_food_db = df_uk_food_db[~((df_uk_food_db['Description'].str.contains(pattern, flags=re.IGNORECASE))\
                                        | (df_uk_food_db['Food Name'].str.contains(pattern, flags=re.IGNORECASE)))]
        df_options = pd.DataFrame()
        df_options_indian_db = pd.DataFrame()
        df_options_nccdb = pd.DataFrame()
        filtered_list = []
        choices = df_uk_food_db['Food Name']
        #print(df['Ingredient'].unique())
        for item in df['Ingredient'].unique():
            comp_var = process.extract(item, choices, limit=6)
            #print(comp_var)
            #print(item)
            if comp_var:
                for i in range(len(comp_var)):
                    if comp_var[i][1] >=90:
                        df_filtered = df_uk_food_db[df_uk_food_db['Food Name'] == comp_var[i][0]][['Food Name','Carbohydrate (g)', 'Protein (g)','Fat (g)','Energy (kcal) (kcal)','AOAC fibre (g)']]
                        df_filtered['Searched Ingredient'] = item
                        df_options = pd.concat([df_options, df_filtered])
                        if comp_var[i][1] == 100:
                            break
        possible_matches = ''
        #api_key = 'Eh9D1nEdlNelglzDArOB0HJm2baBBk4IFrcYUZQG'
        api_key = os.environ.get('NCCDB_API_KEY')
        #print(f'api_key = {api_key}')
        if df_options.empty:
            possible_matches = ''
            ### Pass the whole ingredient list to nccdb as nothing was found on ukdb
            filtered_list = df['Ingredient'].to_list()
            #print(filtered_list)
        else:
            df_options = df_options[['Searched Ingredient','Food Name', 'Carbohydrate (g)', 'Protein (g)', 'Fat (g)','Energy (kcal) (kcal)', 'AOAC fibre (g)']]
            possible_matches_res = '\n\t\t' + df_options.to_markdown(index=False).replace('\n','\n\t\t')
            possible_matches = f'\t\t*Possible matches in [McCance and Widdowson\'s composition of foods integrated dataset](https://www.gov.uk/government'+\
                f'/publications/composition-of-foods-integrated-dataset-cofid#full-publication-update-history)'+\
                "{target=_blank}"+ f' are shown below:*\n{possible_matches_res}'
            ### Pass the ingredients not found on ukdb to indian_db
            filtered_list = df['Ingredient'][~(df['Ingredient'].isin(df_options['Searched Ingredient']))].to_list()

        ### Call indian_db for ingredient not available on ukdb
        if filtered_list:              
            df_options_indian_db = get_indian_db_nutrient_information(filtered_list).fillna(0)
            #print(f'filtered_list before calling indian db: {filtered_list}')
        
        if df_options_indian_db.empty:
            possible_matches += ''
        else:            
            df_options_indian_db = df_options_indian_db.drop_duplicates(subset='Food Name')
            df_options_indian_db = df_options_indian_db[['Searched Ingredient', 'Food Name', 'Carbohydrate (g)', 'Protein (g)', 'Fat (g)', 'Energy', 'Fibre']]
            possible_matches_indian_db = '\n\n\t\t' + df_options_indian_db.to_markdown(index=False).replace('\n','\n\t\t')
            possible_matches += f'\n\n\t\t*Possible matches in [Indian Food Composition Database](https://ifct2017.com/frame.php?page=food'+\
            f')'+\
            "{target=_blank}"+ f' are shown below:*\n{possible_matches_indian_db}'
            
            ## Reduce filtered list to items not found in indian_db
            filtered_list = [item for item in filtered_list if item.upper() not in df_options_indian_db['Searched Ingredient'].values]
            #print(f'filtered_list before calling nccdb: {filtered_list}')
            #print(df_options_indian_db['Searched Ingredient'])
            
        ### Call nccdb for ingredients not available on indian_db
        if filtered_list:              
            try:
                df_options_nccdb = get_nccdb_nutrient_information(api_key, filtered_list).fillna(0)
            except:
                pass
        if df_options_nccdb.empty:
            possible_matches += ''
        else:
            df_options_nccdb.rename(columns = { 'Carbohydrate, by difference' : 'Carbohydrate (g)','Protein' : 'Protein (g)', 'Total lipid (fat)' : 'Fat (g)', 'Energy' : 'Energy (kcal) (kcal)'}, inplace=True)
            df_options_nccdb = df_options_nccdb[['Searched Ingredient','Food Name', 'Carbohydrate (g)', 'Fiber, total dietary', 'Net Carbs', 'Protein (g)', 'Fat (g)', 'Energy (kcal) (kcal)']].drop_duplicates(subset='Food Name')
            possible_matches_nccdb = '\n\n\t\t' + df_options_nccdb.to_markdown(index=False).replace('\n','\n\t\t')
            possible_matches += f'\n\n\t\t*Possible matches in [U.S. Department of Food Central database](https://fdc.nal.usda.gov/fdc-app.html#/'+\
            f')'+\
            "{target=_blank}"+ f' are shown below:*\n{possible_matches_nccdb}'
        #print(possible_matches)
        return possible_matches

    def get_unformatted_line(input_string: str):
        """Takes input_string as input, and removes all cookland notation from steps 
        and retains metadata as is and returned the steps as a list of lines"""

        #Remove individual timer notation ~{25%minutes} or ~{25-30%minutes}
        pattern = r'~{(\d+)(?:-(\d+))?%([^}]+)}'
        replacement = lambda match: f"{match.group(1)}-{match.group(2)} {match.group(3)}" if match.group(2) else f"{match.group(1)} {match.group(3)}"
        input_string = re.sub(pattern, replacement,input_string)
        #split resulting steps with time formatting removed further remove ingredient and cookware formatting
        lines = input_string.replace("{}", '').\
            replace("@", "").\
            replace("%", " ").\
            replace("#", '').\
            replace("~", '').\
            replace("{", ' (').\
            replace("}", ')').\
            splitlines()
        return lines
    
    def remove_markdown_link_in_puml(input_text):
        # Define a regular expression pattern to match [some text](URL) and capture the groups
        pattern = r'\[([^]]+)\]\(([^)]+)\)'
    
        # Use re.sub to replace the matches with the desired format
        transformed_text = re.sub(pattern, r'\1', input_text)
    
        return transformed_text   

    def puml(input_string: str):
        inp_str = ''
        style_str = """
            <style>
            activityDiagram {
              diamond {
                BackgroundColor #darkgreen
                LineColor #white
                FontColor white
              }
            }
            </style>
        """
        lines = get_unformatted_line(input_string)
        #Remove metadata of cooklang that starts with >> and store it in variable inp_str
        for line in lines:
            if line.strip() != "" and not line.startswith(">>"):
                inp_str += f'{line.strip()}\n'
        #steps = inp_str.split('\n')
        steps = inp_str.splitlines()
        steps_string = "<div class=\"grid cards\" markdown>\n\n\n-   ## Steps\n\n\t---"
        out = "\n-   ## Process\n\n\t---\n\n\t```plantuml\n\t@startuml\n\t!theme aws-orange\n\t"+style_str+"\n\tstart\n"
        for step in steps:
            # Convert step into uppercase for uniform comparison
            p_step = remove_markdown_link_in_puml(step.replace("`","").upper())
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
                        out+= f'\t(no) elseif ({insert_newlines(then_removed_l[i].strip(),20)}?) then (yes)\n'
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
                step_line = f"\n\t* [ ] {step.strip()}"
            # Ignore empty line in steps
            elif step != '':
                if step.startswith('**') and step.endswith('**'):
                    # If the step starts with ** and ends with **, apply different formatting and remove **
                    step = step.replace("**","")
                    out += f'\t#Black:**{insert_newlines(p_step.replace("`","").strip(),50)}**/\n'
                    step_line = f"\n\n\t### {step}\n\n"
                else:
                    # If the step does not start with ** and ends with **, apply standard formatting
                    out += f'\t:{insert_newlines(p_step.replace("`","").strip(),50)};\n'
                    step_line = f"\n\t* [ ] {step.strip()}"
            steps_string += step_line
        out += f'\tend\n\t@enduml\n\t```\n\n</div>\n\n'
        out = f'{steps_string}\n\n{out}'
        # Return final markdown for steps and plantuml
        return out

    def parse_cookware(item: str) -> dict[str, str]:
        """Parse cookware item
        e.g. #pot or #potato masher{}
        """
        if item[0] != "#":
            raise ValueError("Cookware should start with #")
        item = item.replace("{}", "")
        return item[1:]


    def parse_quantity(item: str) -> list[str, str]:
        """Parse the quantity portion of an ingredient
        e.g. 2%kg
        """
        if "%" not in item:
            return [item, ""]
        return item.split("%", maxsplit=1)


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

    def find_cookware(step: str) -> list[str]:
        """Find cookware items in a recipe step"""
        return find_specials(step, "#")


    def find_ingredients(step: str) -> list[str]:
        """Find ingredients in a recipe step"""
        return find_specials(step, "@")


    def find_timers(step: str) -> list[str]:
        """Find timers in a recipe step"""
        return find_specials(step, "~")

    def insert_newlines(input_string: str, chars_per_line: int):
        """Inserts newline in the input_string after specified number of characters from char_per_line"""
        words = input_string.split()
        mod = ""
        count = 0
        for word in words:
            if count + len(word) > chars_per_line:
                mod += "\n\t"
                count = 0
            mod += word + " "
            count += len(word) + 1
        return mod.strip()    

    # create a jinja2 filter
    @env.filter
    def generate_toc_full(directory):
        def generate_toc_files(directory, indent='', include_dir_name_flag=False):
            output = ''
            # Generate TOC for files in the current directory
            files = [f for f in os.listdir(directory) if f.endswith('.md')]
            sorted_files = sorted(files, key=lambda x: os.path.getctime(os.path.join(directory, x)))
            for file_name in sorted_files:
                recipe_name = ' '.join(file_name.split('.')[0].split('_')[2:]).title()
                if recipe_name != '':
                    if '\\' in directory:
                        dir_name_mod = directory.split('\\')[1].replace(' ', '%20')
                    else:
                        dir_name_mod_l = directory.split('/')
                        dir_name_mod = dir_name_mod_l[len(dir_name_mod_l) - 1].replace(' ', '%20')
                    if include_dir_name_flag:
                        output += f'{indent}1. [{recipe_name}](./{dir_name_mod}/{file_name})\n'  # Add the file to the TOC with indentation
                    else:
                        output += f'{indent}1. [{recipe_name}](./{file_name})\n'  # Add the file to the TOC with indentation

            return output

        def generate_toc_dirs(directory, indent=''):
            output = ''
            # Recursively generate TOC for subdirectories
            subdirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
            sorted_subdirs = sorted(subdirs, key=lambda x: len(os.listdir(os.path.join(directory, x))), reverse=True)
            for dir_name in sorted_subdirs:
                subdir = os.path.join(directory, dir_name)
                output += f'\n{indent}1. [**{dir_name}**](./{dir_name})\n\n    ---\n\n'  # Add the directory to the TOC with indentation
                output += generate_toc_files(subdir, indent + '    ', include_dir_name_flag=True)

            return output

        output = generate_toc_files(directory)
        output += generate_toc_dirs(directory)

        return output
                        
    @env.filter
    def parse_recipe(input_string):
        cooklang_block = f'\n??? abstract "Recipe in [Cooklang](https://cooklang.org/)' + '{target=_blank' + '}"\n\t```\n\t' + input_string.replace("\n","\n\t") + '```'
        ingredients = {}
        cookwares = set()
        steps = []
        cooking_data = {}
        ################### Extract Ingredients ###########################
        matches = []
        for item in find_ingredients(input_string):
            matches.append(parse_ingredient(item))
        for match in matches:
            ingredient_name = match['name'].title()
            amount = match['quantity']
            unit = match['units']

            ingredient_key = ingredient_name
            if ingredient_key in ingredients:
                ingredients[ingredient_key].append((amount, unit))
            else:
                ingredients[ingredient_key] = [(amount, unit)]
                
        ##################### Extract cookwares ############################
        cookware_matches = find_cookware(input_string)
        for cookware_match in cookware_matches:
            cookware_name = parse_cookware(cookware_match).title()
            cookwares.add(cookware_name)
        
        ##################### Extract cooking data and steps ################
        lines = get_unformatted_line(input_string)
        
        for line in lines:
            if line.strip() != "" and line.startswith(">>"):
                key, value = line.lstrip(">> ").strip().split(": ")
                cooking_data[key.strip()] = value.strip()
            elif line.strip() != "":
                steps.append(line.strip())
        ###################### Ingredient Block ########################
        ingredient_string = ""
        ingredient_string += "<div class=\"grid cards\" markdown>\n\n\n-   ## Ingredients\n\n\t---\n"
        #ingredient_string += "\n## Ingredients\n\n\t---\n"
        ingredient_count = 1
        for ingredient_name in ingredients.keys():
            #check if ingredient has been used more than once so it can be listed accordingly
            if len(ingredients[ingredient_name]) > 1:
                ingredient_line = f"\t\t{ingredient_count}. {ingredient_name}:"
                ingredient_string += ingredient_line + "\n"
                for amount, unit in ingredients[ingredient_name]:
                    ingredient_line = f"\t\t\t- {amount} {unit}"
                    ingredient_string += ingredient_line + "\n"
            else:
                # if ingredient is used only once, list as a single line with amount and units in same line
                ingredient_line = ""
                for amount, unit in ingredients[ingredient_name]:
                    ingredient_line += f"\t\t{ingredient_count}. {ingredient_name}: {amount} {unit}"
                ingredient_string += ingredient_line + "\n"
            ingredient_count += 1
        ###################### Ingredient Listing ########################    
        if cookwares:
            cookware_string = "\n-   ## Cookwares\n\n\t---\n"
            cookware_count = 1
            for cookware in cookwares:
                cookware_line = f"\t{cookware_count}. *{cookware}*"
                cookware_count += 1
                cookware_string += cookware_line + "\n"
        else:
            cookware_string = ''
        cookware_string += '\n\n</div>\n\n'
        if "Title" in cooking_data:
            title = cooking_data["Title"]
            del cooking_data["Title"]
            cooking_data_string = f"## {title}\n\n"
        else:
            cooking_data_string = ""
        ######################### NET CARB TABLE #################
        df_ingredient_db = pd.read_csv('ingredient_db.csv')
        df_unit_db = pd.read_csv('unit_db.csv')
        # Create an empty list to store data frames
        dfs = []
        # Iterate over the dictionary items and create a data frame for each ingredient
        for ingredient, amounts in ingredients.items():
            temp_df = pd.DataFrame(amounts, columns=['Amount', 'Unit'])
            temp_df['Ingredient'] = ingredient
            dfs.append(temp_df)
        # Concatenate the data frames into a single data frame
        df = pd.concat(dfs, ignore_index=True)
        # Now merge df and df_ingredient_db with inner join to get net carb values for recipe ingredients using code below:
        df_merge = df.merge(df_ingredient_db, how='inner', left_on=df['Ingredient'].str.upper(), right_on=df_ingredient_db['Name'].str.upper())
        # Define functions to calculate net carbs, conversion factor etc
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

        def conv_factor(row):
            filtered_units = df_unit_db[df_unit_db['Unit'].str.upper() == replace_unit(row['Unit_x'])]['eq_gms']
            if not filtered_units.empty:
                conv_factor = float(filtered_units.values[0])
                return conv_factor
            return 0
        def calculate_cal_net_carb(row):
            filtered_units = df_unit_db[df_unit_db['Unit'].str.upper() == replace_unit(row['Unit_x'])]['eq_gms']
            if not filtered_units.empty:
                gms_used_in_recipe = float(filtered_units.values[0]) * float(Fraction(replace_amount(row['Amount'])))
                if row['Net_carb/100gms'] != '0' and row['Net_carb/100gms'] != 0:
                    return (gms_used_in_recipe * float(row['Net_carb/100gms']))/100
            return 0
        def calculate_amt_in_gms(row):
            filtered_units = df_unit_db[df_unit_db['Unit'].str.upper() == replace_unit(row['Unit_x'])]['eq_gms']
            if not filtered_units.empty:
                gms_used_in_recipe = float(filtered_units.values[0]) * float(Fraction(replace_amount(row['Amount'])))
                return gms_used_in_recipe
            return 0
        # Add calculated columns to the dataframe:
        df_merge['Conversion Factor'] = df_merge.apply(conv_factor, axis=1)
        df_merge['Amount used in Recipe(gms)'] = df_merge.apply(calculate_amt_in_gms, axis=1)
        df_merge['Calculated Net Carb in recipe'] = df_merge.apply(calculate_cal_net_carb, axis=1).round(2)
        df_merge['Unit_x'] = df_merge['Unit_x'].astype(str).apply(replace_unit)
        df_merge.rename(columns = {'Unit_x' : 'Recipe Unit', 'Unit_y' : 'Converted Unit'}, inplace=True)
        
        # Create final markdown table:
        grand_total = f"**{df_merge['Calculated Net Carb in recipe'].sum().round(2)}**"
        result = df_merge[['Ingredient', 'Amount','Recipe Unit','Conversion Factor', 'Amount used in Recipe(gms)', 'Net_carb/100gms','Source','Calculated Net Carb in recipe']]

        # Create a DataFrame for the grand total
        grand_total_df = pd.DataFrame({'Source':'-','Net_carb/100gms': '-','Amount':'-','Recipe Unit': '-','Ingredient': ['**Grand Total**'], 'Calculated Net Carb in recipe': [grand_total], 'Conversion Factor': '-','Amount used in Recipe(gms)': '-' })

        # Concatenate the result DataFrame with the grand total DataFrame
        result = pd.concat([result, grand_total_df], ignore_index=True)
        
        # Find ingredients that are not on ingredient_db
        df_ingredients_not_found =  df[~df['Ingredient'].str.upper().isin(df_ingredient_db['Name'].str.upper())]
        not_found = ''
        if df_ingredients_not_found.empty:
            not_found = ''
        else:
            not_found = ', '.join(df_ingredients_not_found['Ingredient'].unique())
            possible_match = get_matches(df_ingredients_not_found)
            
        # Add the result DataFrame as markdown 
        netcarb_string = f'???+ Info "Calculated Net Carb Info (Total Net Carbs for entire dish: {grand_total})"\n\t' + result.to_markdown(index=False).replace("\n","\n\t")
        if not_found != '':
            netcarb_string += '\n\n\t!!! warning "Caution"\n\t\t*The calculation is indicative and my lookup list'+\
            ' did not have net carb values for* **' +\
            not_found +\
            '** *and thus not included in the calculations above.*\n\n'
            if possible_match != '': 
                netcarb_string += possible_match
        ######################### NET CARB TABLE ####################################
        
        ########################### COOKING DATA STRING #############################
        if "Image" in cooking_data:
            if "Image-Caption" in cooking_data:
                image_data_string = f"## Image\n\n<figure markdown>\n![image](../../assets/images/"+cooking_data["Image"]+"){: style=\"width: 920px;height: 430px;object-fit: contain;\"}\n<figcaption>" + cooking_data["Image-Caption"] + "</figcaption>\n</figure>\n\n"
                del cooking_data["Image-Caption"]
                del cooking_data["Image"]
            else:
                image_data_string = f"## Image\n\n<figure markdown>\n![image](../../assets/images/"+cooking_data["Image"]+"){: style=\"width: 920px;height: 430px;object-fit: contain;\"}\n</figure>\n\n"
                del cooking_data["Image"]
        else:
            image_data_string = ""        
        #cooking_data_string += "<div class=\"grid cards\" markdown>\n\n"
        temp_cooking_data_string = ""
        one_cooking_data_string = ""
        two_cooking_data_string = ""
        three_cooking_data_string = ""
        four_cooking_data_string = ""
        for key, value in cooking_data.items():
            if key in ('Cooking Time','Serving Size','Type', 'Source'):
                if key == 'Cooking Time':
                    one_cooking_data_string = f":material-timer: *{value}*"
                elif key == 'Serving Size':
                    two_cooking_data_string = f", :fontawesome-solid-chart-pie: *{value}*"
                    if value.split(' ')[0].isdigit():
                        net_carb_per_serving = round((float(grand_total.replace('*', '')) / int(value.split(' ')[0])), 2)
                        net_carb_per_serving_string = f', **Net Carbs per serving:** *[{net_carb_per_serving}](#nutritional-info)* '
                        #print(value.split(' '))
                    else:
                        net_carb_per_serving_string = ''
                elif key == 'Type':
                    if value == 'Vegetarian':
                        three_cooking_data_string = f", **{key}**: :leafy_green:"
                    elif value == 'Vegetarian with Egg':
                        three_cooking_data_string = f", **{key}**: :leafy_green::egg:"
                    else:
                        three_cooking_data_string = f", **{key}**: :cut_of_meat:"
                elif key == 'Source':
                    four_cooking_data_string = f", **{key}**: [:material-origin:]({value})"                
            else:
                cooking_data_string += f", **{key}**: *{value}*"
        if one_cooking_data_string != "":
            temp_cooking_data_string = one_cooking_data_string 
        if two_cooking_data_string != "":
            temp_cooking_data_string += two_cooking_data_string
        if three_cooking_data_string != "":
            temp_cooking_data_string += three_cooking_data_string
        if four_cooking_data_string != "":
            temp_cooking_data_string += four_cooking_data_string + "{target=_blank}"
        cooking_data_string = f'<div class=\"grid cards\" align = \"center\" markdown>\n\n-   ## Key Stats\n\n\t---\n\n\t   ' +\
        temp_cooking_data_string + cooking_data_string +\
        net_carb_per_serving_string + \
        f', **Total Net Carbs:** [{grand_total}](#nutritional-info) '+\
        '\n\n</div>\n\n'
        ############################## Cooking Data ################################
        steps_dia_string = puml(input_string)
        
        
        
        final_output_string = '\n\n' + image_data_string + cooking_data_string + "\n" + \
        ingredient_string + "\n" + cookware_string + "\n\n" +\
        steps_dia_string + '\n\n## Nutritional Info\n\n' + netcarb_string + "\n\n\n"+ cooklang_block 
        return final_output_string
