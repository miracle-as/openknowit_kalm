import os

def get_file_content(file_path):
    with open(file_path, 'r') as f:
        return f.read()
    

def get_file_content_lines(file_path):
    with open(file_path, 'r') as f:
        return f.readlines()
    
