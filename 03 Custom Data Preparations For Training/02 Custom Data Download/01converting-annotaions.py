

"""
Course:  Training YOLO v3 for Objects Detection with Custom Data

Section-4
Creating Custom Dataset in YOLO format
File: converting-annotations.py
"""


# Converting annotations written in csv file into YOLO format
#
# Algorithm:
# Setting up full paths --> List of classes' names -->
# --> Getting encrypted strings -->
# --> Loading initial dataFrame with needed rows -->
# --> Calculating numbers for YOLO format -->
# --> Saving annotations in txt files
#
# Result:
# txt files next to every image with annotations in YOLO format


# Importing needed libraries
# Install Pandas by running one of the following in command line:
# conda install -c anaconda pandas
# or
# pip install pandas
# Don't forget to activate Python v3 environment
import pandas as pd
import os


"""
Start of:
Setting up full paths to directories
"""

# Full or absolute path to the folder with csv annotation files
# Find it with second Py file getting-full-path.py
# Pay attention! If you're using Windows, yours path might looks like:
# r'C:\Users\my_name\OIDv4_ToolKit\OID\csv_folder'
# or:
# 'C:\\Users\\my_name\\OIDv4_ToolKit\\OID\\csv_folder'
full_path_to_csv = 'C:\\Users\\Rishav\\OIDv4_ToolKit\\OID\\csv_folder'

# Full or absolute path to the folder with images
# Find it with second Py file getting-full-path.py
# Pay attention! If you're using Windows, yours path might looks like:
# r'C:\Users\my_name\OIDv4_ToolKit\OID\Dataset\train\Car_Bicycle wheel_Bus'
# or:
# 'C:\\Users\\my_name\\OIDv4_ToolKit\\OID\\Dataset\\train\\Car_Bicycle_wheel_Bus'
full_path_to_images = \
    'C:\\Users\\Rishav\\OIDv4_ToolKit\\OID\\Dataset\\train\\Car_Bicycle_wheel_Bus'

"""
End of:
Setting up full paths to directories
"""


"""
Start of:
List of classes' names
"""

# Defining list for names of classes
# Names has to be spelled correctly
# in the same way they are written in Open Images Dataset
# It is possible to specify as many classes as you downloaded
# It is not needed to use bottom dash
# if class's name consists of two words






#Specify classes That you downloaded with OIDv4
labels = ['Car', 'Bicycle wheel', 'Bus']

"""
End of:
List of classes' names
"""


"""
Start of:
Getting encrypted strings of classes' names
"""

# Reading csv file with classes' names
# Loading two first columns [0, 1] into Pandas dataFrame
# Pay attention! If you're using Windows, it might need to change
# this: + '/' +
# to this: + '\' +
# or to this: + '\\' +
classes = pd.read_csv(full_path_to_csv + '/' + 'class-descriptions-boxable.csv',
                      usecols=[0, 1], header=None)

# Check point
# Showing first 5 rows from the dataFrame
# print(classes.head())

# Defining list for saving encrypted strings
encrypted_strings = []

# Getting encrypted string for every class
# Going through all labels
for v in labels:
    # Getting Pandas sub-dataFrame that has only one row
    # By using 'loc' method we locate needed row
    # that satisfies condition 'classes[1] == v'
    # that is 'find from the 1st column element that is equal to v'
    sub_classes = classes.loc[classes[1] == v]
    # print(sub_classes)  # 570  /m/0k4j  Car

    # Getting element from the first row and first column
    e = sub_classes.iloc[0][0]
    # print(e)  # /m/0k4j

    # Appending found encrypted string into the list
    encrypted_strings.append(e)

# Check point
# Showing initial list with labels and corresponding encrypted strings
# print()
# print(labels)
# print(encrypted_strings)

"""
End of:
Getting encrypted strings of classes' names
"""


"""
Start of:
Getting Pandas dataFrame with annotations that has only needed rows
"""

# Reading csv file with annotations
# Loading only needed columns into Pandas dataFrame
# Pay attention! If you're using Windows, it might need to change
# this: + '/' +
# to this: + '\' +
# or to this: + '\\' +
annotations = pd.read_csv(full_path_to_csv + '/' + 'train-annotations-bbox.csv',
                          usecols=['ImageID',
                                   'LabelName',
                                   'XMin',
                                   'XMax',
                                   'YMin',
                                   'YMax'])

# Check point
# Showing first 5 rows from the dataFrame
# print(annotations.head())

