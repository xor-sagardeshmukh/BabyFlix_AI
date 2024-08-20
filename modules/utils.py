import os

def insert_number_before_extension(file_path, number):
    directory, filename = os.path.split(file_path)
    name, extension = os.path.splitext(filename)
    new_filename = f"{name}({number}){extension}"
    new_path = os.path.join(directory, new_filename)    
    return new_path

def find_next_available_filename(file_path):
    if not os.path.exists(file_path):
        return file_path
    
    directory, filename = os.path.split(file_path)
    
    number = 1
    while True:
        new_filename = insert_number_before_extension(filename, number)
        new_path = os.path.join(directory, new_filename)        
        if not os.path.exists(new_path):
            return new_path        
        number += 1
