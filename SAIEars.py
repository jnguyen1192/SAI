import speech_recognition as sr


class SAIEars:
    """
    This class is used to microphone as an input
    """
    def __init__(self):
        # TODO implement
        # create actions.xml using a predefine list if it isn't correspondant
        pass
    # TODO use test_speech_recognition.py
    #       1) ask for a command and initiate the position
    #       2) do a random command
    #       3) ask for answer yes/no
    #       4) if yes stock on db command and random command
    #       loop to 1

    def create_actions_xml(self):
        """
        Create the file actions.xml using a predefine list
        :return: 0 if it works else -1
        """
        # TODO
        #   The files will have actions
        #   For each action, it can be:
        #       - name
        #       - param1 (optionnaly)
        #           . min
        #           . max
        #       - param2 (optionnaly)
        #           . min
        #           . max
        #       - param3 (optionnaly)
        #           . min
        #           . max
        return -1

    def get_command(self):
        """
        Get the microphone input
        :return: the input as a text or -1
        """
        # TODO implement
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
            try:
                return r.recognize_sphinx(audio)
            except sr.UnknownValueError:
                return self.get_command()
            except sr.RequestError as e:
                print("Sphinx error; {0}".format(e))
                return -1