# Getting Pandas dataFrame that has only needed rows
# By using 'loc' method we locate needed rows
# that has only needed 'encrypted_strings'
# By using copy() we create separate dataFrame
# not just a reference to the initial one
# and, in this way, initial dataFrame will not be changed
sub_ann = annotations.loc[annotations['LabelName'].isin(encrypted_strings)].copy()

# Check point
# Showing first 5 rows from the dataFrame
# print()
# print(sub_ann.head())

"""
End of:
Getting Pandas dataFrame with annotations that has only needed rows
"""


"""
Start of:
Calculating numbers for YOLO format
"""

# Adding new empty columns to dataFrame to save numbers for YOLO format
sub_ann['classNumber'] = ''
sub_ann['center x'] = ''
sub_ann['center y'] = ''
sub_ann['width'] = ''
sub_ann['height'] = ''

# Going through all encrypted classes' strings
# and converting them to numbers
# according to the order they are in the list
for i in range(len(encrypted_strings)):
    # Writing numbers into appropriate column
    sub_ann.loc[sub_ann['LabelName'] == encrypted_strings[i], 'classNumber'] = i

# Calculating bounding box's center in x and y for all rows
# Saving results to appropriate columns
sub_ann['center x'] = (sub_ann['XMax'] + sub_ann['XMin']) / 2
sub_ann['center y'] = (sub_ann['YMax'] + sub_ann['YMin']) / 2

# Calculating bounding box's width and height for all rows
# Saving results to appropriate columns
sub_ann['width'] = sub_ann['XMax'] - sub_ann['XMin']
sub_ann['height'] = sub_ann['YMax'] - sub_ann['YMin']

# Getting Pandas dataFrame that has only needed columns
# By using 'loc' method we locate here all rows
# but only specified columns
# By using copy() we create separate dataFrame
# not just a reference to the previous one
# and, in this way, initial dataFrame will not be changed
r = sub_ann.loc[:, ['ImageID',
                    'classNumber',
                    'center x',
                    'center y',
                    'width',
                    'height']].copy()

# Check point
# Showing first 5 rows from the dataFrame
# print(r.head())

"""
End of:
Calculating numbers for YOLO format
"""


"""
Start of:
Saving annotations in txt files
"""

# Check point
# Getting the current directory
# print(os.getcwd())

# Changing the current directory
# to one with images
os.chdir(full_path_to_images)

# Check point
# Getting the current directory
# print(os.getcwd())

# Using os.walk for going through all directories
# and files in them from the current directory
# Fullstop in os.walk('.') means the current directory
for current_dir, dirs, files in os.walk('.'):
    # Going through all files
    for f in files:
        # Checking if filename ends with '.jpg'
        if f.endswith('.jpg'):
            # Slicing only name of the file without extension
            image_name = f[:-4]
            # Getting Pandas dataFrame that has only needed rows
            # By using 'loc' method we locate needed rows
            # that satisfies condition 'classes['ImageID'] == image_name'
            # that is 'find from the 1st column element
            # that is equal to image_name'
            sub_r = r.loc[r['ImageID'] == image_name]

            # Getting resulted Pandas dataFrame that has only needed columns
            # By using 'loc' method we locate here all rows
            # but only specified columns
            # By using copy() we create separate dataFrame
            # not just a reference to the previous one
            # and, in this way, initial dataFrame will not be changed
            resulted_frame = sub_r.loc[:, ['classNumber',
                                           'center x',
                                           'center y',
                                           'width',
                                           'height']].copy()

            # Preparing path where to save txt file
            # Pay attention! If you're using Windows, it might need to change
            # this: + '/' +
            # to this: + '\' +
            # or to this: + '\\' +
            path_to_save = full_path_to_images + '/' + image_name + '.txt'

            # Saving resulted Pandas dataFrame into txt file
            resulted_frame.to_csv(path_to_save, header=False, index=False, sep=' ')

"""
End of:
Saving annotations in txt files
"""


"""
Some comments

When reading csv file by 'pd.read_csv', and loading it into Pandas dataFrame,
it is possible to load only specific columns:
    usecols=[0, 1]
    usecols=['ImageID', 'LabelName']
It can be useful, when csv file has a large number of columns,
but we need to load a sub-dataFrame of some of the columns.
As a parameter in usecols, can be passed either a list of strings,
according to the columns' names, or a list of integers,
according to columns' indexes.
"""
