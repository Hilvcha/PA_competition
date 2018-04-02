# coding: utf-8
import sys
import os
import argparse
import ast
import re

from conf.configure import Configure
from jinja2 import Environment, PackageLoader, Template

env = Environment(loader=PackageLoader('templates'))
template_path = os.path.join(Configure.base_path, "templates")


def add_function(name, desc):
    """
    add a function of this project
    :param name:
    :return:
    """
    base = Configure.base_path
    add2function(os.path.join(base, "functions"), name, desc)
    add2unittest(os.path.join(base, "unittests"), name, desc)
    add2configure(os.path.join(os.path.join(base, "conf"), "configure.py"), name, desc)
    add2function_file(os.path.join(os.path.join(base, "functions"), "functions.py"), name, desc)
    append2TODO(os.path.join(base, "TODO"), desc)
    print("Have a nice coding! See you next time!")


def add2function(path, name, desc):
    functions_path = os.path.join(path, name + ".py")
    if os.path.exists(functions_path):
        return
    template_file = open(os.path.join(template_path, "function.template")).read()
    temp = Template(template_file)
    with open(functions_path, 'w') as fw:
        fw.write(temp.render(name=name, desc=desc))


def add2unittest(path, name, desc):
    unittests_path = os.path.join(path, "functions_" + name + ".py")
    if os.path.exists(unittests_path):
        return
    template_file = open(os.path.join(template_path, 'unittest.template')).read()
    temp = Template(template_file)
    with open(unittests_path, 'w') as fw:
        fw.write(temp.render(name=name, desc=desc))


def add2configure(conf_path, name, desc):
    with open(conf_path, encoding='utf-8') as conf_file:
        lines = [line for line in conf_file]

    configure = "".join(lines)
    root = ast.parse(configure)

    line_num = 0
    for i in ast.iter_child_nodes(root):
        if type(i) == ast.ClassDef:
            for i in ast.iter_child_nodes(i):
                if type(i) == ast.Assign and i.targets[0].id == 'features':
                    line_num = i.value.elts[-1].lineno
    code_template = Template(' ' * 8 + '\"{{ name }}\",')
    lines.insert(line_num, code_template.render(name=name) + "\n")
    comment_template = Template(' ' * 8 + '# {{ desc }}')
    lines.insert(line_num, comment_template.render(desc=desc) + "\n")
    with open(conf_path, 'wb') as conf_file:
        conf_file.write(''.join(lines).encode('utf-8'))


def add2function_file(filename, name, desc):
    with open(filename, encoding='utf-8') as conf_file:
        lines = [line for line in conf_file]

    configure = "".join(lines)
    root = ast.parse(configure)

    line_num = 0
    line_num2 = 0
    for i in ast.iter_child_nodes(root):
        if type(i) == ast.FunctionDef:
            line_num2 = i.lineno
            for i in ast.iter_child_nodes(i):
                if type(i) == ast.Assign and i.targets[0].id == 'funcs':
                    line_num = i.value.keys[-1].lineno
                    # print(line_num)
    import_template = Template('from functions.{{ name }} import {{ name }}')
    lines.insert(line_num2 - 3, import_template.render(name=name) + "\n")
    code_template = Template(' ' * 8 + '\"{{ name }}\": {{ name }},')
    lines.insert(line_num, code_template.render(name=name) + "\n")
    comment_template = Template(' ' * 8 + '# {{ desc }}')
    lines.insert(line_num, comment_template.render(desc=desc) + "\n")
    with open(filename, 'wb') as conf_file:
        conf_file.write(''.join(lines).encode('utf-8'))


def append2TODO(filename, desc):
    with open(filename, encoding='utf-8') as todo_file:
        lines = [line for line in todo_file]
    todo_template = Template("[ ] {{ desc }}")
    lines.append(todo_template.render(desc=desc) + "\n")
    with open(filename, 'wb') as conf_file:
        conf_file.write(''.join(lines).encode('utf-8'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser("The function adder for PA_competition")
    parser.add_argument("name", help="the name of the function")
    parser.add_argument("-d", "--desc", dest="desc", help="the description of the function",
                        default="Your description HERE")
    args = parser.parse_args()
    print(args.name)
    print(args.desc)
    add_function(args.name, args.desc)
    # add_function("name", "desc")
