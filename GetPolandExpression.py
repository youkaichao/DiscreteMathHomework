class stack:
    def __init__(self):
        self.array = []
    def push(self, x):
        self.array.append(x)
    def pop(self):
        if self.array == []:
            raise OverflowError("The stack is empty!")
        return self.array.pop(-1)
    def top(self):
        if self.array == []:
            raise OverflowError("The stack is empty!")
        return self.array[-1]
    def empty(self):
        return bool(self.array == [])



# 这次吸取教训了吧，让你这么硬编码!
"""
userXXX是用户的输入输出形式，
actualXXX是内部处理的形式，每个联结词都是一个字母在处理上会有好处
actualINDUCE 和 actualEQUAL用的目的是让用户无法恰巧错误地输入了我实际上的字符
"""
userNOT            = "!"
actualNOT            = "!"
userAND              = "&"
actualAND             = "&"
userOR                 = "V"
actualOR               = "V"
userINDUCE           = "->"  # 蕴含词
actualINDUCE         ="\n"
userEQUAL          ="<->"  # 双蕴涵词
actualEQUAL           ="\t"
leftParenthesis        ="("
rightParenthesis      = ")"

map = {userNOT:actualNOT,
            userAND:actualAND,
            userOR:actualOR,
            userINDUCE:actualINDUCE,
            userEQUAL:actualEQUAL}
reverseMap = {map[x] : x for x in map} # 反转映射

explaination = """
输入      输入注意事项注意        代表
{userNOT}         是感叹号                  非
{userAND}          是按位与                  合取
{userOR}          是大写的字母V            析取
{userINDUCE}           减号+大于号                 蕴涵
{userEQUAL}        小于号+减号+大于号           双条件词
注1:输入的所有的空白字符会被忽略
注2:上表是按照联结词优先级递减顺序写的
注3:输入的括号请确保是英文的括号
注4:命题变元不能是两个字母，否则波兰表达式会有歧义
""".format(userNOT = userNOT, userAND = userAND, userOR = userOR, userINDUCE = userINDUCE, userEQUAL = userEQUAL)


googbyePic = """
   ╭╮　　　　　　　╭╮　　
　││　　　　　　　││　　
╭┴┴———————┴┴╮
│　　　　　　　　　　　│　　　
│　　　　　　　　　　　│　　　
│　●　　　　　　　●  　│
│○　　╰┬┬┬╯　　○    │
│　　　　╰—╯　　　　│　
╰——┬Ｏ———Ｏ┬——╯
　 　╭╮　　　　╭╮　　　　
　 　╰┴————┴╯  """

def valid(expression):
    # expression = ""

    parentheses = stack()
    for x in expression:  # 首先进行括号匹配
        if x == leftParenthesis:
            parentheses.push(x)
        elif x == rightParenthesis:
            if parentheses.empty():
                return False
            else:
                parentheses.pop()
    if not parentheses.empty():
        return False # 括号匹配结束
    for (i, x) in enumerate(expression):
        # 检测 非 的使用是否合法
        if x == actualNOT:
            if i != 0 and expression[i - 1] == rightParenthesis:
                return False #非 的前面不能有右括号
            if i == len(expression) - 1 or expression[i + 1] in (actualOR, actualAND, actualINDUCE, actualEQUAL, rightParenthesis):
                return False # 非 不能出现在最后，其后也不能有 "V", "∧", "→", "↔", ")"
    expression = expression.replace(actualNOT, "") # 非 都是合法的，就可以删去了
    for (i, x) in enumerate(expression):
        if x in (actualOR, actualAND, actualINDUCE, actualEQUAL):
            # 这些符号不能在最左边或者左边还是这些符号/左括号
            if i == 0 or expression[i - 1] in (actualOR, actualAND, actualINDUCE, actualEQUAL, leftParenthesis):
                return False
            # 也不能在最右边或者右边还是这些符号/右括号
            if i == len(expression) - 1 or expression[i + 1] in (actualOR, actualAND, actualINDUCE, actualEQUAL, rightParenthesis):
                return False
    # 到这里大概能够保证表达式正确吧

    expression = [expression]  # 看是否有两个相连的字母，那样子变成波兰表达式会有歧义
    for x in (actualNOT, actualAND, actualOR, actualINDUCE, actualEQUAL, rightParenthesis, leftParenthesis):
        L = []
        for each in expression:
            L.extend(each.split(x))
        expression = L

    for x in expression:
        if len(x) >= 2:
            return False
    return True

