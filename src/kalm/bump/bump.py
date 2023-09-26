import os
from pprint import pprint

def prebump():
    #check if pyproject.toml exists
    if os.path.isfile('pyproject.toml'):
        print("pyproject.toml exists")
    else:
        print("pyproject.toml does not exist")
        exit(1)
    #check if pyproject.toml contains poetry section

    #check if pyproject.toml contains poetry section
    read_file = open('pyproject.toml', 'r')
    lines = read_file.readlines()
    read_file.close()
    poetry_section = False
    poetry_section = []
    for line in lines:
        if line.startswith == "[tool.poetry":
            poetry_section = True
        if poetry_section:
            poetry_section.append(line)
            if line.strip() == "[" and not line.startswith == "[tool.poetry":
                poetry_section = False
    print(poetry_section)
    if poetry_section:
        print("poetry section exists")
    else:
        print("poetry section does not exist")

    #check if pyproject.toml contains project section
    project_section = False
    project_section = []
    for line in lines:
        if line.startswith == "[project":
            project_section = True
        if project_section:
            project_section.append(line)
            if line.strip() == "[" and not line.startswith == "[project":
                project_section = False
    print(project_section)
    if project_section:
        print("project section exists")
    else:
        print("project section does not exist")

        
