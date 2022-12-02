import unittest, time, os
from builtins import id
from datetime import date

import self as self

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from Data import TestData


class AndroidBudget(unittest.TestCase):

    def setUp(self):
        desired_caps = {'platformName': 'Android', 'deviceName': '$emulator-5556', 'appPackage': 'protect.budgetwatch',
                        'appActivity': '.MainActivity', 'automationName': 'uiautomator2',
                        'autoGrantPermissions': 'true'}
        self.driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps)

    def test_app_budget_add(self):

        self.skipIntro()

        self.home_device()
        self.activate_app()

        self.driver.implicitly_wait(30)
        # clicar em budget
        budget = self.driver.find_element(By.XPATH,
                                          "//android.widget.TextView[contains(@text, 'Budgets')]")
        budget.click()

        add = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_add')
        add.click()

        name = self.driver.find_element(By.ID, 'protect.budgetwatch:id/budgetNameEdit')
        name.set_text(TestData.budget_type)

        value = self.driver.find_element(By.ID, 'protect.budgetwatch:id/valueEdit')
        value.set_text(TestData.budget_value)

        save = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_save')
        save.click()


        self.assertEqual(TestData.budget_type, self.driver.find_element(By.XPATH,
                                                                        "//android.widget.TextView[contains(@text, 'supermarket')]").get_attribute(
            'text'))

    def test_app_budget_add_error(self):

        self.skipIntro()
        self.driver.implicitly_wait(30)
        # clicar em budget
        budget = self.driver.find_element(By.ID, 'protect.budgetwatch:id/image')
        budget.click()

        add = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_add')
        add.click()

        name = self.driver.find_element(By.ID, 'protect.budgetwatch:id/budgetNameEdit')
        name.set_text("test123")

        value = self.driver.find_element(By.ID, 'protect.budgetwatch:id/valueEdit')
        value.set_text("abcdefg")

        save = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_save')
        save.click()


        self.assertEqual('Budget value is empty',
                         self.driver.find_element(By.ID, 'protect.budgetwatch:id/snackbar_text').get_attribute('text'))

    def test_app_budget_edit_value(self):
        self.skipIntro()

        self.driver.implicitly_wait(30)
        # clicar em budget
        budget = self.driver.find_element(By.XPATH,
                                          "//android.widget.TextView[contains(@text, 'Budgets')]")
        budget.click()

        add = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_add')
        add.click()

        name = self.driver.find_element(By.ID, 'protect.budgetwatch:id/budgetNameEdit')
        name.set_text(TestData.budget_type)

        value = self.driver.find_element(By.ID, 'protect.budgetwatch:id/valueEdit')
        value.set_text(TestData.budget_value)

        save = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_save')
        save.click()

        self.driver.implicitly_wait(30)

        actions = TouchAction(self.driver)

        item = self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, '"+TestData.budget_type+"')]")
        actions.long_press(item)
        actions.perform()

        editmenu = self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, 'Edit')]")
        editmenu.click()

        edit = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_edit')
        edit.click()

        name = self.driver.find_element(By.ID, 'protect.budgetwatch:id/budgetNameEdit')
        name.set_text(TestData.budget_type)

        value = self.driver.find_element(By.ID, 'protect.budgetwatch:id/valueEdit')
        value.set_text(TestData.new_budget_value)

        save = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_save')
        save.click()

        self.assertEqual("0/"+TestData.new_budget_value, self.driver.find_element(By.XPATH,
                                                                        "//android.widget.TextView[contains(@text, '0/800')]").get_attribute(
            'text'))

    def test_app_budget_delete(self):
        self.skipIntro()

        self.driver.implicitly_wait(30)
        # clicar em budget
        budget = self.driver.find_element(By.XPATH,
                                          "//android.widget.TextView[contains(@text, 'Budgets')]")
        budget.click()

        add = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_add')
        add.click()

        name = self.driver.find_element(By.ID, 'protect.budgetwatch:id/budgetNameEdit')
        name.set_text(TestData.budget_type)

        value = self.driver.find_element(By.ID, 'protect.budgetwatch:id/valueEdit')
        value.set_text(TestData.budget_value)

        save = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_save')
        save.click()

        self.driver.implicitly_wait(30)

        actions = TouchAction(self.driver)

        item = self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, '"+TestData.budget_type+"')]")
        actions.long_press(item)
        actions.perform()

        editmenu = self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, 'Edit')]")
        editmenu.click()

        edit = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_edit')
        edit.click()

        options = self.driver.find_element(By.XPATH,
                                           "//android.widget.ImageView[contains(@content-desc, 'More options')]")
        options.click()

        delete = self.driver.find_element(By.XPATH,
                                          "//android.widget.TextView[contains(@text, 'Delete')]")
        delete.click()

        confirm = self.driver.find_element(By.ID, "android:id/button1")
        confirm.click()

        self.assertEqual("You don't have any budgets at the moment. Click the + (plus) button up top "
                         'to get started.\n'
                         '\n'
                         'Budget Watch lets you create budgets, then track spending during the month.',
                         self.driver.find_element(By.ID,
                                                  "protect.budgetwatch:id/helpText").get_attribute('text'))

    def skipIntro(self):
        if self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, 'Welcome to Budget Watch')]"):
            skip = self.driver.find_element(By.ID, 'protect.budgetwatch:id/skip')
            skip.click()


    def landscape_device(self):
         self.driver.orientation = "LANDSCAPE"

    def portrait_device(self):
         self.driver.orientation = "PORTRAIT"

    def home_device(self):
         return self.driver.press_keycode(3)

    def back_device(self):
         return self.driver.press_keycode(4)

    def activate_app(self):
         return self.driver.activate_app('protect.budgetwatch')

    def tearDown(self):
         self.driver.quit()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidBudget)
    unittest.TextTestRunner(verbosity=2).run(suite)
