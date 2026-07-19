
import json
childs = []

def get_child_data(children_data):
    new_child_list = []
    
    for i, child in enumerate(children_data):
        new_child_list.append({
        "id": i,
           "name": child["name"],
        "age": child["age"]
        })
        
    print(new_child_list)