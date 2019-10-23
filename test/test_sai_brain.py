import unittest
import SAIBrain

import cv2
import os


class TestSAIBrain(unittest.TestCase):

    def setUp(self):
        self.current_dir = os.getcwd()
        self.saib = SAIBrain.SAIBrain()

    def test_SAIBrain_create_db_case_ok(self):
        # TODO implement
        assert (True==True)

    def test_SAIBrain_create_db_case_nok(self):
        # TODO implement
        assert (False==False)

    def test_SAIBrain_create_db_case_ok(self):
        # TODO implement
        assert (True==True)

    def test_SAIBrain_create_db_case_nok(self):
        # TODO implement
        assert (False==False)

    def test_SAIBrain_rest_case_ok(self):
        # TODO implement
        assert (True==True)

    def test_SAIBrain_rest_case_nok(self):
        # TODO implement
        assert (False==False)

    def test_SAIBrain_find_new_command_case_ok(self):
        # TODO implement
        # Create a random behavior for:
        #       - mouse movement : x, y,
        #       - mouse click : click, double_click,
        #       - mouse hold-release(with movement): x, y
        # Use a depth of 1
        # TODO Mouse movement
        import random
        # x and y
        # get window width and height
        from win32api import GetSystemMetrics
        # 1080, 1920
        # 864, 1536
        #import tkinter
        import pyautogui
        import random

        x_rand = random.randint(0, pyautogui.size().width)
        y_rand = random.randint(0, pyautogui.size().height)
        #print(pyautogui.size().width)
        #print(pyautogui.size().height)

        #root = tkinter.Tk()
        #width = root.winfo_screenwidth()
        #height = root.winfo_screenheight()
        #print(width, height)

        print("Width =", GetSystemMetrics(0))
        print("Height =", GetSystemMetrics(1))

        assert (True==True)

    def test_SAIBrain_find_new_command_case_nok(self):
        # TODO implement
        assert (False==False)

    """ Optionnal methods"""
    def test_SAIBrain_is_command_exist_case_true(self):
        # TODO implement
        assert (True==True)

    def test_SAIBrain_is_command_exist_case_false(self):
        # TODO implement
        assert (False==False)

    def test_SAIBrain_manage_memory_case_ok(self):
        # TODO implement
        assert (True==True)

    def test_SAIBrain_manage_memory_case_nok(self):
        # TODO implement
        assert (False==False)

    def test_SAIBrain_is_diff_old_image_new_image_case_different_time_ok(self):
        """
        Test if the function works with different time images
        """
        # Result : MSE = 2.02
        self.generic_test_SAIBrain_is_diff_old_image_new_image("old_image_1.png", "new_image_1.png", False)

    def test_SAIBrain_is_diff_old_image_new_image_case_same_images_ok(self):
        """
        Test if the function works with same images
        """
        # Result : MSE = 0.0
        self.generic_test_SAIBrain_is_diff_old_image_new_image("old_image_2.png", "new_image_2.png", True)

    def test_SAIBrain_is_diff_old_image_new_image_case_different_images_ok(self):
        """
        Test if the function works with different images
        """
        # Result : MSE = 9.63
        self.generic_test_SAIBrain_is_diff_old_image_new_image("old_image_3.png", "new_image_3.png", False)

    def generic_test_SAIBrain_is_diff_old_image_new_image(self, name_new_image, name_old_image, pred):
        old_image_path = os.path.join(self.current_dir, "is_diff_old_image_new_image", name_new_image)
        new_image_path = os.path.join(self.current_dir, "is_diff_old_image_new_image", name_old_image)
        old_image = cv2.imread(old_image_path)
        new_image = cv2.imread(new_image_path)
        res = self.saib.is_diff_old_image_new_image(old_image, new_image)
        assert(pred == res)


if __name__ == '__main__':
    unittest.main()
