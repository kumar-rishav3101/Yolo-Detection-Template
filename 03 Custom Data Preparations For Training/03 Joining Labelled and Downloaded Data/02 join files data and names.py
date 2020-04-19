
"""
Course:  Training YOLO v3 for Objects Detection with Custom Data

Section-4
Creating Custom Dataset in YOLO format
File: joined-files-data-and-name.py
"""


# Creating files joined_data.data and classes.names
# for training in Darknet framework
#
# Algorithm:
# Setting up full paths -->
# --> Reading files classes.names from labelled and downloaded data -->
# --> Creating file classes.names for joined data -->
# --> Creating file joined_data.data -->
# --> Updating classes' numbers in annotations
#
# Result:
# Files classes.names and joined_data.data needed to train
# in Darknet framework
# Also, updated indexes of classes' numbers in annotations


# Importing needed library
import os


"""
Start of:
Setting up full paths to directories
"""

# Full or absolute path to the folder with labelled images
# Find it with Py file getting-full-path.py
# Pay attention! If you're using Windows, yours path might looks like:
# r'C:\Users\my_name\Downloads\video-to-annotate'
# or:
# 'C:\\Users\\my_name\\Downloads\\video-to-annotate'
full_path_to_labelled_images = 'F:\\Study\\Practise\\Object Detection\\03 Custom Data Preparations For Training\\01 Lablelling Own Data\\video'

# Full or absolute path to the folder with downloaded images
# Find it with Py file getting-full-path.py
# Pay attention! If you're using Windows, yours path might looks like:
# r'C:\Users\my_name\OIDv4_ToolKit\OID\Dataset\train\Car_Bicycle_wheel_Bus'
# or:
# 'C:\\Users\\my_name\\OIDv4_ToolKit\\OID\\Dataset\\train\\Car_Bicycle_wheel_Bus'
full_path_to_downloaded_images = \
    'C:\\Users\\Rishav\\OIDv4_ToolKit\\OID\\Dataset\\train\\Car_Bicycle_wheel_Bus'

# Full or absolute path to the folder with joined images
# Find it with Py file getting-full-path.py
# Pay attention! If you're using Windows, yours path might looks like:
# r'C:\Users\my_name\Downloads\Labelled-Custom'
# or:
# 'C:\\Users\\my_name\\Downloads\\Labelled-Custom'
full_path_to_joined_images = \
    'F:\\Study\\Practise\\Object Detection\\03 Custom Data Preparations For Training\\03 Joining Labelled and Downloaded Data\\Joined Data'

"""
End of:
Setting up full paths to directories
"""


"""
Start of:
Creating joined file classes.names
"""

# Defining lists for classes from labelled and downloaded data
classes_labelled = []
classes_downloaded = []

# Defining set for classes from labelled and downloaded data
# Repeated elements will not be added
classes_joined = set()

# Reading existing files classes.names for labelled and downloaded data
# Adding all classes into one set
# Appending classes into appropriate lists
# Pay attention! If you're using Windows, it might need to change
# this: + '/' +
# to this: + '\' +
# or to this: + '\\' +
with open(full_path_to_labelled_images + '/' + 'classes.names', 'r') \
     as names_1, \
     open(full_path_to_downloaded_images + '/' + 'classes.names', 'r') \
     as names_2:

    # Going through all lines from first file and adding them into set
    # Making all names with lowercase letters
    for line in names_1:
        classes_joined.add(line.lower().strip())

        # Appending classes into list
        classes_labelled.append(line.lower().strip())

    # Going through all lines from first file and adding them into set
    # Making all names with lowercase letters
    for line in names_2:
        classes_joined.add(line.lower().strip())

        # Appending classes into list
        classes_downloaded.append(line.lower().strip())


# Converting set into the list with only unique names of classes
classes_joined = list(classes_joined)


# Creating file classes.names for joined datasets
# Pay attention! If you're using Windows, it might need to change
# this: + '/' +
# to this: + '\' +
# or to this: + '\\' +
with open(full_path_to_joined_images + '/' + 'classes.names', 'w') \
        as names:

    # Writing lists' elements into joined classes.names file
    # By adding '\n' we move to the next line
    for e in classes_joined:
        names.write(e + '\n')

"""
End of:
Creating joined file classes.names
"""


"""
Start of:
Creating file joined_data.data
"""

# Creating file joined_data.data
# Pay attention! If you're using Windows, it might need to change
# this: + '/' +
# to this: + '\' +
# or to this: + '\\' +
with open(full_path_to_joined_images + '/' + 'joined_data.data', 'w') \
     as data:
    # Writing needed 5 lines
    # Number of classes
    # By using '\n' we move to the next line
    data.write('classes = ' + str(len(classes_joined)) + '\n')

    # Location of the train.txt file
    data.write('train = '
               + full_path_to_joined_images + '/' + 'train.txt' + '\n')

    # Location of the test.txt file
    data.write('valid = '
               + full_path_to_joined_images + '/' + 'test.txt' + '\n')

    # Location of the classes.names file
    data.write('names = '
               + full_path_to_joined_images + '/' + 'classes.names' + '\n')

    # Location where to save weights
    data.write('backup = backup')

