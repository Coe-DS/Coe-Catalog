#!/usr/bin/python3

import pandas as pd, os

catalog_master = pd.read_csv("catalog_from_jenzabar.csv")

def find_if_var_exists(crs_code):
    rootdir="./catalog_sections"
    counter = 0
    for folder, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith('.qmd'):
                fullpath = os.path.join(folder, file)
                with open(fullpath, 'r') as f:
                    for line in f:
                        if "var c."+crs_code in line:
                            counter = counter + 1
                            break

    return counter


def print_course_vars(row, file_id):

    dept_code = row["CRS_CDE"].strip().split()[0]
    crs_code_concat = "".join(row["CRS_CDE"].strip().lower().split())
    crs_code = repr(" ".join(row["CRS_CDE"].strip().split()))
    crs_code_with_title = repr(' '.join(row["CRS_CDE"].strip().split()) + " " + row["CRS_TITLE"].strip().replace("\'",""))

    if find_if_var_exists(crs_code_concat) > 0:
        
        print("  ", crs_code_concat, ":", sep="", file=file_id)
        print("  ", "  ", "short: ", crs_code, sep="", file=file_id)
        print("  ", "  ",  "long: ", crs_code_with_title, sep="", file=file_id)
        
        if row["CATALOG_TEXT"] is not None:
            print("  ", "  ",  "desc: ", repr(str(row["CATALOG_TEXT"]).strip().replace("  "," ")), sep="", file=file_id)
        else:
            print("  ", "  ",  "desc: \" \"", sep="", file=file_id)
        
        print("  ", "  ", "namelink: \'[", crs_code[1:-1], "](departmental_programs/", sep="", end="", file=file_id)
        print(dept_code, "_courses.qmd#courses-in-", "SOMETHING", ")\'", sep="", file=file_id)
        print("  ", "  ", "namelinklong: \'[", repr(crs_code_with_title)[2:-2], "](departmental_programs/", sep="", end="", file=file_id)
        print(dept_code, "_courses.qmd#courses-in-", "SOMETHING", ")\'", sep="", file=file_id)


with open("_variables.yml", "w") as fid:
    print("c:", file=fid)
    f = lambda x : print_course_vars(x,fid)
    catalog_master.apply(f, axis = 1)

