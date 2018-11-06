from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.implicitly_wait(5) # waits for elements for 5 seconds
driver.get("http://www.python.org")
try:
    frame = WebDriverWait(driver, 10).until(
                        EC.frame_to_be_available_and_switch_to_it(0)
                        )
finally:
    print("done")
    assert "Python" in driver.title
    driver.implicitly_wait(5) # waits for elements for 5 seconds
    elem = driver.find_element_by_id("id-search-field")
    elem.clear()
    elem.send_keys("py con")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source

