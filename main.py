import tkinter as tk
from gui import BoardGUI

def main():
    root = tk.Tk()
    root.title('Tic Tac Toe')
    BoardGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()