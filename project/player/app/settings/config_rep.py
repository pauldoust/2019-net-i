########################################################################################################################
# @ Module : Config Rep
#
# @ Author : EMMA (Group I)
# @ Course : Computer Network
# @ Since  : January 2019
# @ Desc   : This Module  implements all mutable (can be updated) system configurations vars representation ( persisted
#                Persisted on the system file
#
########################################################################################################################


##################
# @ DEPENDENCIES
##################
import os
import pickle

from app.utilites.auxiliaries import Auxiliaries


class ConfigRep:
    ####################################################################################################################
    #                                               CONFIG REP  MODULE
    ####################################################################################################################
    IMMUTABLE_VARS = []

    def __init__(self, static_var=dict()):
        self.my_vars = static_var

    def persist_setting(self):
        from app.settings.config import Config
        mutable_vars = list(ConfigRep.get_mutable_vars())

        for mutable_var in mutable_vars:
            self.my_vars[mutable_var] = Config.get_one_config_static_var(mutable_var)

        settings_file_path = Config.MYDB_DIR + os.sep + "settings.pkl"
        output = open(settings_file_path, 'wb')
        pickle.dump(self, output)
        output.close()
        return True

    @staticmethod
    def load_setting():
        from app.settings.config import Config
        settings_file_path = Config.MYDB_DIR + os.sep + "settings.pkl"
        pkl_file = open(settings_file_path, 'rb')
        obj = pickle.load(pkl_file)
        pkl_file.close()

        mutable_vars = ConfigRep.get_mutable_vars()
        for mutable_var in mutable_vars:
            Config.set_one_config_static_var(mutable_var, obj.my_vars[mutable_var])

        return True

    @staticmethod
    def get_mutable_vars():
        from app.settings.config import Config
        all_vars = Config.get_all_config_static_vars()
        return Auxiliaries.diff_list(all_vars, ConfigRep.IMMUTABLE_VARS)

    ####################################################################################################################
    #                                           END CONFIG REP MODULE
    ####################################################################################################################
