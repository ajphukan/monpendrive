import ctypes
from ctypes import wintypes

user32 = ctypes.WinDLL("user32")

TOGGLE_UNHIDEWINDOW = 0x40
TOGGLE_HIDEWINDOW   = 0x80

user32.FindWindowW.restype = wintypes.HWND
user32.FindWindowW.argtypes = (
    wintypes.LPCWSTR, # lpClassName
    wintypes.LPCWSTR) # lpWindowName

user32.SetWindowPos.restype = wintypes.BOOL
user32.SetWindowPos.argtypes = (
    wintypes.HWND, # hWnd
    wintypes.HWND, # hWndInsertAfter
    ctypes.c_int,  # X
    ctypes.c_int,  # Y
    ctypes.c_int,  # cx
    ctypes.c_int,  # cy
    ctypes.c_uint) # uFlags

user32.FindWindowExW.restype = wintypes.HWND
user32.FindWindowExW.argtypes = (
   wintypes.HWND,    # hwndParent
   wintypes.HWND,    # hwndChildAfter
   wintypes.LPCWSTR, # lpszClass
   wintypes.LPCWSTR) # lpszWindow

start_atom = wintypes.LPCWSTR(0xC017) # i.e. MAKEINTATOM(...)

def hide_taskbar():
    handleW1 = user32.FindWindowW(u"Shell_traywnd", u"")
    user32.SetWindowPos(handleW1, 0, 0, 0, 0, 0, TOGGLE_HIDEWINDOW)
    hStart = user32.FindWindowExW(None, None, start_atom, None)
    user32.SetWindowPos(hStart, 0, 0, 0, 0, 0, TOGGLE_HIDEWINDOW)

def unhide_taskbar():
    handleW1 = user32.FindWindowW(u"Shell_traywnd", u"")
    user32.SetWindowPos(handleW1, 0, 0, 0, 0, 0, TOGGLE_UNHIDEWINDOW)
    hStart = user32.FindWindowExW(None, None, start_atom, None)
    user32.ShowWindow(hStart, 3)
