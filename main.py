import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import re
import subprocess
import threading
from tkinter import ttk
import os


class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Редактор кода nom")
        self.file_path = "main.nm"

        # Создаем меню
        menubar = tk.Menu(root)
        file_menu = tk.Menu(menubar, tearoff=0, bg="#000033", fg="white")
        file_menu.add_command(label="Открыть", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_command(label="Очистить", command=self.clear_text)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        # Создаем панель инструментов
        toolbar = tk.Frame(root)
        btn_open = tk.Button(toolbar, text="Открыть", command=self.open_file)
        btn_save = tk.Button(toolbar, text="Сохранить", command=self.save_file)
        btn_clear = tk.Button(toolbar, text="Очистить", command=self.clear_text)
        btn_exit = tk.Button(toolbar, text="Выход", command=root.quit)
        btn_run = tk.Button(toolbar, text="Запустить", command=self.run_code)
        btn_run.pack(side=tk.RIGHT, padx=2, pady=2)
        btn_exit.pack(side=tk.RIGHT, padx=2, pady=2)
        btn_open.pack(side=tk.LEFT, padx=2, pady=2)
        btn_save.pack(side=tk.LEFT, padx=2, pady=2)
        btn_clear.pack(side=tk.LEFT, padx=2, pady=2)

        # Список доступных команд для автодополнения
        self.commands = [
            "if",
            "else",
            "end",
            "pf",
            "var",
            "ref",
            "while",
            "for",
            "repeat",
            "exit",
            "break",
            "add",
            "sub",
            "mul",
            "div",
            "input",
            "file_read",
            "file_write",
            "window",
            "CloseWindow",
        ]

        # Удаляем выпадающий список для выбора команды
        # self.command_var = tk.StringVar()
        # self.command_dropdown = ttk.Combobox(
        #     toolbar,
        #     textvariable=self.command_var,
        #     values=self.commands,
        #     state="readonly",
        # )
        # self.command_dropdown.set("Выберите команду")
        # self.command_dropdown.pack(side=tk.LEFT, padx=2, pady=2)
        # self.command_dropdown.bind("<<ComboboxSelected>>", self.insert_selected_command)

        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Создаем текстовое поле с прокруткой
        self.text_area = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Courier", 12),
            undo=True,
            maxundo=-1,
            autoseparators=True,
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.tag_configure("pf", foreground="#B8860B")  # Тёмно-жёлтый цвет
        self.text_area.tag_configure("input", foreground="#B8860B")  # Тёмно-жёлтый цвет
        self.text_area.tag_configure("var", foreground="red")  # Красный цвет для var
        self.text_area.tag_configure("exit", foreground="#DD33FF")  # Цвет для exit
        self.text_area.tag_configure("ref", foreground="red")  # Красный цвет для ref
        self.text_area.tag_configure(
            "if", foreground="#FF1493"
        )  # Тёмно-розовый цвет для if
        self.text_area.tag_configure(
            "while", foreground="#FF1493"
        )  # Тёмно-розовый цвет для while
        self.text_area.tag_configure(
            "for", foreground="#FF1493"
        )  # Тёмно-розовый цвет для for
        self.text_area.tag_configure(
            "end", foreground="#FF1493"
        )  # Тёмно-розовый цвет для end
        self.text_area.tag_configure(
            "repeat", foreground="#FF1493"
        )  # Тёмно-розовый цвет для repeat
        self.text_area.tag_configure(
            "string", foreground="orange"
        )  # Оранжевый цвет для строк

        # Создаем текстовое поле для терминала
        self.terminal = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, height=10, font=("Courier", 12), bg="black", fg="white"
        )
        self.terminal.pack(fill=tk.BOTH, expand=False)
        self.terminal.tag_configure("error", foreground="red")
        self.terminal.tag_configure("output", foreground="green")

        # Загружаем начальный файл
        self.load_initial_content()

        self.text_area.bind("<KeyRelease>", lambda event: self.highlight_syntax())
        self.highlight_syntax()  # Подсветка синтаксиса при загрузке

        self.text_area.configure(bg="#2E2E2E", fg="white", insertbackground="white")
        self.terminal.configure(bg="#2E2E2E", fg="white", insertbackground="white")
        self.root.configure(bg="#2E2E2E")
        toolbar.configure(bg="#2E2E2E")
        for widget in toolbar.winfo_children():
            widget.configure(bg="#2E2E2E", fg="white")
        menubar.configure(bg="#2E2E2E", fg="white")

        # Удаляем всплывающее меню для выбора команды
        # self.popup_menu = tk.Menu(self.text_area, tearoff=0)
        # for command in self.commands:
        #     self.popup_menu.add_command(
        #         label=command, command=lambda cmd=command: self.insert_command(cmd)
        #     )

        # Удаляем привязку правой кнопки мыши для вызова меню
        # self.text_area.bind("<Button-3>", self.show_popup_menu)

        # Горячие клавиши
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-q>", lambda event: self.root.quit())
        self.root.bind("<Control-r>", lambda event: self.run_code())
        self.root.bind("<Control-e>", lambda event: self.clear_text())
        self.text_area.bind("<Control-z>", lambda event: self.text_area.edit_undo())
        self.text_area.bind("<Control-y>", lambda event: self.text_area.edit_redo())

    def load_initial_content(self):
        try:
            with open(self.file_path, "r") as f:
                content = f.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, content)
        except FileNotFoundError:
            # Если файла нет, создаем его пустым
            with open(self.file_path, "w") as f:
                f.write("")
            self.text_area.delete(1.0, tk.END)

    def highlight_syntax(self):
        self.text_area.tag_remove("pf", "1.0", tk.END)
        self.text_area.tag_remove("input", "1.0", tk.END)
        self.text_area.tag_remove("var", "1.0", tk.END)
        self.text_area.tag_remove("exit", "1.0", tk.END)
        self.text_area.tag_remove("ref", "1.0", tk.END)
        self.text_area.tag_remove("string", "1.0", tk.END)
        content = self.text_area.get("1.0", tk.END)
        start_idx = "1.0"
        while True:
            start_idx = self.text_area.search("pf", start_idx, stopindex=tk.END)
            if not start_idx:
                break
            end_idx = f"{start_idx} + {len('pf')}c"
            self.text_area.tag_add("pf", start_idx, end_idx)
            start_idx = end_idx

        start_idx = "1.0"
        while True:
            start_idx = self.text_area.search("var", start_idx, stopindex=tk.END)
            if not start_idx:
                break
            end_idx = f"{start_idx} + {len('var')}c"
            self.text_area.tag_add("var", start_idx, end_idx)
            start_idx = end_idx

        start_idx = "1.0"
        while True:
            start_idx = self.text_area.search("exit", start_idx, stopindex=tk.END)
            if not start_idx:
                break
            end_idx = f"{start_idx} + {len('exit')}c"
            self.text_area.tag_add("exit", start_idx, end_idx)
            start_idx = end_idx

        start_idx = "1.0"
        while True:
            start_idx = self.text_area.search("ref", start_idx, stopindex=tk.END)
            if not start_idx:
                break
            end_idx = f"{start_idx} + {len('ref')}c"
            self.text_area.tag_add("ref", start_idx, end_idx)
            start_idx = end_idx

        for keyword in ["if", "while", "for", "end", "repeat"]:
            self.text_area.tag_remove(keyword, "1.0", tk.END)
            start_idx = "1.0"
            while True:
                start_idx = self.text_area.search(keyword, start_idx, stopindex=tk.END)
                if not start_idx:
                    break
                end_idx = f"{start_idx} + {len(keyword)}c"
                self.text_area.tag_add(keyword, start_idx, end_idx)
                start_idx = end_idx

        start_idx = "1.0"
        while True:
            match = re.search(r'".*?"', content)
            if not match:
                break
            start_idx = self.text_area.search(
                match.group(0), start_idx, stopindex=tk.END
            )
            if not start_idx:
                break
            end_idx = f"{start_idx} + {len(match.group(0))}c"
            self.text_area.tag_add("string", start_idx, end_idx)
            start_idx = end_idx

        # Исправление поиска строк
        for match in re.finditer(r'".*?"', content):
            start_idx = f"1.0 + {match.start()}c"
            end_idx = f"1.0 + {match.end()}c"
            self.text_area.tag_add("string", start_idx, end_idx)

    def display_terminal_output(self, output, tag):
        # Корректно отображаем переносы строк
        output = output.replace("\r\n", "\n").replace("\r", "\n")
        self.terminal.insert(tk.END, output, tag)
        self.terminal.see(tk.END)

    def run_code(self):
        self.terminal.delete(1.0, tk.END)  # Очистка терминала перед запуском
        try:
            content = self.text_area.get("1.0", tk.END).strip().split("\n")
            imports = []
            import_commands = {}
            import_templates = {}
            import_code = {}
            includes = set()
            # Первый проход: обработка import
            for line in content:
                r = line.strip()
                if r.startswith("import"):
                    match = re.match(r'import\s+"(.*?)"', r)
                    if match:
                        file_name = match.group(1)
                        try:
                            with open(file_name, "r") as f:
                                lines = f.readlines()
                            if len(lines) < 5:
                                self.terminal.insert(
                                    tk.END,
                                    f"Ошибка: файл {file_name} слишком короткий для импорта\n",
                                )
                                continue
                            include_line = lines[0].strip()
                            commands_line = lines[1].strip()
                            template_line = lines[2].strip()
                            count_line = lines[3].strip()
                            try:
                                count = int(count_line)
                            except ValueError:
                                self.terminal.insert(
                                    tk.END,
                                    f"Ошибка: неверное число команд в {file_name}\n",
                                )
                                continue
                            code_lines = [l.rstrip("\n") for l in lines[4 : 4 + count]]
                            # Сохраняем include
                            includes.add(include_line)
                            # Сохраняем шаблон команды и код
                            commands = [c.strip() for c in commands_line.split(",")]
                            for cmd in commands:
                                import_commands[cmd] = True
                                import_templates[cmd] = template_line
                                import_code[cmd] = code_lines
                        except Exception as e:
                            self.terminal.insert(
                                tk.END, f"Ошибка при импорте {file_name}: {str(e)}\n"
                            )
            with open("main.cpp", "w") as file:
                # Записываем стандартные include
                file.write("#include <iostream>\n")
                file.write("#include <string>\n")
                file.write("#include <fstream>\n")
                file.write('#include "raylib.h"\n')
                # Добавляем include из импортов
                for inc in includes:
                    if inc and not inc.startswith("#include"):
                        file.write(f'#include "{inc}"\n')
                    elif inc:
                        file.write(f"{inc}\n")
                file.write("using namespace std;\n")
                file.write("int main() {\n")
                open_blocks = 0
                declared_variables = set()
                for line in content:
                    r = line.strip()
                    if r.startswith("import"):
                        continue  # Уже обработано
                    # Проверяем импортированные команды
                    found_import = False
                    for cmd in import_commands:
                        if r.startswith(cmd):
                            # Поддержка шаблона: заменяем $args на аргументы после команды
                            args = r[len(cmd) :].strip()
                            template = import_templates[cmd]
                            code_lines = import_code[cmd]
                            # Если шаблон содержит $args, подставляем
                            for code_line in code_lines:
                                if "$args" in template:
                                    file.write(
                                        f"    {code_line.replace('$args', args)}\n"
                                    )
                                else:
                                    file.write(f"    {code_line}\n")
                            found_import = True
                            break
                    if found_import:
                        continue
                    # Исправление обработки команд
                    if r.startswith("if"):
                        match = re.search(r"\((.*?)\)", r)
                        if match:
                            file.write(f"    if ({match.group(1)})" + " {\n")
                            open_blocks += 1
                    elif r == "else":
                        file.write("    else {\n")
                        open_blocks += 1
                    elif r == "end":
                        if open_blocks > 0:
                            file.write("    }\n")
                            open_blocks -= 1
                    elif r.startswith("pf"):
                        match = re.search(r"\((.*?)\)", r)
                        if match:
                            file.write(f"    cout << {match.group(1)};\n")
                    elif r.startswith("var"):
                        match = re.match(r"var\s+(\w+)\s*=\s*(.+)", r)
                        if match:
                            var_name = match.group(1)
                            expression = match.group(2).strip()
                            if var_name not in declared_variables:
                                file.write(f"    auto {var_name} = {expression};\n")
                                declared_variables.add(var_name)
                            else:
                                file.write(f"    {var_name} = {expression};\n")
                    elif r.startswith("ref"):
                        match = re.match(r"ref\s+(\w+)\s*=\s*(.+)", r)
                        if match:
                            var_name = match.group(1)
                            new_value = match.group(2).strip()
                            file.write(f"    {var_name} = {new_value};\n")
                    elif r.startswith("file_read"):
                        match = re.match(r'file_read\s+"(.*?)"\s+(\w+)', r)
                        if match:
                            file_name = match.group(1)
                            var_name = match.group(2)
                            if var_name not in declared_variables:
                                file.write(f"    string {var_name};\n")
                                declared_variables.add(var_name)
                            file.write(f'    ifstream inFile("{file_name}");\n')
                            file.write(f"    if (inFile.is_open())" + " {\n")
                            file.write(f"        getline(inFile, {var_name});\n")
                            file.write("        inFile.close();\n")
                            file.write("    } else {\n")
                            file.write(
                                '        cerr << "Ошибка: не удалось открыть файл для чтения." << endl;\n'
                            )
                            file.write("    }\n")
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды file_read\n",
                            )
                    elif r.startswith("file_write"):
                        # file_write "имя_файла" переменная
                        match_var = re.match(r'file_write\s+"(.*?)"\s+(\w+)', r)
                        # file_write "имя_файла" "строка"
                        match_str = re.match(r'file_write\s+"(.*?)"\s+"(.*?)"', r)
                        if match_var:
                            file_name = match_var.group(1)
                            var_name = match_var.group(2)
                            file.write(f'    ofstream outFile("{file_name}");\n')
                            file.write(f"    if (outFile.is_open())" + " {\n")
                            file.write(f"        outFile << {var_name};\n")
                            file.write("        outFile.close();\n")
                            file.write("    } else {\n")
                            file.write(
                                '        cerr << "Ошибка: не удалось открыть файл для записи." << endl;\n'
                            )
                            file.write("    }\n")
                        elif match_str:
                            file_name = match_str.group(1)
                            content = match_str.group(2)
                            file.write(f'    ofstream outFile("{file_name}");\n')
                            file.write(f"    if (outFile.is_open())" + " {\n")
                            file.write(f'        outFile << "{content}";\n')
                            file.write("        outFile.close();\n")
                            file.write("    } else {\n")
                            file.write(
                                '        cerr << "Ошибка: не удалось открыть файл для записи." << endl;\n'
                            )
                            file.write("    }\n")
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды file_write\n",
                            )
                    elif r.startswith("while"):
                        match = re.search(r"\((.*?)\)", r)
                        if match:
                            file.write(f"    while ({match.group(1)})" + " {\n")
                            open_blocks += 1
                    elif r.startswith("for"):
                        match = re.search(r"\((.*?)\)", r)
                        if match:
                            file.write(f"    for ({match.group(1)})" + " {\n")
                            open_blocks += 1
                    elif r == "exit":
                        file.write("    return 0;\n")
                    elif r == "break":
                        file.write("    break;\n")
                    elif r.startswith("repeat"):
                        match = re.match(r"repeat\s+(\d+)", r)
                        if match:
                            count = int(match.group(1))
                            file.write(
                                f"    for (int i = 0; i < {count}; i++)" + " {\n"
                            )
                            open_blocks += 1
                        else:
                            self.terminal.insert(
                                tk.END, "Ошибка: неправильный формат команды repeat\n"
                            )
                    elif r.startswith("add"):
                        match = re.match(r"add\s+(\w+)\s+(\w+)", r)
                        if match:
                            operand1 = match.group(1)
                            operand2 = match.group(2)
                            file.write(f"    cout << ({operand1} + {operand2});\n")
                    elif r.startswith("sub"):
                        match = re.match(r"sub\s+(\w+)\s+(\w+)", r)
                        if match:
                            operand1 = match.group(1)
                            operand2 = match.group(2)
                            file.write(f"    cout << ({operand1} - {operand2});\n")
                    elif r.startswith("mul"):
                        match = re.match(r"mul\s+(\w+)\s+(\w+)", r)
                        if match:
                            operand1 = match.group(1)
                            operand2 = match.group(2)
                            file.write(f"    cout << ({operand1} * {operand2});\n")
                    elif r.startswith("div"):
                        match = re.match(r"div\s+(\w+)\s+(\w+)", r)
                        if match:
                            operand1 = match.group(1)
                            operand2 = match.group(2)
                            file.write(f"    cout << ({operand1} / {operand2});\n")
                    elif r.startswith("input"):
                        match = re.match(r"input\s+(\w+)", r)
                        if match:
                            var_name = match.group(1)
                            if var_name not in declared_variables:
                                file.write(f"    string {var_name};\n")
                                declared_variables.add(var_name)
                            file.write(f"    cin >> {var_name};\n")
                        else:
                            self.terminal.insert(
                                tk.END, "Ошибка: неправильный формат команды input\n"
                            )
                    elif any(op in r for op in ["+", "-", "*", "/"]):
                        match = re.match(r"(\w+)\s*([+\-*/])\s*(\w+)", r)
                        if match:
                            operand1 = match.group(1)
                            operator = match.group(2)
                            operand2 = match.group(3)
                            file.write(
                                f"    cout << ({operand1} {operator} {operand2});\n"
                            )
                    elif r.startswith("window"):
                        # Поддержка window(800, 600, "Мое окно", RAYWHITE)
                        match = re.match(
                            r'window\((\d+),\s*(\d+),\s*"(.*?)",\s*("?)(\w+)\4\)', r
                        )
                        if match:
                            width = match.group(1)
                            height = match.group(2)
                            title = match.group(3)
                            color = match.group(5)
                            file.write(
                                f'    InitWindow({width}, {height}, "{title}");\n'
                            )
                            file.write("    SetTargetFPS(60);\n")
                            file.write("    while (!WindowShouldClose()) {\n")
                            file.write("        BeginDrawing();\n")
                            file.write(f"        ClearBackground({color});\n")
                            open_blocks += 1  # Открываем блок while
                        else:
                            self.terminal.insert(
                                tk.END, "Ошибка: неправильный формат команды window\n"
                            )
                    elif r.startswith("CloseWindow"):
                        file.write("        EndDrawing();\n")
                        file.write("    }\n")  # Закрытие while (!WindowShouldClose())
                        file.write("    CloseWindow();\n")
                        if open_blocks > 0:
                            open_blocks -= 1
                    elif r.startswith("line"):
                        # Поддержка line x1 y1 x2 y2 COLOR
                        match = re.match(
                            r"line\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\w+)", r
                        )
                        if match:
                            x1 = match.group(1)
                            y1 = match.group(2)
                            x2 = match.group(3)
                            y2 = match.group(4)
                            color = match.group(5)
                            file.write(
                                f"        DrawLine({x1}, {y1}, {x2}, {y2}, {color});\n"
                            )
                        else:
                            self.terminal.insert(
                                tk.END, "Ошибка: неправильный формат команды line\n"
                            )
                    elif r.startswith("cursor"):
                        match = re.match(r"cursor\s+(\d+)", r)
                        if match:
                            hide = match.group(1)
                            if hide == "1":
                                file.write("    HideCursor();\n")
                            elif hide == "0":
                                file.write("    ShowCursor();\n")
                            else:
                                self.terminal.insert(
                                    tk.END,
                                    "Ошибка: неправильный формат команды cursor\n",
                                )
                        else:
                            self.terminal.insert(
                                tk.END, "Ошибка: неправильный формат команды cursor\n"
                            )
                    elif r.startswith("text"):
                        # Поддержка text x y "текст" COLOR
                        match = re.match(r'text\s+(\d+)\s+(\d+)\s+"(.*?)"\s+(\w+)', r)
                        if match:
                            x = match.group(1)
                            y = match.group(2)
                            text = match.group(3)
                            color = match.group(4)
                            file.write(
                                f'        DrawText("{text}", {x}, {y}, 20, {color});\n'
                            )
                        else:
                            self.terminal.insert(
                                tk.END, "Ошибка: неправильный формат команды text\n"
                            )
                    elif r.startswith("circle"):
                        # Поддержка circle x y radius COLOR
                        match = re.match(r"circle\s+(\д+)\s+(\д+)\s+(\д+)\s+(\w+)", r)
                        if match:
                            x = match.group(1)
                            y = match.group(2)
                            radius = match.group(3)
                            color = match.group(4)
                            file.write(
                                f"        DrawCircle({x}, {y}, {radius}, {color});\n"
                            )
                        else:
                            self.terminal.insert(
                                tk.END, "Ошибка: неправильный формат команды circle\n"
                            )
                    elif r.startswith("rectangle"):
                        # Поддержка rectangle x y width height COLOR
                        match = re.match(
                            r"rectangle\s+(\д+)\s+(\д+)\s+(\д+)\s+(\д+)\s+(\w+)", r
                        )
                        if match:
                            x = match.group(1)
                            y = match.group(2)
                            width = match.group(3)
                            height = match.group(4)
                            color = match.group(5)
                            file.write(
                                f"        DrawRectangle({x}, {y}, {width}, {height}, {color});\n"
                            )
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды rectangle\n",
                            )
                    elif r.startswith("intput"):
                        match = re.match(r"intput\s+(\w+)", r)
                        if match:
                            var_name = match.group(1)
                            if var_name not in declared_variables:
                                file.write(f"    int {var_name};\n")
                                declared_variables.add(var_name)
                            file.write(f"    cin >> {var_name};\n")
                        else:
                            self.terminal.insert(
                                tk.END, "Ошибка: неправильный формат команды input\n"
                            )
                    elif r.startswith("fullscreen"):
                        file.write("    ToggleFullscreen();\n")
                    elif r.startswith("pressed"):
                        match = re.match(r"pressed\s+(\w+)", r)
                        if match:
                            key = match.group(1)
                            file.write(f"    if (IsKeyPressed({key})) " + "{\n")
                            open_blocks += 1
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды pressed\n",
                            )
                    elif r.startswith("pressrepet"):
                        match = re.match(r"pressrepet\s+(\w+)", r)
                        if match:
                            key = match.group(1)
                            file.write(f"    if (IsKeyPressedRepeat({key})) " + "{\n")
                            open_blocks += 1
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды pressrepet\n",
                            )
                    elif r.startswith("mouse"):
                        match = re.match(r"mouse\s+(\w+)", r)
                        if match:
                            button = match.group(1)
                            file.write(
                                f"    if (IsMouseButtonPressed({button})) " + "{\n"
                            )
                            open_blocks += 1
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды mouse\n",
                            )
                    elif r.startswith("mousepos"):
                        match = re.match(r"mousepos\s+(\w+)", r)
                        if match:
                            var_name = match.group(1)
                            if var_name not in declared_variables:
                                file.write(f"    Vector2 {var_name};\n")
                                declared_variables.add(var_name)
                            file.write(f"    {var_name} = GetMousePosition();\n")
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды mousepos\n",
                            )
                    elif r.startswith("pixel"):
                        match = re.match(r"pixel\s+(\д+)\s+(\д+)\s+(\w+)", r)
                        if match:
                            x = match.group(1)
                            y = match.group(2)
                            color = match.group(3)
                            file.write(f"        DrawPixel({x}, {y}, {color});\n")
                        else:
                            self.terminal.insert(
                                tk.END, "Ошибка: неправильный формат команды pixel\n"
                            )
                    elif r.startswith("circlesector"):
                        match = re.match(
                            r"circlesector\s+(\д+)\s+(\д+)\s+(\д+)\s+(\д+)\s+(\w+)", r
                        )
                        if match:
                            x = match.group(1)
                            y = match.group(2)
                            radius = match.group(3)
                            angle = match.group(4)
                            color = match.group(5)
                            file.write(
                                f"        DrawCircleSector({x}, {y}, {radius}, {angle}, {color});\n"
                            )
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды circlesector\n",
                            )
                    elif r.startswith("circlesectorlines"):
                        match = re.match(
                            r"circlesectorlines\s+(\д+)\s+(\д+)\s+(\д+)\s+(\д+)\s+(\w+)",
                            r,
                        )
                        if match:
                            x = match.group(1)
                            y = match.group(2)
                            radius = match.group(3)
                            angle = match.group(4)
                            color = match.group(5)
                            file.write(
                                f"        DrawCircleSectorLines({x}, {y}, {radius}, {angle}, {color});\n"
                            )
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды circlesectorlines\n",
                            )
                    elif r.startswith("circilelines"):
                        match = re.match(
                            r"circilelines\s+(\д+)\с+(\д+)\с+(\д+)\с+(\д+)\с+(\w+)", r
                        )
                        if match:
                            x = match.group(1)
                            y = match.group(2)
                            radius = match.group(3)
                            angle = match.group(4)
                            color = match.group(5)
                            file.write(
                                f"        DrawCircleLines({x}, {y}, {radius}, {color});\n"
                            )
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды circilelines\n",
                            )
                    elif r.startswith("rectangle_lines"):
                        match = re.match(
                            r"rectangle_lines\s+(\д+)\с+(\д+)\с+(\д+)\с+(\д+)\с+(\w+)",
                            r,
                        )
                        if match:
                            x = match.group(1)
                            y = match.group(2)
                            width = match.group(3)
                            height = match.group(4)
                            color = match.group(5)
                            file.write(
                                f"        DrawRectangleLines({x}, {y}, {width}, {height}, {color});\n"
                            )
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды rectangle_lines\n",
                            )
                    elif r.startswith("rectangle_rounded"):
                        match = re.match(
                            r"rectangle_rounded\s+(\д+)\с+(\д+)\с+(\д+)\с+(\д+)\с+(\w+)",
                            r,
                        )
                        if match:
                            x = match.group(1)
                            y = match.group(2)
                            width = match.group(3)
                            height = match.group(4)
                            color = match.group(5)
                            file.write(
                                f"        DrawRectangleRounded({x}, {y}, {width}, {height}, {color});\n"
                            )
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды rectangle_rounded\n",
                            )
                    elif r.startswith("rectangle_rounded_lines"):
                        match = re.match(
                            r"rectangle_rounded_lines\s+(\д+)\с+(\д+)\с+(\д+)\с+(\д+)\с+(\w+)",
                            r,
                        )
                        if match:
                            x = match.group(1)
                            y = match.group(2)
                            width = match.group(3)
                            height = match.group(4)
                            color = match.group(5)
                            file.write(
                                f"        DrawRectangleRoundedLines({x}, {y}, {width}, {height}, {color});\n"
                            )
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды rectangle_rounded_lines\n",
                            )
                    elif r.startswith("load_image"):
                        match = re.match(r'load_image\s+"(.*?)"\s+(\w+)', r)
                        if match:
                            file_name = match.group(1)
                            var_name = match.group(2)
                            if var_name not in declared_variables:
                                file.write(f"    Image {var_name};\n")
                                declared_variables.add(var_name)
                            file.write(f'    {var_name} = LoadImage("{file_name}");\n')
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды load_image\n",
                            )
                    elif r.startswith("draw_image"):
                        match = re.match(r"draw_image\s+(\w+)\s+(\д+)\с+(\д+)", r)
                        if match:
                            var_name = match.group(1)
                            x = match.group(2)
                            y = match.group(3)
                            file.write(f"        DrawImage({var_name}, {x}, {y});\n")
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды draw_image\n",
                            )
                    elif r.startswith("audio"):
                        match = re.match(r'audio\s+(\w+)\с+"(.*?)"', r)
                        if match:
                            var_name = match.group(1)
                            file_name = match.group(2)
                            if var_name not in declared_variables:
                                file.write(f"    Sound {var_name};\n")
                                declared_variables.add(var_name)
                            file.write(f'    {var_name} = LoadSound("{file_name}");\n')
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды audio\n",
                            )
                    elif r.startswith("play_audio"):
                        match = re.match(r"play_audio\s+(\w+)", r)
                        if match:
                            var_name = match.group(1)
                            file.write(f"        PlaySound({var_name});\n")
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды play_audio\n",
                            )
                    elif r.startswith("stop_audio"):
                        match = re.match(r"stop_audio\s+(\w+)", r)
                        if match:
                            var_name = match.group(1)
                            file.write(f"        StopSound({var_name});\n")
                        else:
                            self.terminal.insert(
                                tk.END,
                                "Ошибка: неправильный формат команды stop_audio\n",
                            )
                file.write("}\n")

            # Компиляция main.cpp
            compile_result = subprocess.run(
                ["g++", "main.cpp", "-o", "main", "-lraylib"],
                capture_output=True,
                text=True,
            )
            if compile_result.returncode != 0:
                self.display_terminal_output(compile_result.stderr, "error")
                return

            # Запуск main с использованием Popen для асинхронного ввода/вывода
            process = subprocess.Popen(
                ["./main"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            def read_output():
                while True:
                    if process.poll() is not None:
                        # Сначала дочитываем остаток вывода после завершения процесса
                        output = process.stdout.read()
                        if output:
                            self.display_terminal_output(output, "output")
                        error = process.stderr.read()
                        if error:
                            self.display_terminal_output(error, "error")
                        break
                    output = process.stdout.readline()
                    if output:
                        self.display_terminal_output(output, "output")
                    error = process.stderr.readline()
                    if error:
                        self.display_terminal_output(error, "error")

            def handle_input():
                user_input = self.terminal.get("1.0", tk.END).strip()
                if user_input:
                    process.stdin.write(user_input + "\n")
                    process.stdin.flush()
                    self.terminal.delete("1.0", tk.END)
                if process.poll() is None:  # Проверяем, завершился ли процесс
                    self.root.after(100, handle_input)

            threading.Thread(target=read_output, daemon=True).start()
            self.root.after(100, handle_input)

        except Exception as e:
            self.display_terminal_output(str(e), "error")

    def open_file(self):
        filename = filedialog.askopenfilename(
            initialdir=".",
            title="Выберите файл",
            filetypes=(("Все файлы", "*.*"), ("C++ файлы", "*.cpp *.h")),
        )
        if filename:
            try:
                with open(filename, "r") as f:
                    content = f.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.file_path = filename
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def save_file(self):
        try:
            with open("main.nm", "w") as f:
                content = self.text_area.get(1.0, tk.END)
                f.write(content)
            messagebox.showinfo("Сохранено", "Файл успешно сохранен.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def clear_text(self):
        self.text_area.delete(1.0, tk.END)

    def insert_autocomplete(self, event):
        """Вставляет выбранную команду из автодополнения в текстовое поле."""
        command = self.autocomplete_var.get()
        self.text_area.insert(tk.INSERT, command + " ")
        self.autocomplete_var.set("")  # Сбросить выбор


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeEditor(root)
    root.geometry("800x600")
    root.mainloop()
