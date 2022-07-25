import sys
import csv
import requests
import fileinput
from itertools import zip_longest 
import os
import pandas as pd

# from tkinter import *
from tkinter import Tk
from tkinter import Frame
from tkinter import Listbox
from tkinter import Checkbutton
from tkinter import Radiobutton
from tkinter import OptionMenu
from tkinter import Label
from tkinter import Button
from tkinter import BOTTOM
from tkinter import TOP
from tkinter import LEFT
from tkinter import RIGHT
from tkinter import IntVar
from tkinter import StringVar
from tkinter import END

from pandas.core import frame

import tkinter as tk
import tkinter.filedialog as fd
import json
from pathlib import Path
from sys import exit
from copy import deepcopy

import argparse
from pathlib import Path
from argparse import ArgumentParser
import os.path

# version 1.33

#Changelog 1.33 changes
# Re-removed reading in cons.csv as utf-8-sig to ensure as it caused a weird character to be added to the first header if it was run on windows. Only required on initial reading of data
# Added examples


# KNOWN Bugs

# - If you export json file with all your settings, you will be unable to re-export the json file.
# -- Interim work around is to take a screenshot your settings and re-create the json and then import it and re-export it will work just not update the list display. All relevant settings should be displayed on the main window.
# 
# - If you import a json and import the json file a second time it will duplicate eveything other than the files listed in the file display window.
# --  The json file stays loaded and shouldn't need to reload the same json file. Close the application and re-open if you need to use a different json. 
# -- Alternativly pass the json in via commandline and it will automatically parse and process the request without any gui interaction required


# TO DO
# - Add option to convert xlsx to csv. If so maybe have them choose which worksheet to export. or just read in the data directly and choose the worksheet. So if it' a worksheet a tab comes up to select the worksheet. Still from Excel formater on having the worksheet and checking.
# - Convert use of global variables to being variables passed through to the classes.
# - Convert using dynamic global variables to using objects.
# - Add functionality to pull data from SQLite DB. So that you can compare against various CSV data and data you have in a DB

root = Tk()
root.title('Compare Match    v1.32')


class JSettings:
    """
    This class manages the methods used for importing and exporting json settings file.

    :param fileList: This is the list of files to compare.
    :param current_column: This is the column headers in each of csv files that contains the data to be compared.
    """

    def __init__(self,fileList,current_column):
        self.fileList = fileList
        self.current_column = current_column
              
    def importj(self, file_location= "", nogui=False): #imports json file. nogui arguement is used if you want to load and immediately submit using a json file
        """
        This function imports json file containing the settings saved from a previous session.
        
        :param file_location: This is the location of the files to import.
        :param nogui: This is used when loading the json via the commandline and bypassing the gui. If the value is set to False will skip the GUI and automatically process the request after loading the json.
        """
                
        global toAddList_nonsymbol
        global fullListfName
        if nogui == False:
            file_location = fd.askopenfilename(parent=root, title='Choose json file to import')
   
        f = open (file_location)
        settings_import = json.load(f)

 
        case_sensitive_v.set(settings_import['case_sensitive'])
        multiple_files_v.set(settings_import['multiple_files'])
        machineable_v.set(settings_import['machineable'])
        all_files.fileList = (settings_import['fileList'])
        to_import_current_column = (settings_import['current_column'])      
        export_columns = (settings_import['export_columns'])
       
        toAddList_nonsymbol = (settings_import['toAddList_nonsymbol'])
  
        fileDisplay.delete(0,'end')  # ensures list of files is cleared when importing a json file

        for i, fNames in enumerate(all_files.fileList):
            temp = os.path.basename(fNames)                   
            temp = os.path.basename(fNames)
            temp = os.path.splitext(temp)[0]
            fileDisplay.insert(END,temp)
            fullListfName.append(temp)

            with open(fNames, 'r',newline='',encoding='utf-8-sig') as f: # gets list of headers to allow choice of which column to compare
                reader = csv.reader(f)
                headers = next(reader)
                    
                f.close()

            all_files.current_column.append(StringVar()) # 
            all_files.current_column[i].set(to_import_current_column[i])

            choices = set(headers)  
  
            popupMenu = OptionMenu(frame, all_files.current_column[i], *choices)
            Label(frame, text="Column Headers").pack
            popupMenu.pack()
   
  
        for items in export_columns:
            finalColumnDisplay.insert(END,items)
                    

  
    def exportj(self):
        """This function exports the various settings and file lists to a json file."""


        to_export_current_column = []


        for i in range(len(all_files.current_column)):
            to_export_current_column.append(all_files.current_column[i].get())

        settings_export = {'case_sensitive':case_sensitive_v.get(),'multiple_files':multiple_files_v.get(),'machineable': machineable_v.get(),'fileList':all_files.fileList,'current_column':to_export_current_column,'export_columns': export_columns,'toAddList_nonsymbol': toAddList_nonsymbol}
        file_types = [('JSON', '*.json*')]
        file_location = fd.asksaveasfile(defaultextension='.json', filetypes=[("json files", '*.json')], title="Choose filename")
        
        with open(file_location.name, "w") as f: 

            json.dump(settings_export, f)      

      

