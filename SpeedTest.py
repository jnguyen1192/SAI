import time
import unittest


class SpeedTest(unittest.TestCase):

    def test_speed_once(self, func, *args):
        beg = time.time()
        func(*args)
        end = time.time()
        return end - beg

    def test_speed_26_screenshot_in_one_second(self):
        """
        The goal is to mesurate how maximum can we take screen in less than a second
        """
        import threading
        import time
        from mss import mss
        import os

        import SAIEyes

        saie = SAIEyes.SAIEyes(eyes_dir="Speedtest", ctm_dir="Speedtest")

        def loop26():
            import d3dshot
            import os
            d = d3dshot.create()
            for i in range(26):
                name = "gross_"+str(i)
                print(name)
                # TODO find the best way
                # first way 9.029s => 2 img/s as a jpg 2.467s => 10 img/s
                #cs = saie.get_current_screen(name+".jpg")
                #saie.save_image_court_term_memory(cs, name + ".jpg")
                # second way 5.343s => 4 img/s as a jpg 2.68s => 10 img/s
                #import pyscreeze
                #pyscreeze._screenshot_win32(name+".png")
                # third way 4.658s => 5 img/s
                #with mss() as sct:
                #    print(sct.shot())
                    # rename monitor-1.png to name+".png"import os
                #    os.replace('monitor-1.png', name+".png")
                    #sct.save()
                # fourth way 4.909 => 5 img/s as a jpg 15 img/s
                d.screenshot_to_disk(directory=os.path.join("Speedtest", "CourtTermMemory"), file_name=name + ".jpg")

        my_thread = threading.Thread(target=loop26)
        my_thread.start()

        my_thread.join()

    def test_take_img_during_10_seconds(self):
        import time
        import d3dshot
        import os
        from datetime import datetime, timezone

        d = d3dshot.create()
        start = time.time()
        end = 0
        i = 0
        print("hello")
        # without current date 180 imgs => 18 img/s
        """while end - start < 10: 
            name = "gross_"+str(i)
            d.screenshot_to_disk(directory=os.path.join("Speedtest", "CourtTermMemory"), file_name=name + ".jpg")
            end = time.time()
            i += 1
        """
        # with current date and deleting on the directory 169 imgs => 16.9 imgs/s
        # with current date on the directory 183 imgs => 18 imgs/s
        while end - start < 10:
            d.screenshot_to_disk(directory=os.path.join("Speedtest", "CourtTermMemory"), file_name=datetime.today().strftime("%Y%m%d%H%M%S%f") + ".jpg")
            end = time.time()
            i += 1




    def test_speed(self, func, *args, nb_test=10):
        sum = 0
        for i in range(nb_test):
            sum += self.test_speed_once(func, *args)
        return sum/nb_test


if __name__ == '__main__':
    unittest.main()