"""
End of:
Creating file joined_data.data
"""


"""
Start of:
Updating classes' numbers in annotations from labelled data
"""

# Check point
# Getting the current directory
# print(os.getcwd())

# Changing the current directory
# to one with images
os.chdir(full_path_to_labelled_images)

# Check point
# Getting the current directory
# print(os.getcwd())

# Using os.walk for going through all directories
# and files in them from the current directory
# Fullstop in os.walk('.') means the current directory
for current_dir, dirs, files in os.walk('.'):
    # Going through all files
    for f in files:
        # Checking if filename ends with '.jpeg' or '.jpg'
        if f.endswith('.jpeg') or f.endswith('.jpg'):
            # Slicing from image's name extension
            name_of_txt = f[:-5] if f.endswith('jpeg') else f[:-4]

            # Preparing path to annotation txt file from labelled
            # data that has the same name as image file has
            # Pay attention!
            # If you're using Windows, it might need to change
            # this: + '/' +
            # to this: + '\' +
            # or to this: + '\\' +
            path_to_txt_file_labelled = \
                full_path_to_labelled_images + '/' + \
                name_of_txt + '.txt'

            # Preparing path to annotation txt file for joined
            # data that has the same name as image file has
            # Pay attention!
            # If you're using Windows, it might need to change
            # this: + '/' +
            # to this: + '\' +
            # or to this: + '\\' +
            path_to_txt_file_joined = \
                full_path_to_joined_images + '/' + \
                name_of_txt + '.txt'

            # Opening annotation txt file from labelled data
            # Updating classes' number in annotation
            # Writing annotation txt file into joined data
            with open(path_to_txt_file_labelled, 'r') as labelled, \
                    open(path_to_txt_file_joined, 'w') as joined:
                # Going through all lines from file
                for line in labelled:
                    # Getting current class's number
                    c_number = int(line[:1])

                    # Getting current class's name from labelled data
                    c_name = classes_labelled[c_number]

                    # Getting new class's number
                    c_number_updated = classes_joined.index(c_name)

                    # Updating current annotation line
                    line_updated = str(c_number_updated) + line[1:]

                    # Writing updated annotation line into joined data
                    joined.write(line_updated)

"""
End of:
Updating classes' numbers in annotations from labelled data
"""


"""
Start of:
Updating classes' numbers in annotations from downloaded data
"""

# Check point
# Getting the current directory
# print(os.getcwd())

# Changing the current directory
# to one with images
os.chdir(full_path_to_downloaded_images)

# Check point
# Getting the current directory
# print(os.getcwd())

# Using os.walk for going through all directories
# and files in them from the current directory
# Fullstop in os.walk('.') means the current directory
for current_dir, dirs, files in os.walk('.'):
    # Going through all files
    for f in files:
        # Checking if filename ends with '.jpeg' or '.jpg'
        if f.endswith('.jpeg') or f.endswith('.jpg'):
            # Slicing from image's name extension
            name_of_txt = f[:-5] if f.endswith('jpeg') else f[:-4]

            # Preparing path to annotation txt file from downloaded
            # data that has the same name as image file has
            # Pay attention!
            # If you're using Windows, it might need to change
            # this: + '/' +
            # to this: + '\' +
            # or to this: + '\\' +
            path_to_txt_file_downloaded = \
                full_path_to_downloaded_images + '/' + \
                name_of_txt + '.txt'

            # Preparing path to annotation txt file for joined
            # data that has the same name as image file has
            # Pay attention!
            # If you're using Windows, it might need to change
            # this: + '/' +
            # to this: + '\' +
            # or to this: + '\\' +
            path_to_txt_file_joined = \
                full_path_to_joined_images + '/' + \
                name_of_txt + '.txt'

            # Opening annotation txt file from labelled data
            # Updating classes' number in annotation
            # Writing annotation txt file into joined data
            with open(path_to_txt_file_downloaded, 'r') as downloaded, \
                    open(path_to_txt_file_joined, 'w') as joined:
                # Going through all lines from file
                for line in downloaded:
                    # Getting current class's number
                    c_number = int(line[:1])

                    # Getting current class's name from downloaded data
                    c_name = classes_downloaded[c_number]

                    # Getting new class's number
                    c_number_updated = classes_joined.index(c_name)

                    # Updating current annotation line
                    line_updated = str(c_number_updated) + line[1:]

                    # Writing updated annotation line into joined data
                    joined.write(line_updated)

"""
End of:
Updating classes' numbers in annotations from downloaded data
"""
