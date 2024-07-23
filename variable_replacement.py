#!/usr/bin/env python
# coding: utf-8

import os, re, json


def clean_rendered_files():
    current_directory = os.getcwd()
    qmd_directory = os.path.join(current_directory, 'catalog_sections')
    
    rendered_qmd_files = []
    for root, dirs, files in os.walk(qmd_directory):
        for file in files:
            if file.endswith("_rendered.qmd"):
                rendered_qmd_files.append(os.path.join(root, file))

    for file in rendered_qmd_files:
        os.remove(file)

    
def process_qmd_files():
    current_directory = os.getcwd()
    qmd_directory = os.path.join(current_directory, 'catalog_sections')
    
    qmd_files = find_qmd_files(qmd_directory)
    
    for qmd_file in qmd_files:
        replaced_text = replace_variables(qmd_file, current_directory)
            
        # Save the replaced text to a new file
        output_file = os.path.join(current_directory, qmd_file[0:-4] + "_rendered.qmd")
        with open(output_file, 'w', encoding='utf-8') as qmd_output_file:
            qmd_output_file.write(replaced_text)
        
        print("File has been successfully replaced as", output_file)
        
        
def find_qmd_files(qmd_directory):
    qmd_files = []
    for root, dirs, files in os.walk(qmd_directory):
        for file in files:
            if file.endswith(".qmd"):
                qmd_files.append(os.path.join(root, file))
    return qmd_files

def replace_variables(qmd_file, current_directory):
    course_dir = os.path.join(current_directory,'courses.json')
    course_extra_dir = os.path.join(current_directory,'courses_extra.json')
    
    with open(course_dir, 'r', encoding='utf-8') as json_file:
        course_data = json.load(json_file)
    with open(course_extra_dir, 'r', encoding='utf-8') as json_file:
        course_extra_data = json.load(json_file)

    course_data['c'].update(course_extra_dir['c'])

    with open(qmd_file, 'r', encoding='utf-8') as file:
        text = file.read()
        # Specify a pattern 
        pattern = r"{{< var (.*?)\.(.*?)\.(.*?) >}}"
        # Find variables that match the patterns 
        matches = re.findall(pattern, text)
        # Replaced variables components with their name and attributes 
        for match in matches:
            com_1, com_2, com_3 = match
            if com_2 in course_data['c'] and com_3 in course_data['c'][com_2]:
                replacement = course_data[com_1][com_2][com_3].strip("'\"")
            else:
                replacement = f"+++MISSING INFO: {com_1}.{com_2}.{com_3} +++"
                
            # Replace the variable pattern with the replacement
            variable_pattern = "{{< var " + ".".join(match) + " >}}"
            text = text.replace(variable_pattern, replacement)
        
        return text




# Delete the old rendered files first
clean_rendered_files()

# Process and create the new rendered files
process_qmd_files()