class InputFiles:
    """
    This class for loading input files and grabbing initial headers to allow for choice of column to compare.
    
    :param fileList: This is the list of files to compare.
    :param current_column: This is the column headers in each of csv files that contains the data to be compared.
    """

    def __init__(self,fileList,current_column):
        self.fileList = fileList
        self.current_column = current_column

    def load_files(self):
        """This function is used for loading the files into the file list and allowing you to choose which headers in each csv file you wish to compare. """
        
        new_filez = fd.askopenfilenames(parent=root, title='Choose a file')

        previousState = len(self.fileList) 
        
        tempListing = []
        tempListing = deepcopy(self.fileList)
        tempNewFiles = deepcopy(new_filez)

        new_filez_list = [*tempNewFiles]
        fileList_list = list(tempListing)
        
        duplicated_fileList = fileList_list + new_filez_list
        unique_fileList = []

        for item in duplicated_fileList: # used to ensure the display list stays in the same order as previous so it matches with previous drop column headers
            if item not in unique_fileList: unique_fileList.append(item)
     
        self.fileList = tuple(unique_fileList) 

        fileDisplay.delete(0,'end') # clears previous files in the file display, and adds new items. This is to prevent duplication
        for i, fNames in enumerate(self.fileList):
            global fullList  # to-do convert to passing in the variable instead of using global
            temp = os.path.basename(fNames)                    
            temp = os.path.basename(fNames)
            temp = os.path.splitext(temp)[0]
            fileDisplay.insert(END,temp)
            fullListfName.append(temp)
            if len(current_column) <= i:

                with open(fNames, 'r',newline='',encoding='utf-8-sig') as f: # displays drop down list of headers in CSV file to choose which column to compare
                    reader = csv.reader(f)
                    headers = next(reader)
                    
                    f.close()
                    
                current_column.append(StringVar()) 
                current_column[i].set(headers[0])
                choices = set(headers)
                popupMenu = OptionMenu(frame, current_column[i], *choices)
                Label(frame, text="Column Header").pack
                popupMenu.pack()#side = BOTTOM



