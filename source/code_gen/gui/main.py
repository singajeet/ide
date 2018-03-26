import wx
import wx.aui
from .editor import MainFrame

def start_it():
    app = wx.App()
    MainFrame(None)
    app.MainLoop()

