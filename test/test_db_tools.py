import unittest
import tools.db_tools as dbt
import tools.sql_queries as sqt
import tools.docker_tools as dtt


class TestDb_tools(unittest.TestCase):

    # @source:http://stezz.blogspot.com/2011/04/calling-only-once-setup-in-unittest-in.html
    ClassIsSetup = False
    ClassIsTeardown = 1
    # TODO automaticly count the number of unittest
    ClassIsTeardownTotal = 6  # nb total of unittest

    def setUp(self):
        # TODO run db backup container
        if not self.ClassIsSetup:
            # run db container
            try:
                if not dtt.is_image_exist("c_sai_postgres"):
                    res = dbt.create_image_using_dockerfile("postgres")
                    if res == -1:
                        raise Exception("Image not created correctly")
                if not dtt.is_container_exist("c_sai_postgres"):
                    res = dbt.run_db()
                else:
                    res = 0
            except Exception as e:
                print(e)
                res = -1
            # wait database connection
            dbt.wait_db_connection()
            assert (res == 0)
            self.__class__.ClassIsSetup = True

    def tearDown(self):
        if self.ClassIsTeardown == self.ClassIsTeardownTotal:  # the number of test case
            # stop and remove db container
            pass#dtt.clean_container("c_sai_postgres")
        else:
            self.__class__.ClassIsTeardown = self.ClassIsTeardown + 1

    def generic_db_tools_all_tables_created(self, test=False):
        """
        Function to test if tables exist
        :return:
        """
        tables_name = ['Strategie', 'Action', 'Has_action']
        for name in tables_name:
            res = dbt.select_one_with_parameters(sqt.IS_TABLE_EXISTS, (name,), test)
            assert(res != -1)
            assert res

    def test_db_tools_all_tables_created(self):
        """
        Test if all the tables are created
        """
        self.generic_db_tools_all_tables_created()

    def test_create_image_backup(self):
        """
        Test if the image for backup is correctly build
           1) Create the image
           2) Check using docker client if the image is correctly added
           3) Optionally: check if all library are in the container
               docker run -it --name c_sai_backup c_sai_backup dpkg -s postgresql
               docker rm c_sai_backup
               docker run -it --name c_sai_backup c_sai_backup dpkg -s postgresql-contrib
               docker rm c_sai_backup
               docker run -it --name c_sai_backup c_sai_backup dpkg -s postgresql-client
               docker rm c_sai_backup
                   Package: postgresql-contrib
                   Status: install ok installed
                   [...]
               We need to check the status for each package
        """
        # 1)
        assert dbt.create_image_using_dockerfile("backup") == 0
        # 2)
        assert dtt.is_image_exist("c_sai_backup")
        # 3)
        assert dtt.is_package_exist("postgresql", "backup")
        assert dtt.is_package_exist("postgresql-contrib", "backup")
        assert dtt.is_package_exist("postgresql-client", "backup")
        assert not dtt.is_package_exist("notexistpackage", "backup")

    def test_get_last_backup(self):
        """
        Test function get_last_backup
        """
        # create a new backup
        file_name = dbt.new_backup()
        # get the last backup file name
        last_backup = dbt.get_last_backup()
        # remove the new backup
        dbt.remove_backup(file_name)
        # test the function
        assert file_name == last_backup

    def test_db_tools_new_backup(self):
        """
        Test function new_backup
        Configure docker-machine share folder to use this
          1) Create a backup using the corresponding container which need to be launch on Setup with new data
          2) Check if the backup works:
              2.1) The correct date
              2.2) The correct tables
              2.3) The correct data
        """
        # 1) create a backup with a new raw on table action
        # add a raw on table action prod
        new_raw_table = "test_new_backup"
        tmp_container_name = "tmp_postgres"
        assert dbt.query_with_parameters(sqt.INSERT_ON_ACTION, (new_raw_table,)) == 0
        file_name = dbt.new_backup()
        assert file_name != -1

        # 2) create a temporary database using a new postgres container with a different port (here 5433)
        if not dtt.is_image_exist("c_sai_postgres"):
            res = dbt.create_image_using_dockerfile("postgres")
            if res == -1:
                raise Exception("Image not created correctly")
        if not dtt.is_container_exist("c_sai_" + tmp_container_name):
            tmp_db_run = dbt.run_db(tmp_container_name, "postgres", 5433)
            # wait database connection
            dbt.wait_db_connection(True)
        else:
            tmp_db_run = 0
        assert tmp_db_run == 0
        # load the previous backup into the new db
        dbt.load_last_backup(tmp_container_name)
        # 2.1)  check if date is correct
        date = dbt.datetime.now().replace(microsecond=0).strftime("%Y%m%dT%H%M")  # without seconds
        assert date in file_name
        # 2.2) check if all the tables exists
        self.generic_db_tools_all_tables_created(True)
        # 2.3) check if the main data are presents (Actions ...)
        assert dbt.select_one_with_parameters(sqt.IS_RAW_EXISTS_ON_ACTION, (new_raw_table,), True)
        assert not dbt.select_one_with_parameters(sqt.IS_RAW_EXISTS_ON_ACTION, ("other",), True)
        assert dbt.remove_backup(file_name) == 0

        # clean the db, stop and remove the tmp_postgres container
        # delete the new raw on table action prod
        assert dbt.query_with_parameters(sqt.DELETE_ON_ACTION, (new_raw_table,)) == 0
        # stop and remove the tmp_postgres container
        assert dtt.clean_container("c_sai_" + tmp_container_name) == 0

    def test_fufill_db(self):
        """
        Test if function fufill_db works correctly
        """

        import tkinter as tk
        import SAIEars

        class Application(tk.Frame):
            def __init__(self, master=None):
                super().__init__(master)
                self.master = master
                self.master.geometry("600x600") #You want the size of the app to be 500x500
                self.my_frame = tk.Frame(self.master, width=600, height=600)
                self.my_frame.pack()  # Note the parentheses added here
                #self.master.resizable(0, 0) #Don't allow resizing in the x or y direction
                self.create_widgets()
                self.saiears = SAIEars.SAIEars()
                self.sounds = []
                self.b_sounds = {}
                self.current_sound = -1

            def create_widgets(self):
                """
                Create all the widgets of the frame
                """
                self.create_arrows_button_1()
                self.create_keypress_1()

            def get_list_sounds(self):
                """
                Get the list of sound as an array of numpy array
                :return: a list of numpy array
                """
                # TODO
                #   Use a function from db_tools to select id, sound from table sound
                #   Optionnaly: Get the method with the sound
                pass

            def play_sound(self, event=""):
                """
                Play the sound using the number
                :param num_sound: the numero of the sound
                :return: 0 if it works else -1
                """
                try:
                    # TODO refactor into SAISpirit or SAISpeech
                    import sounddevice
                    import time
                    fs = 16000
                    sounddevice.play(self.sounds[self.b_sounds[event.widget]][0], #  self.b_sounds[event.widget] give the correct sound
                                     fs)  # releases GIL https://www.scivision.dev/playing-sounds-from-numpy-arrays-in-python/

                except Exception as e:
                    print(e)
                    return -1

            def get_next_sound_using_sai_ears(self):
                """
                Get a numpy array that represent the sound recording
                :return: a numpy array or -1
                """
                # TODO
                #   Use SAIEars to record a sound
                #   Then return the sound
                return self.saiears.get_next_sound_detected()

            def insert_new_sound_using_method(self, method, new_sound):
                """
                Insert a new sound on the db
                :param method: the method (reward or penalize)
                :param new_sound: the new sound as a numpy array
                :return: 0 if it works else -1
                """
                # TODO
                #   Use a function from db_tools to insert a new sound
                #   Optionally: create the corresponding table
                pass

            def update_color_current_sound(self):
                """
                Update the colors of the sounds buttons
                :return: 0 if it works else -1
                """
                # TODO
                #   Select all sounds buttons and recreate them
                #   Using the current_sound change the color of the specific button
                #   Use parameter bg on corresponding button on link https://pythonexamples.org/python-tkinter-button-background-color/

            def left_keypress_2(self, event=""):
                print("left phase 2")
                # TODO select previous sound
                self.current_sound = (self.current_sound - 1) % len(self.sounds)
                # TODO change the color of the selected sound

            def right_keypress_2(self, event=""):
                print("right phase 2")
                # TODO select next sound
                self.current_sound = (self.current_sound + 1) % len(self.sounds)
                # TODO change the color of the selected sound

            def up_keypress_2(self, event=""):
                # TODO save on db and quit windows with confirmation
                #   Insert the sounds using table sound(numpy_array, method)
                #   Use function message box on link https://pythonspot.com/tkinter-askquestion-dialog/ to create a confirm dialog
                #   optionally: create a csv file containing the sounds
                #       Open a csv file
                #       Write on the csv file each sound using pandas
                #       Close the csv file
                print("up phase 2")

            def down_keypress_2(self, event=""):
                # TODO remove current sound
                print("down phase 2")
                del self.sounds[self.current_sound]
                self.refresh_buttons_sounds()
                if self.current_sound > len(self.sounds) - 1:
                    self.current_sound = len(self.sounds) - 1

            def space_keypress_2(self, event=""):
                # TODO play current sound
                print("space phase 2")
                fs = 16000
                import sounddevice
                sounddevice.play(self.sounds[self.current_sound][0],
                                 fs)  # releases GIL https://www.scivision.dev/playing-sounds-from-numpy-arrays-in-python/


            # TODO the same functions but with _2 and the correct behavior
            def left_keypress_1(self, event=""):
                # TODO penalize behavior
                print("left")
                if type(self.current_sound) != type(-1):
                    self.sounds.append((self.current_sound, "penalize"))
                    print((self.current_sound, "penalize"), "added")
                    self.current_sound = -1
                else:
                    print("No sound to add")

            def right_keypress_1(self, event=""):
                # TODO reward behavior
                print("right")
                if type(self.current_sound) != type(-1):
                    self.sounds.append((self.current_sound, "reward"))
                    print((self.current_sound, "reward"), "added")
                    self.current_sound = -1
                else:
                    print("No sound to add")

            def down_keypress_1(self, event=""):
                # TODO record next sound behavior
                print("down")
                # TODO test record next sound
                print("Waiting for a sound")
                next_sound = self.get_next_sound_using_sai_ears()
                self.current_sound = next_sound
                print("New sound recorded")
                # TODO Define a button to listen the current sound
                #   For example the space button to record a new sound

            def refresh_buttons_sounds(self):
                """
                Refresh the buttons using the list of sounds
                :return: 0 if it works else -1
                """
                try:
                    print("Sounds :", self.sounds)
                    # TODO remove existing buttons before create them
                    if len(self.b_sounds) > 0:
                        for b in self.b_sounds:
                            tk.Button.destroy(b)
                    self.b_sounds = {}
                    if self.sounds != []:
                        arrow_padding_y = 20
                        arrow_padding_x = 40
                        for i in range(len(self.sounds)):
                            newButton = tk.Button(self.my_frame, text="Sound " + str(i + 1) + " " + self.sounds[i][1])
                            newButton.bind("<Button-1>", self.play_sound)
                            newButton.place(x=arrow_padding_x, y=arrow_padding_y + 50 * i)
                            self.b_sounds[newButton] = i
                    return 0
                except Exception as e:
                    print(e)
                    return -1

            def up_keypress_1(self, event=""):
                # TODO stop the recording and create the list of sound
                print("up")
                self.refresh_buttons_sounds()
                # TODO
                #  change behavior of all buttons to go on phase 2
                #  change text of all buttons of the windows
                self.create_arrows_button_2()
                self.create_keypress_2()
                self.current_sound = 0

                    #Board.boardButtons.append(newButton)

            def space_keypress_1(self, event=""):
                # TODO play the current sound recorded
                print("space")
                # TODO refactor into SAISpirit or SAISpeech
                import sounddevice
                import time
                if type(self.current_sound) != type(-1):
                    fs = 16000
                    sounddevice.play(self.current_sound, fs)  # releases GIL https://www.scivision.dev/playing-sounds-from-numpy-arrays-in-python/
                    time.sleep(1)
                pass

            def create_arrows_button_1(self):
                """
                Create the arrows button of phase 1
                """
                arrow_padding_y = 400
                arrow_padding_x = 260
                self.b_up = tk.Button(self.my_frame)
                self.b_up["text"] = "↑"
                self.b_up["command"] = self.up_keypress_1
                self.b_up["width"] = 10
                self.b_up.place(x=arrow_padding_x + 110, y=arrow_padding_y + 0)

                self.l_up = tk.Label(self.my_frame, text="Create sound list")
                self.l_up.place(width=120, x=arrow_padding_x + 80, y=arrow_padding_y + 40)

                self.b_left = tk.Button(self.my_frame)
                self.b_left["text"] = "←"
                self.b_left["command"] = self.left_keypress_1
                self.b_left["width"] = 10
                self.b_left.place(x=arrow_padding_x + 10, y=arrow_padding_y + 70)

                self.l_left = tk.Label(self.my_frame, text="Penalize")
                self.l_left.place(width=120, x=arrow_padding_x + 0, y=arrow_padding_y + 110)

                self.b_right = tk.Button(self.my_frame)
                self.b_right["text"] = "→"
                self.b_right["command"] = self.right_keypress_1
                self.b_right["width"] = 10
                self.b_right.place(x=arrow_padding_x + 210, y=arrow_padding_y + 70)

                self.l_right = tk.Label(self.my_frame, text="Reward")
                self.l_right.place(width=120, x=arrow_padding_x + 200, y=arrow_padding_y + 110)

                self.b_down = tk.Button(self.my_frame)
                self.b_down["text"] = "↓"
                self.b_down["command"] = self.down_keypress_1
                self.b_down["width"] = 10
                self.b_down.place(x=arrow_padding_x + 110, y=arrow_padding_y + 70)

                self.l_down = tk.Label(self.my_frame, text="Record sound")
                self.l_down.place(width=120, x=arrow_padding_x + 100, y=arrow_padding_y + 110)

                self.b_space = tk.Button(self.my_frame)
                self.b_space["text"] = ""
                self.b_space["command"] = self.space_keypress_1
                self.b_space["width"] = 20
                self.b_space.place(x=arrow_padding_x + -220, y=arrow_padding_y + 70)

                self.l_space = tk.Label(self.my_frame, text="Play current sound")
                self.l_space.place(width=120, x=arrow_padding_x + -200, y=arrow_padding_y + 110)

            def create_arrows_button_2(self):
                """
                Create the arrows button of phase 2
                """
                arrow_padding_y = 400
                arrow_padding_x = 260
                self.b_up = tk.Button(self.my_frame)
                self.b_up["text"] = "↑"
                self.b_up["command"] = self.up_keypress_1
                self.b_up["width"] = 10
                self.b_up.place(x=arrow_padding_x + 110, y=arrow_padding_y + 0)

                self.l_up = tk.Label(self.my_frame, text="Save on db")
                self.l_up.place(width=120, x=arrow_padding_x + 80, y=arrow_padding_y + 40)

                self.b_left = tk.Button(self.my_frame)
                self.b_left["text"] = "←"
                self.b_left["command"] = self.left_keypress_2
                self.b_left["width"] = 10
                self.b_left.place(x=arrow_padding_x + 10, y=arrow_padding_y + 70)

                self.l_left = tk.Label(self.my_frame, text="Previous sound")
                self.l_left.place(width=120, x=arrow_padding_x + 0, y=arrow_padding_y + 110)

                self.b_right = tk.Button(self.my_frame)
                self.b_right["text"] = "→"
                self.b_right["command"] = self.right_keypress_1
                self.b_right["width"] = 10
                self.b_right.place(x=arrow_padding_x + 210, y=arrow_padding_y + 70)

                self.l_right = tk.Label(self.my_frame, text="Next sound")
                self.l_right.place(width=120, x=arrow_padding_x + 200, y=arrow_padding_y + 110)

                self.b_down = tk.Button(self.my_frame)
                self.b_down["text"] = "↓"
                self.b_down["command"] = self.down_keypress_1
                self.b_down["width"] = 10
                self.b_down.place(x=arrow_padding_x + 110, y=arrow_padding_y + 70)

                self.l_down = tk.Label(self.my_frame, text="Remove sound")
                self.l_down.place(width=120, x=arrow_padding_x + 100, y=arrow_padding_y + 110)

                self.b_space = tk.Button(self.my_frame)
                self.b_space["text"] = ""
                self.b_space["command"] = self.space_keypress_1
                self.b_space["width"] = 20
                self.b_space.place(x=arrow_padding_x + -220, y=arrow_padding_y + 70)

                self.l_space = tk.Label(self.my_frame, text="Play current sound")
                self.l_space.place(width=120, x=arrow_padding_x + -200, y=arrow_padding_y + 110)

            def create_keypress_1(self):
                self.master.bind('<Left>', self.left_keypress_1)
                self.master.bind('<Right>', self.right_keypress_1)
                self.master.bind('<Down>', self.down_keypress_1)
                self.master.bind('<Up>', self.up_keypress_1)
                self.master.bind('<space>', self.space_keypress_1)

            def create_keypress_2(self):
                # TODO refactor to have the new behavior for phase 2
                self.master.bind('<Left>', self.left_keypress_2)
                self.master.bind('<Right>', self.right_keypress_2)
                self.master.bind('<Down>', self.down_keypress_2)
                self.master.bind('<Up>', self.up_keypress_2)
                self.master.bind('<space>', self.space_keypress_2)


        print("BeforeBefore")
        root = tk.Tk()
        print("Before")
        app = Application(master=root)
        print("After")

        app.mainloop()
        print("AfterAfter")


        assert True

    def test_db_tools_run_db_case_nok(self):
        # TODO implement
        assert (-1)

    def test_db_tools_query_without_parameters_case_ok(self):
        # TODO implement
        assert (True == True)

    def test_db_tools_query_without_parameters_case_nok(self):
        # TODO implement
        assert (False == False)

    def test_db_tools_query_with_parameters_case_ok(self):
        # TODO implement
        assert (True==True)

    def test_db_tools_query_with_parameters_case_nok(self):
        # TODO implement
        assert (False==False)


if __name__ == '__main__':
    unittest.main()
