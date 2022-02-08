import tkinter as tk
from tkinter import StringVar
import csv
from tkinter import simpledialog, messagebox

# GUI for the program
class gui:

    # Initialize
    def __init__(self):
        self.wn = tk.Tk()
        self.wn.geometry("720x480")

        self.cityList = list()
        self.readCounties("MontanaCounties.csv")

        self.lblSearch = tk.Label(self.wn, text="Search by City. Leave box empty for all counties")
        self.lblSearch.grid(row=1, column=1, columnspan=2)

        self.searchVar = StringVar()
        txtBoxSearch = tk.Entry(self.wn, textvariable=self.searchVar)
        txtBoxSearch.grid(row=2, column=1, padx=5, pady=5)

        btnSearch = tk.Button(self.wn, text="Search", width=10)
        btnSearch.grid(row=2, column=2, sticky=tk.W, pady=5, padx=5)
        btnSearch.config(command=self.search)

        self.txtList = tk.Listbox(self.wn, width=30, height=20)
        self.txtList.grid(row=3, column=1, pady=5, padx=5, columnspan=2)

        btnExit = tk.Button(self.wn, text="Save and exit", width=10)
        btnExit.grid(row=4, column=1, columnspan=2)
        btnExit.config(command=self.exit)

        self.btnAddNew = tk.Button(self.wn, text="Add New", width=10)
        self.btnAddNew.config(command=self.btnAddNewFunction)

    def exit(self):
        with open('MontanaCounties.csv', 'w', newline="\n") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["County", "City", "License Plate Prefix"])
            for row in self.cityList:
                writer.writerow(row)
        self.wn.destroy()

    # Start the GUI
    def start(self):
        self.wn.mainloop()

    # Read the csv into a dictionary
    def readCounties(self, filename):
        with open(filename) as csvFile:
            reader = csv.reader(csvFile)
            index = 1
            for row in reader:
                self.cityList.append([row[0], row[1], row[2]])

    # Search for a license prefix
    def search(self, event=None):
        self.lblSearch.config(text="Search by City. Leave box empty for all counties")

        self.txtList.delete(0, tk.END)
        if self.searchVar.get() == '':
            index = 0
            foundFlag = True
            for row in self.cityList:
                self.txtList.insert(index, row[1] + ", " + row[0] + ", " + row[2])
        else:
            index = 0
            foundFlag = False
            for row in self.cityList:
                if row[1].lower() == self.searchVar.get().lower():
                    foundFlag = True
                    self.txtList.insert(index, row[1] + ", " + row[0] + ", " + row[2])
        if not foundFlag:
            self.lblSearch.config(text="City not found. Would you like to add it to the list?")
            self.btnAddNew.grid(row=1, column=3)

    def btnAddNewFunction(self):
        usrInput = simpledialog.askstring(title="Add new city", prompt="Enter county name or license prefix: ")
        if usrInput is not None:
            usrInputLwr = usrInput.lower()
            found = False
            for row in self.cityList:
                if usrInputLwr == row[0].lower() or usrInput == row[2]:
                    found = True
                    self.cityList.append([row[0], self.searchVar.get(), row[2]])
                    break
            if not found:
                messagebox.showinfo(title="Info", message="County or prefix not found.")
                self.searchVar.set("")
                self.search()
            else:
                self.search()
        self.btnAddNew.grid_forget()

if __name__ == "__main__":
    gui = gui()
    gui.start()
