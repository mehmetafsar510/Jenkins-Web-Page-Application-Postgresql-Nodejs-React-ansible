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

fn_field = driver.find_element_by_class_name('form-control')
fn = 'Todoapp' + str(random.randint(0, 100))
fn_field.send_keys(fn)
driver.find_element_by_class_name('btn-success').click()
sleep(2)


element =driver.find_element_by_xpath("/html/body/div/div/table/tbody/tr/td[3]/button")
print("yes", element.is_displayed())
element.click()
sleep(2)

fn_field = driver.find_element_by_class_name('form-control')
fn = 'Todoapp'
fn_field.send_keys(fn)
driver.find_element_by_class_name('btn-success').click()
sleep(2)

element =driver.find_element_by_xpath("/html/body/div/div/table/tbody/tr/td[2]/button")
print("yes", element.is_displayed())
element.click()
sleep(2)

fn_field = driver.find_element_by_xpath("/html/body/div[1]/div/table/tbody/tr/td[2]/div/div/div/div[2]/input") 
fn = 'Clarusway'
fn_field.send_keys(fn)
sleep(2)

element = driver.find_element_by_xpath("/html/body/div[1]/div/table/tbody/tr/td[2]/div/div/div/div[3]/button[1]") 
print("yes", element.is_displayed())
element.click()
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
