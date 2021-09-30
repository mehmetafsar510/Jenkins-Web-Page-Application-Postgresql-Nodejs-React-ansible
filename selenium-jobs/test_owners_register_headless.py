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
url = "https://clarusway.mehmetafsar.com/"
print(url)
driver.get(url)
owners_link = driver.findElement(By.cssSelector("input[value=\"Add\"]"))
owners_link.click()
sleep(2)
# Register new Owner to Todo App
fn_field = driver.findElement(By.cssSelector("input[value=\"Add\"]"))
fn = 'Todoapp' + str(random.randint(0, 100))
fn_field.send_keys(fn)
fn_field.send_keys(Keys.Add)
sleep(1)
fn_field = driver.findElement(By.cssSelector("input[value=\"Edit\"]"))
fn_field.send_keys('Clarusway')
fn_field.send_keys(Keys.Edit)
sleep(1)
fn_field = driver.findElement(By.cssSelector("input[value=\"Delete\"]"))
fn_field.send_keys(Keys.Delete)
sleep(1)
fn_field = driver.findElement(By.cssSelector("input[value=\"Add\"]"))
fn = 'Todoapp' + str(random.randint(0, 100))
fn_field.send_keys(fn)
fn_field.send_keys(Keys.Add)


# Wait 10 seconds to get updated Owner List
sleep(10)
# Verify that new user is added to Owner List
if fn in driver.page_source:
    print(fn, 'is added and found in the Todo')
    print("Test Passed")
else:
    print(fn, 'is not found in the Todo Table')
    print("Test Failed")
driver.quit()