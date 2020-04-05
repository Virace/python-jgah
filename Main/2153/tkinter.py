# -*- coding: utf-8 -*-
# @Time    : 2020-04-03
# @Author  : Virace

# Tk窗口 StringVar字符串变量 Label标签 Entry输入框 Button按钮 messagebox信息框
from tkinter import Tk, StringVar, Label, Entry, Button, messagebox

# 默认用户名密码
DEFAULT_USERNAME = 'root'
DEFAULT_PASSWORD = 'root'

# 创建根窗口, 指的就是主窗口. 之后的一切组件全在root上展现
root = Tk()
# 设置窗口标题
root.title('第一个GUI程序.')

# 设置窗口大小长x宽, 单位像素. 通常tk组件都有geometry方法
# 最后显示出的长宽是受系统缩放影响的.
root.geometry('350x200')

# 创建两个变量来存放用户名和密码
username = StringVar()
password = StringVar()

# 创建两个标签用来提示, place为设置组件在窗口中的坐标位置
Label(root, text='用户名:').place(x=20, y=50)
Label(root, text='密码:').place(x=20, y=90)
# 创建两个输入框, 并将文本变量与其对接
Entry(root, textvariable=username).place(x=120, y=50)
# show就是输入框显示的样子, 一般密码设置为星号. 可以随意设置符号
Entry(root, textvariable=password, show='✿').place(x=120, y=90)


def event_login():
    """
    登录按钮事件
    :return:
    """
    global username
    global password
    # 去除空格, 并且全部小写
    str_username = username.get().strip().lower()
    # 密码也去除空格, 除非允许密码带空格
    str_password = password.get().strip()
    if str_username == '' or str_password == '':
        messagebox.showwarning('输入错误', '用户名密码不能为空')
    elif str_username == DEFAULT_USERNAME and str_password == DEFAULT_PASSWORD:
        messagebox.showinfo('成功', '登录成功')
        # 登录成功后做别的东西
    else:
        messagebox.showwarning('错误', '用户名或密码错误')


# 登录按钮， 并绑定event_login函数. 按下按钮即触发
Button(root, text='Login', command=event_login).place(x=150, y=130)

# 窗口循环
root.mainloop()
