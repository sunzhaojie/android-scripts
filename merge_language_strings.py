# encoding=utf-8
import os
import sys
from Tkinter import *
import tkFileDialog
import tkMessageBox
import re
# import regex

# 映射关系
LANGUANGE_MAPPED_1 = {
    "en": "values/",
    "ar-eg": "values-ar/",
    "de-de": "values-de/",
    "es-xl": "values-es/",
    "es-us": "values-es-rUS/",
    "fr-fr": "values-fr/",
    "hi-in": "values-hi/",
    "id-id": "values-in/",
    "it-it": "values-it/",
    "ja-jp": "values-ja/",
    "ko-kr": "values-ko/",
    "nl-nl": "values-nl/",
    "pl-pl": "values-pl/",
    "pt-pt": "values-pt/",
    "pt-br": "values-pt-rBR/",
    "ru-ru": "values-ru/",
    "th-th": "values-th/",
    "tr-tr": "values-tr/",
    "uk-ua": "values-uk/",
    "vi-vn": "values-vi/",
    "zh-cn": "values-zh-rCN/",
    "zh-tw": "values-zh-rTW/"
}

LANGUANGE_MAPPED_2 = {
    "en": "values/",
    "areg": "values-ar/",
    "dede": "values-de/",
    "esxl": "values-es/",
    "esus": "values-es-rUS/",
    "frfr": "values-fr/",
    "hiin": "valueshi/",
    "idid": "values-in/",
    "itit": "values-it/",
    "jajp": "values-ja/",
    "kokr": "values-ko/",
    "nlnl": "values-nl/",
    "plpl": "values-pl/",
    "ptpt": "values-pt/",
    "ptbr": "values-pt-rBR/",
    "ruru": "values-ru/",
    "thth": "values-th/",
    "trtr": "values-tr/",
    "ukua": "values-uk/",
    "vivn": "values-vi/",
    "zhcn": "values-zh-rCN/",
    "zhtw": "values-zh-rTW/"
}

LANGUANGE_MAPPED = dict(LANGUANGE_MAPPED_1.items() +
                        LANGUANGE_MAPPED_2.items())


def mergeStrings(level, pathIn, pathOut, annotation):
    '''
    递归遍历所有目录，合并多语言
    pathIn：多语翻译返回的地址 如/Users/sunzhaojie/Desktop/多语返回
    pathOut：项目工程地址 如/Users/sunzhaojie/WorkSapce/AndroiStudio/baidu/demo
    annotation：此次合入注释
    '''
    dirList = []
    fileList = []
    files = os.listdir(pathIn)
    dirList.append(str(level))
    for f in files:
        if(os.path.isdir(pathIn + '/' + f)):
            # 排除隐藏文件夹
            if(f[0] == '.'):
                pass
            else:
                dirList.append(f)
        if(os.path.isfile(pathIn + '/' + f)):
            fileList.append(f)
    i_dl = 0
    for dl in dirList:
        if(i_dl == 0):
            i_dl = i_dl + 1
        else:
            mergeStrings((int(dirList[0]) + 1),
                         pathIn + '/' + dl, pathOut, annotation)
    for fl in fileList:
        strs = pathIn.split('/')
        # 转化为小写，从而忽略大小写进行映射
        fileName = strs[-1].lower()
        # 查找映射并忽略隐藏文件
        if LANGUANGE_MAPPED.has_key(fileName) and fl[0] != '.':
            print ''
            print fileName + '/' + fl + ' ===========>>> ' + LANGUANGE_MAPPED[fileName] + 'strings.xml'
            mergeSingleStrings(pathIn + '/' + fl, pathOut +
                               LANGUANGE_MAPPED[fileName] + 'strings.xml', annotation)


