import os

####################################################################################################
#                                                                                                  #
#                           Function to get formatted metadata                                     #
#                                                                                                  #
####################################################################################################

def fn_metadata_string(input_string,image_path):
    #print(image_path)
    meta_data = {}
    meta_data_string_title = ""
    meta_data_string = ""
    image_data_string = ""
    lines = input_string.splitlines()

    for line in lines:
        if line.strip() != "" and line.startswith(">>"):
            key, value = line.lstrip(">> ").strip().split(": ")
            meta_data[key.strip()] = value.strip()
    if "Title" in meta_data:
        title = meta_data["Title"]
        del meta_data["Title"]
        meta_data_string_title = f"## {title}\n\n"
    else:
        meta_data_string = ""
    if "Image" in meta_data:
        final_image_path = os.path.join(image_path,meta_data["Image"])
        print(final_image_path)
        if "Image-Caption" in meta_data:
            #image_data_string += f"<figure markdown>![image]({image_path}"+meta_data["Image"]+"){: style=\"width: 920px;height: 430px;object-fit: contain;\"}<figcaption>" + meta_data["Image-Caption"] + "</figcaption></figure>"
            image_data_string += f"""
<figure class = "card">
<p><img alt="image" src="{final_image_path}" style="width: 920px;height: 430px;object-fit: contain;"></p>
<figcaption>{meta_data["Image-Caption"]}</figcaption>
</figure>
"""
            del meta_data["Image-Caption"]
            del meta_data["Image"]
        else:
            #image_data_string += f"<figure markdown>![image]({image_path}"+meta_data["Image"]+"){: style=\"width: 920px;height: 430px;object-fit: contain;\"}</figure>"
            image_data_string += f"""
<figure class = "card" >
<p><img alt="image" src="{image_path}/{meta_data["Image"]}" style="width: 920px;height: 430px;object-fit: contain;"></p>
</figure>
"""
            del meta_data["Image"]

    #cooking_data_string += "<div class=\"grid cards\" markdown>\n\n"
    temp_meta_data_string = ""
    other_meta_data_string = ""
    one_meta_data_string = ""
    two_meta_data_string = ""
    three_meta_data_string = ""
    four_meta_data_string = ""
    for key, value in meta_data.items():
        if key in ('Cooking Time','Serving Size','Type', 'Source'):
            if key == 'Cooking Time':
                one_meta_data_string = f":material-timer: *{value}*"
            elif key == 'Serving Size':
                two_meta_data_string = f":fontawesome-solid-chart-pie: *{value}*"
            elif key == 'Type':
                if value == 'Vegetarian':
                    three_meta_data_string = f"**{key}**: :leafy_green:"
                elif value == 'Vegetarian with Egg':
                    three_meta_data_string = f"**{key}**: :leafy_green::egg:"
                else:
                    three_meta_data_string = f"**{key}**: :cut_of_meat:"
            elif key == 'Source':
                four_meta_data_string = f"**{key}**: [:material-origin:]({value})"                
        else:
            other_meta_data_string += f"**{key}**: *{value}*" + '\n{ .card }\n\n'
    if one_meta_data_string != "":
        temp_meta_data_string = one_meta_data_string + '\n{ .card }\n\n'
    if two_meta_data_string != "":
        temp_meta_data_string += two_meta_data_string + '\n{ .card }\n\n'
    if three_meta_data_string != "":
        temp_meta_data_string += three_meta_data_string + '\n{ .card }\n\n'
    if four_meta_data_string != "":
        temp_meta_data_string += four_meta_data_string+"{target=_blank}" + '\n{ .card }\n\n'
    
    if image_data_string != "":
        meta_data_string += f'## Key Stats\n<div class="grid" markdown><div class="grid" markdown>{image_data_string}</div>\n\n<div align="center" class="grid" markdown>\n\n {temp_meta_data_string}{other_meta_data_string}\n</div></div>'
    else:
        meta_data_string += f'## Key Stats\n<div class="grid" markdown><div align="center" class="grid" markdown>\n\n {temp_meta_data_string}{other_meta_data_string}\n</div></div>'

    #print(meta_data_string.replace('\n{ .card }\n\n','\n'))
    return meta_data_string_title, meta_data_string
