def check_data(input_dict, output_dict):
    correct_data = []
    for key in input_dict:
        print(f"{key} : {input_dict[key]} : {output_dict[key]}")
        if str(input_dict[key]) == str(output_dict[key]):
            correct_data.append(True)
        else:
            correct_data.append(False)
    return correct_data