def mergeSingleStrings(pathIn, pathOut, annotation):
    '''
    合并单个多语言
    pathIn: 返回多语具体语言的地址 如/Users/sunzhaojie/Desktop/多语返回/ar-eg/string.xml
    pathOut: 项目中对应strings.xml的地址如/Users/sunzhaojie/WorkSapce/AndroiStudio/baidu/demo/app/src/main/res/values-ar/strings.xml
    annotation: 合入多语的注释
    '''

    # 自动添加开始处的注释
    strs = '\n    <!--' + annotation + ' by auto merge-->\n'
    f = open(pathIn)
    # 读取待合入文案的所有内容
    lines = f.readlines()
    # 记录合入的文案条数
    count = 0

    for line in lines:
        # 过滤头尾空白字符
        line = line.strip()
        lineTemp = line
        # 通过正则匹配注释，是注释直接加入
        if re.match(r'^\s*<!--.*-->\s*$', lineTemp):
            strs = strs + '    ' + line + '\n'
            continue
        # 通过正则提取具体的文案(<string name="">...</string>)
        lineTemps = re.split(
            r'^\s*<\s*string\s+name\s*=\s*\".+\"\s*>|</\s*string\s*>\s*$', lineTemp)
        # 不是文案，继续下面一行
        if len(lineTemps) != 3:
            continue
        # 是文案，提取文案内容
        contet = lineTemps[1]
        # 对文案内容进行特殊字符格式检查并自动纠正，目前包括%、和单双引号
        lineTemp = lineTemp.replace(contet, checkSpecialChars(contet))
        # 文案特殊字符使用错误进行自动纠正之后，输出原文和纠正之后的文案，方便用户进行判断
        if line != lineTemp:
            print '#########################注意 START #########################'
            print '#########################返回文案是[%s]，格式检查自动纠正为[%s]，请确认!' % (line, lineTemp)
            print '#########################注意  END  #########################'
        # 每行前面添加一个TAB(自动格式化)
        strs = strs + '    ' + lineTemp + '\n'
        count = count + 1

    # 自动添加结尾处的注释
    strs = strs + '    <!--' + annotation + ' by auto merge-->\n'
    # 最后一行添加</resources>
    strs = strs + '\n</resources>'
    f.close()

    # 有文案要合入
    if count > 0:
        # 读取项目中具体语言的strings.xml
        f = open(pathOut, 'r+')
        all_the_lines = f.readlines()
        f.seek(0)
        f.truncate()
        for line in all_the_lines:
            # 将项目中具体语言的strings.xml中的</resources>替换为处理后的文案
            line = line.replace('</resources>', strs)
            f.write(line)
        f.close()

    print '合入文案:%d条' % (count)
    # 考虑到多语公司返回文案有可能格式不太规范，这里用放宽条件的正则匹配寻找返回多语中的文案条数，然后和合入的文案条数进行对比，不符则输出提示
    originCount = len(re.findall(
        r'<\s*string\s*name\s*=\s*\".+\"\s*>', ''.join(lines), re.I))
    if(originCount != count):
        print '#########################警告 START #########################'
        print '#########################返回文案有%d条，只合入了%d条文案，请确认' % (originCount, count)
        print '#########################注警告 END  #########################'


def checkSpecialChars(contet):
    '''
    对文案内容进行特殊字符格式检查并自动纠正，目前包括%、和单双引号
    '''
    contet = checkPercent(contet)
    contet = checkQuotationMarks(contet)
    return contet