class ProcessFiles:
    """This class manages processing the files and doing the comparing of data once the submit button has been clicked.

    :param fileList: This is the list of files to compare
    """
    
    def __init__(self, fileList):
        self.fileList = fileList

    def processing(self):
        """This function is for processing the files and comparing the data based on the settings that were previously chosen."""
        
        if machineable_v.get() == 1: 
            in_symbol = "A"
            not_in_symbol = "M"
        else:
            in_symbol = "+"
            not_in_symbol = "-"            


        tempIterator = 0

        notInList = []
      
        toAddList_nonsymbol_lower = [[x.lower() for x in sublst] for sublst in toAddList_nonsymbol]
        fullListfName_lower = [item.lower() for item in fullListfName]
        for combinations in toAddList_nonsymbol_lower:
               
            for i, fNames in enumerate(toAddList_nonsymbol_lower[tempIterator]):
                

                if i == 0:
                    notInList.append([])
                    notInList[tempIterator] = str(toAddList_nonsymbol_lower[tempIterator][i])
                else:
                    notInList[tempIterator] = (str(notInList[tempIterator]) + in_symbol + str(toAddList_nonsymbol_lower[tempIterator][i]))
                
            for i, fNames in enumerate(fullListfName_lower):
                if fNames not in toAddList_nonsymbol_lower[tempIterator]:
                    notInList[tempIterator] = str(notInList[tempIterator]) + not_in_symbol + fNames.lower()
                              
            tempIterator = tempIterator + 1

        lower_notInList = [x.lower() for x in notInList]
        
        lg = 0
        masterList = []
        processing_header = []

        # adding items to list to compare from each file. "list" list is used to store values from the volumes. "file" list used to store file name to use as headers
        for line in csv.reader(fileinput.input(files=all_files.fileList,openhook=fileinput.hook_encoded("utf-8-sig"))): 
            if fileinput.filelineno() == 1:
                lg = lg + 1
                processing_header = line
                processing_header_index = processing_header.index(all_files.current_column[lg-1].get())

                globals()['list'+str(lg)] = [] # used to store lists
                globals()['file'+str(lg)] = fileinput.filename()
                globals()['file'+str(lg)] = os.path.basename(globals()['file'+str(lg)].replace(".csv",""))
                globals()['file'+str(lg)] = globals()['file'+str(lg)].lower()    
                continue

            if case_sensitive_v.get() == 1:    # <---------------------------------------CASE SENSITIVE CHECKBOX
                masterList.append(line[processing_header_index])
                globals()['list'+str(lg)].append(line[processing_header_index])
            
            else:    # <---------------------------------------CASE SENSITIVE CHECKBOX   
                masterList.append(line[processing_header_index].lower().rstrip().lstrip())
                globals()['list'+str(lg)].append(line[processing_header_index].lower().rstrip().lstrip())

        masterSet = set(masterList)
        masterDict = dict.fromkeys(masterSet,"")

        ## Add Matches to cols (FileName+)

        x = 0
        i = 1
        lg_extra = lg + 1
        while i <= lg:
            matchesSet = masterSet & set(globals()['list'+str(i)])
            matches = list(matchesSet)
            while x < len(matches): 
                if machineable_v.get() == 1:    # <---------------------------------------Machineable CHECKBOX  
                    masterDict[matches[x]] += str(globals()['file'+str(i)]) + in_symbol 
                else:    # <---------------------------------------Machineable CHECKBOX  
                    masterDict[matches[x]] += str(globals()['file'+str(i)]) + in_symbol
                                
                if i == lg:
                    masterDict[matches[x]] = masterDict[matches[x]][:-1] # removes the last +/addition character if it's on all files
                x += 1

            x = 0
            i += 1
  

        
        ## Add differeces to cols (-FileName)

        x = 0
        i = 1
        lg_extra = lg + 1
        while i <= lg:
            matchesSet = masterSet - set(globals()['list'+str(i)])
            differences = list(matchesSet)
            while x < len(differences): 
                if machineable_v.get() == 1: # <---------------------------------------Machineable CHECKBOX
                    last_char = masterDict[differences[x]][-1]
                    if last_char == in_symbol:  # changed + to A for Evie's script
                        masterDict[differences[x]] = masterDict[differences[x]][:-1]
                    masterDict[differences[x]] += not_in_symbol + str(globals()['file'+str(i)]) ## Move the minus to the start after.  changed - to M for Evie's script
                    x += 1
                else: # <---------------------------------------Machineable CHECKBOX
                    last_char = masterDict[differences[x]][-1]
                    if last_char == in_symbol:  # changed + to A for Evie's script
                        masterDict[differences[x]] = masterDict[differences[x]][:-1]
                    masterDict[differences[x]] += not_in_symbol + str(globals()['file'+str(i)]) ## Move the minus to the start after.  changed - to M for Evie's script
                    x += 1
            x = 0
            i += 1


        consDict = {}
        for pair in masterDict.items():
            if pair[1] not in consDict.keys():
                consDict[pair[1]] = []

            consDict[pair[1]].append(pair[0])

        with open('cons.csv', 'w', newline='') as f: # completed compare, but in rows instead of columns. Didn't have encoding added before recently added
            c = csv.writer(f)

            for key, value in consDict.items():
                c.writerow([key] + value)


        with open('cons.csv') as infile, \
                open('final.csv', 'w', newline='') as outfile: # transposes rows into columns. Didn't have encoding added before recently added
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            writer.writerows(zip_longest(*reader, fillvalue=''))
        

        df2 = pd.read_csv('final.csv', dtype = str, skipinitialspace=True)

        filtered_columns = list(set(notInList) & set(df2.columns))


        df2 = df2[filtered_columns]
     
        if notInList == []:
      
            if multiple_files_v.get() == 1: # <---------------------------------------MultiFile CHECKBOX
                df1 = pd.read_csv('final.csv', dtype = str)
                for column in df1.columns:
                    df1[column].to_csv(column + '.csv',index=False)


        elif not notInList == [] and filtered_columns == []:
        
            with open('filtered_final.csv', 'w', newline='') as f: # csv file containing only the filtered list
                c = csv.writer(f)
                c.writerow("No Matches")
        

        else:

            df3 = pd.read_csv('final.csv', dtype = str, skipinitialspace=True, usecols=filtered_columns)
            df3.to_csv('filtered_final.csv', encoding='utf-8',index = False)

            if multiple_files_v.get() == 1: # <---------------------------------------MultiFile CHECKBOX

                df1 = pd.read_csv('filtered_final.csv', dtype = str)

                for column in df1.columns:
                    df1[column].to_csv(column + '.csv',index=False)





        if os.path.exists("cons.csv"): # delete cons.csv was the initial final.csv but in rows. No longer needed once transposed to columns
            os.remove("cons.csv")
        else:
            print("The file does not exist")            



