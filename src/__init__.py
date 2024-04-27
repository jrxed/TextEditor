from .controller import *

if not os.path.exists("cache"):
    os.mkdir("cache")

if not os.path.exists(PATH_TO_SAVE_OPENED_FILES):
    with open(PATH_TO_SAVE_OPENED_FILES, 'w') as file:
        file.write('{}')

if not os.path.exists(PATH_TO_SAVE_APP_DATA):
    with open(PATH_TO_SAVE_APP_DATA, 'w') as file:
        file.write('{}')
