import re


def preprocess_info_dict(info_dict):
    for key, value in info_dict.items():
        if key == "resource-id":
            value_remove_app = value.split("/")[1]
            replace_underscore = value_remove_app.replace("_", " ")
            info_dict[key] = replace_underscore


        if key == "name":
            replace_underscore = value.replace("_", " ")
            info_dict[key] = replace_underscore

        camel_case_value = process_camel_case(value)
        info_dict[key] = camel_case_value

    return info_dict



def process_camel_case(string):
    if len(string) ==0:
        sentence=""
    else:
        splitted = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', string)).split()
        sentence = splitted[0]
        if len(splitted)>1:
            for i in [1,len(splitted)-1]:
                sentence = sentence + " " + splitted[i]
    return sentence