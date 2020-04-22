import yaml


def get_parameters():
    with open('parameters.yaml') as file:
        parameters_list = yaml.load(file, Loader=yaml.FullLoader)
        return parameters_list
