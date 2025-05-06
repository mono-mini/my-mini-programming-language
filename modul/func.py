import os
import re

os.makedirs("../project", exist_ok=True)


def create_file():
    with open("main.cpp", "w") as file:
        file.write("#include <iostream>\n#include <fstream>\n\n")
        file.write("int main() {\n")


def pf(znak):
    file = open("main.cpp", "a")
    file.write("    std::cout << " + znak + ";\n")
    file.close()


def exit():
    with open("main.cpp", "a") as file:
        file.write("    return 0;\n}\n")


def ref(var_name_ref, var_new_value):
    with open("main.cpp", "a") as file:
        file.write(f"    {var_name_ref} = {var_new_value};\n")


def var(var_name, var_value):
    with open("main.cpp", "a") as file:
        file.write(f"    auto {var_name} = {var_value};\n")


def if_(condition):
    with open("main.cpp", "a") as file:
        file.write(f"    if ({condition}) " + "{\n")


def end():
    with open("main.cpp", "a") as file:
        file.write("}\n")


def else_():
    with open("main.cpp", "a") as file:
        file.write("else" + "{\n")


def break_():
    with open("main.cpp", "a") as file:
        file.write("break;\n")


def continue_():
    with open("main.cpp", "a") as file:
        file.write("continue;\n")


def while_(condition):
    with open("main.cpp", "a") as file:
        file.write(f"while ({condition}) " + "{\n")


def while_true_():
    with open("main.cpp", "a") as file:
        file.write("while (true) {\n")


def for_(condition):
    with open("main.cpp", "a") as file:
        file.write(f"for ({condition}) " + "{\n")


def do_while(condition):
    with open("main.cpp", "a") as file:
        file.write(f"do " + "{\n")
        file.write(f"}} while ({condition});\n")


def switch_(condition):
    with open("main.cpp", "a") as file:
        file.write(f"switch ({condition}) " + "{\n")


def case_(condition):
    with open("main.cpp", "a") as file:
        file.write(f"case {condition}:\n")


def default_():
    with open("main.cpp", "a") as file:
        file.write(f"default:\n")


def repeat(number):
    with open("main.cpp", "a") as file:
        file.write(f"for (int i = 0; i < {number}; i++) " + "{\n")


def add(var1, var2):
    with open("main.cpp", "a") as file:
        file.write(f"    {var1} + {var2};\n")
    with open("main.cpp", "r") as file:
        a = file.readlines()
    b = re.search(r"add (.*?), (.*?)", a)
    if b:
        var1 = b.group(1)
        var2 = b.group(2)
        with open("main.cpp", "a") as file:
            file.write(f"    {var1} + {var2};\n")
    else:
        with open("main.cpp", "a") as file:
            file.write(f"    {var1} + {var2};\n")


def array(array_name, array_type, array_size):
    with open("main.cpp", "a") as file:
        file.write(f"    {array_type} {array_name}[{array_size}];\n")


def array_add(array_name, index, value):
    with open("main.cpp", "a") as file:
        file.write(f"    {array_name}[{index}] = {value};\n")


def array_print(array_name):
    with open("main.cpp", "a") as file:
        file.write(f"    for (const auto& elem : {array_name}) {{\n")
        file.write(f"        std::cout << elem << ' ';\n")
        file.write(f"    }}\n")


def array_update(array_name, index, value):
    with open("main.cpp", "a") as file:
        file.write(f"    {array_name}[{index}] = {value};\n")


def array_create(array_name, array_type, array_size):
    with open("main.cpp", "a") as file:
        file.write(f"    {array_type} {array_name}[{array_size}];\n")


def input(var_name):
    with open("main.cpp", "a") as file:
        file.write(f"    std::cin >> {var_name};\n")


def var_input(var_name):
    with open("main.cpp", "a") as file:
        file.write(f"    auto {var_name};\n")


def var_intput(var_name):
    with open("main.cpp", "a") as file:
        file.write(f"    int {var_name};\n")


def intput(var_name):
    with open("main.cpp", "a") as file:
        file.write(f"    std::cin >> {var_name};\n")


def try_():
    with open("main.cpp", "a") as file:
        file.write("    try {\n")


def catch_(exception_type):
    with open("main.cpp", "a") as file:
        file.write(f"    }} catch ({exception_type}& e) {{\n")
