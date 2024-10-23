import unittest
import pyautogui
import time
import os

class TestToDoApp(unittest.TestCase):

    def setUp(self):
        # Run the Tkinter app in a separate thread
        self.process = os.popen('python your_script_name.py')
        time.sleep(2)  # Wait for the app to launch

    def tearDown(self):
        # Close the app process
        self.process.close()

    def test_add_task(self):
        # Add a new task using pyautogui
        pyautogui.click(100, 100)  # Adjust the coordinates to click on "Task Name" field
        pyautogui.write("Test Task with GUI")
        pyautogui.click(100, 150)  # Click on the "Status" field
        pyautogui.write("Pending")
        pyautogui.click(100, 200)  # Click on the "Add Task" button
        time.sleep(1)

        # Assert if the task was added successfully
        tasks = pyautogui.locateOnScreen('task_image.png')
        self.assertIsNotNone(tasks)

if __name__ == '__main__':
    unittest.main()