def transform(expression):
    order = {
                actualNOT                        :   [],  # 非的优先级：现出现的优先级低，这个和其他联结词不一样
                 actualAND                        :   [actualNOT, actualAND],
                 actualOR                        :   [actualNOT, actualAND, actualOR],
                 actualINDUCE                        :  [actualNOT, actualAND, actualOR, actualINDUCE],
                 actualEQUAL                        :   [actualNOT, actualAND, actualOR, actualINDUCE, actualEQUAL],
                 leftParenthesis                          :  [],
                 rightParenthesis                          :   [actualNOT, actualAND, actualOR, actualINDUCE, actualEQUAL, leftParenthesis]
             }
    # key是现在要决定的符号，在栈顶取一个符号，如果在value里面，就说明栈顶的符号该弹出了
    expression = "{leftParenthesis}{expression}{rightParenthesis}".format(leftParenthesis=leftParenthesis, expression=expression, rightParenthesis=rightParenthesis)
    # 加一对括号

    operator = stack() # 记录符号的
    Poland = stack()  # 记录波兰表达式
    ReversePoland = stack() # 记录逆波兰表达式
    index = 0
    operator.push(expression[index]) # 左括号入栈
    index += 1
    while index < len(expression):
        if expression[index] in (actualNOT, actualAND, actualOR, actualINDUCE, actualEQUAL, leftParenthesis):
            while operator.top() in order[expression[index]]:
                if operator.top() == actualNOT:
                    Poland.push(operator.top() + Poland.pop())
                    ReversePoland.push(ReversePoland.pop() + operator.top())
                    operator.pop()
                else:
                    temp1 = Poland.pop()
                    temp2 = Poland.pop()
                    Poland.push(operator.top() + temp2 + temp1)
                    temp1 = ReversePoland.pop()
                    temp2 = ReversePoland.pop()
                    ReversePoland.push(temp2 + temp1 + operator.top())
                    operator.pop()
            else:
                operator.push(expression[index])

            index += 1  # 一开始没有加这句话......

        elif expression[index] == rightParenthesis:
            # 右括号单独处理
            while operator.top() != leftParenthesis:
                if operator.top() == actualNOT:
                    Poland.push(operator.top() + Poland.pop())
                    ReversePoland.push(ReversePoland.pop() + operator.top())
                    operator.pop()
                else:
                    temp1 = Poland.pop()
                    temp2 = Poland.pop()
                    Poland.push(operator.top() + temp2 + temp1)
                    temp1 = ReversePoland.pop()
                    temp2 = ReversePoland.pop()
                    ReversePoland.push(temp2 + temp1 + operator.top())
                    operator.pop()
            # 左括号和右括号匹配,弹出左括号
            operator.pop()
            if index == len(expression) - 1:
                #右括号已经弹出了
                return Poland.top(), ReversePoland.top()

            index += 1 # 一开始没有加这句话......

        else:
            variable = ""
            while index < len(expression) and expression[index]  not in (actualNOT, actualAND, actualOR, actualINDUCE, actualEQUAL, leftParenthesis, rightParenthesis):
                variable += expression[index]
                index += 1
            Poland.push(variable)
            ReversePoland.push(variable)
            #记录一个命题变元

def replace(expression, map):
    # map的key是要转换的，value是转换结果
    for x in map:
        expression = expression.replace(x, map[x])
    return expression

googbye = "感谢使用，下次再见!\n%s"%googbyePic

from tkinter import *
from tkinter.messagebox import *

def setTextOut(text):
    textForOut.delete(0.0, END)
    textForOut.insert(1.0, text)

def funcForButton():
    expression = enter.get()
    expression = expression.strip()
    if expression:
        expression = "".join(expression.split())
        expression = replace(expression, map)

        if not valid(expression):
            setTextOut("输入的不是合法的表达式!")
        else:
            Poland, ReversePoland = transform(expression)
            Poland = replace(Poland, reverseMap)
            ReversePoland = replace(ReversePoland, reverseMap)

            setTextOut("等价的波兰表达式是:" + Poland + "\n" + "等价的逆波兰表达式是:" + ReversePoland)
    else:
        setTextOut("请输入指令!")

def on_closing():
    showinfo("GoodBye!", googbye)
    root.destroy()


root = Tk()
root.title("中缀表达式转波兰表达式")
root.maxsize(600, 600)
root.protocol("WM_DELETE_WINDOW", on_closing)

# root.minsize(600, 600)

textForExplanation = Text(root, height=15)
textForExplanation.insert(1.0, "你好，该程序用于将中缀表达式转化为波兰表达式或者逆波兰表达式！\n"
                          +"你的中缀表达式可以用到以下的命题联结词:" + explaination)
textForExplanation.pack()

#提示框
textForHint = Text(root, height=2)
textForHint.insert(1.0, "请在下方输入你的中缀表达式")
textForHint.pack()

#输入框
enter = Entry(root)
enter.pack()

Button(root, text="确定", command=funcForButton).pack()

textForOut = Text(root)
textForOut.pack()

root.mainloop()
