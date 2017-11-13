from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from xvfbwrapper import Xvfb
from bs4 import BeautifulSoup

def available_curses(carne, passw, visible=False, close=True):
    """
    Enters ematricula.ucr.ac.cr and then
    goes to the section that has the information
    about available careers.

    Example usage:

    Launch a invisible browser and get the curses.
    -> available_curses('b53777', 'mypassword')
    
    Launch a visible browser to see step by step what is done.
    -> available_curses('b53777', 'mypassword', visible=True)

    Launch a visible browser and don't close when finished.
    -> available_curses('b53777', 'mypassword', visible=True, close=False)
    """

    # Create and start a virtualdisplay
    vdisplay = Xvfb()

    # Launch the display if visible is false
    if not visible:
        vdisplay.start()
    
    # Open the browser and does the magic
    driver = webdriver.Firefox() 
    driver.get('https://ematricula.ucr.ac.cr/ematricula/login.do')
    carne_box = driver.find_element_by_name('carne')
    pass_box = driver.find_element_by_name('pin')
    carne_box.send_keys(carne)
    pass_box.send_keys(passw)
    driver.find_element_by_name('crudMethod').click()
    wait_until_title_contains(driver, 'Sistema eMatricula')
    driver.find_element_by_link_text('Cursos Pendientes del Plan').click()
    wait_until_element_is_located(driver, 'formCarreras')
    career_dropdown = driver.find_element_by_name("carrera")
    careers = [x for x in career_dropdown.find_elements_by_tag_name('option')[1:]]
    
    for each_career in careers:
        print(each_career.get_attribute('innerHTML'))
        print(each_career.get_attribute('value'))
	each_career.click()
	wait_until_class_is_located(driver,'data')
        table=driver.find_element_by_class_name("data")
        body= table.find_element_by_xpath("//tbody")
        tr = [x for x in body.find_elements_by_xpath("//tr")[1:]]
        print ("I found the table and the body ")

    # Quit the browser
    if close:
        driver.quit()

    # If not visible, stop display
    if not visible:
        vdisplay.stop()

def wait_until_title_contains(driver, piece, timeout=10):
    """
    Wait until the title contains the piece.
    Default timeout will be 10 seconds.
    
    """
    try:
        # Wait until title contains...                                         
        element = WebDriverWait(driver, timeout).until(
            EC.title_contains(piece)
        )
    except TimeoutException:
        raise WebDriverException("It appears that there's someone logged in already...")
    
    finally:
        # Log succesfully                                                      
        print("Loaded page that contains '"+piece+"' succesfully...")
    
def wait_until_element_is_located(driver, element_id, timeout=10):
    """
    Wait until the element is located in the driver.
    Default timeout will be 10 seconds.

    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
    finally:
        print("Loaded page that contains '"+element_id+"' succesfully...")

def wait_until_class_is_located(driver, element_class, timeout=10):
    """
    Wait until the element is located in the driver.
    Default timeout will be 10 seconds.

    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, element_class))
        )
    finally:
        print("Loaded page that contains '"+element_class+"' succesfully...")
