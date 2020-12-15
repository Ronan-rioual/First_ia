import tkinter.messagebox
from functools import partial
import tkinter as tk
from functions import *
from tkinter import filedialog 
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import ttk

class Application(tk.Tk):

    def __init__(self):
        
        tk.Tk.__init__(self)
        self.geometry("1524x720")
        self.create_widget()
        self.v=tk.IntVar()
        self.mainFunc()
        


    def create_widget(self):

        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)


        self.menu1 = tk.Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Fichier",menu=self.menu1)


        """Titre"""
        self.champ_titre=tk.Label(self,text="Data Visualisation",padx="10",pady="10")
        self.champ_titre.config(font=("Courier", 44))
        self.champ_titre.pack(side="top")
        
        self.main=tk.Frame(self)
        self.main.pack()


    def browseFiles(self): 
        global filename
        filename = filedialog.askopenfilename(initialdir = "/", 
                                            title = "Select a File", 
                                            filetypes = (("CSV files", 
                                                            "*.csv*"), 
                                                        ("all files", 
                                                            "*.*"))) 
        self.openedFileLabel.configure(text=filename.split("/")[-1])
        self.runImportFrame()


    def mainFunc(self):    
        
        for widget in self.main.winfo_children():
            widget.forget()

        tk.Button(self.main,text="Selectionner un fichier",command=self.browseFiles,padx=10).grid(row=0,column=0)
        self.openedFileLabel=tk.Label(self.main,padx=10)
        self.openedFileLabel.grid(row=0,column=1)

    def runImportFrame(self):
        tk.Label(self.main,text="Choisissez un séparateur :",padx=10,pady=10).grid(row=1,column=0)
        self.sepVar=tk.StringVar()
        self.separatorEntry=tk.Entry(self.main,textvariable=self.sepVar)
        self.separatorEntry.grid(row=1,column=1)

        tk.Button(self.main,text="Lancer l'importation",padx=10,command=self.runImport).grid(row=1,column=3)
        
        

    def runImport(self):
        try:
            sep=self.sepVar.get()
            sep=str(sep)
            self.dataFrame=getDataSet(filename,sep)
            self.displayOperationWindow()
            
        except:
            msg="Veuillez saisir un separateur valide"
            tkinter.messagebox.showinfo( "Erreur", msg)

    def displayDataFrame(self):

        self.newWindow = tk.Toplevel(self) 
        self.newWindow.title("New Window") 
        self.newWindow.geometry("1024x620") 
        pd.set_option('display.max_rows', None)
        self.text = tk.Text(self.newWindow)
        self.text.insert(tk.END, str(self.dataFrame))
        self.text.pack(fill = "both",expand = True)

    def displayColumnList(self):

        self.newWindow = tk.Toplevel(self) 
        self.newWindow.title("New Window") 
        self.newWindow.geometry("1024x620") 
        pd.set_option('display.max_rows', None)
        self.text = tk.Text(self.newWindow)
        self.text.insert(tk.END, str(self.dataFrame.columns))
        self.text.pack(fill = "both",expand = True)

    def encodeColumns(self):

        self.newWindow = tk.Toplevel(self) 
        self.newWindow.title("New Window") 
        self.newWindow.geometry("1024x620") 
        tk.Label(self.newWindow,text="Choisissez les colonnes a encoder").pack()
        self.listbox=tk.Listbox(self.newWindow,selectmode="multiple")
        for i in range(len(self.dataFrame.columns.values)):
            self.listbox.insert(i+1,self.dataFrame.columns.values[i])

        self.listbox.pack()
        tk.Button(self.newWindow,text="Lancer l'encodage",command=self.runEncoding).pack()

    def runEncoding(self):
        try:
            self.dataFrame=encodeColumns(self.dataFrame,[self.listbox.get(i) for i in self.listbox.curselection()])
            self.newWindow.destroy()
            self.displayDataFrame()
        except:
            msg="Veuillez saisir des colonnes valide"
            tkinter.messagebox.showinfo( "Erreur", msg)
      
    def scaleColumns(self):

        self.newWindow = tk.Toplevel(self) 
        self.newWindow.title("New Window") 
        self.newWindow.geometry("1024x620") 
        tk.Label(self.newWindow,text="Choisissez les colonnes a scaler").pack()
        self.listbox=tk.Listbox(self.newWindow,selectmode="multiple")
        for i in range(len(self.dataFrame.columns.values)):
            self.listbox.insert(i+1,self.dataFrame.columns.values[i])

        self.listbox.pack()
        tk.Button(self.newWindow,text="Lancer le scaling",command=self.runScaling).pack()

    def runScaling(self):
        try:
            self.dataFrame=scaleFeatures(self.dataFrame,[self.listbox.get(i) for i in self.listbox.curselection()])
            self.newWindow.destroy()
            self.displayDataFrame()
        except:
            msg="Veuillez saisir des colonnes valide"
            tkinter.messagebox.showinfo( "Erreur", msg)

    def runNanSearch(self):
        try:
            self.dataFrame=transformNan(self.dataFrame)
            
            self.displayDataFrame()
        except:
            msg="Veuillez saisir des colonnes valide"
            tkinter.messagebox.showinfo( "Erreur", msg)

    def plotFrame(self):
        self.newWindow = tk.Toplevel(self) 
        self.newWindow.title("New Window") 
         
        tk.Label(self.newWindow,text="Choisissez X").grid(row=0,column=0)
        tk.Label(self.newWindow,text="Choisissez Y").grid(row=0,column=1)
        self.listboxX=ttk.Combobox(self.newWindow,value=self.dataFrame.columns.values)
        self.listboxY=ttk.Combobox(self.newWindow,value=self.dataFrame.columns.values)

      
        self.listboxX.grid(row=1,column=0)
        self.listboxY.grid(row=1,column=1)
        tk.Button(self.newWindow,text="Lancer le tracé de graphique",command=self.runPloting).grid(row=2,column=1)

    def runPloting(self):
        try:
            x=self.listboxX.get().replace("'","")
            y=self.listboxY.get().replace("'","")
            plt.plot(self.dataFrame[x],self.dataFrame[y],"ro")
        
            plt.show()
        
            
        except:
            msg="Veuillez saisir des colonnes valide"
            tkinter.messagebox.showinfo( "Erreur", msg)

    def regression(self):
        self.newWindow = tk.Toplevel(self) 
        self.newWindow.title("New Window") 
        
        tk.Label(self.newWindow,text="Choisissez target").grid(row=0,column=0)
        tk.Label(self.newWindow,text="Choisissez features").grid(row=0,column=1)
        self.listboxX=tk.Listbox(self.newWindow,selectmode="multiple")
        for i in range(len(self.dataFrame.columns.values)):
            self.listboxX.insert(i+1,self.dataFrame.columns.values[i])
        self.listboxY=ttk.Combobox(self.newWindow,value=self.dataFrame.columns.values)

        self.listboxX.grid(row=1,column=1)
        self.listboxY.grid(row=1,column=0)
        
        tk.Button(self.newWindow,text="Creer les train & test sets",command=self.testSets).grid(row=2,column=1)


    def testSets(self):
        self.listeColumns=[self.listboxX.get(i) for i in self.listboxX.curselection()]
        self.X=self.dataFrame.loc[:,self.listeColumns].values
        y=self.listboxY.get().replace("'","").replace("]","")
        self.Y=self.dataFrame.loc[:,y].values

        self.x_test, self.x_app, self.y_test, self.y_app =createTestAndTrainSet(self.X,self.Y)
        tk.Button(self.newWindow,text="Regression linéaire ",command=self.linearReg).grid(row=3,column=1)
        tk.Button(self.newWindow,text="Regression polynomiale",command=self.polyReg).grid(row=4,column=1)

    def linearReg(self):
        self.newWindow = tk.Toplevel(self) 
        self.newWindow.title("New Window") 
        model = linear_model.LinearRegression()
        model.fit(self.x_app,self.y_app)

        tk.Label(self.newWindow,text="Choisir le pas (0=Defaut) :").grid(row=0,column=0)
        self.pasEntryVar=tk.IntVar()
        tk.Entry(self.newWindow,textvariable=self.pasEntryVar).grid(row=0,column=1)
        
        tk.Label(self.newWindow,text="Choisir le nombre d'iteration (0=Defaut) :").grid(row=1,column=0)
        self.iterationEntryVar=tk.IntVar()
        tk.Entry(self.newWindow,textvariable=self.iterationEntryVar).grid(row=1,column=1)

        tk.Button(self.newWindow,command=self.runLinearReg,text="Lancer la regression lineaire").grid(row=2,column=1)

    def runLinearReg(self):
        model = linear_model.LinearRegression()

        try:
            if int(self.pasEntryVar.get())!=0:
                model.set_params(tol=int(self.pasEntryVar.get()))
            if int(self.iterationEntryVar.get())!=0:
                model.set_params(max_iter=int(self.pasEntryVar.get()))
        except:
            print("erreur")

        model.fit(self.x_app,self.y_app)
        plt.plot(self.X,self.Y,"ro")
        plt.plot(self.x_test,model.predict(self.x_test))
        plt.show()

    def polyReg(self):
        self.newWindow = tk.Toplevel(self) 
        self.newWindow.title("New Window") 
        tk.Label(self.newWindow,text="Choisir le pas (0=Defaut) :").grid(row=0,column=0)
        self.pasEntryVar=tk.IntVar()
        tk.Entry(self.newWindow,textvariable=self.pasEntryVar).grid(row=0,column=1)
        
        tk.Label(self.newWindow,text="Choisir le nombre d'iteration (0=Defaut) :").grid(row=1,column=0)
        self.iterationEntryVar=tk.IntVar()
        tk.Entry(self.newWindow,textvariable=self.iterationEntryVar).grid(row=1,column=1)
        tk.Label(self.newWindow,text="Choisir le degre (obligatoire) :").grid(row=3,column=0)
        self.degreEntryVar=tk.IntVar()
        tk.Entry(self.newWindow,textvariable=self.degreEntryVar).grid(row=3,column=1)

        tk.Button(self.newWindow,command=self.runPolyReg,text="Lancer la regression lineaire").grid(row=4,column=1)

    def runPolyReg(self):
        model = linear_model.LinearRegression()

        try:
            if int(self.pasEntryVar.get())!=0:
                model.set_params(alpha=int(self.pasEntryVar.get()))
            if int(self.iterationEntryVar.get())!=0:
                model.set_params(max_iter=int(self.pasEntryVar.get()))
            poly = PolynomialFeatures(int(self.degreEntryVar.get()))
            Xpoly=poly.fit_transform(self.x_app)
        except:
            print("erreur")

        model.fit(Xpoly,self.y_app)
        plt.plot(self.x_app,self.y_app,"ro")

        plt.scatter(self.x_app,model.predict(Xpoly))
        print(self.x_app)
        print("y=")
        print(model.predict(Xpoly))
        plt.show()

    def displayOperationWindow(self):
        self.mainFunc()
        
        self.operationFrame=tk.Frame(self)
        self.operationFrame.pack()
        tk.Button(self.operationFrame,text="Afficher le dataframe",padx=10,width=30,command=self.displayDataFrame).grid(row=0,column=0)
        tk.Button(self.operationFrame,text="Afficher la liste des colonnes",width=30,padx=10,command=self.displayColumnList).grid(row=0,column=1)
        tk.Button(self.operationFrame,text="Encoder les colonnes",padx=10,width=30,command=self.encodeColumns).grid(row=0,column=2)
        tk.Button(self.operationFrame,text="Supprimer les valeurs manquantes",padx=10,width=30,command=self.runNanSearch).grid(row=0,column=3)
        tk.Button(self.operationFrame,text="Scale Features",padx=10,width=30,command=self.scaleColumns).grid(row=0,column=4)
        tk.Button(self.operationFrame,text="Graphiques",padx=10,width=30,command=self.plotFrame).grid(row=1,column=0)
        tk.Button(self.operationFrame,text="Regression",padx=10,width=30,command=self.regression).grid(row=2,column=2)
        


app=Application()
app.mainloop()
        

