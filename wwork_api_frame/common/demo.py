#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description:
# @Author : 
# @Time : 2021/10/14 14:20
from api_frame_study.common.helper import *
from api_frame_study.common.debug_talk import *

project_path = get_project_path()
# department_api_file = os.path.join(project_path, "data/department_api.yaml")
# template_info = read_yaml(os.path.join(project_path, "data/department_api.yaml"))
# replace_data = os.path.join(project_path, "data/create_department_data.yaml")
# data = read_yaml(os.path.join(project_path, "data/get_access_token_data.yaml"))

access_token_data = read_yaml(os.path.join(project_path, "data/get_access_token_data.yaml"))
print(access_token_data)
print()


# with open(os.path.join(project_path, "data/extract_data.yaml"), "r") as f:
#     yaml_data = yaml.safe_load(f)
#     yaml_data['id'] = 35
#     print(yaml_data)
#     # yaml.safe_dump(data, stream=f)
