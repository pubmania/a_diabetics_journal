"""
Basic example of a Mkdocs-macros module
"""

import re
import os

def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    - filter: a function with one of more arguments,
        used to perform a transformation
    """
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
                output += f'\n{indent}1. [**{dir_name}**](./{dir_name}/index.md)\n\n    ---\n\n'  # Add the directory to the TOC with indentation
                output += generate_toc_files(subdir, indent + '    ', include_dir_name_flag=True)

            return output

        output = generate_toc_files(directory)
        output += generate_toc_dirs(directory)

        return output
