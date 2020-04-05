# -*- coding: utf-8 -*-
# @Time    : 2020-04-03
# @Author  : Virace

import PySimpleGUI as sg

# 默认用户名密码
DEFAULT_USERNAME = 'root'
DEFAULT_PASSWORD = 'root'

sg.theme('LightGrey4')  # 没错设置主题

# 创建布局， 多维数组. 将窗口组件按行排列, 想要如何显示全靠你的数组"长啥样"
layout = [[sg.Text('用户名:', size=(6, 1)), sg.InputText()],
          [sg.Text('密码:', size=(6, 1)), sg.InputText(password_char='❀')],
          [sg.Button('登录')]]

# 创建窗口
window = sg.Window('第二个GUI程序.', layout)

# 窗口事件循环
while True:
    event, values = window.read()  # 读取事件和值
    if event == '登录':
        # 去除空格, 并且全部小写
        str_username = values[0].strip().lower()
        # 密码也去除空格, 除非允许密码带空格
        str_password = values[1].strip()
        if str_username == '' or str_password == '':
            sg.Popup('输入错误', '用户名密码不能为空')
        elif str_username == DEFAULT_USERNAME and str_password == DEFAULT_PASSWORD:
            sg.Popup('成功', '登录成功')
            # 登录成功后做别的东西
        else:
            sg.Popup('错误', '用户名或密码错误')
    elif event is None:
        break

window.close()
