#coding utf-8

"""
Created on Mon Mar 27 13:55:00 2021
Updated on Sun Mar 27

@author: 2020-0572
"""

# librairies importation
import tkinter as TK
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk, messagebox
import tkinter.filedialog as TKFD
from PIL import Image
import os
 
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# je ne sais pas si les librairies sur windows sont directement installés (sur mac, elles le sont) 
import datetime as dt
import pandas as pd
import numpy as np
        
    
#classes importation
from classes import *



class Interface():
    def __init__(self):
        #Dictionnaires des éléments du laboratoire
        self.Laboratory = {'Laboratory': None, 'Universities' : [], 'Research Teams' : [], 'Internals' : [], 'Externals' : [], 'Research Projects' : [], 'PhD' : [], 'Magazines' : [], 'Journals articles' : [], 'Conferences articles' : [], 'Reports' :[]}

        # Réalisation de l'interface utilisateur/Configuration
        self.main = TK.Tk()
        self.main.title("Research lab app - Database") #nom de la fenêtre
        self.main.geometry("920x600")
        self.main.minsize(920, 600)
        self.main.maxsize(1280,800)
        #self.main.iconbitmap("C:\Users\Hoover48\Downloads\PROJET_MINI_POO_KANG\MINI_POO\AM.png") #logo à changer
        self.main.config(background = '#961364') 
        
        # MENU
        self.menubar = Menu(self.main)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.XMLLoading)
        filemenu.add_command(label="Save as...", command=self.XMLregistration)
        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.main.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="Show status", command=self.status)
        editmenu.add_command(label="Show population pyramide", command=self.population_pyramid)

        editmenu.add_separator()
        editmenu.add_command(label="Show articles rate", command = self.articles_collab_rate)
        editmenu.add_command(label="Show PhD rate", command = self.PhD_collab_rate)
        self.menubar.add_cascade(label="Options", menu=editmenu)

        self.main.config(menu=self.menubar)

        #BOX LABELS
        self.welcome = TK.Label(self.main, text = "Research Lab - Main menu", font = ("Courrier", 15), bg = '#FF8728', fg= '#961364' )
        self.welcome.grid(row=0,column=0, columnspan=15, sticky = "w e n s", padx=5, pady=5)
        




        '''NOTEBOOK : pour créer des onglets'''
        self.notebook = ttk.Notebook(self.main)
        self.notebook.grid(row=1, column=1, columnspan=14)
        







        
        ''' TAB #1'''
        self.tab0 = TK.Frame(self.notebook, bg ='#961364')
        self.tab0.pack(fill="both", expand=1)
        self.notebook.add(self.tab0, text = 'Organization')
        

        #IMAGE LOGO AM
        can = Canvas(self.tab0, width=430,height=100)
        img = TK.PhotoImage(file="C:\\Users\\Hoover48\\Documents\\VSCode\\Portfolio\\Projects\\OOP_IS_researchlab\\PROJET_MINI_POO_KANG\\MINI_POO\\AM.png")
        can.create_image(10,10,anchor=NW, image = img)
        can.grid(row = 16, column=14,columnspan=15)

        #C:\Users\Hoover48\Documents\VSCode\Portfolio\Projects\OOP_IS_researchlab\PROJET_MINI_POO_KANG\MINI_POO

        #DELETE BUTTONS    
        delete_button = TK.Button(self.tab0, text='Delete', bg = '#961364', command = self.delete_button)
        delete_button.grid(row=9,column= 1)
        deleteall_button = TK.Button(self.tab0, text='Delete all', bg = '#961364', command = self.delete_all)
        deleteall_button.grid(row=10,column= 1)


        TK.Label(self.tab0, text = "Research Teams", bg = '#961364', fg = 'white').grid(row=1, column=1)
        
        #RESEARCH TEAMS TREEVIEWS
        self.Listbox0 = ttk.Treeview(self.tab0)
        self.Listbox0.grid(row=2,column=1,rowspan=10, columnspan= 12)
        self.Listbox0['columns']=('Research teams name', 'Head')
        self.Listbox0.column('#0', width=0, stretch=NO)
        self.Listbox0.column('Research teams name', anchor=CENTER, width=170)
        self.Listbox0.column('Head', anchor=CENTER, width=180)
        self.Listbox0.heading('#0', text='', anchor=CENTER)
        self.Listbox0.heading('Research teams name', text='Research teams name', anchor=CENTER)
        self.Listbox0.heading('Head', text='Head', anchor=CENTER)
        self.Listbox0.bind('<Double-1>', self.show_members)

        #COMPANIES TREEWIVEW
        TK.Label(self.tab0, text = "Companies (partners)", bg = '#961364', fg = 'white').grid(row=13, column=1)
        self.Listbox0b = ttk.Treeview(self.tab0)
        self.Listbox0b.grid(row=14,column=1,rowspan=10, columnspan= 12)
        self.Listbox0b['columns']=('Companies name', 'Funding')
        self.Listbox0b.column('#0', width=0, stretch=NO)
        self.Listbox0b.column('Companies name', anchor=CENTER, width=250)
        self.Listbox0b.column('Funding', anchor=CENTER, width=100)
        self.Listbox0b.heading('#0', text='', anchor=CENTER)
        self.Listbox0b.heading('Companies name', text='Companies name', anchor=CENTER)
        self.Listbox0b.heading('Funding', text='Funding', anchor=CENTER)
        for col in self.Listbox0b['columns']: #SORT ELEMENT BY BUDGET
            self.Listbox0b.heading(col, text=col, command=lambda: \
                        self.treeview_sort_column(self.Listbox0b, col, False))

        #WELCOME TEXT
        TK.Label(self.tab0, text = "Welcome to the lab app ! \nHere is an organization table of the lab. \n You can navigate via the tabs above.\nEnjoy !", bg = '#961364', fg = 'white').grid(row=2, column=15, rowspan= 10, columnspan=10)

        #BLANK SPACE
        TK.Label(self.tab0, text = "    \n    ", bg = '#961364', fg = 'white').grid(row=10, column=13, sticky = 'W',padx = 5, pady = 5)
        
        



    
        '''TAB #2'''
        self.tab2 = TK.Frame(self.notebook, bg ='#961364')
        self.tab2.pack(fill="both", expand=1)
        self.notebook.add(self.tab2, text = 'Personnal')

        #CHOIX DU PERSONNEL : INT/EXT
        self.Cat2 = TK.StringVar(self.tab2)
        self.Cat2.set("All members") # default value
        TK.Label(self.tab2, text = "Category", bg = '#961364', fg = 'white').grid(row=2, column=10)
        self.w2 = TK.OptionMenu(self.tab2, self.Cat2, "All members", "Internals", "Externals")
        self.w2.grid(row=2,column=11)
        self.apply2 = TK.Button(self.tab2, text='Apply', command = self.apply_button)
        self.apply2.grid(row=2,column= 12)

        #LISTE DÉROULANTE / DROPDOWN LIST
        self.Cat3 = TK.StringVar(self.tab2)
        self.Cat3.set("Conception") # default value
        self.w3 = ttk.Combobox(self.tab2, textvariable = self.Cat3, width = 10)
        self.w3['values'] = ("Conception", "Fabrication", "Commande")
        self.w3['state'] = "readonly"
        self.w3.grid(row=15,column=6)
        self.Listbox2 = TK.Listbox(self.tab2, width = 30, height = 15)
        self.Listbox2.grid(row=3,column=10,rowspan=10, columnspan= 7)
        
        #SHOW MEMBERS DETAILS WITH DOUBLE CLICK
        self.Listbox2.bind('<Double-1>', self.display_details)

        #TITLE
        TK.Label(self.tab2, text = "Add member", bg = '#961364', fg = 'white').grid(row=2, column=7, sticky = 'W',padx = 5, pady = 5)

        #IMPLEMENTING VAR/ENTRY
        self.VarNameI = TK.StringVar()
        self.VarFirstNameI = TK.StringVar()
        self.VarGenderI = TK.IntVar()
        self.VarBDI = TK.StringVar()
        self.VarBPI = TK.StringVar()
        self.VarOffice = TK.StringVar()
        self.VarCompany = TK.StringVar()
        TK.Entry(self.tab2, textvariable = self.VarNameI).grid(row=3, column=7, columnspan=3)
        TK.Entry(self.tab2, textvariable = self.VarFirstNameI).grid(row=4, column=7, columnspan=3)
        TK.Entry(self.tab2, textvariable = self.VarBDI).grid(row=6, column=7,columnspan=3)
        TK.Entry(self.tab2, textvariable = self.VarBPI).grid(row=7, column=7,columnspan=3)
        TK.Entry(self.tab2, textvariable = self.VarOffice).grid(row=8, column=7,columnspan=3)
        TK.Entry(self.tab2, textvariable = self.VarCompany).grid(row=9, column=7,columnspan=3)
        TK.Label(self.tab2, text = "Name", bg = '#961364', fg = 'white').grid(row=3, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab2, text = "First Name",  bg = '#961364', fg = 'white').grid(row=4, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab2, text = "Gender",  bg = '#961364', fg = 'white').grid(row=5, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Radiobutton(self.tab2, text = 'Male', variable = self.VarGenderI, value=0, bg = '#961364', fg ="white").grid(row=5, column=7, sticky = 'W',padx = 5, pady = 5)
        TK.Radiobutton(self.tab2, text = 'Female', variable = self.VarGenderI, value=1,bg = '#961364', fg = "white").grid(row=5, column=8, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab2, text = "Birth Date", bg = '#961364', fg = 'white').grid(row=6, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab2, text = "Birth Place",  bg = '#961364', fg = 'white').grid(row=7, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab2, text = "Office (if internal)",  bg = '#961364', fg = 'white').grid(row=8, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab2, text = "Company (if external)",  bg = '#961364', fg = 'white').grid(row=9, column=6, sticky = 'W',padx = 5, pady = 5)
        
        #BUTTONS
        TK.Button(self.tab2, text = "Add member", command = self.add_personnal).grid(row=11,column=7)
        
        #SETTING RESEARCH TEAM RATE
        self.VarTA = TK.StringVar()
        TK.Label(self.tab2, text = "Set research team rate", bg = '#961364', fg = 'white').grid(row=14, column=6, columnspan=4, sticky = 'W',padx = 5, pady = 5)
        TK.Entry(self.tab2, textvariable = self.VarTA).grid(row=15, column=7,columnspan=3)
        TK.Button(self.tab2, text = "Set rate", command = self.set_TA).grid(row=15,column=10)

        #DISPLAY HISTORY (CARREER) BUTTON
        self.displayhistory = TK.Button(self.tab2, text='History', bg = '#961364', command = self.display_history)
        self.displayhistory.grid(row=6,column= 17)

        #PHD PUBLICATION AVG BUTTON - TRAITEMENT
        self.avg = TK.Button(self.tab2, text='#Publications during PhD', bg = '#961364', command = self.PhD_avg_pub)
        self.avg.grid(row=7,column=17)

        #DELETE BUTTON
        deleteP = TK.Button(self.tab2, text='Delete', bg = '#961364', command = self.delete_button)
        deleteP.grid(row=8,column= 17)

        #Bibliography (TRAITEMENT)
        TK.Label(self.tab2, text = "Personnal bibliography details", bg = '#961364', fg = 'white').grid(row=16, column=6, columnspan=4, sticky = 'W',padx = 5, pady = 5) #TITRE
        
        #choix de l'entité
        self.VarEntity = TK.StringVar() 
        self.VarEntity.set("Laboratory")
        self.Entity = ttk.Combobox(self.tab2, textvariable = self.VarEntity, width = 10)
        self.Entity["values"] = ("Laboratory", "Personnal", "Research Teams") #Affichier la bibliography du labo ? d'un personnel? d'un axe de recherche ?
        self.Entity.grid(row=17, column=10)
            
        
        TK.Label(self.tab2, text = "Start", bg = '#961364', fg = 'white').grid(row=17, column=6) #DATE DEBUT
        #année
        self.Catstartyear = TK.StringVar(self.tab2) 
        self.Catstartyear.set("Year") # default value
        self.startyear = ttk.Combobox(self.tab2, textvariable = self.Catstartyear,width = 4)
        self.startyear["values"] = ("2010" ,"2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021")
        self.startyear.grid(row=17, column =7)
        self.Catstartmonth = TK.StringVar(self.tab2)
        # mois
        self.Catstartmonth.set("Month") # default value
        self.startmonth = ttk.Combobox(self.tab2, textvariable = self.Catstartmonth, width = 5)
        self.startmonth["values"]=("1" ,"2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")
        self.startmonth.grid(row=17, column =8)
        self.Catstartday = TK.StringVar(self.tab2)
        #jour
        self.Catstartday.set("Day") # default value
        self.startday = ttk.Combobox(self.tab2, textvariable = self.Catstartday, width=3)
        self.startday["values"] = ("1" ,"2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30","31" )
        self.startday.grid(row=17,column=9)

        TK.Label(self.tab2, text = "End", bg = '#961364', fg = 'white').grid(row=18, column=6) #DATE FIN
        #année
        self.Catendyear = TK.StringVar(self.tab2) 
        self.Catendyear.set("Year") # default value
        self.endyear = ttk.Combobox(self.tab2, textvariable = self.Catendyear,width = 4)
        self.endyear["values"] = ("2010" ,"2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021")
        self.endyear.grid(row=18, column =7)
        #mois
        self.Catendmonth = TK.StringVar(self.tab2) 
        self.Catendmonth.set("Month") # default value
        self.endmonth = ttk.Combobox(self.tab2, textvariable = self.Catendmonth, width = 5)
        self.endmonth["values"] = ("1" ,"2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")
        self.endmonth.grid(row=18, column =8)
        #jour
        self.Catendday = TK.StringVar(self.tab2)
        self.Catendday.set("Day") # default value
        self.endday = ttk.Combobox(self.tab2, textvariable = self.Catendday, width=3)
        self.endday["values"] = ("1" ,"2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30","31" )
        self.endday.grid(row=18,column=9)
        

        #AFFIHCER LA BIBLIOGRAPHY ENTRE 2 DATES
        self.bibly = TK.Button(self.tab2, text='show bibliography', bg = '#961364', command = self.bibliography)
        self.bibly.grid(row=18,column=10)

        #PUBLICATION EN MOYENNE ENTRE 2 DATES
        self.avg = TK.Button(self.tab2, text='publication avg', bg = '#961364', command = self.publication_avg)
        self.avg.grid(row=19,column=10)





        '''TAB #2BIS'''
        self.tab1 = TK.Frame(self.notebook, bg ='#961364')
        self.tab1.pack(fill="both", expand=YES)
        self.notebook.add(self.tab1, text = 'Magazines')

        #TITLE
        TK.Label(self.tab1, text = "Add magazine", bg = '#961364', fg = 'white').grid(row=2, column=7, sticky = 'W',padx = 5, pady = 5)

        #TREEVIEW
        #titre-treeview
        TK.Label(self.tab1, text = "Existing magazines", bg = '#961364', fg = 'white').grid(row=2, column=11, columnspan=2)
        self.Listbox1 = ttk.Treeview(self.tab1)
        self.Listbox1.grid(row=3,column=11,rowspan=10, columnspan= 12)
        self.Listbox1['columns']=('Name', 'Short', 'Articles')
        self.Listbox1.column('#0', width=0, stretch=NO)
        self.Listbox1.column('Name', anchor=CENTER, width=300)
        self.Listbox1.column('Short', anchor=CENTER, width=100)
        self.Listbox1.column('Articles', anchor=CENTER, width=100)
        self.Listbox1.heading('#0', text='', anchor=CENTER)
        self.Listbox1.heading('Name', text='Name', anchor=CENTER)
        self.Listbox1.heading('Short', text='Short', anchor=CENTER)
        self.Listbox1.heading('Articles', text='Articles', anchor=CENTER)

        for col in self.Listbox1['columns']: #permet de trier les éléments par nb d'article
            self.Listbox1.heading(col, text=col, command=lambda: \
                        self.treeview_sort_column(self.Listbox1, col, False))

        

        #afficher les details de revues en double click
        self.Listbox1.bind('<Double-1>', self.display_mag)

        #IMPLEMENTING ENTRY/LABELS/VARIABLES
        self.VarNameM = TK.StringVar()
        self.VarShortM = TK.StringVar()
        self.VarYear = TK.StringVar()
        self.VarIFM = TK.StringVar()
        self.VarQuartileM = TK.StringVar()
        TK.Entry(self.tab1, textvariable = self.VarNameM).grid(row=3, column=7, columnspan=3)
        TK.Entry(self.tab1, textvariable = self.VarShortM).grid(row=4, column=7, columnspan=3)
        TK.Entry(self.tab1, textvariable = self.VarYear).grid(row=14, column=7,columnspan=3)
        TK.Entry(self.tab1, textvariable = self.VarIFM).grid(row=14, column=12,columnspan=3)
        TK.Entry(self.tab1, textvariable = self.VarQuartileM).grid(row=15, column=12,columnspan=3)
        TK.Label(self.tab1, text = "          \n       ", bg = '#961364', fg = 'white').grid(row=3, column=10, rowspan=10, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab1, text = "Name", bg = '#961364', fg = 'white').grid(row=3, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab1, text = "Short",  bg = '#961364', fg = 'white').grid(row=4, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab1, text = "Add information",  bg = '#961364', fg = 'white').grid(row=12, column=6, columnspan = 5, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab1, text = "Year",  bg = '#961364', fg = 'white').grid(row=14, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab1, text = "Impact Factor (IF)", bg = '#961364', fg = 'white').grid(row=14, column=11, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab1, text = "Quartile",  bg = '#961364', fg = 'white').grid(row=15, column=11, sticky = 'W',padx = 5, pady = 5)
        
        #ADD REVUES, INFORMATION BUTTONS
        TK.Button(self.tab1, text = "Add magazine", command = self.add_magazine).grid(row=5,column=7)
        TK.Button(self.tab1, text = "Add information", command = self.add_information).grid(row=16,column=7)

 





        '''TAB #3'''
        self.tab3 = TK.Frame(self.notebook, bg ='#961364')
        self.tab3.pack(fill="both", expand=YES)
        self.notebook.add(self.tab3, text = 'Publications')

        #SELECT WHAT TO DISPLAY (Journals, conf, report...)
        self.Cat4 = TK.StringVar(self.tab2)
        self.Cat4.set("All publications")
        TK.Label(self.tab3, text = "Category", bg = '#961364', fg = 'white').grid(row=2, column=13)
        self.w4 = TK.OptionMenu(self.tab3, self.Cat4, "All publications", "Journals articles", "Conferences articles", "Reports")
        self.w4.grid(row=2,column=14,columnspan=1)
        self.apply3 = TK.Button(self.tab3, text='Apply', command = self.apply_button)
        self.apply3.grid(row=2,column= 15)
        
        #LISTBOX
        self.Listbox3 = TK.Listbox(self.tab3, width = 40, height = 15)
        self.Listbox3.grid(row=3,column=13,rowspan=10, columnspan= 10)

        #DISPLAY PUBLICATIONS DETAILS BY DOUBLE CLICK 
        self.Listbox3.bind('<Double-1>', self.display_pub)

        #BLANK SPACE
        TK.Label(self.tab3, text = " \n ", bg = '#961364', fg = 'white').grid(row=2, column=9, rowspan = 10, columnspan=5)

        #TITLE
        TK.Label(self.tab3, text = "Add publications", bg = '#961364', fg = 'white').grid(row=2, column=7, sticky = 'W',padx = 5, pady = 5)

        #IMPLEMENT VAR/ENTRY/LABELS
        self.VarTitleP = TK.StringVar() ; self.VarAvailableP = TK.StringVar() ; self.VarDOIP = TK.StringVar() ; self.VarMagazineP = TK.StringVar()
        self.VarDatesP = TK.StringVar() ; self.VarNomP = TK.StringVar() ; self.VarPlaceP = TK.StringVar()
        self.VarAuthorsP = TK.StringVar()
        TK.Entry(self.tab3, textvariable = self.VarTitleP).grid(row=3, column=7, columnspan=3)
        TK.Entry(self.tab3, textvariable = self.VarAvailableP).grid(row=4, column=7, columnspan=3)
        TK.Entry(self.tab3, textvariable = self.VarDOIP).grid(row=5, column=7,columnspan=3)
        TK.Entry(self.tab3, textvariable = self.VarMagazineP).grid(row=6, column=7,columnspan=3)
        TK.Entry(self.tab3, textvariable = self.VarNomP).grid(row=7, column=7,columnspan=3)
        TK.Entry(self.tab3, textvariable = self.VarDatesP).grid(row=8, column=7,columnspan=3)
        TK.Entry(self.tab3, textvariable = self.VarPlaceP).grid(row=9, column=7,columnspan=3)
        TK.Entry(self.tab3, textvariable = self.VarAuthorsP).grid(row=14, column=7,columnspan=3)
        TK.Label(self.tab3, text = "          \n       ", bg = '#961364', fg = 'white').grid(row=3, column=11, rowspan=10, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab3, text = "Title", bg = '#961364', fg = 'white').grid(row=3, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab3, text = "Release date",  bg = '#961364', fg = 'white').grid(row=4, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab3, text = "DOI",  bg = '#961364', fg = 'white').grid(row=5, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab3, text = "Magazine (if journal)",  bg = '#961364', fg = 'white').grid(row=6, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab3, text = "Name (if conferences)",  bg = '#961364', fg = 'white').grid(row=7, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab3, text = "Dates (if conferences)", bg = '#961364', fg = 'white').grid(row=8, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab3, text = "Place (if conferences)",  bg = '#961364', fg = 'white').grid(row=9, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab3, text = "Add author",  bg = '#961364', fg = 'white').grid(row=14, column=6, sticky = 'W',padx = 5, pady = 5)
        
        #ADDING BUTTONS
        TK.Button(self.tab3, text = "Add publications", command = self.add_publication).grid(row=11,column=9)
        TK.Button(self.tab3, text = "Add authors", command = self.add_author).grid(row=15,column=9)

    



        '''TAB #4'''
        self.tab4 = TK.Frame(self.notebook, bg ='#961364')
        self.tab4.pack(fill="both", expand=YES)
        self.notebook.add(self.tab4, text = 'Projects')

        #SELECT WHAT TO DISPLAY (research projects or phd)
        self.Cat5 = TK.StringVar(self.tab4)
        self.Cat5.set("All projects")
        TK.Label(self.tab4, text = "Category", bg = '#961364', fg = 'white').grid(row=2, column=14)
        self.w5 = TK.OptionMenu(self.tab4, self.Cat5, "All projects", "Research projects", "PhD")
        self.w5.grid(row=2,column=15,columnspan=1)
        self.apply4 = TK.Button(self.tab4, text='Apply', command = self.apply_button)
        self.apply4.grid(row=2,column= 16)
        
        #LISTBOX
        self.Listbox4 = TK.Listbox(self.tab4, width = 50, height = 5)
        self.Listbox4.grid(row=3,column=14,rowspan=2, columnspan= 10)
        self.Listbox4.bind('<Double-1>', self.display_project)

        #TITLE
        TK.Label(self.tab3, text = "Add projects", bg = '#961364', fg = 'white').grid(row=2, column=7, sticky = 'W',padx = 5, pady = 5)

        #IMPLEMENTING LABEL/VAR/ENTRY
        self.VarNamePhD = TK.StringVar() ; self.VarStartPhD = TK.StringVar() ; self.VarJuryMembers = TK.StringVar()
        self.VarExpectedEnd = TK.StringVar() ; self.VarShortPhD = TK.StringVar() ; self.VarEndPhD = TK.StringVar() ; self.VarHeadPhD = TK.StringVar() ; self.VarBudget = TK.StringVar() ; self.VarCompanyPhD = TK.StringVar() ; self.VarMembersPhD = TK.StringVar()
        self.VarPlacePhD = TK.StringVar() ; self.VarDefenseDate = TK.StringVar() ; self.VarDirectorPhD = TK.StringVar() ; self.VarSupervisorsPhD = TK.StringVar() ; self.VarJuryMembersPhD = TK.StringVar()

        '''Elements communs aux projets de recherche et theses'''
        TK.Entry(self.tab4, textvariable = self.VarNamePhD).grid(row=3, column=7, columnspan=3)
        TK.Entry(self.tab4, textvariable = self.VarStartPhD).grid(row=4, column=7, columnspan=3)
        TK.Label(self.tab4, text = "Research projects",  bg = '#961364', fg = 'white').grid(row=5, column=7, sticky = 'W',padx = 5, pady = 5)
        TK.Entry(self.tab4, textvariable = self.VarExpectedEnd).grid(row=6, column=7,columnspan=3)
        TK.Entry(self.tab4, textvariable = self.VarShortPhD).grid(row=7, column=7,columnspan=3)
        TK.Label(self.tab4, text = "PhD",  bg = '#961364', fg = 'white').grid(row=5, column=15, sticky = 'W',padx = 5, pady = 5)
        TK.Entry(self.tab4, textvariable = self.VarPlacePhD).grid(row=6, column=15,columnspan=3)
        TK.Label(self.tab4, text = "Name", bg = '#961364', fg = 'white').grid(row=3, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab4, text = "Start",  bg = '#961364', fg = 'white').grid(row=4, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab4, text = "Expected End",  bg = '#961364', fg = 'white').grid(row=6, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab4, text = "Short",  bg = '#961364', fg = 'white').grid(row=7, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab4, text = "Place", bg = '#961364', fg = 'white').grid(row=6, column=14, sticky = 'W',padx = 5, pady = 5)
        
        ''' Project : nom, datefinprev, datedebut, acronyme -- end, head, members, budget, company'''

        TK.Label(self.tab4, text = "End", bg = '#961364', fg = 'white').grid(row=9, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab4, text = "Head", bg = '#961364', fg = 'white').grid(row=10, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab4, text = "Members", bg = '#961364', fg = 'white').grid(row=11, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab4, text = "Budget", bg = '#961364', fg = 'white').grid(row=12, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab4, text = "Company", bg = '#961364', fg = 'white').grid(row=13, column=6, sticky = 'W',padx = 5, pady = 5)
        TK.Entry(self.tab4, textvariable = self.VarEndPhD).grid(row=9, column=7,columnspan=3)
        TK.Entry(self.tab4, textvariable = self.VarHeadPhD).grid(row=10, column=7,columnspan=3)
        TK.Entry(self.tab4, textvariable = self.VarMembersPhD).grid(row=11, column=7,columnspan=3)
        TK.Entry(self.tab4, textvariable = self.VarBudget).grid(row=12, column=7,columnspan=3)
        TK.Entry(self.tab4, textvariable = self.VarCompanyPhD).grid(row=13, column=7,columnspan=3)

        ''' PhD : nom, datelancement, lieurealisation -- defense date, director, supervisors, jury members'''

        TK.Label(self.tab4, text = "Defense date", bg = '#961364', fg = 'white').grid(row=9, column=14, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab4, text = "Director", bg = '#961364', fg = 'white').grid(row=10, column=14, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab4, text = "Supervisor", bg = '#961364', fg = 'white').grid(row=11, column=14, sticky = 'W',padx = 5, pady = 5)
        TK.Label(self.tab4, text = "Jury member", bg = '#961364', fg = 'white').grid(row=12, column=14, sticky = 'W',padx = 5, pady = 5)
        TK.Entry(self.tab4, textvariable = self.VarDefenseDate).grid(row=9, column=15,columnspan=3)
        TK.Entry(self.tab4, textvariable = self.VarDirectorPhD).grid(row=10, column=15,columnspan=3)
        TK.Entry(self.tab4, textvariable = self.VarSupervisorsPhD).grid(row=11, column=15,columnspan=3)
        TK.Entry(self.tab4, textvariable = self.VarJuryMembersPhD).grid(row=12, column=15,columnspan=3)

        #BOUTONS POUR AJOUTER DES INFOS
        TK.Button(self.tab4, text = "Add project", command = self.add_project).grid(row=8,column=13)
        TK.Button(self.tab4, text = "Set", command = self.set_project).grid(row=9,column=13)
        TK.Button(self.tab4, text = "Set", command = self.set_project).grid(row=10,column=13)
        TK.Button(self.tab4, text = "Set", command = self.set_project).grid(row=11,column=13)
        TK.Button(self.tab4, text = "Set", command = self.set_project).grid(row=12,column=13)
        TK.Button(self.tab4, text = "Set", command = self.set_project).grid(row=13,column=13)
        TK.Button(self.tab4, text = "Set", command = self.set_PhD).grid(row=9,column=21)
        TK.Button(self.tab4, text = "Set", command = self.set_PhD).grid(row=10,column=21)
        TK.Button(self.tab4, text = "Set", command = self.set_PhD).grid(row=11,column=21)
        TK.Button(self.tab4, text = "Set", command = self.set_PhD).grid(row=12,column=21)

        self.main.mainloop()
        
    def delete_button(self): #supprimer des membres du personnel
        self.Listbox2.delete(ANCHOR)
        for element in self.Laboratory["Internals"]:
            if element.__repr__() == self.Listbox.get(ANCHOR):
                self.Laboratory["Internals"].pop(element)
                print("Internal {} {} deleted".format(element.FirstName, element.Name))
        for element in self.Laboratory["Externals"]:
            if element.__repr__() == self.Listbox.get(ANCHOR):
                self.Laboratory["Internals"].pop(element)
                print("External {} {} deleted".format(element.FirstName, element.Name))
    
    def delete_all(self): #supprimer tous les membres
        self.Listbox.delete(0,500)
        self.Laboratory["Internals"] = []
        self.Laboratory["Externals"] = []

    def display_details(self,event): # afficher les infos des membres
        if self.Listbox2.curselection()[0] != None:
            for element in self.Laboratory["Internals"]:
                if element.__repr__() == self.Listbox2.get(ANCHOR):
                    bd = str(element.BD.year) + "/" + str(element.BD.month) + "/" + str(element.BD.day)
                    rt=''
                    for resteam in list(element.Taux.keys()) :
                        rt = '- {} : {}\n'.format(resteam,element.Taux[resteam] )
                    print("Name : {} \n First Name : {} \n Gender : {} \n Birth Date : {} \n Birth Place : {} \n Office : {} \n Research Teams rate : \n {}".format(str(element.Name), str(element.FirstName), str(element.Gender), str(bd), str(element.Country), str(element.Office),rt ))
            # On l'affiche également dans une fenetre de dialogue de type pop-up
                    TK.messagebox.showinfo(title = "Information - {}".format(str(element.Name + " " + element.FirstName)), message = " Name : {} \n First Name : {} \n Gender : {} \n Birth Date : {} \n Birth Place : {} \n Office : {} \n Research Teams rate : \n {}".format(str(element.Name), str(element.FirstName), str(element.Gender), str(bd), str(element.Country), str(element.Office), rt )) 
            for element in self.Laboratory["Externals"]:
                if element.__repr__() == self.Listbox2.get(ANCHOR):
                    bd = str(element.BD.year) + "/" + str(element.BD.month) + "/" + str(element.BD.day)
                    print("Name : {} \n First Name : {} \n Gender : {} \n Birth Date : {} \n Birth Place : {} \n Company : {} \n Position : {} \n Laboratory : {}".format(str(element.Name), str(element.FirstName), str(element.Gender), str(bd), str(element.Country), str(element.Company), str(element.Poste), str(element.Laboratoire)))
            # On l'affiche également dans une fenetre de dialogue de type pop-up
                    TK.messagebox.showinfo(title = "Information - {}".format(str(element.Name + " " + element.FirstName)), message = " Name : {} \n First Name : {} \n Gender : {} \n Birth Date : {} \n Birth Place : {} \n Company : {} \n Position : {} \n Laboratory : {}".format(str(element.Name), str(element.FirstName), str(element.Gender), str(bd), str(element.Country), str(element.Company), str(element.Poste), str(element.Laboratoire) )) 
        
    def display_mag(self,event): #afficher les infos des revues
        if self.Listbox1.selection() != None:
            name, short, qty = self.Listbox1.item(self.Listbox1.selection()[0],'values')
            for element in self.Laboratory["Magazines"]:
                if element.Name == name:
                    print("Name : {} \n Short : {} \n IF : {} \n Quartile : {}".format(str(element.Name), str(element.Short), str(element.IF), str(element.Quartile)))
                    TK.messagebox.showinfo(title = "Magazine details - {}".format(str(element.Name)), message = " Name : {} \n Short : {} \n IF : {} \n Quartile : {}".format(str(element.Name), str(element.Short), str(element.IF), str(element.Quartile)))

    def show_members(self,event): #afficher le taux d'appartenance de tous les membres d'un axe
        if self.Listbox0.selection() != None:
            name, head = self.Listbox0.item(self.Listbox0.selection()[0],'values')
            text = ''
            for element in self.Laboratory["Research Teams"]:
                if element.Name == name :
                    for memb in list(element.TauxAppartenance.keys()) :
                        text += '\n {} : {}'.format(memb, element.TauxAppartenance[memb])
            print( "{}\n{}".format(name, str(text)))
            TK.messagebox.showinfo(title = "Research teams : {} - members' rate".format(str(name)), message = text)

    def display_pub(self, event): #afficher les infos de publications
        if self.Listbox3.curselection()[0] != None:
            for element in self.Laboratory["Journals articles"]:
                if element.__repr__() == self.Listbox3.get(ANCHOR):
                    authors = ''
                    for author in element.Authors :
                        authors += '{} {}, '.format(author.FirstName,author.Name)
                    authors[:-3]
                    print(" Title : {} \n Release date : {} \n DOI : {} \nAuthors : {} \n Mag : {}".format(str(element.Title), str(element.Available), str(element.DOI), authors, str(element.Mag)))
            # On l'affiche également dans une fenetre de dialogue de type pop-up
                    TK.messagebox.showinfo(title = "Journal article - {}".format(str(element.Title)), message = " Title : {} \n Release date : {} \n DOI : {} \n Authors :{}\n Mag : {}".format(str(element.Title), str(element.Available), str(element.DOI), authors, str(element.Mag)))
            for element in self.Laboratory["Conferences articles"]:
                if element.__repr__() == self.Listbox3.get(ANCHOR):
                    authors = ''
                    for author in element.Authors :
                        authors += '{} {}, '.format(author.FirstName,author.Name)
                    authors[:-3]
                    bd = str(element.Available.year) + "/" + str(element.Available.month) + "/" + str(element.Available.day)
                    print("Title : {} \n Release date : {} \n DOI: {} \n Names : {} \n Dates : {} \n Place : {} ".format(str(element.Title), str(element.Available), str(element.DOI), authors, str(element.Name), str(element.Dates), str(element.Place)))
            # On l'affiche également dans une fenetre de dialogue de type pop-up
                    TK.messagebox.showinfo(title = "Conference article - {}".format(str(element.Title)), message = " Title : {} \n Release date : {} \n DOI : {} \n Authors : {} \n Names : {} \n Dates : {} \n Place : {} ".format(str(element.Title), str(element.Available), str(element.DOI), authors, str(element.Name), str(element.Dates), str(element.Place)))
            for element in self.Laboratory["Reports"]:
                if element.__repr__() == self.Listbox3.get(ANCHOR):
                    bd = str(element.Available.year) + "/" + str(element.Available.month) + "/" + str(element.Available.day)
                    print("Title : {} \n Release date : {} ".format(str(element.Title), str(element.Available)))
            # On l'affiche également dans une fenetre de dialogue de type pop-up
                    TK.messagebox.showinfo(title = "Report - {}".format(str(element.Title)), message = " Title : {} \n Release date : {} ".format(str(element.Title), str(element.Available)))
    
    def display_project(self,event): #afficherl es infos de projets
        if self.Listbox4.curselection()[0] != None:
            for element in self.Laboratory["PhD"]:
                if element.__repr__() == self.Listbox4.get(ANCHOR):
                    supervisors = '' ; jurymembers = '' ; director = " {} (rate : {})".format(str(list(element.Director.keys())[0]),str(list(element.Director.values())[0]))
                    for super in list(element.Supervisors.keys()) :
                        supervisors += str(super.Name) + ' ' + str(super.FirstName) + ', '
                    supervisors = supervisors[:-2]
                    for _jury in list(element.JuryMembers.keys()) :
                        jurymembers += "{} ({}), ".format(_jury, element.JuryMembers[_jury])
                    jurymembers = jurymembers[:-2]
                    print("Name : {} \n Start : {} \n Defense Date : {} \n Place : {} \n Director Name : {} \n Supervisors : {} \n Jury Members : {} ".format(str(element.Name), str(element.Start), str(element.DefenseDate), str(element.Place), director, supervisors, jurymembers))
                    TK.messagebox.showinfo(title = "PhD info - {}".format(str(element.Name)), message ="Name : {} \n Start : {} \n Defense Date : {} \n Place : {} \n Director Name : {} \n Supervisors : {} \n Jury Members : {} \n Project Linked : {} \n Production ref : {} ".format(str(element.Name), str(element.Start), str(element.DefenseDate), str(element.Place), director, supervisors, jurymembers, element.Project, element.ProdRef))
            for element in self.Laboratory["Research Projects"]:
                if element.__repr__() == self.Listbox4.get(ANCHOR):
                    members = '' ; companies = ''
                    for _member in element.Members :
                        members += str(_member.Name) + ' ' + str(_member.FirstName) + ', '
                    members = members[:-2]
                    for _company in list(element.CompaniesInvolved.keys()) :
                        companies += str(_company) + ' (' + str(element.CompaniesInvolved[_company])+ '€)' + ', '
                    companies = companies[:-2]
                    print("Name : {} \n Start : {} \n Expected End : {} \n End : {} \n Budget : {} \n Short : {} \n Members : {} \n Head : {} \n Companies Involved : {}".format(str(element.Name), str(element.Start), str(element.ExpectedEnd), str(element.End), str(element.Budget), str(element.Short), members, str(element.Head), companies))
                    TK.messagebox.showinfo(title = "PhD info - {}".format(str(element.Name)), message ="Name : {} \n Start : {} \n Expected End : {} \n End : {} \n Budget : {} \n Short : {} \n Members : {} \n Head : {} \n Companies Involved : {} \n Production ref : {}".format(str(element.Name), str(element.Start), str(element.ExpectedEnd), str(element.End), str(element.Budget), str(element.Short), members, str(element.Head), companies, element.ProdRef))


    def display_history(self): #afficher l'historique de carrière d'un interne/ ou les invitations d'un externe
        if self.Listbox2.curselection()[0] != None:
            for element in self.Laboratory["Internals"]:
                if element.__repr__() == self.Listbox2.get(ANCHOR):
                    text = "Position : {} \nStart : {} \nEnd : {}".format(str(element.Career[0][0]), str(element.Career[0][1]), "ongoing")
                    for poste in element.Career[1:] :
                        pos = poste[0]
                        start = poste[1]
                        end = poste[2]
                        text += "\n\n" + "Position : {} \nStart : {} \nEnd : {}".format(pos, start, end)
                    TK.messagebox.showinfo(title = "Carreer - {}".format(str(element.Name + " " + element.FirstName)), message = text)
                    print(text)
            for element in self.Laboratory["Externals"]:
                if element.__repr__() == self.Listbox2.get(ANCHOR):
                    text = "Invitation by : {} \nStart : {} \nEnd : {}".format(str(element.History[0][2]), element.History[0][0], element.History[0][1])
                    for poste in element.History[1:] :
                        pos = poste[2]
                        start = poste[0]
                        end = poste[1]
                        text += "\n\n" + "Invitation by : {} \nStart : {} \nEnd : {}".format(pos, start, end)
                    TK.messagebox.showinfo(title = "Invitation history - {}".format(str(element.Name + " " + element.FirstName)), message = text)
                    print(text)


    def apply_button(self): #permet d'appliquer la sélection d'une liste déroulante
        if self.Cat2.get() == "All members": #PERSONNEL
            self.Listbox2.delete(0,500) #supprimer les éléments avant d'insérer
            for _internalPOO in self.Laboratory["Internals"]:
                self.Listbox2.insert('end', _internalPOO)
            for _externalPOO in self.Laboratory["Externals"]:
                self.Listbox2.insert('end', _externalPOO)
        elif self.Cat2.get() == "Internals" : 
            self.Listbox2.delete(0,500) #supprimer les éléments avant d'insérer
            for _internalPOO in self.Laboratory["Internals"]:
                self.Listbox2.insert('end', _internalPOO)
        elif self.Cat2.get() == "Externals": 
            self.Listbox2.delete(0,500) #supprimer les éléments avant d'insérer
            for _externalPOO in self.Laboratory["Externals"]:
                self.Listbox2.insert('end', _externalPOO)
        
        if self.Cat4.get() == "All publications" : #PUBLICATIONS
            self.Listbox3.delete(0,500) #supprimer les éléments avant d'insérer
            for _publicationPOO in self.Laboratory["Journals articles"]:
                self.Listbox3.insert('end', _publicationPOO)
            for _publicationPOO in self.Laboratory["Conferences articles"]:
                self.Listbox3.insert('end', _publicationPOO)
            for _publicationPOO in self.Laboratory["Reports"]:
                self.Listbox3.insert('end', _publicationPOO)
        elif self.Cat4.get() == "Journals articles" : 
            self.Listbox3.delete(0,500) #supprimer les éléments avant d'insérer
            for _publicationPOO in self.Laboratory["Journals articles"]:
                self.Listbox3.insert('end', _publicationPOO)
        elif self.Cat4.get() == "Conferences articles" : 
            self.Listbox3.delete(0,500) #supprimer les éléments avant d'insérer
            for _publicationPOO in self.Laboratory["Conferences articles"]:
                self.Listbox3.insert('end', _publicationPOO)
        elif self.Cat4.get() == "Reports" : 
            self.Listbox3.delete(0,500) #supprimer les éléments avant d'insérer
            for _publicationPOO in self.Laboratory["Reports"]:
                self.Listbox3.insert('end', _publicationPOO)
    
        if self.Cat5.get() == "All projects" : #PROJETS
            self.Listbox4.delete(0,500) #supprimer les éléments avant d'insérer
            for _publicationPOO in self.Laboratory["PhD"]:
                self.Listbox4.insert('end', _publicationPOO)
            for _publicationPOO in self.Laboratory["Research Projects"]:
                self.Listbox4.insert('end', _publicationPOO)
        elif self.Cat5.get() == "PhD" : 
            self.Listbox4.delete(0,500) #supprimer les éléments avant d'insérer
            for _publicationPOO in self.Laboratory["PhD"]:
                self.Listbox4.insert('end', _publicationPOO)
        elif self.Cat5.get() == "Research projects" : 
            self.Listbox4.delete(0,500) #supprimer les éléments avant d'insérer
            for _publicationPOO in self.Laboratory["Research Projects"]:
                self.Listbox4.insert('end', _publicationPOO)  
        
        self.delButton() #supprimer les éléments avant d'insérer
        for _publicationPOO in self.Laboratory["Magazines"]:
            self.Listbox1.insert(parent='', index=0, text='', values = (_publicationPOO.Name, _publicationPOO.Short, len(_publicationPOO.Publications)) )

    def delButton(self): #
        x = self.Listbox1.get_children()
        for item in x:
            self.Listbox1.delete(item) 

    def treeview_sort_column(self, tv, col, reverse): #trier les columns d'un treeview en cliquant dessus
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda: \
                self.treeview_sort_column(tv, col, not reverse))


    def add_personnal(self): #ajouter un personnel
        #female internal
        if self.VarNameI.get() != '' and self.VarFirstNameI.get() != '' and self.VarBDI.get() != '' and self.VarBPI.get() != '' and self.VarOffice !='' and self.VarGenderI.get() == 1 and self.VarCompany.get() == '':
            internalPOO = Internal(self.VarNameI.get(), self.VarFirstNameI.get(), 'F', self.VarBDI.get(), self.VarBPI.get(), self.VarOffice.get())
            if internalPOO not in self.Laboratory["Internals"]:
                self.Laboratory["Internals"].append(internalPOO) #AJOUTER DANS LA LISTE DE DONNÉES
                self.Listbox2.insert('end', internalPOO) #INSÉRER DANS LA LISTBOX DE L'INTERFACE
                print("{} added in self.Laboratory internal members".format(internalPOO)) #AFFICHER LES DETAILS
        #male internal
        elif self.VarNameI.get() != '' and self.VarFirstNameI.get() != '' and self.VarBDI.get() != '' and self.VarBPI.get() != '' and self.VarOffice !='' and self.VarGenderI.get() == 0 and self.VarCompany.get() == '':
            internalPOO = Internal(self.VarNameI.get(), self.VarFirstNameI.get(), 'M', self.VarBDI.get(), self.VarBPI.get(), self.VarOffice.get())
            if internalPOO not in self.Laboratory["Internals"]:
                self.Laboratory["Internals"].append(internalPOO)
                self.Listbox2.insert('end', internalPOO)
                print("{} added in self.Laboratory internal members".format(internalPOO))
        #female external
        elif self.VarNameI.get() != '' and self.VarFirstNameI.get() != '' and self.VarBDI.get() != '' and self.VarBPI.get() != '' and self.VarCompany !='' and self.VarGenderI.get() == 1 and self.VarOffice.get() == '':
            internalPOO = External(self.VarNameI.get(), self.VarFirstNameI.get(), 'F', self.VarBDI.get(), self.VarBPI.get(), self.VarCompany.get())
            if internalPOO not in self.Laboratory["Externals"]:
                self.Laboratory["Externals"].append(internalPOO)
                self.Listbox2.insert('end', internalPOO)
                print("{} added in self.Laboratory external members".format(internalPOO))
        #female external
        elif self.VarNameI.get() != '' and self.VarFirstNameI.get() != '' and self.VarBDI.get() != '' and self.VarBPI.get() != '' and self.VarCompany !='' and self.VarGenderI == 0 and self.VarOffice.get() == '':
            internalPOO = External(self.VarNameI.get(), self.VarFirstNameI.get(), 'M', self.VarBDI.get(), self.VarBPI.get(), self.VarCompany.get())
            if internalPOO not in self.Laboratory["Externals"]:
                self.Laboratory["Externals"].append(internalPOO)
                self.Listbox2.insert('end', internalPOO)
                print("{} added in self.Laboratory external members".format(internalPOO))

    def add_publication(self): #AJOUTER DES PUBLICATIONS - même format que le personnel
        if self.VarTitleP.get() != '' and self.VarAvailableP.get() != '' and self.VarDOIP != '':
            if self.VarMagazineP.get() != '' :
                journalPOO = Journal(self.VarTitleP.get(), self.VarAvailableP.get(), self.VarDOIP.get(), self.VarMagazineP.get())
                self.Laboratory['Journals articles'].append(journalPOO)
                self.Listbox3.insert('end',journalPOO)
            elif self.VarNomP.get() != '' and self.VarDatesP.get() != '' and self.VarPlaceP != '':
                confPOO = Conference(self.VarTitleP.get(), self.VarAvailableP.get(), self.VarDOIP.get(),self.VarNomP.get(), self.VarDatesP.get(), self.VarMagazineP.get())
                self.Laboratory['Conferences articles'].append(confPOO)
                self.Listbox3.insert('end',confPOO)
            elif self.VarNomP.get() == '' and self.VarDatesP.get() == '' and self.VarPlaceP == '' and self.VarNomP.get() == '' and self.VarDatesP.get() == '' and self.VarPlaceP == '' and self.VarMagazineP.get() != '':
                confPOO = Conference(self.VarTitleP.get(), self.VarAvailableP.get(), self.VarDOIP.get(),self.VarNameP.get(), self.VarDatesP.get(), self.VarMagazineP.get())
                self.Laboratory['Report'].append(confPOO)
                self.Listbox3.insert('end',confPOO)
    
    def add_project(self): #AJOUTER UN PROJET - même format que ajouter un personnel
        if self.VarNamePhD.get() != '' and self.VarStartPhD.get() != '' :
            if self.VarExpectedEnd.get() != '' and self.VarShortPhD.get() !='' :
                ResearchPOO = Research_Project(self.VarNamePhD.get(), self.VarExpectedEnd.get(), self.VarStartPhD.get(), self.VarShortPhD.get())
                self.Laboratory['Research Projects'].append(ResearchPOO)
                self.Listbox4.insert('end',ResearchPOO)
            elif self.VarPlacePhD != '':
                PhDPOO = PhD(self.VarNamePhD.get(), self.VarStartPhD.get(), self.VarPlacePhD.get())
                self.Laboratory['PhD'].append(PhDPOO)
                self.Listbox4.insert('end',PhDPOO)
    
    def set_project(self): #AJOUTER INFORMATIONS A UN PROJET DE RECHERCHE
        if self.Listbox4.curselection()[0] != None:
            if self.VarEndPhD.get() != '' and self.VarHeadPhD.get() == '' and self.VarMembersPhD.get() == '' and self.VarBudget.get() == '' and self.VarCompanyPhD.get() == '':
                for element in self.Laboratory["Research Projects"]:
                    if element.__repr__() == self.Listbox4.get(ANCHOR):
                        element.End = self.VarEndPhD.get()
            elif self.VarEndPhD.get() == '' and self.VarHeadPhD.get() != '' and self.VarMembersPhD.get() == '' and self.VarBudget.get() == '' and self.VarCompanyPhD.get() == '':
                for element in self.Laboratory["Research Projects"]:
                    if element.__repr__() == self.Listbox4.get(ANCHOR):
                        element.Head = self.VarHeadPhD.get()
            elif self.VarEndPhD.get() == '' and self.VarHeadPhD.get() == '' and self.VarMembersPhD.get() != '' and self.VarBudget.get() == '' and self.VarCompanyPhD.get() == '':
                for element in self.Laboratory["Research Projects"]:
                    if element.__repr__() == self.Listbox4.get(ANCHOR):
                        for int in self.Laboratory['Internals']:
                            if int.Name == self.VarMembersPhD.get():
                                element.Members.append(int)
            elif self.VarEndPhD.get() == '' and self.VarHeadPhD.get() == '' and self.VarMembersPhD.get() == '' and self.VarBudget.get() != '' and self.VarCompanyPhD.get() != '':
                for element in self.Laboratory["Research Projects"]:
                    if element.__repr__() == self.Listbox4.get(ANCHOR):
                        element.CompaniesInvolved.append(Company(self.VarCompanyPhD.get(), self.VarBudget))

    def set_PhD(self): #AJOUTER INFORMATIONS A UN PROJET DE THESES
        if self.Listbox4.curselection()[0] != None:
            if self.VarDefenseDate.get() != '' and self.VarDirectorPhD.get() == '' and self.VarSupervisorsPhD.get() == '' and self.VarJuryMembers.get() == '':
                for element in self.Laboratory["PhD"]:
                    if element.__repr__() == self.Listbox4.get(ANCHOR):
                        element.DefenseDate = str(self.VarDefenseDate.get())
            elif self.VarDefenseDate.get() == '' and self.VarDirectorPhD.get() != '' and self.VarSupervisorsPhD.get() == '' and self.VarJuryMembers.get() == '':
                for element in self.Laboratory["PhD"]:
                    if element.__repr__() == self.Listbox4.get(ANCHOR):
                        element.Director = self.VarDirectorPhD.get()
            elif self.VarDefenseDate.get() == '' and self.VarDirectorPhD.get() == '' and self.VarSupervisorsPhD.get() != '' and self.VarJuryMembers.get() == '':
                for element in self.Laboratory["PhD"]:
                    if element.__repr__() == self.Listbox4.get(ANCHOR):
                        for int in self.Laboratory('Internals'):
                            if int.Name == self.VarSupervisorsPhD.get():
                                element.Supervisors.append(int)
            elif self.VarDefenseDate.get() == '' and self.VarDirectorPhD.get() == '' and self.VarSupervisorsPhD.get() == '' and self.VarJuryMembers.get() != '':
                for element in self.Laboratory["PhD"]:
                    if element.__repr__() == self.Listbox4.get(ANCHOR):
                        element.JuryMembers.append(self.VarJuryMembers.get())

    def add_magazine(self): # AJOUTER UNE REVUE - même format que ajouter un personnel
        if self.VarNameM.get() != '' and self.VarShortM.get() != '' :
            MagazinePOO = Magazine(self.VarNameM.get(), self.VarShortM.get())
            self.Laboratory["Magazines"].append(MagazinePOO)
            self.Listbox1.insert(parent = '', index=0, text='', values=(MagazinePOO.Name,MagazinePOO.Short,len(MagazinePOO.Publications)))

    def add_information(self): # AJOUTER UNE INFORMATION A UNE REVUE
        if self.Listbox1.selection() != None:
            name, short, qty = self.Listbox1.item(self.Listbox1.selection()[0],'values')
            for magazinePOO in self.Laboratory["Magazines"]:
                if name == magazinePOO.Name and self.VarYear.get() != '' and self.VarIFM.get() != '' and self.VarQuartileM.get() == '':
                    magazinePOO._add_IF(str(self.VarYear.get()), str(self.VarIFM.get()) )
                    print(magazinePOO.IF)
                elif name == magazinePOO.Name and self.VarYear.get() != '' and self.VarIFM.get() == ''  and self.VarQuartileM.get() != '':
                    magazinePOO._add_Quartile(str(self.VarYear.get()), str(self.VarQuartileM.get()) )
                    print(magazinePOO.Quartile)

    def add_author(self, theauthor): #AJOUTER UN AUTEUR A UNE PUBLICATION
        if self.VarAuthorsP.get() != None and isinstance(theauthor, (Staff, Internal, External)):
            self.VarAuthorsP.append(theauthor)
        

    def set_TA(self):   #CHANGER LE TAUX D'APPARTENANCE D'UN MEMBRE D'UN AXE   
        for researchteam in self.Laboratory["Research Teams"]:
            for memberPOO in self.Laboratory["Internals"]:
                if self.Cat3.get() == researchteam.Name and memberPOO.__repr__() == self.Listbox2.get(ANCHOR) and self.VarTA.get() != '' and len(self.Listbox2.curselection()) > 0 :
                    memberPOO._set_TauxAppartenance(researchteam, float(self.VarTA.get()))
                    print(memberPOO.Taux)
                    TK.messagebox.showinfo(title = "Research team rate", message="{} {} rate set to {}".format(self.Listbox2.get(ANCHOR), self.Cat3.get(), self.VarTA.get()))

    '''CHARGEMENT'''
    def XMLLoading(self):
        fichieracharger = TKFD.askopenfilename(title = "Chargement du fichier XML d'étudiants...", defaultextension = ".xml", filetypes = [("XML", "*.xml")], multiple = False)
        if fichieracharger != "": 
            # Chargement du fichier XML
            parser = ET.XMLParser(encoding="utf-8")
            treexml = ET.parse(fichieracharger,parser=parser)
            
            # Obtention du tronc de l'arbre XML
            root = treexml.getroot()

            for o in root.iter("Organization"):
                for _universityXML in o.findall('University Name'):
                    universityPOO = Company(_universityXML.get("Name"))
                    self.Laboratory["Universities"].append(universityPOO)
                for _researchteamXML in o.findall("Research_Team"):
                    researchteamPOO = Axe_Recherche(_researchteamXML.attrib["Name"])
                    self.Laboratory["Research Teams"].append(researchteamPOO)
            for m in root.iter("Members"): #scan de tous les membres du fichier et instanciation de leurs objets
                for _memberxml in m.findall("Member"): #scan des internes
                    memberPOO = Internal(_memberxml.attrib['Name'], _memberxml.attrib['FirstName'], _memberxml.attrib["Gender"], _memberxml.attrib["BD"], _memberxml.attrib["Country"], _memberxml.attrib["Office"])
                    # Scan de leurs postes et ajout des postes dans leur carrière
                    for _positionxml in _memberxml.findall("Position"):
                        memberPOO._add_Position(_positionxml.attrib["Name"], _positionxml.get("Start"), _positionxml.get("End"))
                    # Scan de leurs taux d'appartenance, et stockage du taux des internes dans les objets
                    for _researchxml in _memberxml.findall("Research_Team"):
                        for team in self.Laboratory["Research Teams"]:
                            if team.Name  == _researchxml.attrib["Name"] :
                                memberPOO._set_TauxAppartenance(team,float(_researchxml.attrib["Rate"]))
                                '''if _researchxml.attrib["Rate"] == 1.0 :
                                    team._set_Head(memberPOO, 1)
                                print(team.Head)'''
                    # TODO Ajout de ces objet à la liste Promotion
                    self.Laboratory["Internals"].append(memberPOO)
                print("Internal members added")
                
                for o in root.iter("Organization"):
                    for _researchteamXML in o.findall("Research_Team"): #scan des axes de recherchet et ajout des responsables
                        for team in self.Laboratory["Research Teams"]:
                            if _researchteamXML.attrib["Name"] == team.Name :
                                for interne in self.Laboratory["Internals"]:
                                    if interne.Name == _researchteamXML.attrib["Head"]:
                                        team._set_Head(interne,1)
                                        break
                                break

                print("Research Teams added")
    
                for _externalxml in m.findall("External_Member"): # Scan de tous les externes du fichier et instanciation de leurs objets
                    memberPOO = External(_externalxml.attrib['Name'], _externalxml.attrib['FirstName'], _externalxml.attrib["Gender"], _externalxml.get("BD"), _externalxml.attrib["Country"], _externalxml.attrib["Company"])
                    for _visitxml in _externalxml.findall("Stay"):
                        memberPOO._AddInvitation(_visitxml.attrib["Start"],_visitxml.attrib["End"],_visitxml.get("Invitation by"))
                    self.Laboratory["Externals"].append(memberPOO)
                print("External members added")
            
            
  
                

            # SCAN DES PUBLICATIONS
            for p in root.iter("Publications"):
                for m in p.findall("Journals"): #Revues
                    for _magazinexml in m.findall("Journal"): 
                        name = _magazinexml.attrib["Name"]
                        short = _magazinexml.attrib["Short"]
                        magazinePOO = Magazine(name,short)
                        for _perfxml in _magazinexml.findall("Performances"):
                                year = _perfxml.attrib["Year"]
                                magazinePOO.Quartile[year] = _perfxml.attrib["Quartile"]
                                magazinePOO.IF[year] = _perfxml.attrib["IF"]
                        self.Laboratory["Magazines"].append(magazinePOO)
                print("Magazines added")

                for _journalxml in p.findall("Journal_paper"): #Articles de journaux
                    for revue in self.Laboratory["Magazines"]:
                        if revue.Short == _journalxml.attrib["Journal"]:
                            journalPOO = Journal(_journalxml.attrib["Title"],_journalxml.attrib["Available"],_journalxml.attrib["DOI"], revue)
                            revue.Publications.append(journalPOO)
                    for author in _journalxml.findall("Author"):
                        for member in self.Laboratory["Internals"]:
                            if member.Name == author.attrib["Name"]:
                                member.release(journalPOO)
                        for member in self.Laboratory["Externals"]:
                            if member.Name == author.attrib["Name"]:
                                member.release(journalPOO)
                if journalPOO not in self.Laboratory["Journals articles"]:
                    self.Laboratory["Journals articles"].append(journalPOO)
                print("Journals articles added")
    
                for _conferencexml in p.findall("Conference"): #Articles de conférences
                    conferencePOO = Conference(_conferencexml.attrib["Title"], _conferencexml.attrib["Available"], _conferencexml.attrib["DOI"], _conferencexml.attrib["Conference_Name"], _conferencexml.attrib["Dates"], _conferencexml.attrib["Place"])
                    for author in _conferencexml.findall("Author"):
                        for member in self.Laboratory["Internals"]:
                            if member.Name == author.attrib["Name"]:
                                member.release(conferencePOO)
                        for member in self.Laboratory["Externals"]:
                            if member.Name == author.attrib["Name"]:
                                member.release(conferencePOO)
                if conferencePOO not in self.Laboratory["Conferences articles"]:
                    self.Laboratory["Conferences articles"].append(conferencePOO)
                print("Conferences articles added")
            
                for _reportxml in p.findall("Report"): #Rapports techniques
                    reportPOO = Report(_reportxml.attrib["Title"],_reportxml.attrib["Available"])
                    for author in _reportxml.findall("Author"):
                        for member in self.Laboratory["Internals"]:
                            if member.Name == author.attrib["Name"]:
                                member.release(reportPOO)
                if reportPOO not in self.Laboratory["Reports"]:
                    self.Laboratory["Reports"].append(reportPOO)
                print("Reports added")
                
            LaboratoryPOO = Laboratory(root.attrib["Name"])
            for interne in self.Laboratory["Internals"]:
                for organization in root.iter("Organization"):
                    if interne.Name == organization.attrib["Laboratory_Head_Name"]:
                        LaboratoryPOO._set_Head(interne)
            self.Laboratory["Laboratory"] = LaboratoryPOO
            print("Laboratory name ({}) added".format( root.attrib["Name"]))


        # SCAN DES PROJETS DE RECHERCHES ET DE THÈSES et instanciation de leurs objets
            for p in root.iter("Projects"):  
                
                for _projectxml in p.findall("Project"): # projets de recheches
                    projectPOO = Research_Project(_projectxml.attrib["Name"], _projectxml.attrib["Expected_End"], _projectxml.get("Start"), _projectxml.attrib["Short"])
                    for _companyxml in _projectxml.findall("Company_Involved"):
                        companyPOO = Company(_companyxml.attrib["Name"])
                        projectPOO._add_Company(companyPOO, _companyxml.get("Funding"))
                    for member in _projectxml.findall("Member"):
                        for internal in self.Laboratory["Internals"] :
                            if member.attrib["Name"] == internal.Name :
                                projectPOO._add_Member(internal)
                        for external in self.Laboratory["Externals"]:
                            if member.attrib["Name"] == external.Name :
                                projectPOO._add_Member(external)
                        for prod in _projectxml.findall("Production"):
                            print(prod.get("Ref"))
                            projectPOO._set_ProdRef(prod.get("Ref"), self.Laboratory["Journals articles"],self.Laboratory["Conferences articles"], self.Laboratory["Reports"])
                    if projectPOO not in self.Laboratory["Research Projects"]:
                        self.Laboratory["Research Projects"].append(projectPOO)
                print("Research Projects added")

                for _PhDxml in p.findall("PhD"): #PhD
                    PhDPOO = PhD(_PhDxml.attrib["Name"], _PhDxml.attrib["Start"], _PhDxml.attrib["Place"])
                    PhDPOO._set_DefenseDate(_PhDxml.get("Defense_Date"))
                    for int in self.Laboratory['Internals']:
                        if int.Name == _PhDxml.get('Candidate'):
                            PhDPOO._set_Candidate(int)
                            break
                    for _juryxml in _PhDxml.findall("Jury_Members"):
                        for _memberxml in _juryxml.findall("Member"):
                            print(_memberxml.attrib["Name"], _memberxml.attrib["Role"])
                            PhDPOO._add_JuryMember(_memberxml.attrib["Name"],str(_memberxml.attrib["Role"]))
                    for _headxml in _PhDxml.findall("PhD_Director"):
                        for internal in self.Laboratory["Internals"]:
                            if internal.Name == _headxml.attrib["Name"]:
                                PhDPOO._set_Director(internal, _headxml.attrib["Rate"])
                                internal.add_PhD(PhDPOO)
                    for _supxml in _PhDxml.findall("Supervisor"):
                        for internal in self.Laboratory["Internals"]:
                            if internal.Name == _supxml.attrib["Name"]:
                                PhDPOO._add_Supervisor(internal, _supxml.attrib["Rate"])
                        for external in self.Laboratory["Externals"]:
                            if external.Name == _supxml.attrib["Name"]:
                                PhDPOO._add_Supervisor(external, _supxml.attrib["Rate"])
                    for prod in _PhDxml.findall("Production"):
                        print(prod.get("Ref"))
                        PhDPOO._set_ProdRef(prod.get("Ref"), self.Laboratory["Journals articles"],self.Laboratory["Conferences articles"], self.Laboratory["Reports"])
                    for proj in _PhDxml.findall("Project_Link"):
                        print(proj.get("Name"))
                        PhDPOO._set_Project(proj.get("Name"), self.Laboratory["Research Projects"])
                    if PhDPOO not in self.Laboratory["PhD"]:
                        self.Laboratory["PhD"].append(PhDPOO)
                print("PhD added")

        #### INSERT TO LISTBOX OR TREEVIEW
        
        
            self.Listbox2.delete(0,500)
            self.Listbox3.delete(0,500)
            self.Listbox4.delete(0,500)
        for _internalPOO in self.Laboratory["Internals"]:
            self.Listbox2.insert('end', _internalPOO)
        for _externalPOO in self.Laboratory["Externals"]:
            self.Listbox2.insert('end', _externalPOO)    
        for _publicationPOO in self.Laboratory["Journals articles"]:
            self.Listbox3.insert('end', _publicationPOO)
        for _publicationPOO in self.Laboratory["Conferences articles"]:
            self.Listbox3.insert('end', _publicationPOO)
        for _publicationPOO in self.Laboratory["Reports"]:
            self.Listbox3.insert('end', _publicationPOO)
        for _publicationPOO in self.Laboratory["PhD"]:
            self.Listbox4.insert('end', _publicationPOO)
        for _publicationPOO in self.Laboratory["Research Projects"]:
            self.Listbox4.insert('end', _publicationPOO)
            for _comp in list(_publicationPOO.CompaniesInvolved.keys()):
                fund = _publicationPOO.CompaniesInvolved[_comp]
                self.Listbox0b.insert(parent='', index=0, text='', values = (_comp,fund))
        for _publicationPOO in self.Laboratory["Magazines"]:
            self.Listbox1.insert(parent='', index='end', text='', values = (_publicationPOO.Name, _publicationPOO.Short, len(_publicationPOO.Publications)) )
        for _publicationPOO in self.Laboratory["Research Teams"]:
            name = _publicationPOO.Name ; hd = list(_publicationPOO.Head.keys())[0]
            self.Listbox0.insert(parent='', index='end', text='', values = (name, hd) )

        print(self.Laboratory) 




    '''ENREGISTREMENT'''
    def XMLregistration(self):
        root = ET.Element("Laboratory") # Création d'un élement racine du futur arbre XML 
        
        # Pour chaque objet appartenant à la liste des étudiants, créer son élément XML associé
        labo_name = str(self.Laboratory["Laboratory"].Head.Name)
        organization_branch = ET.SubElement(root,"Organization", {"Laboratory_Head_Name" : labo_name})
        root.append(organization_branch)
        for _elementPOO in self.Laboratory["Research Teams"]:
            elementXML = ET.SubElement(organization_branch,"Research Team" , {"Name": str(_elementPOO.Name), "Head": str(list(_elementPOO.Head.keys())[0].Name)})
            root.append(elementXML)
            # Lui ajouter tous les éléments enfants structurant ses évaluations

        #ajout des membres (int/ext)
        members_branch = ET.SubElement(root,"Members")
        root.append(members_branch)
        for _elementPOO in self.Laboratory["Internals"]:
            elementXML = ET.SubElement(members_branch,"Member", {"FirstName": str(_elementPOO.FirstName), "Name": str(_elementPOO.Name), "Gender" : str(_elementPOO.Gender), "BD" : str(_elementPOO.BD), "Country" : str(_elementPOO.Country), "Office" : str(_elementPOO.Office)})
            for _infoPOO in _elementPOO.Career :
                poste = str(_infoPOO[1]) ; debut = str(_infoPOO[1]) ; fin = str(_infoPOO[2])
                infoXML = ET.SubElement(elementXML,"Position", {"Name" : poste, "Start" : debut, "End": fin})
                elementXML.append(infoXML)
            members_branch.append(elementXML)
        for _elementPOO in self.Laboratory["Externals"]:
            elementXML = ET.SubElement(members_branch,"External_Member", {"FirstName": str(_elementPOO.FirstName), "FirstName": str(_elementPOO.Name), "Gender" : str(_elementPOO.Gender), "BD" : str(_elementPOO.BD), "Country" : str(_elementPOO.Country), "Company" : str(_elementPOO.Company)})
            for _infoPOO in _elementPOO.History :
                debut = str(_infoPOO[0]) ; fin = str(_infoPOO[1]) ; inviteur = str(_infoPOO[2])
                infoXML = ET.SubElement(elementXML,"Stay", { "Start" : debut, "End": fin, "Invitation by" : inviteur})                    #print(_infoXML.attrib)
                elementXML.append(infoXML)
            members_branch.append(elementXML)
            
        #ajout des projet (recherche/these)
        projects_branch = ET.SubElement(root,"Projects")
        root.append(projects_branch)
        for _elementPOO in self.Laboratory["PhD"]:
            elementXML = ET.SubElement(projects_branch,"PhD", {"Name": str(_elementPOO.Name), "Candidate": str(_elementPOO.Candidate.Name), "Start" : str(_elementPOO.Start), "Defense_Date" : str(_elementPOO.DefenseDate), "Place" : str(_elementPOO.Place)})
            elementXML.append(ET.SubElement(elementXML,"PhD_Director", { "Name" : str(list(_elementPOO.Director.keys())[0].Name), "Rate": str(list(_elementPOO.Director.values())[0])}))
            for _infoPOO in list(_elementPOO.Supervisors.keys()) :
                infoXML = ET.SubElement(elementXML,"PhD_Supervisor", { "Name" : str(_infoPOO.Name), "Rate": str(_elementPOO.Supervisors[_infoPOO])})                    
                #print(_infoXML.attrib)
                elementXML.append(infoXML)
            juryXML = ET.SubElement(projects_branch,"Jury_Members")
            elementXML.append(juryXML)
            for _infoPOO in list(_elementPOO.JuryMembers.keys()) :
                infoXML = ET.SubElement(elementXML,"Member", { "Name" : str(_infoPOO), "Role": str(_elementPOO.JuryMembers[str(_infoPOO)])})                    
                #print(_infoXML.attrib)
                juryXML.append(infoXML)
            projects_branch.append(elementXML)
        for _elementPOO in self.Laboratory["Research Projects"]:
            elementXML = ET.SubElement(projects_branch,"Project", {"Name": str(_elementPOO.Name), "Start" : str(_elementPOO.Start), "Expected_End" : str(_elementPOO.ExpectedEnd), "Head" : str(_elementPOO.Head), "Short" : str(_elementPOO.Short)})
            for _infoPOO in _elementPOO.Members :
                infoXML = ET.SubElement(elementXML,"Member", {"Name" : str(_infoPOO.Name)})
                elementXML.append(infoXML)
            for _infoPOO in list(_elementPOO.CompaniesInvolved.keys()):
                infoXML = ET.SubElement(elementXML,"Company_Involved", {'Name':str(_infoPOO), 'Funding' : _elementPOO.CompaniesInvolved[_infoPOO]})
                elementXML.append(infoXML)
            projects_branch.append(elementXML)
        
        #ajout des publications (journaux, conf, report)
        publications_branch = ET.SubElement(root, "Publications")
        root.append(publications_branch)
        for _elementPOO in self.Laboratory["Journals articles"]:
            elementXML = ET.SubElement(publications_branch,"Journal_paper", {'Title' : str(_elementPOO.Title), 'Available' : str(_elementPOO.Available), 'Journal' : str(_elementPOO.Mag), 'DOI':str(_elementPOO.DOI)})
            for _infoPOO in _elementPOO.Authors:
                infoXML = ET.SubElement(elementXML,"Author", {'Name': str(_infoPOO.Name)})
                elementXML.append(infoXML)
            publications_branch.append(elementXML)
        for _elementPOO in self.Laboratory["Conferences articles"]:
            elementXML = ET.SubElement(publications_branch,"Conference", {"Title" : str(_elementPOO.Title), "Available" : str(_elementPOO.Available), "Conference_Name": str(_elementPOO.Name), "Place":str(_elementPOO.Place), "Dates":str(_elementPOO.Dates), "DOI":str(_elementPOO.DOI)})
            for _infoPOO in _elementPOO.Authors:
                infoXML = ET.SubElement(elementXML,"Author", {'Name': str(_infoPOO.Name)})
                elementXML.append(infoXML)
            publications_branch.append(elementXML)
        for _elementPOO in self.Laboratory["Reports"]:
            elementXML = ET.SubElement(publications_branch,"Report", {'Title':str(_elementPOO.Title), 'Avaialble': str(_elementPOO.Available)})
            for _infoPOO in _elementPOO.Authors:
                infoXML = ET.SubElement(elementXML,"Author", {'Name': str(_infoPOO.Name)})
                elementXML.append(infoXML)
            publications_branch.append(elementXML)
        
        #ajout des revues
        mag_branch = ET.SubElement(root,"Journals")
        root.append(mag_branch)
        for _elementPOO in self.Laboratory["Magazines"]:
            elementXML = ET.SubElement(mag_branch,"Journal", {'Name' : str(_elementPOO.Name), 'Short' : str(_elementPOO.Short)})
            for _infoPOO in list(_elementPOO.IF.keys()):
                infoXML = ET.SubElement(elementXML,"Performances", {'Year': str(_infoPOO), 'Quartile' : str(_elementPOO.Quartile[_infoPOO]), 'IF' : str(_elementPOO.IF[_infoPOO])})
                elementXML.append(infoXML)
            publications_branch.append(elementXML)


        # Enregistrement dans un arbre XML et enregistrement du fichier associé
        newTree = ET.ElementTree(root)
        

        pathname = TKFD.asksaveasfilename(title = "Enregistrement en XML..." , defaultextension = ".xml", filetypes = [("XML","*.xml")])
        if pathname != "":
            newTree.write(pathname, encoding='utf-8',xml_declaration=True)
            print("Ecriture du fichier XML réalisée au chemin précisé : {}".format(pathname))
            
        del(newTree)




    '''TRAITEMENTS'''

    def status(self): #regrouper les membres par statut
        Members_Position = {"Doctorant": '', "Masterant" : '', "Technicien": '', "Secrétaire": '', "Maître de conférences":'', "Professeur des Universités":'' }
        for interne in self.Laboratory["Internals"]:
            for position in list(Members_Position.keys()):
                if position == interne.Career[0][0]:
                    Members_Position[position] += interne.FirstName + ' ' + interne.Name + ', '
        
        TK.messagebox.showinfo(title = "Members position", message = "Doctorants : {}\n\nMasterant : {}\n\nTechnicien : {}\n\nSecrétaire : {}\n\nMaître de conférences : {}\n\nProfesseur des Universités : {}".format(str(Members_Position["Doctorant"][:-2]), str(Members_Position["Masterant"][:-2]),str(Members_Position["Technicien"][:-2]), str(Members_Position["Secrétaire"][:-2]), str(Members_Position["Maître de conférences"][:-2]), str(Members_Position["Professeur des Universités"][:-2])))
        print(Members_Position) 
             
       

    def population_pyramid(self): #afficher la pyramide des âges
        def calculate_age(born):
            today = dt.date.today()
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        yo2024m, yo2529m, yo3034m, yo3539m, yo4044m, yo4549m, yo5054m, yo5559m, yo6064m = 0, 0, 0, 0, 0, 0, 0, 0, 0
        yo2024f, yo2529f, yo3034f, yo3539f, yo4044f, yo4549f, yo5054f, yo5559f, yo6064f = 0, 0, 0, 0, 0, 0, 0, 0, 0
        age_bracket = ["20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64"]

        for interne in self.Laboratory["Internals"]:
            
            if interne.Gender == "F" :
                yo = calculate_age(interne.BD)
                if yo>=20 and yo<25:
                    yo2024f +=1
                elif yo>=25 and yo<30:
                    yo2529f +=1
                elif yo>=30 and yo<35:
                    yo3034f +=1
                elif yo>=35 and yo<40:
                    yo3539f +=1
                elif yo>=40 and yo<45:
                    yo4044f +=1
                elif yo>=45 and yo<50:
                    yo4549f +=1
                elif yo>=50 and yo<55:
                    yo5054f +=1
                elif yo>=55 and yo<60:
                    yo5559f +=1
                elif yo>=60 and yo<64:
                    yo6064f +=1
            elif interne.Gender == "M" :
                yo = calculate_age(interne.BD)
                if yo>=20 and yo<25:
                    yo2024m +=1
                elif yo>=25 and yo<30:
                    yo2529m +=1
                elif yo>=30 and yo<35:
                    yo3034m +=1
                elif yo>=35 and yo<40:
                    yo3539m +=1
                elif yo>=40 and yo<45:
                    yo4044m +=1
                elif yo>=45 and yo<50:
                    yo4549m +=1
                elif yo>=50 and yo<55:
                    yo5054m +=1
                elif yo>=55 and yo<60:
                    yo5559m +=1
                elif yo>=60 and yo<64:
                    yo6064m +=1
            
        df = pd.DataFrame({'Age': age_bracket, 'Male' : [yo2024m, yo2529m, yo3034m, yo3539m, yo4044m, yo4549m, yo5054m, yo5559m, yo6064m], 'Female' : [yo2024f, yo2529f, yo3034f, yo3539f, yo4044f, yo4549f, yo5054f, yo5559f, yo6064f]})
            
        #define x and y limits
        y = range(0, len(df))
        x_male = df['Male']
        x_female = df['Female']

        #define plot parameters
        fig, axes = plt.subplots(ncols=2, sharey=True, figsize=(9, 6))

        #specify background color and plot title
        fig.patch.set_facecolor('xkcd:light grey')
        plt.figtext(.5,.9,"Population Pyramid ", fontsize=15, ha='center')
                
        #define male and female bars
        axes[0].barh(y, x_male, align='center', color='royalblue')
        axes[0].set(title='Males')
        axes[1].barh(y, x_female, align='center', color='lightpink')
        axes[1].set(title='Females')

        #adjust grid parameters and specify labels for y-axis
        axes[1].grid()
        axes[0].set(yticks=y, yticklabels=df['Age'])
        axes[0].invert_xaxis()
        axes[0].grid()

        #display plot
        plt.show()



    def bibliography(self): #afficher les bibliography selon le choix : laboratoire, axe de recherche ou personnel
        entity = self.VarEntity.get() #entité choisi par l'utilisateur
        start = dt.date(int(self.Catstartyear.get()), int(self.Catstartmonth.get()), int(self.Catstartday.get())) #date debut
        end = dt.date(int(self.Catendyear.get()),int(self.Catendmonth.get()),int(self.Catendday.get())) #date fin
        Bibliography = [] #stockage de la biblio

        if entity == "Laboratory": #BIBLIOGRAPHY DU LABORATOIRE ENTIER
            for publication in self.Laboratory['Journals articles'] : #JOURNAUX
                if isinstance(publication, Journal) and publication._get_Available()> start and publication._get_Available()<end: #vérifier si la date de publication est bien comprise entre les deux dates
                    authors = '' #les auteurs
                    for i in publication.Authors :
                        authors += i.FirstName + ' ' + i.Name  + ', '
                    authors = authors[:-2]
                    Bibliography.append("{}. {}. {}. {}. {}".format(authors, publication.Available.year, publication.Title, publication.Title, publication.DOI))
            for publication in self.Laboratory['Conferences articles'] :
                if isinstance(publication, Conference):
                    authors = ''
                    for i in publication.Authors :
                        authors += i.FirstName + ' ' + i.Name  + ', '
                    authors = authors[:-2]
                    Bibliography.append("{}. {}. {} à {}".format(authors, publication.Available.year, publication.Dates, publication.Place))
            for publication in self.Laboratory['Reports'] :
                if isinstance(publication, (PhD)) and publication._get_Available()> start and publication._get_Available()<end:
                    authors = ''
                    for i in publication.Authors :
                        authors += i.FirstName + ' ' + i.Name  + ', '
                    authors = authors[:-2]
                    Bibliography.append("{}. {}. {}. Thèse. Ville : {}".format(publication.authors, publication.Available.year, publication.Title, publication.Place))#NOM, Prénom de l’auteur, année de soutenance. Titre. Thèse. Discipline. Ville : Université ou école.
                elif isinstance(publication, (Research_Project)) and publication._get_Available()> start and publication._get_Available()<end:
                    authors = ''
                    for i in publication.Authors :
                        authors += i.FirstName + ' ' + i.Name  + ', '
                    authors = authors[:-2]
                    Bibliography.append("{}. {}. {}. Thèse".format(authors, publication.Available.year, publication.Title,))#NOM, Prénom de l’auteur, année de soutenance. Titre. Thèse. Discipline. Ville : Université ou école.
                elif isinstance(publication, (Report)) and publication._get_Available()> start and publication._get_Available()<end:
                    authors = ''
                    for i in publication.Authors :
                        authors += i.FirstName + ' ' + i.Name  + ', '
                    authors = authors[:-2]
                    Bibliography.append("{}. {}. {}. Thèse".format(authors, publication.Available.year, publication.Title,))#NOM, Prénom de l’auteur, année de soutenance. Titre. Thèse. Discipline. Ville : Université ou école.
        elif entity == "Personnal" and self.Listbox2.curselection()[0] != None: #BIBLIOGRAPHY D'UN PERSONNEL : à sélectionner dans la listbox
            for element in self.Laboratory["Internals"]:
                if element.__repr__() == self.Listbox2.get(ANCHOR):
                    for publication in element.Bibliography :
                        if isinstance(publication, Journal) and publication._get_Available()> start and publication._get_Available()<end:
                            authors = ''
                            for i in publication.Authors :
                                authors += i.FirstName + ' ' + i.Name  + ', '
                            authors = authors[:-2]
                            Bibliography.append("{}. {}. {}. {}. {}".format(authors, publication.Available.year, publication.Title, publication.Mag,publication.DOI))
                        elif isinstance(publication, Conference):
                            authors = ''
                            for i in publication.Authors :
                                authors += i.FirstName + ' ' + i.Name  + ', '
                            authors = authors[:-2]
                            Bibliography.append("{}. {}. {} à {}".format(authors, publication.Available.year, publication.Dates, publication.Place))
                        elif isinstance(publication, (PhD)) and publication._get_Available()> start and publication._get_Available()<end:
                            authors = ''
                            for i in publication.Authors :
                                authors += i.FirstName + ' ' + i.Name  + ', '
                            authors = authors[:-2]
                            Bibliography.append("{}. {}. {}. Thèse. Ville : {}".format(authors, publication.Available.year, publication.Title, publication.Place))#NOM, Prénom de l’auteur, année de soutenance. Titre. Thèse. Discipline. Ville : Université ou école.
                        elif isinstance(publication, (Research_Project)) and publication._get_Available()> start and publication._get_Available()<end:
                            authors = ''
                            for i in publication.Authors :
                                authors += i.FirstName + ' ' + i.Name  + ', '
                            authors = authors[:-2]
                            Bibliography.append("{}. {}. {}. Thèse".format(authors, publication.Available.year, publication.Title,))#NOM, Prénom de l’auteur, année de soutenance. Titre. Thèse. Discipline. Ville : Université ou école.
                        elif isinstance(publication, (Report)) and publication._get_Available()> start and publication._get_Available()<end:
                            authors = ''
                            for i in publication.Authors :
                                authors += i.FirstName + ' ' + i.Name  + ', '
                            authors = authors[:-1]
                            Bibliography.append("{}. {}. {}. Thèse".format(authors, publication.Available.year, publication.Title,))#NOM, Prénom de l’auteur, année de soutenance. Titre. Thèse. Discipline. Ville : Université ou école.
        elif entity == "Research Teams" and self.Listbox0.selection() != None: #BIBLIOGRAPHY D'UN AXE DE RECHERCHE A SELECTIONNER DANS LA LISTBOX DU PREMIER ONGLET
            name, head = self.Listbox0.item(self.Listbox0.selection()[0],'values')
            for team in self.Laboratory["Research Teams"]:
                if team.Name == name :
                    author_list = list(team.TauxAppartenance)
                    print(author_list)
                    for element in self.Laboratory["Internals"]:
                        if element in author_list:
                            for publication in element.Bibliography :
                                if isinstance(publication, Journal) and publication._get_Available()> start and publication._get_Available()<end:
                                    authors = ''
                                    for i in publication.Authors :
                                        authors += i.FirstName + ' ' + i.Name  + ', '
                                    authors = authors[:-2]
                                    text="{}. {}. {}. {}. {}".format(authors, publication.Available.year, publication.Title, publication.Mag,publication.DOI)
                                    if text not in Bibliography : 
                                        Bibliography.append(text)
                                elif isinstance(publication, Conference):
                                    authors = ''
                                    for i in publication.Authors :
                                        authors += i.FirstName + ' ' + i.Name  + ', '
                                    authors = authors[:-2]
                                    text = "{}. {}. {} à {}".format(authors, publication.Available.year, publication.Dates, publication.Place)
                                    if text not in Bibliography : 
                                        Bibliography.append(text)
                                elif isinstance(publication, (PhD)) and publication._get_Available()> start and publication._get_Available()<end:
                                    authors = ''
                                    for i in publication.Authors :
                                        authors += i.FirstName + ' ' + i.Name  + ', '
                                    authors = authors[:-2]
                                    text = "{}. {}. {}. Thèse. Ville : {}".format(authors, publication.Available.year, publication.Title, publication.Place)#NOM, Prénom de l’auteur, année de soutenance. Titre. Thèse. Discipline. Ville : Université ou école.
                                    if text not in Bibliography : 
                                        Bibliography.append(text)
                                elif isinstance(publication, (Research_Project)) and publication._get_Available()> start and publication._get_Available()<end:
                                    authors = ''
                                    for i in publication.Authors :
                                        authors += i.FirstName + ' ' + i.Name  + ', '
                                    authors = authors[:-2]
                                    text = "{}. {}. {}. Thèse".format(authors, publication.Available.year, publication.Title)#NOM, Prénom de l’auteur, année de soutenance. Titre. Thèse. Discipline. Ville : Université ou école.
                                    if text not in Bibliography : 
                                        Bibliography.append(text)
                                elif isinstance(publication, (Report)) and publication._get_Available()> start and publication._get_Available()<end:
                                    authors = ''
                                    for i in publication.Authors :
                                        authors += i.FirstName + ' ' + i.Name  + ', '
                                    authors = authors[:-1]
                                    text = "{}. {}. {}. Thèse".format(authors, publication.Available.year, publication.Title)#NOM, Prénom de l’auteur, année de soutenance. Titre. Thèse. Discipline. Ville : Université ou école.
                                    if text not in Bibliography : 
                                        Bibliography.append(text)
        #Changer le titre selon l'entité choisis
        if entity == "Laboratory":
            text = '{}'.format(str(Bibliography[0]))
            for pub in Bibliography[1:] :
                text += '\n\n' + str(pub) #retour à la ligne
            TK.messagebox.showinfo(title = "Laboratory bibliography", message = text)
        elif entity == "Personnal":
            text = '{}'.format(str(Bibliography[0]))
            for pub in Bibliography[1:] :
                text += '\n\n' + str(pub)
            TK.messagebox.showinfo(title = "Personnal bibliography", message = text)
        elif entity == "Research Teams":
            text = '{}'.format(str(Bibliography[0]))
            for pub in Bibliography[1:] :
                text += '\n\n' + str(pub)
            TK.messagebox.showinfo(title = "Research teams bibliography", message = text)


    def publication_avg(self): #publication moyenne entre 2 dates d'un individu - même format que bibliography
        qty = 0 # avec un compteur
        start = dt.date(int(self.Catstartyear.get()), int(self.Catstartmonth.get()), int(self.Catstartday.get()))
        end = dt.date(int(self.Catendyear.get()),int(self.Catendmonth.get()),int(self.Catendday.get()))
        author = ''
        if self.Listbox2.curselection()[0] != None:
            for element in self.Laboratory["Internals"]:
                if element.__repr__() == self.Listbox2.get(ANCHOR) :
                    author = str(element.FirstName) + ' ' + str(element.Name)
                    for publication in element.Bibliography :
                        if publication._get_Available()> start and publication._get_Available()<end:
                            qty +=1
            print("{} publication average : {}".format(author, qty))
            TK.messagebox.showinfo(title = "{} bibliography".format(author), message="{} publication average from {} to {} : {}".format(author, start, end, qty))




    def articles_collab_rate(self):
        #si on cherche le nb d'articles en collab avec des personnels externes
        news = len(self.Laboratory["Journals articles"]); conf = len(self.Laboratory["Conferences articles"])
        total =  news + conf #total de publications
        counter = 0  #compteur
        for article in self.Laboratory["Journals articles"]:
            external = False
            for author in article.Authors :
                if isinstance(author,External):
                    external = True
                    counter +=1
                    break
        for article in self.Laboratory["Conferences articles"]:
            for author in article.Authors :
                if isinstance(author,External):
                    counter +=1
                    break
        res = counter/total * 100
        print(res)
        TK.messagebox.showinfo(title  = "Articles rate", message = "Articles written in collaboration with external members : {} %".format(str(res))) 
            
    
    def PhD_collab_rate(self):
        #si on cherche le nb d'articles co-encadré par des personnels externes
        phd = len(self.Laboratory["PhD"])
        total =  phd
        counter = 0
        for thesis in self.Laboratory["PhD"]:
            external = False
            for author in list(thesis.Supervisors.keys()) :
                if isinstance(author,External):
                    external = True
                    counter +=1
                    break
        res = counter/total * 100
        print(res)
        TK.messagebox.showinfo(title  = "PhD rate", message ="PhD supervised by external members rate : {} %".format(str(res)))
            
    def PhD_avg_pub(self): #nombre de publication durant leur thèse
        if self.Listbox2.curselection()[0] != None:
            startstr = ''
            endstr = ''
            for element in self.Laboratory["Internals"]:
                if element.__repr__() == self.Listbox2.get(ANCHOR) :
                    total = len(element.Bibliography)
                    counter = 0
                    for project in element.PhD :
                        if project.DefenseDate != None :
                            start = project.Start ; startstr = str(start.year) + "/" + str(start.month) + '/' + str(start.day)
                            end = project.DefenseDate ; endstr = str(end.year) + "/" + str(end.month) + '/' + str(end.day)
                            qty = 0
                            for publication in element.Bibliography :
                                if publication.Available > start and publication.Available < end:
                                    qty += 1
                            counter += qty
            res=counter/total*100
            print(res)
            TK.messagebox.showinfo(title  = "Publications on their PhD time", message ="Publication rate from {} to {} : {} ".format(startstr, endstr, str(res)))



