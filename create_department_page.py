#!/usr/bin/env python
# coding: utf-8

import os, re, json


def clean_department_file():
    current_directory = os.getcwd()
    qmd_directory = os.path.join(current_directory, 'catalog_sections')
    
    rendered_qmd_files = []
    for root, dirs, files in os.walk(qmd_directory):
        for file in files:
            if file.endswith("departmental_programs_rendered.qmd"):
                rendered_qmd_files.append(os.path.join(root, file))

    for file in rendered_qmd_files:
        os.remove(file)

    
def process_departmental_files():
    current_directory = os.getcwd()
    qmd_directory = os.path.join(current_directory, 'catalog_sections')
    
    qmd_files = []
    for root, dirs, files in os.walk(qmd_directory):
        for file in files:
            if file.endswith("departmental_programs.qmd"):
                qmd_files.append(os.path.join(root, file))

    if len(qmd_files) > 1:
        error("Too many departmental_programs.qmd files detected!")

    with open(qmd_files[0],"r") as fid:
        dept_text = fid.read().strip().split("\n")

    output_file = open(qmd_files[0][0:-4]+"_rendered.qmd", "w")
    
    for line in dept_text:
        if line.startswith(r"{{< include "):
            with open(os.path.join(qmd_directory, line.split()[2][0:-4] + "_rendered.qmd")) as ind_dep:
                ind_dep_text = ind_dep.read()
                output_file.write("\n\n")
                output_file.write(ind_dep_text)
        else:
            output_file.write(line)
    
    output_file.close()


clean_department_file()
process_departmental_files()