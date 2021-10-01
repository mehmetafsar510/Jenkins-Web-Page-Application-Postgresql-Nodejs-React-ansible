from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import os
# Set chrome options for working with headless mode (no screen)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("headless")
chrome_options.add_argument("no-sandbox")
chrome_options.add_argument("disable-dev-shm-usage")

# Update webdriver instance of chrome-driver with adding chrome options
driver = webdriver.Chrome(options=chrome_options)

# Connect to the application
url = "https://clarus.mehmetafsar.com/"
print(url)
driver.get(url)
owners_link = driver.find_element_by_class_name('btn-success')
owners_link.click()
sleep(2)
# Register new Owner to Todo App
fn_field = driver.find_element_by_class_name('form-control')
fn = 'Todoapp' + str(random.randint(0, 100))
fn_field.send_keys(fn)
driver.find_element_by_class_name('btn-success').click()
sleep(1)
element = driver.find_element_by_class_name('btn-warning')
driver.execute_script("arguments[0].click();", element)
fn_field1 = driver.find_element_by_class_name('form-control')
fn_field1.send_keys('Clarusway')
driver.execute_script("arguments[0].click();", element)
sleep(2)
fnson = 'TodoappClarusway'

# Verify that new user is added to Owner List
if fnson in driver.page_source:
    print(fnson, 'is added and found in the Todo')
    print("Test Passed")
else:
    print(fnson, 'is not found in the Todo Table')
    print("Test Failed")
driver.quit()
