import resources.resources as resources


def string_to_list(input_string):

    input_string.replace(" ", "1")
    
    output = list(input_string.split("\n"))
    
    for item in output:
        item.replace("1", " ")

    return output

def remove_empty_elements(input_list):
    new_list = []
    for e in input_list:
        if e:
            new_list.append(e)
    
    return new_list

def remove_periods(input_list):
    output_list = []
    for e in input_list:
        e = e.replace(".", "")

        output_list.append(e)
    return output_list



