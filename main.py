import re
from modul import func

func.create_file()

# Создание файла main.cpp
with open("main.cpp", "w") as file:
    file.write("#include <iostream>\n#include <fstream>\n\n")
    file.write("int main() {\n")

while True:
    inp = input(">>> ")

    # Обработка команды pf
    if inp.startswith("pf"):
        match = re.search(r"pf\((.*?)\)", inp)
        if match:
            content = match.group(1).strip()
            func.pf(content)
        else:
            print("Ошибка: не найдено содержимое внутри pf")
        continue
    # Обработка команды exit
    elif inp == "exit":
        func.exit()
        break
    # Обработка команды ref
    elif inp.startswith("ref"):
        match_ref = re.match(r"ref\s+(\w+)\s*=\s*(.+)", inp)
        if match_ref:
            var_name_ref = match_ref.group(1)
            var_new_value = match_ref.group(2).strip()
            func.ref(var_name_ref, var_new_value)
        else:
            print("Ошибка: неправильный формат команды ref")
        continue
    # Обработка команды var
    elif inp.startswith("var"):
        match_var = re.match(r"var\s+(\w+)\s*=\s*(.+)", inp)
        if match_var:
            var_name = match_var.group(1)
            var_value = match_var.group(2).strip()
            func.var(var_name, var_value)
        else:
            print("Ошибка: неправильный формат команды var")
        continue
    # Обработка команды var/ref с add
    elif inp.startswith("var") or inp.startswith("ref"):
        match_var_ref = re.match(
            r"(var|ref)\s+(\w+)\s*=\s*(\w+|\d+)\s*\+\s*(\w+|\д+)", inp
        )
        if match_var_ref:
            command_type = match_var_ref.group(1)
            var_name = match_var_ref.group(2)
            operand1 = match_var_ref.group(3)
            operand2 = match_var_ref.group(4)
            expression = f"{operand1} + {operand2}"
            if command_type == "var":
                func.var(var_name, expression)
            elif command_type == "ref":
                func.ref(var_name, expression)
        else:
            print("Ошибка: неправильный формат команды var/ref с оператором +")
        continue
    # Обработка команды if
    elif inp.startswith("if"):
        match = re.search(r"if\s*\((.*?)\)", inp)
        if match:
            condition = match.group(1).strip()
            func.if_(condition)
            print("Введите команды внутри if. Для завершения используйте 'end'.")
            while True:
                inner_inp = input("if >>> ")
                if inner_inp == "end":
                    func.end()
                    break
                elif inner_inp.startswith("if"):
                    match_inner_if = re.search(r"if\s*\((.*?)\)", inner_inp)
                    if match_inner_if:
                        condition_inner_if = match_inner_if.group(1).strip()
                        func.if_(condition_inner_if)
                        print("Вложенный if. Для завершения используйте 'end'.")
                        while True:
                            nested_inp = input("nested if >>> ")
                            if nested_inp == "end":
                                func.end()
                                break
                            elif nested_inp.startswith("pf"):
                                match_nested_pf = re.search(r"pf\((.*?)\)", nested_inp)
                                if match_nested_pf:
                                    content_nested_pf = match_nested_pf.group(1).strip()
                                    func.pf(content_nested_pf)
                                else:
                                    print("Ошибка: не найдено содержимое внутри pf")
                            elif nested_inp.startswith("var"):
                                match_nested_var = re.match(
                                    r"var\s+(\w+)\s*=\s*(.+)", nested_inp
                                )
                                if match_nested_var:
                                    var_name_nested = match_nested_var.group(1)
                                    var_value_nested = match_nested_var.group(2).strip()
                                    func.var(var_name_nested, var_value_nested)
                                else:
                                    print("Ошибка: неправильный формат команды var")
                            elif nested_inp.startswith("ref"):
                                match_nested_ref = re.match(
                                    r"ref\s+(\w+)\s*=\s*(.+)", nested_inp
                                )
                                if match_nested_ref:
                                    var_name_nested_ref = match_nested_ref.group(1)
                                    var_new_value_nested = match_nested_ref.group(
                                        2
                                    ).strip()
                                    func.ref(var_name_nested_ref, var_new_value_nested)
                                else:
                                    print("Ошибка: неправильный формат команды ref")
                            elif nested_inp == "break":
                                func.break_()
                            elif nested_inp == "continue":
                                func.continue_()
                            else:
                                print("Неизвестная команда внутри вложенного if")
                    else:
                        print("Ошибка: не найдено условие внутри вложенного if")
                elif inner_inp.startswith("pf"):
                    match_inner_pf = re.search(r"pf\((.*?)\)", inner_inp)
                    if match_inner_pf:
                        content_inner_pf = match_inner_pf.group(1).strip()
                        func.pf(content_inner_pf)
                    else:
                        print("Ошибка: не найдено содержимое внутри pf")
                elif inner_inp.startswith("var"):
                    match_inner_var = re.match(r"var\s+(\w+)\s*=\s*(.+)", inner_inp)
                    if match_inner_var:
                        var_name_inner = match_inner_var.group(1)
                        var_value_inner = match_inner_var.group(2).strip()
                        func.var(var_name_inner, var_value_inner)
                    else:
                        print("Ошибка: неправильный формат команды var")
                elif inner_inp.startswith("ref"):
                    match_inner_ref = re.match(r"ref\s+(\w+)\s*=\s*(.+)", inner_inp)
                    if match_inner_ref:
                        var_name_inner_ref = match_inner_ref.group(1)
                        var_new_value_inner = match_inner_ref.group(2).strip()
                        func.ref(var_name_inner_ref, var_new_value_inner)
                    else:
                        print("Ошибка: неправильный формат команды ref")
                elif inner_inp == "break":
                    func.break_()
                elif inner_inp == "continue":
                    func.continue_()
                else:
                    print("Неизвестная команда внутри if")
        else:
            print("Ошибка: не найдено условие внутри if")
        continue
    # Обработка команды end
    elif inp == "end":
        func.end()
        continue
    # Обработка команды else
    elif inp == "else":
        func.else_()
        continue
    # Обработка команды while
    elif inp.startswith("while"):
        match = re.search(r"while\s*\((.*?)\)", inp)
        if match:
            condition = match.group(1).strip()
            func.while_(condition)
        else:
            print("Ошибка: не найдено условие внутри while")
        continue
    # Обработка команды for
    elif inp.startswith("for"):
        match = re.search(r"for\s*\((.*?)\)", inp)
        if match:
            condition = match.group(1).strip()
            func.if_(condition)
        else:
            print("Ошибка: не найдено условие внутри for")
        continue
    # Обработка команды do
    elif inp.startswith("do"):
        match = re.search(r"do\s*\((.*?)\)", inp)
        if match:
            condition = match.group(1).strip()
            func.if_(condition)
        else:
            print("Ошибка: не найдено условие внутри do")
        continue
    # Обработка команды break
    elif inp == "break":
        func.end()
        continue
    # Обработка команды continue
    elif inp == "continue":
        func.end()
        continue
    # Обработка команды default
    elif inp == "default":
        func.end()
        continue
    # Обработка команды while true
    elif inp == "while true":
        func.while_true_()
        print("Введите команды внутри while true. Для завершения используйте 'end'.")
        while True:
            inner_inp = input("while true >>> ")
            if inner_inp == "end":
                func.end()
                break
            elif inner_inp.startswith("pf"):
                match_inner = re.search(r"pf\((.*?)\)", inner_inp)
                if match_inner:
                    content = match_inner.group(1).strip()
                    func.pf(content)
                else:
                    print("Ошибка: не найдено содержимое внутри pf")
            elif inner_inp.startswith("var"):
                match_var = re.match(r"var\s+(\w+)\s*=\s*(.+)", inner_inp)
                if match_var:
                    var_name = match_var.group(1)
                    var_value = match_var.group(2).strip()
                    func.var(var_name, var_value)
                else:
                    print("Ошибка: неправильный формат команды var")
            elif inner_inp.startswith("ref"):
                match_ref = re.match(r"ref\s+(\w+)\s*=\s*(.+)", inner_inp)
                if match_ref:
                    var_name_ref = match_ref.group(1)
                    var_new_value = match_ref.group(2).strip()
                    func.ref(var_name_ref, var_new_value)
                else:
                    print("Ошибка: неправильный формат команды ref")
            elif inner_inp == "break":
                func.break_()
            elif inner_inp == "continue":
                func.continue_()
            else:
                print("Неизвестная команда внутри while true")
    elif inp == "end2":
        func.end()
        func.end()
    elif inp == "end3":
        func.end()
        func.end()
        func.end()
    elif inp == "end4":
        func.end()
        func.end()
        func.end()
        func.end()
    elif inp == "end5":
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
    elif inp == "end6":
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
    elif inp == "end7":
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
    elif inp == "end8":
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
    elif inp == "end9":
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
    elif inp == "end10":
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
        func.end()
    elif inp == "":
        print("Ошибка: пустая команда")
        continue
    elif inp == "help":
        print(
            "Доступные команды:\n"
            "pf(content) - вывести content\n"
            "var name = value - создать переменную\n"
            "ref name = value - изменить значение переменной\n"
            "if(condition) - условие if\n"
            "else - условие else\n"
            "while(condition) - цикл while\n"
            "for(condition) - цикл for\n"
            "do(condition) - цикл do-while\n"
            "break - выйти из цикла\n"
            "continue - продолжить цикл\n"
            "exit - завершить программу\n"
            "clear - очистить файл main.cpp\n"
            "repet - повторить предыдущую команду\n"
            "end - завершить блок if/while/for\n"
        )
        continue
    elif inp == "clear":
        with open("main.cpp", "w") as file:
            file.write("#include <iostream>\n#include <fstream>\n\n")
            file.write("int main() {\n")
        print("main.cpp очищен.")
        continue
    elif inp.startswith("repeat"):
        match = re.match(r"repeat\s+(\д+)", inp)
        if match:
            count = int(match.group(1))
            func.repeat(count)
            print("Введите команды внутри repeat. Для завершения используйте 'end'.")
            while True:
                inner_inp = input("repeat >>> ")
                if inner_inp == "end":
                    func.end()
                    break
                elif inner_inp.startswith("pf"):
                    match_inner = re.search(r"pf\((.*?)\)", inner_inp)
                    if match_inner:
                        content = match_inner.group(1).strip()
                        func.pf(content)
                    else:
                        print("Ошибка: не найдено содержимое внутри pf")
                elif inner_inp.startswith("var"):
                    match_var = re.match(r"var\s+(\w+)\s*=\s*(.+)", inner_inp)
                    if match_var:
                        var_name = match_var.group(1)
                        var_value = match_var.group(2).strip()
                        func.var(var_name, var_value)
                    else:
                        print("Ошибка: неправильный формат команды var")
                elif inner_inp.startswith("ref"):
                    match_ref = re.match(r"ref\s+(\w+)\s*=\s*(.+)", inner_inp)
                    if match_ref:
                        var_name_ref = match_ref.group(1)
                        var_new_value = match_ref.group(2).strip()
                        func.ref(var_name_ref, var_new_value)
                    else:
                        print("Ошибка: неправильный формат команды ref")
                elif inner_inp == "break":
                    func.break_()
                elif inner_inp == "continue":
                    func.continue_()
                else:
                    print("Неизвестная команда внутри repeat")
    elif inp in "repeat":
        repeat = int(re.match(r"repeat\s+(\w+)", inp))
        if repeat:
            func.repeat(repeat)
        else:
            print("Ошибка: неправильный формат команды repeat")
    elif inp in "add":
        a = int(re.match(r"add\s+(\w+)\s+(\w+)", inp))
        if a:
            func.add(a)
        else:
            print("Ошибка: неправильный формат команды add")
    elif inp.startswith("array create"):
        match = re.match(r"array create\s+(\w+)\s+(\w+)\s+(\w+)", inp)
        if match:
            array_name = match.group(1)
            array_type = match.group(2)
            array_size = match.group(3)
            if array_size.isdigit():
                array_size = int(array_size)
            else:
                print("Ошибка: размер массива должен быть числом")
                continue
            func.array_create(array_name, array_type, array_size)

        else:
            print("Ошибка: неправильный формат команды array create")
    elif inp.startswith("array delete"):
        match = re.match(r"array delete\s+(\w+)", inp)
        if match:
            array_name = match.group(1)
            func.array_delete(array_name)
        else:
            print("Ошибка: неправильный формат команды array delete")

    elif inp.startswith("array add"):
        match = re.match(r"array add\s+(\w+)\s+(\д+)\s+(\w+)", inp)
        if match:
            array_name = match.group(1)
            index = match.group(2)
            value = match.group(3)
            func.array_add(array_name, index, value)
        else:
            print("Ошибка: неправильный формат команды array add")
    elif inp.startswith("array print"):
        match = re.match(r"array print\s+(\w+)", inp)
        if match:
            array_name = match.group(1)
            func.array_print(array_name)
        else:
            print("Ошибка: неправильный формат команды array print")
    elif inp.startswith("array update"):
        match = re.match(r"array update\s+(\w+)\s+(\д+)\s+(\w+)", inp)
        if match:
            array_name = match.group(1)
            index = match.group(2)
            value = match.group(3)
            func.array_update(array_name, index, value)
        else:
            print("Ошибка: неправильный формат команды array update")

    elif inp.startswith("input"):
        match = re.match(r"input\s+(\w+)", inp)
        if match:
            var_name = match.group(1)
            with open("main.cpp", "r") as file:
                content = file.read()
            if f"auto {var_name} =" not in content and f"{var_name} =" not in content:
                func.var_input(var_name)
            func.input(var_name)
        else:
            print("Ошибка: неправильный формат команды input var_name")
    elif inp.startswith("intput"):
        match = re.match(r"intput\s+(\w+)", inp)
        if match:
            var_name = match.group(1)
            with open("main.cpp", "r") as file:
                content = file.read()
            if f"auto {var_name} =" not in content and f"{var_name} =" not in content:
                func.var_intput(var_name)
            func.intput(var_name)
        else:
            print("Ошибка: неправильный формат команды intput var_name")
    elif inp == "try":
        func.try_()
        print(
            "Введите команды внутри try. Для завершения используйте 'catch exception_type' или 'end'."
        )
        while True:
            inner_inp = input("try >>> ")
            if inner_inp.startswith("catch"):
                match = re.match(r"catch\s+(\w+)", inner_inp)
                if match:
                    exception_type = match.group(1)
                    func.catch_(exception_type)
                    print(
                        "Введите команды внутри catch. Для завершения используйте 'end'."
                    )
                else:
                    print("Ошибка: неправильный формат команды catch")
            elif inner_inp == "end":
                func.end()
                break
            elif inner_inp.startswith("pf"):
                match_inner = re.search(r"pf\((.*?)\)", inner_inp)
                if match_inner:
                    content = match_inner.group(1).strip()
                    func.pf(content)
            elif inner_inp.startswith("var"):
                match_var = re.match(r"var\s+(\w+)\s*=\s*(.+)", inner_inp)
                if match_var:
                    var_name = match_var.group(1)
                    var_value = match_var.group(2).strip()
                    func.var(var_name, var_value)
                else:
                    print("Ошибка: неправильный формат команды var")
            elif inner_inp.startswith("ref"):
                match_ref = re.match(r"ref\s+(\w+)\s*=\s*(.+)", inner_inp)
                if match_ref:
                    var_name_ref = match_ref.group(1)
                    var_new_value = match_ref.group(2).strip()
                    func.ref(var_name_ref, var_new_value)
                else:
                    print("Ошибка: неправильный формат команды ref")
            elif inner_inp == "break":
                func.break_()
            elif inner_inp in "input":
                match = re.match(r"input\s+(\w+)", inner_inp)
                if match:
                    var_name = match.group(1)
                    with open("main.cpp", "r") as file:
                        content = file.read()
                    if (
                        f"auto {var_name} =" not in content
                        and f"{var_name} =" not in content
                    ):
                        func.var_input(var_name)
                    func.input(var_name)
                else:
                    print("Ошибка: неправильный формат команды input var_name")
            elif inner_inp.startswith("intput"):
                match = re.match(r"intput\s+(\w+)", inner_inp)
                if match:
                    var_name = match.group(1)
                    with open("main.cpp", "r") as file:
                        content = file.read()
                    if (
                        f"auto {var_name} =" not in content
                        and f"{var_name} =" not in content
                    ):
                        func.var_intput(var_name)
                    func.intput(var_name)
                else:
                    print("Ошибка: неправильный формат команды intput var_name")
            elif inner_inp.startswith("while"):
                match = re.search(r"while\s*\((.*?)\)", inner_inp)
                if match:
                    condition = match.group(1).strip()
                    func.while_(condition)
                else:
                    print("Ошибка: не найдено условие внутри while")
            elif inner_inp.startswith("for"):
                match = re.search(r"for\s*\((.*?)\)", inner_inp)
                if match:
                    condition = match.group(1).strip()
                    func.if_(condition)
                else:
                    print("Ошибка: не найдено условие внутри for")
            elif inner_inp.startswith("do"):
                match = re.search(r"do\s*\((.*?)\)", inner_inp)
                if match:
                    condition = match.group(1).strip()
                    func.if_(condition)
                else:
                    print("Ошибка: не найдено условие внутри do")
            elif inner_inp == "repeat":
                match = re.match(r"repeat\s+(\d+)", inner_inp)
                if match:
                    count = int(match.group(1))
                    func.repeat(count)
                    print(
                        "Введите команды внутри repeat. Для завершения используйте 'end'."
                    )
                    while True:
                        nested_inp = input("repeat >>> ")
                        if nested_inp == "end":
                            func.end()
                            break
                        elif nested_inp.startswith("pf"):
                            match_nested = re.search(r"pf\((.*?)\)", nested_inp)
                            if match_nested:
                                content_nested = match_nested.group(1).strip()
                                func.pf(content_nested)
                            else:
                                print("Ошибка: не найдено содержимое внутри pf")
                        elif nested_inp.startswith("var"):
                            match_nested_var = re.match(
                                r"var\s+(\w+)\s*=\s*(.+)", nested_inp
                            )
                            if match_nested_var:
                                var_name_nested = match_nested_var.group(1)
                                var_value_nested = match_nested_var.group(2).strip()
                                func.var(var_name_nested, var_value_nested)
                            else:
                                print("Ошибка: неправильный формат команды var")
                        elif nested_inp.startswith("ref"):
                            match_nested_ref = re.match(
                                r"ref\s+(\w+)\s*=\s*(.+)", nested_inp
                            )
                            if match_nested_ref:
                                var_name_nested_ref = match_nested_ref.group(1)
                                var_new_value_nested = match_nested_ref.group(2).strip()
                                func.ref(var_name_nested_ref, var_new_value_nested)
                            else:
                                print("Ошибка: неправильный формат команды ref")
                        elif nested_inp == "break":
                            func.break_()
                        elif nested_inp == "continue":
                            func.continue_()
                        else:
                            print("Неизвестная команда внутри repeat")

            else:
                print("Неизвестная команда внутри try")
