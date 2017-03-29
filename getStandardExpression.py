# -*- coding: utf-8 -*-
#  @author 游凯超
import sys
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
但是在actual和user不同的情况下，用户可能恰巧输入了我的actual表示，那会引发错误
actualINDUCE 和 actualEQUAL用的目的是让用户无法恰巧错误地输入了我实际上的字符
"""

pretty = False # 相当于条件编译了
if pretty:
    userNOT = "!"
    actualNOT = "!"
    userAND = "&"
    actualAND = "&"
    userOR = "V"
    actualOR = "V"
    userINDUCE = "->"  # 蕴含词
    actualINDUCE = "\n"
    userEQUAL = "<->"  # 双蕴涵词
    actualEQUAL = "\t"
    leftParenthesis = "("
    rightParenthesis = ")"
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
注4:每个命题变元只能是一个字母
""".format(userNOT=userNOT, userAND=userAND, userOR=userOR, userINDUCE=userINDUCE, userEQUAL=userEQUAL)
else:
    userNOT            = "!"
    actualNOT            = "!"
    userAND              = "&"
    actualAND             = "&"
    userOR                 = "|"
    actualOR               = "|"
    userINDUCE           = "^"  # 蕴含词
    actualINDUCE         ="^"
    userEQUAL          ="~"  # 双蕴涵词
    actualEQUAL           ="~"
    leftParenthesis        ="("
    rightParenthesis      = ")"
    explaination = """
输入      输入注意事项注意        代表
{userNOT}         是感叹号                  非
{userAND}          是按位与                  合取
{userOR}          是C++或||的一部分            析取
{userINDUCE}           C++的异或                 蕴涵
{userEQUAL}        shift+键盘数字1左边的键           双条件词
注1:输入的所有的空白字符会被忽略
注2:上表是按照联结词优先级递减顺序写的
注3:输入的括号请确保是英文的括号
注4:每个命题变元只能是一个字母
""".format(userNOT = userNOT, userAND = userAND, userOR = userOR, userINDUCE = userINDUCE, userEQUAL = userEQUAL)

true, false = "1", "0" # 说不定下次改成"True", "False",反正常数就不能直接出现

# 所有的联结词
actualLinkVerbs = (actualNOT, actualAND, actualOR, actualINDUCE, actualEQUAL)

map = {userNOT:actualNOT,
            userAND:actualAND,
            userOR:actualOR,
            userINDUCE:actualINDUCE,
            userEQUAL:actualEQUAL}
reverseMap = {map[x] : x for x in map} # 反转映射


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

def splitByIter(expression, sequence):
    expression = [expression]  # split by using an iterable sequence
    for x in sequence:
        L = []
        for each in expression:
            L.extend(each.split(x))
        expression = L
    return expression

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

    expression = splitByIter(expression, (actualNOT, actualAND, actualOR, actualINDUCE, actualEQUAL, rightParenthesis, leftParenthesis))

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
                return {"Poland": Poland.top(), "ReversePoland": ReversePoland.top()}
                # 用键的形式给出总会更有意义一些

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

def countDigits(x):  # 计算二进制的位数
    digits, value = 0, x
    while value > 0:
        value //= 2
        digits += 1
    if x == 0:
        digits = 1
    return digits

def sequenceGenerator(n):
    for x in range((1 << n)):
        L = [0 for x in range(n)]  # 构建空序列, 由 n 个bool值构成
        binStr = bin(x)
        digits = countDigits(x)
        for i in range(1, 1 + digits):
            L[-i] = int(binStr[-i])
        yield tuple(L)

def induce(a, b):
    return (not a) or b

def equal(a, b):
    return induce(a, b) and induce(b, a)

def And(a, b):
    return a and b

def Or(a, b):
    return a or b

# 通过字符串来对应函数,又由于and or是关键字，所以得包装成函数
doubleFuncs = {actualAND:And, actualOR:Or, actualINDUCE:induce, actualEQUAL:equal}

# 参数都得是字符串,这是输出格式控制
sep = "\t"
def printTheHead(variables, expression, out = sys.stdout):
    line = sep.join(list(variables) + [expression])
    print(line, file=out)
def printOneLine(sequence, finalValue, out = sys.stdout):
    line = sep.join(list(sequence) + [finalValue])
    print(line, file=out)


googbye = "感谢使用，下次再见!\n%s"%googbyePic

from tkinter import *
from tkinter.messagebox import *

