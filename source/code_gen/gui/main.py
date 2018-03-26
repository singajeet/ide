import wx
import wx.aui
from code_gen.gui.editor import MainFrame

def start_it():
    app = wx.App()
    MainFrame(None)
    app.MainLoop()

