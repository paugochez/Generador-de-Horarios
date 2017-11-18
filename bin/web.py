from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from xvfbwrapper import Xvfb
from bs4 import BeautifulSoup
import pickle
import sys


def  available_curses(carne,  passw,  visible=True,  close=True):
    """
    Enters ematricula.ucr.ac.cr and downloads  the courses left in the
    plan and creates a .txt file with them

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
        cambio=0
        each_tr= tr[0]
        my_courses = []
        for data in each_tr.find_elements_by_xpath("//td"):
            my_courses.append(data.get_attribute('innerHTML').strip())
                        
        print ("Los cursos se descargaron exitosamente. Cantidad de cursos faltantes")
        print (len(tr))
        
        clean_courses=[]
        file = open("cursos.txt","w")
        for i in range(0,len(tr)):
            new_Subject = Subject()
            new_Subject.sigla = my_courses[i*5]
            new_Subject.curso = my_courses[i*5+1]
            new_Subject.creditos = my_courses[i*5+2]
            clean_courses.append(new_Subject)
            file.write(my_courses[i*5] +'\t'+ my_courses[i*5+1] +'\t'+my_courses[i*5+2]+"\t \n")
                
            
        file.close() 
    # Quit the browser
    if close:
        driver.quit()

    # If not visible, stop display
    if not visible:
        vdisplay.stop()

def wait_until_title_contains(driver, piece, timeout=20):
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
    
def wait_until_element_is_located(driver, element_id, timeout=20):
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

def wait_until_class_is_located(driver, element_class, timeout=20):
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

class Subject: #Object that contains subject elements
    sigla = ""
    curso = ""
    creditos = 0


