########################################################################################################################
# @ Module : Config
#
# @ Author : EMMA (Group I)
# @ Course : Computer Network
# @ Since  : January 2019
# @ Desc   : This Module  implements all system configurations vars (DISTRIBUTOR PORT, HUB IP ...) and related features
#
#
########################################################################################################################


##################
# @ DEPENDENCIES
##################
import ipaddress
import os
from os.path import dirname
from pathlib import Path

from app.settings.config_rep import ConfigRep
from app.utilites.auxiliaries import Auxiliaries
from app.utilites.netutils import Netutils


class Config:
    ####################################################################################################################
    #                                               CONFIG MODULE
    ####################################################################################################################

    # Default Configurations
    LIST_PENDING_LIB = list()
    LIST_IN_PROGRESS_LIB = list()
    LIST_DOWNLOADED_LIB = list()
    ROOT_DIR = dirname(dirname(dirname(__file__)))
    DATA_DIR = ROOT_DIR+os.sep+"data"
    LIBS_DIR = DATA_DIR + os.sep + "libs"
    STUFFS_DIR = DATA_DIR + os.sep + "temp"
    MYDB_DIR = DATA_DIR + os.sep + "mydb"
    DOWNLOAD_DIR = DATA_DIR + os.sep + "download"
    LOG_DIR = DATA_DIR + os.sep + "logs"
    DISTRIBUTOR_PORT = 0
    HUB_IP = "198.58.103.254"
    #HUB_IP = "192.168.43.188"
    HUB_PORT = 7777
    DEBUG_MODE = False

    @staticmethod
    def persist_setting():
        config_rep = ConfigRep()
        return config_rep.persist_setting()

    @staticmethod
    def load_setting():
        return ConfigRep.load_setting()


    @staticmethod
    def is_setup():
        settings_file_path = Config.MYDB_DIR + os.sep + "settings.pkl"
        settings_path = Path(settings_file_path)
        if settings_path.exists() is False:
            return True
        else:
            return False

    @staticmethod
    def data_repo_inspection():
        try:
            # Check if all the dir exist and create them if not
            Config.create_dir(Config.DATA_DIR)
            Config.create_dir(Config.LIBS_DIR)
            Config.create_dir(Config.STUFFS_DIR)
            Config.create_dir(Config.MYDB_DIR)
            Config.create_dir(Config.DOWNLOAD_DIR)
            Config.create_dir(Config.LOG_DIR)
            return True

        except Exception as e:
            Auxiliaries.console_log(e)
            return False

    @staticmethod
    def create_dir(dir_name):
        # Check if all the dir exist and create them if not
        dir_path = Path(dir_name)
        # Create dir if not exist
        if dir_path.is_dir() is False:
            dir_path.mkdir()
        return True


    @staticmethod
    def add_pending_download_lib(library_id):
        try:
            if library_id not in Config.LIST_PENDING_LIB:
                Config.LIST_PENDING_LIB.append(library_id)
                Config.persist_setting()

            return True
        except Exception as e:
            Auxiliaries.console_log(e)
            return False

    @staticmethod
    def remove_pending_download_lib(library_id):
        try:
            Config.LIST_PENDING_LIB.remove(library_id)
            Config.persist_setting()
            return True
        except Exception as e:
            Auxiliaries.console_log(e)
            return False

    @staticmethod
    def add_in_progress_download_lib(library_id):
        try:
            if library_id not in Config.LIST_IN_PROGRESS_LIB:
                Config.LIST_IN_PROGRESS_LIB.append(library_id)
                Config.persist_setting()
            return True
        except Exception as e:
            Auxiliaries.console_log(e)
            return False

    @staticmethod
    def remove_in_progress_download_lib(library_id):
        try:
            Config.LIST_IN_PROGRESS_LIB.remove(library_id)
            Config.persist_setting()
            return True
        except Exception as e:
            Auxiliaries.console_log(e)
            return False

    @staticmethod
    def add_downloaded_lib(library_id):
        try:
            if library_id not in Config.LIST_DOWNLOADED_LIB:
                Config.LIST_DOWNLOADED_LIB.append(library_id)
                Config.persist_setting()
            return True
        except Exception as e:
            Auxiliaries.console_log(e)
            return False

    @staticmethod
    def remove_downloaded_lib(library_id):
        try:
            Config.LIST_DOWNLOADED_LIB.remove(library_id)
            Config.persist_setting()
            return True
        except Exception as e:
            Auxiliaries.console_log(e)
            return False

    @staticmethod
    def view_global_var():
        all_static_vars = Config.get_all_config_static_vars()
        all_static_vars_dict = dict()

        for static_var in all_static_vars:
            all_static_vars_dict[static_var] = Config.get_one_config_static_var(static_var)

        return all_static_vars_dict

    @staticmethod
    def update_global_var(key, value):

        # Checking existence and mutability of key
        IMMUTABLE_GLOBAL_VARS = ["LIST_PENDING_LIB", "LIST_IN_PROGRESS_LIB", "LIST_DOWNLOADED_LIB"]
        if key not in Config.get_all_config_static_vars():
            return False, "GlobalVars [{}] in not found".format(key)

        if key in IMMUTABLE_GLOBAL_VARS:
            return False, "GlobalVars [{}] is not mutable ".format(key)

        # Casting new Value to the type of old value
        old_value = Config.get_one_config_static_var(key)
        old_value_type = type(old_value)
        try:
            value = old_value_type(value)
        except Exception as e:
            Auxiliaries.console_log(e)
            return False, "GlobalVars [{}] can not be casted to Type: {}  ".format(key, str(old_value_type))

        # Execute Special parser when applicable
        status, msg = Config.special_parsor(key, value)
        if status is False:
            return status, msg

        # Update Value
        try:
            Config.set_one_config_static_var(key, value )
        except Exception as e:
            Auxiliaries.console_log(e)
            return False, "Error occurred while updating GlobalVars [{}]".format(key)

        return True, "GlobalVars [{}] has been successfully updated.".format(key)

    @staticmethod
    def get_all_config_static_vars():
        _vars = [i for i in dir(Config) if not callable(i)]
        static_vars = list()
        while len(_vars) > 0:
            cur_var = _vars[0]
            if cur_var == "__class__":
                break
            static_vars.append(cur_var)
            del(_vars[0])
        return static_vars

    @staticmethod
    def get_one_config_static_var(static_var_key):
        return getattr(Config, static_var_key)

    @staticmethod
    def set_one_config_static_var(static_var_key, static_var_value):
        return setattr(Config,static_var_key, static_var_value)

    @staticmethod
    def special_parsor(key, value):

        if key == "HUB_PORT" or key == "DISTRIBUTOR_PORT":
            if Auxiliaries.parse_port(value) is False:
                return False, "Invalid Port number provided range [0,65535]"
        if key == "HUB_IP":
            if Netutils.parse_ip_address(value) is False:
                return False, "'{}' does not appear to be an IPv4 or IPv6 address".format(value)

        return True, "Special parsor successfully completed"

    ####################################################################################################################
    #                                           END CONFIG MODULE
    ####################################################################################################################


if __name__ == "__main__":
    Auxiliaries.console_log(Config.update_global_var("DISTRIBUTOR_PORT", 5003))
    Auxiliaries.console_log(Config.get_all_config_static_vars())
    #Auxiliaries.console_log(Config.view_global_var())
    pass