def checkPercent(contet):
    '''
    检查并自动纠正%的使用正确性

    功能：
    1.将\%替换为%%
    2.将除占位符之外的未转义的%替换为%%

    注意点：
    1.对于一个%会优先检查是不是符合占位符，因而在某些情况下会出现歧义.
    比如"%%sx"这种情况，第二个%是和后面的s连起来成为占位符第一个%未转义呢，还是%%就是转义的%呢？
    因而使用者在具体使用的时候要观察输出日志，如果出现自动纠正%的时候进行判断一下是否符合自己的场景

    2.正则查找未转义的%，因为一个未转义的%前面有可能有若干个连续的%%，所以会用到可变长度的逆序环视.
    而Python自带的正则解释器re不支持可变长度的逆序环视，如果要使用该正则匹配未转义的%确保安装了regex(安装方法:sudo pip install regex).
    也提供了不使用regex替换未转义%的方法, 代码见下面.

    3.对于阿拉伯语言(RTL语言)%的检查纠正方法和正常语言保持一致，因为在把RTL语言语言合入values-ar的strings.xml中时，AS会自动进行左右变换。
    如“حفظ %s%%”合入之后自动变为”%%s% حفظ”, 而“حفظ %%s%”合入之后却变为”%s%% حفظ”。
    '''
    result = contet
    # 将\%替换为%%
    result = result.replace('\%', '%%')

    # 使用re.split(r'%(?=(\d+\$)?[sd])',result)正则划分，返回的结果却不是按照找到的%进行划分,会多出几个有规律的子串.
    # 目前退而求其次使用ugly的替换在分割方法，待后续解决.
    uglyStr = '<sunzhaojie19950710>'
    result = re.sub(r'%(?=(\d+\$)?[sd])', uglyStr, result)
    # 以占位符%进行分割字符串
    strs = result.split(uglyStr)

    result = ''
    i = 0
    # 遍历分割得到的所有字符串，进行检查纠正
    for str in strs:
        i = i + 1

        '''
        第一种方法
        通过正则找到未转义的%，进行替换
        Python自带的正则解释器re不支持可变长度的逆序环视，如果要使用该正则匹配未转义的%确保安装了regex(安装方法:sudo pip install regex).
        使用下面正则别忘了import regex
        '''
        # str = regex.sub(r"(?<=(^|[^%])(%%)*)%(?!%)", '%%', str)

        '''
        第二种方法
        未安装regex使用下面的代码,安装了的可以使用上面的正则
        通过ugly的替换在替换方法进行替换为转义的%
        '''
        str = str.replace('%%', uglyStr)
        str = str.replace('%', '%%')
        str = str.replace(uglyStr, '%%')

        # 添加占位符的%
        result = result + str + '%'
    if i > 0:
        # 去除多余的最后一个%
        result = result[:-1]

    return result


def checkQuotationMarks(contet):
    '''
    检查单双引号的正确性并自动纠正
    '''
    result = contet

    # 具体转义有两种做法，直接添加反斜杠或者使用相应的html实体符

    result = re.sub(r'(?<![\\])\'', '\\\'', result)
    # re.sub(r'(?<![\\])\'','&apos;',result)

    result = re.sub(r'(?<![\\])\"', '\\\"', result)
    # re.sub(r'(?<![\\])\"','&quot;',result)

    return result


class Application(Frame):
    '''
    界面相关
    '''

    projectPath = ''
    stringsPath = ''
    annotation = ''

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.projectPathLabel = Label(self, text='')
        self.projectPathLabel.pack()
        self.projectPathSelectButton = Button(
            self, text='选择项目工程(AS)', command=self.selectProjectPath)
        self.projectPathSelectButton.pack()

        self.stringsPathLabel = Label(self, text='')
        self.stringsPathLabel.pack()
        self.stringsPathSelectButton = Button(
            self, text='选择多语返回文件', command=self.selectStringsPath)
        self.stringsPathSelectButton.pack()

        self.annotationInput = Entry(self)
        self.annotationInput.pack()

        self.mergeStringsButton = Button(
            self, text='开始合入', command=self.startMergeStrings)
        self.mergeStringsButton.pack()

    def selectProjectPath(self):
        fname = tkFileDialog.askdirectory(
            title=u"选择文件", initialdir=(os.path.expanduser(r"./")))
        self.projectPath = fname
        self.projectPath = self.projectPath + '/app/src/main/res/'
        self.projectPathLabel['text'] = fname

    def selectStringsPath(self):
        fname = tkFileDialog.askdirectory(
            title=u"选择文件", initialdir=(os.path.expanduser(r"./")))
        self.stringsPath = fname
        self.stringsPathLabel['text'] = fname

    def startMergeStrings(self):
        if self.projectPath == '' or self.stringsPath == '':
            tkMessageBox.showerror('错误', '请选择正确的项目地址和多语返回地址')
            return
        self.annotation = self.annotationInput.get() or ''
        mergeStrings(1, self.stringsPath, self.projectPath, self.annotation)
        tkMessageBox.showinfo('成功', '合入成功，请看控制台的输出日志')


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')

    app = Application()
    rt = app.master
    rt.title('自动合入多语')
    tmpcnf = '%dx%d+%d+%d' % (300, 300, (rt.winfo_screenwidth() -
                                         300) / 2, (rt.winfo_screenheight() - 300) / 2)
    rt.geometry(tmpcnf)
    app.mainloop()
