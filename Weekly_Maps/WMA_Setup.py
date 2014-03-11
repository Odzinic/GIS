import Tkinter, tkFileDialog
import os
from shutil import copyfile

root = Tkinter.Tk()

curr_dir = os.getcwd()
main_dir = tkFileDialog.askdirectory(parent=root, initialdir="/",
                                    title='Please select a directory')

os.makedirs(os.path.join(main_dir, "Input_Image"))
os.makedirs(os.path.join(main_dir, "Input_Template"))
os.makedirs(os.path.join(main_dir, "Input_Vectors"))

copyfile(os.path.join(curr_dir, "Maps.py"), os.path.join(main_dir, "Maps.py"))

