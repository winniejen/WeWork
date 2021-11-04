#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description:
# @Author : 
# @Time : 2021/10/12 18:45
import os

import pytest

from api_frame_study.common.helper import clear_yaml, get_project_path

project_path = get_project_path()
conf_file = os.path.join(project_path, "conf/config.ini")
extract_data_file = os.path.join(project_path, "data/extract_data.yaml")


@pytest.fixture(scope="session", autouse=True)
def clear_extract_file():
    clear_yaml(extract_data_file)


def pytest_collection_modifyitems(session, items):
    # 期望用例顺序
    appoint_items = ["test_get_access_token", 'test_create_department',
                     'test_update_department', 'test_get_department', 'test_delete_department']

    # 指定运行顺序
    run_items = []
    for i in appoint_items:
        for item in items:
            module_item = item.name.split("[")[0]
            if i == module_item:
                run_items.append(item)

    for i in run_items:
        run_index = run_items.index(i)
        items_index = items.index(i)
        if run_index != items_index:
            n_data = items[run_index]
            run_index = items.index(n_data)
            items[items_index], items[run_index] = items[run_index], items[items_index]
