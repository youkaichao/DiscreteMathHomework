# -*- coding: utf-8 -*-
#  @author 游凯超
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
输出      输入注意事项注意        代表
{userNOT}         是感叹号                  非
{userAND}          是按位与                  合取
{userOR}          是大写的字母V            析取
{userINDUCE}           减号+大于号                 蕴涵
{userEQUAL}        小于号+减号+大于号           双条件词
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
输出      输入注意事项注意        代表
{userNOT}         是感叹号                  非
{userAND}          是按位与                  合取
{userOR}          是C++或||的一部分            析取
{userINDUCE}           C++的异或                 蕴涵
{userEQUAL}        shift+键盘数字1左边的键           双条件词
""".format(userNOT = userNOT, userAND = userAND, userOR = userOR, userINDUCE = userINDUCE, userEQUAL = userEQUAL)

true, false = "1", "0" # 说不定下次改成"True", "False",反正常数就不能直接出现
requirements = """
输入要求：
1:第一行是命题变元，用空格分开
2::后面若干行是真值表，每行的命题变元的值已经写好，只需要填入该解释下的真值值为0或者1
"""
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
def printTheHead(variables, expression):
    line = sep.join(list(variables) + [expression])
    print(line)
def printOneLine(sequence, finalValue):
    line = sep.join(list(sequence) + [finalValue])
    print(line)

# 有些提示输出一次就够了
print("你好，该程序从真值表中得到合式公式")
print(requirements)
print("程序输出的符号解释如下:", end="")
print(explaination)

while True:
    # 确保用户不因为手误直接回车了
    while True:
        variables = str(input("请输入命题变元(单独一个0表示结束):"))
        variables = variables.split()  # 分离命题变元
        if variables:
            break
        else:
            print("没有输入!")
    if variables[0] == "0":
        break
    first = True
    finalFormula = ""
    for x in sequenceGenerator(len(variables)):
        while True:
            # 每行的开头怎么输入是确定的，凡是确定的东西，就不应该让用户去输入，否则又要增加检验
            valueOfThisExplanation = [str(each) for each in x]
            valueOfThisExplanation = sep.join(valueOfThisExplanation)
            line = str(input("请输入真值表在该解释{valueOfThisExplanation}下的真值:".format(valueOfThisExplanation=valueOfThisExplanation)))
            line = valueOfThisExplanation.split() + line.split()
            if len(line) != len(variables) + 1:
                # 长度不对或者输入了234之类的不是真值表的有效数据
                print("无效输入!真值个数不对")
            elif line[-1] not in (true, false):
                print("无效输入!存在{true}和{false}之外的数据!".format(true=true, false=false))
            else:
                break

        if line[-1] == false:
            continue
        # 用主析取范式
        minium = ""  # 极小项
        for index in range(len(line) - 1):
            if index != 0:
                minium += userAND
            if line[index] == true:
                minium += variables[index]
            else:
                minium += userNOT + variables[index]
        minium = "({minium})".format(minium=minium)
        if first:
            finalFormula += minium
            first = False
        else:
            finalFormula += userOR + minium
    print("对应的公式为：{finalFormula}".format(finalFormula=finalFormula))

print("感谢使用，下次再见!\n%s"%googbyePic)
input("按任意键后回车继续...")

