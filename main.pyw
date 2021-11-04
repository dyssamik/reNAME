from tkinter import Frame, StringVar, Label, Button, Entry, END, messagebox, Tk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askyesno
from os import listdir, rename
from os.path import isfile, join, splitext

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.sv_pre = StringVar()
        self.sv_post = StringVar()
        self.pack()
        self.create_widgets()
        self.pack_widgets()

    def create_widgets(self):
        self.welcome_lbl = Label(self, text="Renaming multiple files is easy! Just follow the steps:", font="Arial 16")
        self.dir_lbl = Label(self, text="1. Choose a directory where the files are located.", font="Arial 12")
        self.dir_btn = Button(self, text="Choose folder...", command=self.open_dir_dlg, font="Arial 12")
        self.dir_res = Label(self, text="(Full path will be shown here)", font="Arial 12")
        self.name_lbl = Label(self, text="2. Enter what will be in the name before and after number.", font="Arial 12")
        self.prefix_lbl = Label(self, text="Prefix", font="Arial 12")
        self.prefix_txt = Entry(self, font="Arial 12", textvariable=self.sv_pre, validate="focusout", validatecommand=self.callback)
        self.number_lbl = Label(self, text="Middle part (unchangeable)", font="Arial 12")
        self.add_lbl_1 = Label(self, text="+", font="Arial 12")
        self.number_txt = Entry(self, font="Arial 12")
        self.number_txt.insert(END, "1, 2, 3...")
        self.number_txt.configure(state="disabled")
        self.postfix_lbl = Label(self, text="Postfix", font="Arial 12")
        self.add_lbl_2 = Label(self, text="+", font="Arial 12")
        self.postfix_txt = Entry(self, font="Arial 12", textvariable=self.sv_post, validate="focusout", validatecommand=self.callback)
        self.name_res = Label(self, text="(Name will be shown here)", font="Arial 12")
        self.rename_lbl = Label(self, text="3. Press this button.", font="Arial 12")
        self.rename_btn = Button(self, text="reNAME!", command=self.rename_files, font="Arial 12")

    def pack_widgets(self):
        self.welcome_lbl.grid(row=0, column=0, columnspan=5, pady=15)
        self.dir_lbl.grid(row=1, column=0, columnspan=5, pady=0)
        self.dir_btn.grid(row=2, column=0, columnspan=5, pady=10)
        self.dir_res.grid(row=3, column=0, columnspan=5, pady=(0, 15))
        self.name_lbl.grid(row=4, column=0, columnspan=5, pady=5)
        self.prefix_lbl.grid(row=5, column=0, padx=(15, 5), pady=0)
        self.number_lbl.grid(row=5, column=2, pady=0)
        self.postfix_lbl.grid(row=5, column=4, padx=(5, 15), pady=0)
        self.prefix_txt.grid(row=6, column=0, padx=(15, 5), pady=10)
        self.add_lbl_1.grid(row=6, column=1, pady=10)
        self.number_txt.grid(row=6, column=2, pady=10)
        self.add_lbl_2.grid(row=6, column=3, pady=10)
        self.postfix_txt.grid(row=6, column=4, padx=(5, 15), pady=10)
        self.name_res.grid(row=7, column=0, columnspan=5)
        self.rename_lbl.grid(row=8, column=0, columnspan=5, pady=(15, 0))
        self.rename_btn.grid(row=9, column=0, columnspan=5, pady=(5, 20))

    def open_dir_dlg(self):
        self.folder_selected = askdirectory()
        if len(self.folder_selected) > 0:
            self.dir_res.configure(text=self.folder_selected)

    def callback(self):
        if (self.sv_pre.get() != "") and (self.sv_post.get() != ""):
            self.res = self.sv_pre.get() + "_number_" + self.sv_post.get() + ".ext"
        elif (self.sv_pre.get() == "") and (self.sv_post.get() != ""):
            self.res = "number_" + self.sv_post.get() + ".ext"
        elif (self.sv_pre.get() != "") and (self.sv_post.get() == ""):
            self.res = self.sv_pre.get() + "_number.ext"
        else:
            self.res = "number.ext"
        self.name_res.configure(text=self.res)
        return True

    def rename_files(self):
        answer = askyesno("Confirmation", "WARNING! All files will be renamed. Do you wish to proceed?")
        
        if answer:
            try:
                path = self.folder_selected
                if len(path) > 0:
                    files = [f for f in listdir(path) if isfile(join(path, f))]

                    for index, file in enumerate(files):
                        filename, file_ext = splitext(file)
                        src = join(path, file)
                        dst = join(path, self.sv_pre.get() + str(index + 1) + self.sv_post.get() + file_ext)

                        rename(src, dst)
                else:
                    messagebox.showerror("Error", "No folder selected")
            except AttributeError:
                messagebox.showerror("Error", "No folder selected")

def main():
    root = Tk()
    root.title("reNAME")
    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()