def get_selection_fileDisplay():
    """This function is used for adding the selections from the Listbox field to the second Listbox field showing the different combinations you have selected. """

    global AddListIterator
    sel_list = []
    toAddList = ""
      
    pj = 0
    sel_list.append(fileDisplay.curselection())
    AddListIterator = AddListIterator + 1
    toAddList_nonsymbol.append([]) 
    for pj,i in enumerate(sel_list[0]):
         
        index_locator = all_files.fileList[int(i)]
        index_locator = (index_locator,)
        for ij, fNames in enumerate(index_locator):
            
            temp = os.path.basename(fNames)                    
            temp = os.path.basename(fNames)
            temp = os.path.splitext(temp)[0]
            if pj == 0:
                toAddList = toAddList + temp
                toAddList_nonsymbol[AddListIterator].append(temp)
            else:
                toAddList = toAddList + "+" + temp
                toAddList_nonsymbol[AddListIterator].append(temp)
    finalColumnDisplay.insert(END,toAddList)
    export_columns.append(toAddList)


toAddList_nonsymbol = []
AddListIterator = -1
fileList = {}
fullListfName = []
current_column = []
export_columns = []
all_files = InputFiles(fileList,current_column)
toProcessFiles = ProcessFiles(fileList)
toImportExport = JSettings(fileList,current_column)

#loading frames

frame = Frame(root) 
frame.pack()
middleframe = Frame(root)
middleframe.pack( side = BOTTOM )
bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )

# loading button variables
radioChoice = IntVar()
case_sensitive_v = IntVar()
multiple_files_v = IntVar()
machineable_v = IntVar()

# loading buttons
actioncheckb1 = Checkbutton(frame, text="Case Sensitive match", variable=case_sensitive_v)
actioncheckb1.pack(side=tk.LEFT)
actioncheckb2 = Checkbutton(frame, text="Mutliple exported files", variable=multiple_files_v)
actioncheckb2.pack(side=tk.LEFT)
actioncheckb3 = Checkbutton(frame, text="Machineable(A/M vs +/-)", variable=machineable_v)
actioncheckb3.pack(side=tk.LEFT)



importj = Button(middleframe,
                   text="Import Settings",
                   command= lambda: toImportExport.importj())
importj.pack(side=tk.LEFT)

exportj = Button(middleframe, 
                   text="Export Settings", 
                   command=lambda: toImportExport.exportj())
exportj.pack(side=tk.LEFT)




browsebutton = Button(bottomframe,
                   text="Browse",
                   command= lambda: all_files.load_files())
browsebutton.pack(side=tk.LEFT)

submit = Button(bottomframe, 
                   text="Submit", 
                   command=lambda: toProcessFiles.processing())
submit.pack(side=tk.LEFT)

qbutton = Button(bottomframe, 
                   text="QUIT", 
                   fg="red",
                   command=exit)
qbutton.pack(side=tk.LEFT)


match_select_button = Button(frame,
                   text="Choose Combination",
                   command= lambda: get_selection_fileDisplay())
match_select_button.pack(side=tk.BOTTOM)
 
fileDisplay = Listbox(frame, selectmode = "multiple", height=30, width=30) # Frames will resize however buttons will vanish if you go smaller than whatever this frame is set to for height
fileDisplay.pack(side=tk.LEFT)

finalColumnDisplay = Listbox(frame, height=30, width=30) # Frames will resize however buttons will vanish if you go smaller than whatever this frame is set to for height
finalColumnDisplay.pack(side=tk.RIGHT)


# used to auto import and parse of json
parser = argparse.ArgumentParser()

parser.add_argument("file_path", nargs='?', type=Path, default='-')
p = parser.parse_args()


if p.file_path.exists() == True:
    
    toImportExport.importj(file_location = p.file_path,nogui=True)
    toProcessFiles.processing()
    exit()

else:
    
    print("loading without imported json")

root.mainloop()
