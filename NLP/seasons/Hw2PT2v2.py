from keras.applications import VGG16
from keras.models import Model
from keras.layers import Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from matplotlib import pyplot
import sys
from keras.optimizers import SGD
import os
from PIL import Image
import shutil
import random


# # Get the current working directory
# current_directory = os.getcwd()
# print(current_directory)

# # Define categories
# categories = ['clouds', 'rain', 'sunrise', 'shine']

# # Create train and test directories for each category in the current directory
# for category in categories:
#     os.makedirs(os.path.join(current_directory, category, 'train'), exist_ok=True)
#     os.makedirs(os.path.join(current_directory, category, 'test'), exist_ok=True)


# Directory containing the images
# folder_path = r'dataset2'

# Desired dimensions
# new_width = 224
# new_height = 224

# for filename in os.listdir(folder_path):
#     # Open the image file
#     with Image.open(os.path.join(folder_path, filename)) as img:
#         # Check if the image dimensions are not already 224x224
#         if img.size != (new_width, new_height):
#             # Convert the image to RGB mode
#             img = img.convert('RGB')
#             # Resize the image
#             img_resized = img.resize((new_width, new_height))
#             # Save the resized image, overwrite the original file
#             img_resized.save(os.path.join(folder_path, filename))
#             print(f"Resized {filename} to 224x224 pixels.")
#         else:
#             print(f"{filename} already has dimensions 224x224.")

# print("All images processed.")

# from sklearn.model_selection import train_test_split

# random_seed = 1
# val_ratio = 0.1
# src_directory = 'dataset2'
# train_directory = 'dataset2/train'
# test_directory = 'dataset2/test'

# # Create train and test directories if they don't exist
# os.makedirs(train_directory, exist_ok=True)
# os.makedirs(test_directory, exist_ok=True)

# import os


# # List all files in the directory

# def remove_all_pictures(root_dir):
#     # Iterate over each directory in the root directory
#     for dir_name in os.listdir(root_dir):
#         dir_path = os.path.join(root_dir, dir_name)
#         # Check if the current item is a directory
#         if os.path.isdir(dir_path):
#             print(f"Processing directory: {dir_name}")
#             # Call the remove function to delete all files within this directory
#             remove(dir_path)

# def remove(dir):
#     file_list = os.listdir(dir)

#     # Iterate over the file list and remove each file
#     for file_name in file_list:
#         file_path = os.path.join(dir, file_name)
#         os.remove(file_path)

# remove_all_pictures(train_directory)
# remove_all_pictures(test_directory)

# print("All files in the directory have been removed.")


# # Iterate through each file in the source directory
# for file in os.listdir(src_directory):
#     src = src_directory + "\\" + file
#     # src = os.path.join(src_directory, file)
    
#     # Determine destination directory based on random splitting
#     dst_dir = train_directory if random.random() >= val_ratio else test_directory
    
#     # Copy the file to the appropriate directory based on its label
#     if file.startswith('cloudy'):
#         dst = os.path.join(dst_dir, 'cloudy')
#     elif file.startswith('rain'):
#         dst = os.path.join(dst_dir, 'rain')
#     elif file.startswith('shine'):
#         dst = os.path.join(dst_dir, 'shine')
#     elif file.startswith('sunrise'):
#         dst = os.path.join(dst_dir, 'sunrise')
#     elif file.startswith('train') or file.startswith('test'):
#         continue
    
#     # Copy the file
#     shutil.copy(src, dst)

# print("Data split into train and test sets.")

# def totalNums(directory):
#     files = os.listdir(directory)
#     total_files = len(files)
#     print("Total number of files in " + directory + ":", total_files)

# totalNums('dataset2/test/cloudy')
# totalNums('dataset2/test/rain')
# totalNums('dataset2/test/shine')
# totalNums('dataset2/test/sunrise')
# totalNums('dataset2/train/cloudy')
# totalNums('dataset2/train/rain')
# totalNums('dataset2/train/shine')
# totalNums('dataset2/train/sunrise')



def define_model():
    # Load model
    model = VGG16(weights='imagenet',include_top=False, input_shape=(224, 224, 3))
    
    # Freeze layers
    for layer in model.layers:
        layer.trainable = False
    
    # Add new classifier layers
    flat1 = Flatten()(model.layers[-1].output)
    class1 = Dense(128, activation='relu', kernel_initializer='he_uniform')(flat1)
    output = Dense(4, activation='softmax')(class1)  # 4 categories, so use softmax
    
    # Define new model
    model = Model(inputs=model.inputs, outputs=output)
    
    # Compile model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model

# Plot diagnostic learning curves
def summarize_diagnostics(history):
    # Plot loss
    pyplot.subplot(211)
    pyplot.title('Cross Entropy Loss')
    pyplot.plot(history.history['loss'], color='blue', label='train')
    pyplot.plot(history.history['val_loss'], color='orange', label='test')

    # Plot accuracy
    pyplot.subplot(212)
    pyplot.title('Classification Accuracy')
    pyplot.plot(history.history['accuracy'], color='blue', label='train')
    pyplot.plot(history.history['val_accuracy'], color='orange', label='test')

    # Save plot to file
    filename = sys.argv[0].split('/')[-1]
    pyplot.savefig(filename + '_plot.png')
    pyplot.close()




# Run the test harness for evaluating a model
def run_test_harness():
    # Define model
    model = define_model()

    # Create data generator
    datagen = ImageDataGenerator(featurewise_center=True)

    # Specify ImageNet mean values for centering
    datagen.mean = [123.68, 116.779, 103.939]

    # Prepare iterator
    train_it = datagen.flow_from_directory('dataset2/train/',
                                           class_mode='categorical', batch_size=64, target_size=(224, 224))
    test_it = datagen.flow_from_directory('dataset2/test/',
                                          class_mode='categorical', batch_size=64, target_size=(224, 224))

    # Fit model
    history = model.fit_generator(train_it, steps_per_epoch=len(train_it),validation_data=test_it, validation_steps=len(test_it), epochs=5, verbose=1)

    # Evaluate model
    _, acc = model.evaluate_generator(test_it, steps=len(test_it), verbose=1)
    print('> %.3f' % (acc * 100.0))

    # Learning curves
    summarize_diagnostics(history)

# Entry point, run the test harness
run_test_harness()

