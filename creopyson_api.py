import creopyson, logging

def enableLogging():
    logging.basicConfig(level=logging.DEBUG)

    ## Hide urllib3 logging
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def creo_connection(
    file_path:str
) -> creopyson.Client:
    """
    Connects to creo using creopy method connect()
    If Creo is not running, the given file will be opened

    :param file_path: path to file that creo should open
    :rtype: creopyson.Client
    """
    try:
        creopyson_client = creopyson.Client()
        creopyson_client.connect()

    except:
        raise RuntimeError("""\n
            Error: Unable to connect to creo server
            Please check if both creo and creoson server are running\n
        """) from None

    return creopyson_client
    

def set_creo_version(
    creo_cxn:creopyson.Client
) -> None:
    """
    Sets the Creo version to 7

    :param creo_cxn: instance of the creo connection
    :rtype: None
    """
    creopyson.creo_set_creo_version(client=creo_cxn, version=7)


def set_creo_working_path(
    creo_cxn:creopyson.Client,
    file_path:str
) -> bool:
    """
    Sets the working directory to file_path

    :param creo_cxn: Creo connection
    :param file_path: path that will be the new working directory
    :rtype: bool
    """
    try:
        creopyson.creo_cd(client=creo_cxn, dirname=file_path)  # set current working directory.
        return True
    except:
        print('Error: Unable to set new working path for creo\nPlease check if path is valid.')
        return False


def run_creo(
    creo_cxn:creopyson.Client,
    creo_path:str
) -> None:
    """
    Runs creo parametric if it is not already running

    :param creo_cxn: Creo connection
    :param file_path: path of file to be opened. Currently this is the working directory
    :rtype: None
    :throws RuntimeError: if creo cannot run
    """
    try:
        if not creo_cxn.is_creo_running():
                print("""Atempting to run creo parametric.\nWarning! - Please do not press any keys until creo is running...""")
                # Something wrong with this function, runs creo but crashes program anyways...
                creo_cxn.start_creo(path=creo_path, use_desktop=True)
    except: 
        raise RuntimeError('Error: Something went wrong when trying to run creo') from None

def open_file(
    creo_cxn:creopyson.Client,
    file_name:str,
    working_path:str
) -> None:
    """
    Openes the file if it isn't already opened

    :param creo_cxn: Creo connection
    :param file_name: name of file to be opened
    :rtype: None
    :throws RuntimeError: if file cannot be opened
    """
    try:
        if not creopyson.file_exists(client=creo_cxn, file_=file_name):  # returns False if file is not in memory (missleading function name)
            creopyson.file_open(client=creo_cxn, file_=file_name, display=True, dirname=working_path)  # Open `my_file.prt` in Creo.
        else:
            print('File does not exist')
    except: 
        raise RuntimeError('Error: Something went wrong when trying to open file') from None

def modify_model_dimensions(
    creo_cxn:creopyson.Client,
    file_name:str,
    new_values:dict=None
) -> bool:
    """
    Changes the dimension values of the given paramaters passed in a dict


    :param creo_cxn: Creo connection
    :param file_name: name of file to be used
    :param values: a dictionary of key-value pairs of paramaters in Creo and their dimension values
    :rtype: bool
    :throws RuntimeError: if file cannot be opened
    """
    try:
        for key, val in new_values.items():
            if type(val) is str:
                if val.isnumeric():
                    val = int(val)

            if type(val) is not int and type(val) is not float:
                print(f'Type of {key} is invalid')
                return False

            if val < 0:
                print(f'Value of {key} is negative')
                return False
            
            creopyson.dimension_set(client=creo_cxn, file_=file_name, name=key, value=val)
            print(f"{key} changed to: {val}")

        creopyson.file_regenerate(client=creo_cxn, file_=file_name)  # Regenerate file, raise `Warning` if regeneration fails.
        return True
    except: 
        raise RuntimeError('Error: Unable to modify dimension values') from None

def modify_paramaters(
    creo_cxn:creopyson.Client,
    file_name:str,
    new_values:dict
) -> bool:
    """
    Changes the dimension values of the given paramaters passed in a dict


    :param creo_cxn: Creo connection
    :param file_name: name of file to be used
    :param values: a dictionary of key-value pairs of paramaters in Creo and their dimension values
    :rtype: bool
    """
    try:
        for key, val in new_values.items():
            creopyson.parameter_set(client=creo_cxn, file_=file_name, name=key, value=val)
            print(f'Text changed to: {val}')

        creopyson.file_regenerate(client=creo_cxn, file_=file_name)  # Regenerate file, raise `Warning` if regeneration fails.
        return True
    except: 
        print('Error: Unable to modify paramaters')
        return False

def get_material_list(
    creo_cxn:creopyson.Client,
    file_name:str
) -> list:
    """
    Returns a list of materials for the active model


    :param creo_cxn: Creo connection
    :param file_name: name of file to be used
    :rtype: list
    """
    try:
        return creopyson.file_list_materials(client=creo_cxn, file_=file_name)
    except:
        raise RuntimeError('Error: Unable to retrieve material list')  from None
    

def modify_material(
    creo_cxn:creopyson.Client,
    file_name:str,
    new_material:str
) -> bool:
    """
    Changes the current material for a part or parts

    :param creo_cxn: Creo connection
    :param file_name: name of file to be used
    :param material: material name
    :rtype: bool
    """
    try:
        creopyson.file_set_cur_material(client=creo_cxn, material=new_material, file_=file_name)
        print(f"The material has changed to: {new_material}")
        return True
    except: 
        print('Error: Unable to modify material')
        return False