class SAIBrain:
    """
    This class will manipulate data to learn things or manage memory
    """
    def __init__(self, nb_best_command=5, nb_time_rest_second=3600):
        """
        It will set the core of the SIA
        """
        self.nb_best_command = nb_best_command
        self.nb_time_rest_second = nb_time_rest_second

    def create_db(self):
        """
        Create the db containing commands
        :return:
        """
        try:
            # TODO implement
            return 0
        except Exception:
            return -1

    def rest(self):
        """
        It will rest and manage the memory
        :return: 0 if it works else -1
        """
        try:
            # TODO implement
            return 0
        except Exception:
            return -1

    def find_new_command(self):
        """
        It will search a new command
        :return: 0 if it works else -1
        """
        try:
            # TODO implement
            return 0
        except Exception:
            return -1

    """ Optionnal methods"""
    def is_command_exist(self, command):
        """
        It will check if the command looks like another command
        :return: True if it works else False
        """
        # TODO implement
        return False

    def manage_memory(self):
        """
        It will compress every image used to get only interesting data
        :return: 0 if it works else -1
        """
        try:
            # TODO implement
            return 0
        except Exception:
            return -1
