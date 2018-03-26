"""
.. module:: main
   :platform: Any
   :synopsis: main entry point for the app
.. moduleauthor:: Ajeet Singh
"""
from UMLToCodeApp.cmd_manager import interactive

if __name__ == '__main__':
    cmd = interactive.CmdManager()
    cmd.start()