def setTextOut(text):
    textForOut.delete(0.0, END) # 清空原有内容
    textForOut.insert(1.0, text)

def funcForButton():
    expression = enter.get()
    expression = expression.strip()
    with open("buffer.txt", "w", encoding="utf-8") as f:
    # 打开一个文件供缓存
        if not expression:
            setTextOut("指令不能为空!")
            return

        expression = "".join(expression.split())
        expression = replace(expression, map)

        if not valid(expression):
            setTextOut("输入的不是合法的表达式!")
            return
        else:
            variables = splitByIter(expression, list(map.values()) + ["(", ")"])  # 分的时候括号也要用来分隔
            variables = [x for x in variables if x]  # 调试才知道，这里可能有空
            variables = list(set(variables))  # 删除重复的命题变元
            variables.sort()  # 真值表的书写顺序是字典序
            ReversePoland = transform(expression)["ReversePoland"]

            printTheHead(variables, replace(expression, reverseMap), out=f)
            if ReversePoland == variables[0]:  # 只有一个字母P
                printOneLine(["0"], "0", out=f)
                printOneLine(["1"], "1", out=f)
            else:
                for each in sequenceGenerator(len(variables)):
                    each = list(each)
                    variablesToItsTruthValue = {x: y for (x, y) in zip(variables, each)}  # 各个命题变元的初始化
                    variablesToItsTruthValue[True] = 1
                    variablesToItsTruthValue[False] = 0

                    statement = stack()  # 存储命题变元的栈
                    for x in ReversePoland:
                        if x not in actualLinkVerbs:
                            statement.push(x)  # 这个是命题变元
                        elif x == actualNOT:
                            statement.push(not variablesToItsTruthValue[statement.pop()])
                        else:
                            # 这是栈啊，大哥，先出来的应该是双目运算符右边的......
                            temp1 = statement.pop()
                            temp2 = statement.pop()
                            statement.push(doubleFuncs[x](variablesToItsTruthValue[temp2], variablesToItsTruthValue[temp1]))
                    # 至此栈内只有一个真值了
                    each = [str(x) for x in each]
                    printOneLine(each, str(int(statement.pop())), out=f)
    with open("buffer.txt", "r", encoding="utf-8") as f:
    # 再打开该文件进行读入真值表
        lines = f.readlines()
        if not lines:
            return # 上次操作有误，没有输出结果
        temp = lines[0].split()
        variables = temp[0:-1]# 第一行最后一个是公式，不需要
        del temp
        indexOfLines = 1 # 省去一个for循环
        firstOfOr = True # 主析取范式的first
        firstOfAnd = True # 主合取范式的first
        finalOrFormula = ""
        finalAndFormula = ""  # 合取公式
        for x in range(1 << len(variables)):
            # 读取一行
            line = lines[indexOfLines].split() # 一开始忘了split
            indexOfLines += 1

            # 要设置两个first才行
            if line[-1] == false:
                maximun = ""  # 极大项
                for index in range(len(line) - 1):
                    if index != 0:
                        maximun += userOR
                    if line[index] == false:
                        maximun += variables[index]
                    else:
                        maximun += userNOT + variables[index]
                maximun = "({maximun})".format(maximun=maximun)
                if firstOfAnd:
                    finalAndFormula += maximun
                    firstOfAnd = False
                else:
                    finalAndFormula += userAND + maximun
            else:
                minium = ""  # 极小项
                for index in range(len(line) - 1):
                    if index != 0:
                        minium += userAND
                    if line[index] == true:
                        minium += variables[index]
                    else:
                        minium += userNOT + variables[index]
                minium = "({minium})".format(minium=minium)
                if firstOfOr:
                    finalOrFormula += minium
                    firstOfOr = False
                else:
                    finalOrFormula += userOR + minium
        setTextOut("对应的为主析取范式为：{finalOrFormula}".format(finalOrFormula=finalOrFormula)
                   + "\n" +"对应的为主合取范式为：{finalAndFormula}".format(finalAndFormula=finalAndFormula) )


def on_closing():
    showinfo("GoodBye!", googbye)
    root.destroy()


root = Tk()
root.title("中缀表达式转范式")
root.maxsize(600, 600)
root.protocol("WM_DELETE_WINDOW", on_closing)

# root.minsize(600, 600)

textForExplanation = Text(root, height=15)
textForExplanation.insert(1.0, "你好，该程序用于将中缀表达式转化为主析取范式和主合取范式！\n"
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
