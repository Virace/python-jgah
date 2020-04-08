# -*- coding: utf-8 -*-
# @Time    : 2020-04-05
# @Author  : Virace

from cefpython3 import cefpython as cef

import math
import os
import sys

import win32api
import win32con
import win32gui

DEFAUTL_URL = 'https://api.virace.cc/jgah/cef/'
DEFAULT_USERNAME = 'root'
DEFAULT_PASSWORD = 'root'
DEFAULT_WINDOW_TITLE = '处女座之最 - 演示程序'

# Globals
WindowUtils = cef.WindowUtils()
# 全局窗口句柄
g_windows_handle = None
# 多线程
g_multi_threaded = False


class BindFunction:
    @staticmethod
    def get_title(callback):
        callback.Call(DEFAULT_WINDOW_TITLE)

    @staticmethod
    def login(data, callback):
        if 'username' not in data or 'password' not in data:
            callback.Call(False, '提交格式不正确')
        elif data['username'] == '' or data['password'] == '':
            callback.Call(False, '用户名密码不能为空')
        elif data['username'] == DEFAULT_USERNAME and data['password'] == DEFAULT_PASSWORD:
            callback.Call(True)
        else:
            callback.Call(False, '用户名或密码错误.')

    @staticmethod
    def min():
        win32gui.PostMessage(g_windows_handle, win32con.WM_SYSCOMMAND, win32con.SC_MINIMIZE)

    @staticmethod
    def max():
        # 判断窗口状态
        if win32gui.GetWindowPlacement(g_windows_handle)[1] == win32con.SW_SHOWMAXIMIZED:
            win32gui.PostMessage(g_windows_handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE)
        else:
            win32gui.PostMessage(g_windows_handle, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE)

    @staticmethod
    def close():
        win32gui.PostMessage(g_windows_handle, win32con.WM_CLOSE)

    @staticmethod
    def move():
        # 捕获鼠标
        win32gui.ReleaseCapture()
        # 移动
        win32gui.SendMessage(g_windows_handle, win32con.WM_SYSCOMMAND, win32con.SC_MOVE + win32con.HTCAPTION, 0)
        pass


def main():
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error

    settings = {
        "multi_threaded_message_loop": g_multi_threaded,
    }
    cef.Initialize(settings=settings)

    window_proc = {
        win32con.WM_CLOSE: close_window,
        win32con.WM_DESTROY: exit_app,
        win32con.WM_SIZE: WindowUtils.OnSize,
        win32con.WM_SETFOCUS: WindowUtils.OnSetFocus,
        win32con.WM_ERASEBKGND: WindowUtils.OnEraseBackground
    }
    global g_windows_handle
    g_windows_handle = create_window(title=DEFAULT_WINDOW_TITLE,
                                     class_name=DEFAULT_WINDOW_TITLE,
                                     width=1100,
                                     height=730,
                                     window_proc=window_proc,
                                     icon="resources/chromium.ico")

    window_info = cef.WindowInfo()
    window_info.SetAsChild(g_windows_handle)

    if g_multi_threaded:
        # When using multi-threaded message loop, CEF's UI thread
        # is no more application's main thread. In such case browser
        # must be created using cef.PostTask function and CEF message
        # loop must not be run explicitilly.
        cef.PostTask(cef.TID_UI,
                     create_browser,
                     window_info,
                     {},
                     DEFAUTL_URL)
        win32gui.PumpMessages()

    else:
        create_browser(window_info=window_info,
                       settings={},
                       url=DEFAUTL_URL)
        cef.MessageLoop()

    cef.Shutdown()


def create_browser(window_info, settings, url):
    assert (cef.IsThread(cef.TID_UI))
    bind_js(cef.CreateBrowserSync(window_info=window_info,
                                  settings=settings,
                                  url=url))


def bind_js(browser):
    """
    绑定js事件, 也可以用LoadHandler调用
    :param browser:
    :return:
    """
    bindings = cef.JavascriptBindings()
    bindings.SetFunction("py_title", BindFunction.get_title)
    bindings.SetFunction("py_login", BindFunction.login)
    bindings.SetFunction("py_move", BindFunction.move)
    bindings.SetFunction("py_windows_min", BindFunction.min)
    bindings.SetFunction("py_windows_max", BindFunction.max)
    bindings.SetFunction("py_windows_close", BindFunction.close)
    browser.SetJavascriptBindings(bindings)


def create_window(title, class_name, width, height, window_proc, icon):
    # Register window class
    wndclass = win32gui.WNDCLASS()
    wndclass.hInstance = win32api.GetModuleHandle(None)
    wndclass.lpszClassName = class_name
    wndclass.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
    wndclass.hbrBackground = win32con.COLOR_WINDOW
    wndclass.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wndclass.lpfnWndProc = window_proc
    atom_class = win32gui.RegisterClass(wndclass)
    assert (atom_class != 0)

    # Center window on screen.
    screenx = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screeny = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    xpos = int(math.floor((screenx - width) / 2))
    ypos = int(math.floor((screeny - height) / 2))
    if xpos < 0:
        xpos = 0
    if ypos < 0:
        ypos = 0

    # Create window
    window_style = (win32con.WS_POPUP | win32con.WS_CLIPCHILDREN
                    | win32con.WS_VISIBLE)
    window_handle = win32gui.CreateWindow(class_name, title, window_style,
                                          xpos, ypos, width, height,
                                          0, 0, wndclass.hInstance, None)
    assert (window_handle != 0)

    # Window icon
    icon = os.path.abspath(icon)
    if not os.path.isfile(icon):
        icon = None
    if icon:
        # Load small and big icon.
        # WNDCLASSEX (along with hIconSm) is not supported by pywin32,
        # we need to use WM_SETICON message after window creation.
        # Ref:
        # 1. http://stackoverflow.com/questions/2234988
        # 2. http://blog.barthe.ph/2009/07/17/wmseticon/
        bigx = win32api.GetSystemMetrics(win32con.SM_CXICON)
        bigy = win32api.GetSystemMetrics(win32con.SM_CYICON)
        big_icon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON,
                                      bigx, bigy,
                                      win32con.LR_LOADFROMFILE)
        smallx = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        smally = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        small_icon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON,
                                        smallx, smally,
                                        win32con.LR_LOADFROMFILE)
        win32api.SendMessage(window_handle, win32con.WM_SETICON,
                             win32con.ICON_BIG, big_icon)
        win32api.SendMessage(window_handle, win32con.WM_SETICON,
                             win32con.ICON_SMALL, small_icon)

    return window_handle


def close_window(window_handle, message, wparam, lparam):
    browser = cef.GetBrowserByWindowHandle(window_handle)
    browser.CloseBrowser(True)
    # OFF: win32gui.DestroyWindow(window_handle)
    return win32gui.DefWindowProc(window_handle, message, wparam, lparam)


def exit_app(*_):
    win32gui.PostQuitMessage(0)
    return 0


if __name__ == '__main__':
    main()
