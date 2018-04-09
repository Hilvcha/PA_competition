# coding: utf-8
import os
import argparse
import ast
import time
import yaml

from conf.configure import Configure
from jinja2 import Environment, PackageLoader, Template

env = Environment(loader=PackageLoader('templates'))
template_path = os.path.join(Configure.base_path, "templates")


def add_feature(name, desc):
    """
        add a feature to this project
    :param desc:
    :param name:
    :return:
    """
    _data = read_username()
    _data.update(time=time.asctime(time.localtime(time.time())))
    _data.update(name=name)
    _data.update(desc=desc)
    print(_data)
    base = Configure.base_path
    add2function(os.path.join(base, "functions"), _data)
    add2unittest(os.path.join(base, "unittests"), _data)
    add2configure(os.path.join(os.path.join(base, "conf"), "configure.py"), _data)
    add2function_file(os.path.join(os.path.join(base, "functions"), "functions.py"), _data)
    append2todo(os.path.join(base, "TODO"), _data)
    print("Have a nice coding! See you next time!")


def add2function(path, data):
    functions_path = os.path.join(path, data["name"] + ".py")
    if os.path.exists(functions_path):
        return
    template_file = open(os.path.join(template_path, "function.template")).read()
    temp = Template(template_file)
    with open(functions_path, 'w') as fw:
        fw.write(temp.render(data))


def add2unittest(path, data):
    unittests_path = os.path.join(path, "functions_" + data["name"] + ".py")
    if os.path.exists(unittests_path):
        return
    template_file = open(os.path.join(template_path, 'unittest.template')).read()
    temp = Template(template_file)
    with open(unittests_path, 'w') as fw:
        fw.write(temp.render(data))


def add2configure(conf_path, data):
    with open(conf_path, encoding='utf-8') as conf_file:
        lines = [line for line in conf_file]

    configure = "".join(lines)
    root = ast.parse(configure)

    line_num = 0
    for i in ast.iter_child_nodes(root):
        if type(i) == ast.ClassDef:
            for j in ast.iter_child_nodes(i):
                if type(j) == ast.Assign and j.targets[0].id == 'features':
                    line_num = j.value.elts[-1].lineno
    code_template = Template(' ' * 8 + '\"{{ name }}\",')
    lines.insert(line_num, code_template.render(data) + "\n")
    comment_template = Template(' ' * 8 + '# {{ desc }}')
    lines.insert(line_num, comment_template.render(data) + "\n")
    with open(conf_path, 'wb') as conf_file:
        conf_file.write(''.join(lines).encode('utf-8'))


def add2function_file(filename, data):
    with open(filename, encoding='utf-8') as conf_file:
        lines = [line for line in conf_file]

    configure = "".join(lines)
    root = ast.parse(configure)

    line_num = 0
    line_num2 = 0
    for i in ast.iter_child_nodes(root):
        if type(i) == ast.FunctionDef:
            line_num2 = i.lineno
            for j in ast.iter_child_nodes(i):
                if type(j) == ast.Assign and j.targets[0].id == 'funcs':
                    line_num = j.value.keys[-1].lineno
                    # print(line_num)
    import_template = Template('from functions.{{ name }} import {{ name }}')
    lines.insert(line_num2 - 3, import_template.render(data) + "\n")
    code_template = Template(' ' * 8 + '\"{{ name }}\": {{ name }},')
    lines.insert(line_num, code_template.render(data) + "\n")
    comment_template = Template(' ' * 8 + '# {{ desc }}')
    lines.insert(line_num, comment_template.render(data) + "\n")
    with open(filename, 'wb') as conf_file:
        conf_file.write(''.join(lines).encode('utf-8'))


def append2todo(filename, data):
    with open(filename, encoding='utf-8') as todo_file:
        lines = [line for line in todo_file]
    todo_template = Template("[ ] {{ desc }}")
    lines.append(todo_template.render(data) + "\n")
    with open(filename, 'wb') as conf_file:
        conf_file.write(''.join(lines).encode('utf-8'))


def read_username(filename="_user_config.yaml"):
    return yaml.load(open(filename))


if __name__ == '__main__':
    parser = argparse.ArgumentParser("The function adder for PA_competition")
    parser.add_argument("name", help="the name of the function")
    parser.add_argument("-d", "--desc", dest="desc", help="the description of the function",
                        default="Your description HERE")
    args = parser.parse_args()
    add_feature(args.name, args.desc)
