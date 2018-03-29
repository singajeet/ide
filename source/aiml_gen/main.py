"""
.. module:: main
   :platform: Any
   :synopsis: Utility to generate AIML files
.. moduleauthor:: ajeet singh
"""
from prompt_toolkit.shortcuts import prompt

def start():
    """Start the while loop for prompt
    """
    text = None
    while text not in ['quit', 'exit']:
        text = prompt('provide pattern')
