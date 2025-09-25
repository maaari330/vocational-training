import tkinter as tk


class Calc(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.create_widget()
        self.focus_set()
        self.bind("<Key>", self.key_click)

    def create_widget(self):
        # current num, calc
        self.cur_num = "0"
        self.cur_formula = ""
        self.already_calc = False
        # btn dict for hover
        self.btn_dict = {}
        # fomula Label
        lbf_fomula = tk.LabelFrame(self, text="Formula")
        lbf_fomula.pack(anchor=tk.E)
        self.fomula = tk.StringVar(self, value="0")
        self.lb_fomula = tk.Label(lbf_fomula, textvariable=self.fomula)
        self.lb_fomula.pack()

        # current number Label
        lbf_currentNum = tk.LabelFrame(self, text="Result")
        lbf_currentNum.pack(anchor=tk.E)
        self.result = tk.StringVar(self, value="0")
        self.lb_currentNum = tk.Label(lbf_currentNum, textvariable=self.result)
        self.lb_currentNum.pack()

        # C button
        lbf_c = tk.Frame(self)
        lbf_c.pack(anchor=tk.W)
        btn_c = tk.Button(lbf_c, command=self.cancel_all, text="C", width=3)
        btn_c.grid(column=0, row=0)
        self.btn_dict[btn_c.cget("text")] = btn_c

        # Equal button
        btn_equal = tk.Button(lbf_c, command=self.calc, text="=", width=3)
        btn_equal.grid(column=3, row=0)
        self.btn_dict[btn_equal.cget("text")] = btn_equal

        # 0~9 button
        lbf_num = tk.Frame(self)
        lbf_num.pack()
        for i, j in enumerate([7, 8, 9, 4, 5, 6, 1, 2, 3, 0]):
            btn = tk.Button(lbf_num, text=str(j), width=3)
            btn.bind("<Button-1>", self.num_btn_push)
            btn.grid(column=i % 3, row=i // 3)
            self.btn_dict[btn.cget("text")] = btn

        # dot button
        btn_dot = tk.Button(lbf_num, command=self.dotcalc, text=".", width=3)
        btn_dot.grid(column=1, row=3)
        self.btn_dict[btn_dot.cget("text")] = btn_dot

        # operator button
        for k, l in enumerate(["/", "*", "+", "-"]):
            btn = tk.Button(lbf_num, text=l, width=3)
            btn.bind("<Button-1>", self.num_operator_push)
            btn.grid(column=4, row=k)
            self.btn_dict[btn.cget("text")] = btn

    # 0~9 add
    def num_btn_push(self, event=None, kbd=None):
        num = kbd or event.widget["text"]
        if self.cur_num == "0":
            self.cur_num = num
        else:
            self.cur_num += num
        self.result.set(self.cur_num)

    # cancel
    def cancel_all(self):
        self.cur_num = "0"
        self.cur_formula = ""
        self.result.set("0")
        self.fomula.set("")

    # dot add
    def dotcalc(self):
        if not self.cur_num:
            self.cur_num = "0."
        elif "." not in self.cur_num:
            self.cur_num += "."
        else:
            return
        self.result.set(self.cur_num)

    # operator add
    def num_operator_push(self, event=None, kbd=None):
        ope = kbd or event.widget["text"]
        if self.already_calc:
            self.cur_num = self.result.get()
            self.already_calc = False
        temp = self.cur_formula + self.cur_num
        if not self.cur_formula:
            self.cur_formula = self.cur_num + ope
        elif not temp[-1].isnumeric():
            self.cur_formula = self.cur_formula[:-1] + ope
        else:
            self.cur_formula = temp + ope
        self.fomula.set(self.cur_formula)
        self.cur_num = ""

    # calculate equal
    def calc(self):
        try:
            ope = "="
            if self.cur_formula and self.cur_formula[-1] in ["/", "*", "+", "-"]:
                self.cur_formula = self.cur_formula[:-1]
            if self.cur_num and self.cur_num[-1] == ".":
                self.cur_num = self.cur_num[:-1]
            res = self.cur_formula + self.cur_num
            if not res:
                return
            self.fomula.set(res + ope)
            res_view = eval(res)
        except ZeroDivisionError:
            self.result.set("ZeroDivisionError")
            self.after(3000, self.cancel_all)
        else:
            if isinstance(res_view, float):
                if res_view.is_integer():
                    res_view = f"{int(res_view):d}"
                else:
                    res_view = f"{res_view:12f}".rstrip("0").rstrip(".")
            self.result.set(res_view)
            self.cur_num = "0"
            self.cur_formula = ""
            self.already_calc = True

    # key click
    def key_click(self, event):
        if event.char.isdigit():
            self.num_btn_push(kbd=event.char)
        elif event.char == "c":
            self.cancel_all()
        elif event.char == ".":
            self.dotcalc()
        elif event.char in ["/", "*", "+", "-"]:
            self.num_operator_push(kbd=event.char)
        elif event.keysym == "Return" or event.char == "=":
            self.calc()

        if event.char in self.btn_dict.keys():
            btn = self.btn_dict.get(event.char)
            btn.configure(relief=tk.SUNKEN)
            self.after(
                200, lambda b=btn: b.configure(relief=tk.RAISED)
            )  # afterは引数なしだから関数作成時点でbtnに固定


root = tk.Tk()
root.geometry("210x280+100+100")
root.title("MyCalc Step1")
app = Calc(master=root)
app.mainloop()
