from enum import Enum
from xdrlib import ConversionError
import creopyson, os, creopyson_api as api

def display_title_bar() -> None:
    # Clears the terminal screen, and displays a title bar.
    os.system('cls')
              
    print("\t**********************************************")
    print("\t*****  CreoAPI - made by Artur Kasprzyk  *****")
    print("\t***************  Version 1.0.2  **************")
    print("\t**********************************************\n\n")

def get_user_input() -> str:
    # Let users know what they can do.
    print("[1] - Set working path")
    print("[2] - Modify model paramaters")
    print("[3] - Modify text paramaters")
    print("[4] - Modify text")
    print("[5] - Change the models material")

    print("[q] - Quit / exit the program")

    return input("\nWhat would you like to do?\n")

def get_user_input_parameters() -> str:
    # Let users know what they can do.
    print("\n[0] - Modify width")   # W
    print("[1] - Modify height")    # H
    print("[2] - Modify depth / offset")     # L
    print("[d] - Done")

    return input("\nPlease pick one\n")

def get_user_input_material(
    creo_cxn:creopyson.Client,
    file_name:str
) -> str:
    # Print a list of materials for the active model.
    # return a value from the list
    material_list = api.get_material_list(creo_cxn, file_name)
    for i in range(len(material_list)):
        print(f"[{i}] - {material_list[i]}")

    index = input("\nPlease pick one\n")

    try:
        if index.isnumeric():
            index = int(index)
            if index < len(material_list):
                return material_list[index]
            else:
                print("Error: Index does not exist")
                return ''
        else:
            print("Error: Invalid material option type")
    except:
        raise ConversionError('Error: Unable to convert to int')

def set_working_path(
    creo_cxn:creopyson.Client
) -> str:
    new_path = input("\nPlease choose the new creo working path:\n")
    returned_path = api.set_creo_working_path(creo_cxn, new_path)
    if returned_path:
        print(f"\nWorking path set to: {new_path}\n")
    

def init(
) -> None:
    # CONSTANTS
    CREO_PATH = 'C:/Program Files/PTC/Creo 7.0.1.0/Parametric/bin/nitro_proe_remote.bat'
    FILE_NAME = 'ar_ka_13k1.prt'
    WORKING_PATH = 'D:/Documents/CREO_API/01'
    class MAIN_OPTIONS(Enum):
        SET_WORKING_PATH = '1'
        MODEL_PARAM = '2'
        TEXT_PARAM = '3'
        TEXT = '4'
        MATERIAL = '5'
        QUIT = 'q'

    class MODEL_OPTIONS(Enum):
        W = '0'
        H = '1'
        L = '2'
        DONE = 'd'

    class TEXT_OPTIONS(Enum):
        T_W = '0'
        T_H = '1'
        T_L = '2'
        DONE = 'd'

    # VARIABLES
    user_input = ''
    new_text = {}
    new_material = ''
    new_connection_path = ''

    ## Enabling logging and configuring the logger 
    ## Turn on only in dev mode
    ## api.enableLogging()

    display_title_bar()

    print('------ Configuration ------\n')
    print('Please check if both Creo and Creoson Server are running before continuing.')

    ## Connecting to Creo via API
    new_path_answer = input(
        f"""Current creo path to establish a connection: {CREO_PATH}\nDo you want to set a new path? (y/n)\n"""
    )
    if new_path_answer.lower() in ('y', 'yes'):
        CREO_PATH = input('Please choose the new creo connection path:\n')

    creo_cxn = api.creo_connection(CREO_PATH)

    creo_version_answer = input("Is your current creo version < 7? (y/n)\n")
    ## If you are using Creo 7 you must declare it once per session to prevent errors on deprecated features
    if creo_version_answer.lower() not in ('y', 'yes'):
        api.set_creo_version(creo_cxn)

    
    ## Atempts to run Creo
    ## Runs Creo but crashes anyways (something wrong with creopyson)
    api.run_creo(creo_cxn, CREO_PATH)


    ## Set working path for Creo
    creo_working_path_answer = input(
        f"""Current creo working path is: {WORKING_PATH}\n 
        Do you want to set a new working path? (y/n)\n"""
    )

    if creo_working_path_answer.lower() in ('y', 'yes'):
        WORKING_PATH = input("\nPlease choose the new creo working path:\n")

    api.set_creo_working_path(creo_cxn, WORKING_PATH)
    print(f"\nWorking path set to: {WORKING_PATH}\n")

    ## Check if file is open in Creo
    ## Opens file if not currently open
    api.open_file(creo_cxn, FILE_NAME, WORKING_PATH)

    while user_input.lower() != MAIN_OPTIONS.QUIT.value:
        user_input = get_user_input()
        new_values = {}

        match user_input:
            ## Set new working directory for creo
            case MAIN_OPTIONS.SET_WORKING_PATH.value:
                os.system('cls')
                set_working_path(creo_cxn)

            ## Change dimension values of the given model
            case MAIN_OPTIONS.MODEL_PARAM.value:
                while user_input.lower() != MODEL_OPTIONS.DONE.value:
                    os.system('cls')
                    user_input = get_user_input_parameters()

                    match user_input:
                        case MODEL_OPTIONS.W.value:
                            new_values['w'] = input("MODEL WIDTH: \n")

                        case MODEL_OPTIONS.H.value:
                            new_values['h'] = input("MODEL HEIGHT: \n")

                        case MODEL_OPTIONS.L.value:
                            new_values['l'] = input("MODEL DEPTH: \n")

                os.system('cls')
                if bool(new_values):
                    model_changed = api.modify_model_dimensions(creo_cxn, FILE_NAME, new_values)
                    if model_changed:
                        print('Succesfully updated the models parameters')
                        new_values = {}
                    else:
                        print('Something went wrong when updating the models parameters')

            ## Change dimension values of the given text
            case MAIN_OPTIONS.TEXT_PARAM.value:
                while user_input.lower() != TEXT_OPTIONS.DONE.value:
                    os.system('cls')
                    user_input = get_user_input_parameters()

                    match user_input:
                        case TEXT_OPTIONS.T_W.value:
                            new_values['t_w'] = input("TEXT WIDTH: \n")

                        case TEXT_OPTIONS.T_H.value:
                            new_values['t_h'] = input("TEXT HEIGHT: \n")

                        case TEXT_OPTIONS.T_L.value:
                            new_values['t_l'] = input("TEXT OFFSET: \n")
                
                os.system('cls')
                if bool(new_values):
                    model_changed = api.modify_model_dimensions(creo_cxn, FILE_NAME, new_values)
                    if model_changed:
                        print('Succesfully updated the texts parameters')
                        new_values = {}
                    else:
                        print('Something went wrong when updating the texts parameters')

            ## Change text
            case MAIN_OPTIONS.TEXT.value:
                ## ak_text is the name of the parameter that holds text value
                new_text['ak_text'] = input("NEW TEXT: \n")
                text_changed = api.modify_paramaters(creo_cxn, FILE_NAME, new_text)
                os.system('cls')
                if text_changed:
                    print('Succesfully updated text')
                else:
                    print('Something went wrong when updating text')

            ## Change the material of the active model
            case MAIN_OPTIONS.MATERIAL.value:
                new_material = get_user_input_material(creo_cxn, FILE_NAME)
                os.system('cls')
                if new_material != '':
                    material_changed = api.modify_material(creo_cxn, FILE_NAME, new_material)
                else: 
                    material_changed = False
                    print('Error: Index does not exist')
                    
                if material_changed:
                    print('Succesfully updated material')
                    new_material = ''
                else:
                    print('Something went wrong when updating material')

## Start the application
init()


    
