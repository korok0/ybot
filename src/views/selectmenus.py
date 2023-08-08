import discord
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\.."))
print(f"PR Buttons: {project_root}")
sys.path.append(project_root)

from src.utils.utility import Utility

class SteamSelectMenu():
    # this is a steam menu
    pass