Interface().Laboratory

    
'''

#créer une premiere fenêtre
splash = TK.Tk()
#splash.title("Research lab app - Welcome") #nom de la fenêtre
splash.overrideredirect(True)
splash.geometry("480x360")
splash.minsize(480,360)
splash.maxsize(720,480)
splash.iconbitmap("/Users/laetitia/Desktop/PROJET_MINI_POO/AM.ico")
splash.config(background = '#961364')

#creation d'image
#
#

#frame
frame = TK.Frame(splash)
frame.pack(expand='YES')

#ajouter un premier texte
welcome = TK.Label(frame, text = "Welcome to the lab app !", font = ("Courrier", 40), fg = '#FF8728', bg= '#961364' )
welcome.pack()

#main window
def main_window():
    #fermeture de l'écran splash
    splash.destroy()
    
    #configuration de la fenêtre
    main = TK.Tk()
    main.title("Research lab app - Main screen") #nom de la fenêtre
    main.geometry("480x360")
    main.minsize(480,360)
    main.maxsize(720,480)
    main.iconbitmap("/Users/laetitia/Desktop/PROJET_MINI_POO/AM_logo.ico") #logo à changer
    main.config(background = '#961364') 
    
    # welcome = TK.Label(main, text = "Main screen", font = ("Courrier", 25), fg = '#FF8728', bg= '#961364' )
    # welcome.pack(pady=5)
    
    
    def Add_Staff():
        mylabel = TK.Label(main, text= e.get()).grid(row=1, column=4)
    
    
    
    # TODO 2 Créer le bouton charger XML et lui associer la bonne procédure
    
    TK.Button(main, text = "XML Uploading").grid(row=0,column=0, columnspan=5, sticky = "w e n s", padx=5, pady=5)
    
    TK.Label(main, text = "Project Name", bg = '#961364', fg = 'white').grid(row=1, column=3, sticky = 'W',padx = 5, pady = 5)
    TK.Label(main, text = "Date",  bg = '#961364', fg = 'white').grid(row=2, column=3, sticky = 'W',padx = 5, pady = 5)
    
    VarProject = TK.StringVar()
    VarDate = TK.StringVar()
    
    # TODO 2 Créer les deux zone de texte (entry) associées aux variables définies ci-dessus et les positionner dans la grille.
    TK.Entry(main, textvariable = VarProject).grid(row=1, column=4)
    TK.Entry(main, textvariable = VarDate).grid(row=2, column=4)
    
    Listbox = TK.Listbox(main)
    # TODO2 positionner cette zone de liste
    Listbox.grid(row=1,column=1,rowspan=3)
    
    # TODO 2 Créer le bouton ajouter une note, puis lui associer la bonne procédure
    # TODO 2 Créer le bouton enregistrer XML, puis lui associer la bonne procédure
    TK.Button(main, text = "Add project", command = Add_Staff).grid(row=3,column=3, columnspan=2)
    TK.Button(main, text = "Upload", bg = '#FF8728').grid(row=4,column=2, columnspan=3)
    
    main.mainloop()


    
    
#splash screen timer 
splash.after(3000, main_window)'''



