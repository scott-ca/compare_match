# compare_match

### **Current version: 1.33**

# **Summary**

compare_match is a tool for comparing multiple csv files with each other providing you with an exported list where the entries in the various csv files exist within each other. The tool does a multi-directional compare with all included files, and not a single file compared to multiple file.

Any settings chosen the tool including file locations can be saved to a json file. This can later be used to import to allow for quick comparisons that require the same settings. IE. reoccurring monthly comparisons between various systems that contain names or devices. Since the systems providing the export will have files with the same names and formatting the same json file can be used on them to compare the values.

The json file can also be used as an argument via command line (no flags required) to automatically load settings and process the required files.

# **Overview**


When launching the tool you will be provided with a GUI interface similar to the one shown below.

![compare_match](https://user-images.githubusercontent.com/59944183/128587587-02895559-aab5-4f46-83b2-2fffac4bee71.png)


When comparing files a csv file called final.csv will be created. It will have columns containing the files the values were matched in. Between all the columns a value will only be listed in one column. This is because the columns are separated by which files they are apart of, in addition to which files they are not included in. It will list all files separated by a "+" at the start of the file name (except the first filename) and a minus prior to any files that they weren't part of.

Some examples with the column headers are below

"test1+test2+test4-test3" - Entries in this column were found in test1,test2,test4, but not in test3.
"test1-test2-test3-test4" - Entries in this column were only found in test1.
"test2+test4-test1-test3" - Entries found in this column were only found in test2 and test4 and were not in test 1 or test3.

By default no files or combinations will be listed in the display windows, in addition the middle section between the two display windows with the column headers in the above screenshot will also be blank.

You will want to select browse and choose the files to compare. They the files being compared can be in different directories, and can be added either by highlighting all files and choosing open or by adding some files and choosing browse again and adding the remaining files. When a file is selected, it will show a drop down next to the file. This drop down will show all the headers in the file. Select the header matching the column in the selected csv that you wish to compare values against.

Once you have selected all of your files you will want to select the combination of matches you wish to view. By default if you don't choose any, it will select all possible combinations.

To select a combination click on each of the files you wish to know that they ONLY exist in those files (and not in the unselected files) and choose combination. You can do this any number of times. They will show up in the second display area similar to the above screenshot.

***Please note, by default you will have a file called final.csv created that has all matches. However, if you choose to view only specific combinations you will get an additional file called filtered_final.csv that will contain only the selected combinations* 

You have three additional options on the left hand side to choose from. You can choose any combination of these options, and are not limited to choosing which one suites your needs.

**Case Sensitive match** - This will only consider values that match the same case to be grouped together. If this is not selected all values in the column will be converted to lower case to match values that may not be in the same letter casing due to the various systems they were exported from. 

**Multiple exported files** - This will create additional files matching the names of the columns in final.csv. In the example in the screenshot above you would get 3 additional files containing the values only in their columns. The files would be named "test1+test2+test4-test3.csv", "test1-test2-test3-test4.csv", "test2+test4-test1-test3.csv"

**Machinable** - This changes the file headers to replace +/- symbols with A/M symbols. This is to allow for other systems that may take the export as an import that may not accept those characters. This will update the file names if used in conjunction with the "Multiple exported files" option. In addition while the filenames are automatically converted to lowercase, the A/M characters would remain capital letters to allow them to be identified with words that may have those letters in the file name.

If you wish to create a json file to save the selected settings, file locations, column headers click the save button. You will be prompted for a name and location to save the file.

This file can later be used to return you to the current state and allow you to process the comparison. As briefly mentioned in the initial summary, this is useful if you receive regular exports from various systems in csv format and you would like to use the tool to audit between the systems. IE. reoccurring monthly comparisons between various systems that contain employee names or computer names. Given that systems providing csv exports typically give you the files in the same format with the same headers, the settings saved in the json will be true in the new files as well. If you use this method, ensure you save the new csv files to the same location as that information is saved in the json file.

The json file can also be used as an argument via command line (no flags required) to automatically load settings and process the required files. This can be done by running "compare_match.py settings.json"

# **IMPORTANT NOTE**

You can compare files in directories outside of the one the tool is located in, the same is true for the json file. However, the output files containing the results will be create in the directory it is run from. The three main file names you will want to ensure aren't in the same directory as where this is run from is "cons.csv", "final.csv", "final_filtered.csv". The first two files will always be created, and the cons.csv will be deleted once the comparison is completed. final_filtered.csv is created if you choose to have only specific comparison combinations shown.

The only other files that are created are files that happen to share the same name as all the file names being used split by either "+"/"-"/"A"/"M" this will vary by any given comparison. These files will also only be created if you choose the "Multiple files exported".
**Changelog 1.33 changes**
-Re-removed reading in cons.csv as utf-8-sig to ensure as it caused a weird character to be added to the first header if it was run on windows. Only required on initial reading of data
- Added examples

# **Known Bugs**

- If you export json file with all your settings, you will be unable to re-export the json file.
- Interim work around is to take a screenshot your settings and re-create the json and then import it and re-export it will work just not update the list display. All relevant settings should be displayed on the main window.
- If you import a json and import the json file a second time it will duplicate eveything other than the files listed in the file display window.
-  The json file stays loaded and shouldn't need to reload the same json file. Close the application and re-open if you need to use a different json. 
- Alternativly pass the json in via commandline and it will automatically parse and process the request without any gui interaction required


# **TO DO**
 Add option to convert xlsx to csv. If so maybe have them choose which worksheet to export. or just read in the data directly and choose the worksheet. So if it' a worksheet a tab comes up to select the worksheet. Still from Excel formater on having the worksheet and checking.
- Convert use of global variables to being variables passed through to the classes.
- Convert using dynamic global variables to using objects.
- Add functionality to pull data from SQLite DB. So that you can compare against various CSV data and data you have in a DB



**I am happy to hear any feedback including but not limited to any features that you may like to see added. I won't make any commitments to add any of the features, however I will review them and should time allow see which features I may be able to implement.**


