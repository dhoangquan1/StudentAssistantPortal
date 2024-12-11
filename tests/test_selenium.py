import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from time import sleep

# Student fixure - 1
@pytest.fixture
def student1():
    return  {'email':'quan@wpi.edu', 
             'first_name':'Quan', 
             'last_name':'Dinh',
             'wpi_id':'123456789',
             'phone':'4079298011',
             'major':'CS',
             'gpa':'4',
             'grad_date':'02282026',
             'password':'123',
             'prev_enroll': 'CS1101 - Introduction to Program Design'
             }

# Student fixure - 2
@pytest.fixture
def student2():
    return  {'email':'christine@wpi.edu', 
             'first_name':'Christine', 
             'last_name':'Mae',
             'wpi_id':'987654321',
             'phone':'4079298011',
             'major':'DS',
             'gpa':'3',
             'grad_date':'02282027',
             'password':'123',
             'prev_enroll': 'CS2022 - Discrete Mathematics'
             }

# Instructor fixure - 1
@pytest.fixture
def instructor1():
    return  {'email':'instr@wpi.edu', 
             'first_name':'Instructor1', 
             'last_name':'One',
             'wpi_id':'789561564',
             'phone':'4079298011',
             'password':'123',
             }

# Instructor fixure - 2
@pytest.fixture
def instructor2():
    return  {'email':'instr2@wpi.edu', 
             'first_name':'Instructor1', 
             'last_name':'Two',
             'wpi_id':'987654320',
             'phone':'4079298011',
             'password':'123',
             }

 # Section fixure - 1
@pytest.fixture
def section1():
    return {'section_number': '01', 
            'term': '2025C',
            'course': 'CS1101 - Introduction To Program Design'}
    
 # Section fixure - 2
@pytest.fixture
def section2():
    return {'section_number': '02', 
            'term': '2026D',
            'course': 'CS2022 - Discrete Mathematics'}
    
 # Position fixure - 1
@pytest.fixture
def position1():
    return {'section': 'CS1101-01: Introduction To Program Design',
            'sa_num': '2',
            'min_gpa': '3.5',
            'min_grade': 'B',
            'require_exp': 'False'}
    
 # Position fixure - 2
@pytest.fixture
def position2():
    return {'section': 'CS2022-02: Discrete Mathematics',
            'sa_num': '3',
            'min_gpa': '4',
            'min_grade': 'A',
            'require_exp': 'True'}

 # Application fixure - 1
@pytest.fixture
def application1():
    return {'year': '2021', 
            'term': 'A',
            'grade': 'A'}

 # Application fixure - 2
@pytest.fixture
def application2():
    return {'year': '2022', 
            'term': 'C',
             'grade': 'B'}


"""
Download the chrome driver and make sure you have chromedriver executable in your PATH variable. 
To download the ChromeDriver to your system navigate to its download page. 
https://chromedriver.chromium.org/downloads  
"""

@pytest.fixture
def browser():
    CHROME_PATH = "C:\\WebDriver\\chromedriver-win64"
    print(CHROME_PATH)
    
    options = webdriver.ChromeOptions()
    options.add_argument("--force-device-scale-factor=0.4")
    options.headless = True

    service = Service(executable_path = CHROME_PATH + '\\chromedriver.exe')
    
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(8)
    
    yield driver

    # For cleanup, quit the driver
    driver.quit()


def test_register_form_student1(browser,student2):

    browser.get('http://localhost:5000/student/register')
    # Enable this to maximize the window
    # browser.maximize_window()
    browser.find_element(By.NAME, "first_name").send_keys(student2['first_name'])
    sleep(2)
    browser.find_element(By.NAME, "last_name").send_keys(student2['last_name'])
    sleep(2)
    browser.find_element(By.NAME, "email").send_keys(student2['email'])
    sleep(2)
    browser.find_element(By.NAME, "wpi_id").send_keys(student2['wpi_id'])
    sleep(2)
    Select(browser.find_element(By.NAME, "phone_code")).select_by_visible_text('US (+1)')
    sleep(2)
    browser.find_element(By.NAME, "phone").send_keys(student2['phone'])
    sleep(2)
    browser.find_element(By.NAME, "password").send_keys(student2['password'])
    sleep(2)
    browser.find_element(By.NAME, "password2").send_keys(student2['password'])    
    sleep(2)
    prev_enroll = browser.find_element(By.NAME, "sa_courses").click()
    sleep(2)
    browser.find_element(By.NAME, "major").send_keys(student2['major'])    
    sleep(2)
    browser.find_element(By.NAME, "gpa").send_keys(student2['gpa'])    
    sleep(2)
    browser.find_element(By.NAME, "grad_date").send_keys(student2['grad_date'])    
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    # print(content)
    assert 'Congratulations, you are now a registered user!' in content

def test_register_form_student2(browser,student1):

    browser.get('http://localhost:5000/student/register')
    # Enable this to maximize the window
    # browser.maximize_window()
    browser.find_element(By.NAME, "first_name").send_keys(student1['first_name'])
    sleep(2)
    browser.find_element(By.NAME, "last_name").send_keys(student1['last_name'])
    sleep(2)
    browser.find_element(By.NAME, "email").send_keys(student1['email'])
    sleep(2)
    browser.find_element(By.NAME, "wpi_id").send_keys(student1['wpi_id'])
    sleep(2)
    Select(browser.find_element(By.NAME, "phone_code")).select_by_visible_text('US (+1)')
    sleep(2)
    browser.find_element(By.NAME, "phone").send_keys(student1['phone'])
    sleep(2)
    browser.find_element(By.NAME, "password").send_keys(student1['password'])
    sleep(2)
    browser.find_element(By.NAME, "password2").send_keys(student1['password'])    
    sleep(2)
    prev_enroll = browser.find_element(By.NAME, "sa_courses").click()
    sleep(2)
    browser.find_element(By.NAME, "major").send_keys(student1['major'])    
    sleep(2)
    browser.find_element(By.NAME, "gpa").send_keys(student1['gpa'])    
    sleep(2)
    browser.find_element(By.NAME, "grad_date").send_keys(student1['grad_date'])    
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    # print(content)
    assert 'Congratulations, you are now a registered user!' in content
    
def test_register_form_instructor1(browser,instructor2):

    browser.get('http://localhost:5000/instructor/register')
    # Enable this to maximize the window
    # browser.maximize_window()
    browser.find_element(By.NAME, "first_name").send_keys(instructor2['first_name'])
    sleep(2)
    browser.find_element(By.NAME, "last_name").send_keys(instructor2['last_name'])
    sleep(2)
    browser.find_element(By.NAME, "email").send_keys(instructor2['email'])
    sleep(2)
    browser.find_element(By.NAME, "wpi_id").send_keys(instructor2['wpi_id'])
    sleep(2)
    Select(browser.find_element(By.NAME, "phone_code")).select_by_visible_text('US (+1)')
    sleep(2)
    browser.find_element(By.NAME, "phone").send_keys(instructor2['phone'])
    sleep(2)
    browser.find_element(By.NAME, "password").send_keys(instructor2['password'])
    sleep(2)
    browser.find_element(By.NAME, "password2").send_keys(instructor2['password'])    
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    # print(content)
    assert 'Congratulations, you are now a registered user!' in content

def test_register_form_instructor2(browser,instructor1):

    browser.get('http://localhost:5000/instructor/register')
    # Enable this to maximize the window
    # browser.maximize_window()
    browser.find_element(By.NAME, "first_name").send_keys(instructor1['first_name'])
    sleep(2)
    browser.find_element(By.NAME, "last_name").send_keys(instructor1['last_name'])
    sleep(2)
    browser.find_element(By.NAME, "email").send_keys(instructor1['email'])
    sleep(2)
    browser.find_element(By.NAME, "wpi_id").send_keys(instructor1['wpi_id'])
    sleep(2)
    Select(browser.find_element(By.NAME, "phone_code")).select_by_visible_text('US (+1)')
    sleep(2)
    browser.find_element(By.NAME, "phone").send_keys(instructor1['phone'])
    sleep(2)
    browser.find_element(By.NAME, "password").send_keys(instructor1['password'])
    sleep(2)
    browser.find_element(By.NAME, "password2").send_keys(instructor1['password'])    
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    # print(content)
    assert 'Congratulations, you are now a registered user!' in content

def test_register_form_error(browser,student2):

    browser.get('http://localhost:5000/student/register')
    # Enable this to maximize the window
    # browser.maximize_window()
    browser.find_element(By.NAME, "first_name").send_keys(student2['first_name'])
    sleep(2)
    browser.find_element(By.NAME, "last_name").send_keys(student2['last_name'])
    sleep(2)
    browser.find_element(By.NAME, "email").send_keys(student2['email'])
    sleep(2)
    browser.find_element(By.NAME, "wpi_id").send_keys(student2['wpi_id'])
    sleep(2)
    Select(browser.find_element(By.NAME, "phone_code")).select_by_visible_text('US (+1)')
    sleep(2)
    browser.find_element(By.NAME, "phone").send_keys(student2['phone'])
    sleep(2)
    browser.find_element(By.NAME, "password").send_keys(student2['password'])
    sleep(2)
    browser.find_element(By.NAME, "password2").send_keys(student2['password'])    
    sleep(2)
    prev_enroll = browser.find_element(By.NAME, "sa_courses").click()
    sleep(2)
    browser.find_element(By.NAME, "major").send_keys(student2['major'])    
    sleep(2)
    browser.find_element(By.NAME, "gpa").send_keys(student2['gpa'])    
    sleep(2)
    browser.find_element(By.NAME, "grad_date").send_keys(student2['grad_date'])    
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    assert 'Register' in content
    assert 'Please use a different email.' in content

def test_login_form(browser,student2):
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "email").send_keys(student2['email'])
    sleep(2)
    browser.find_element(By.NAME, "password").send_keys(student2['password'])
    sleep(2)
    browser.find_element(By.NAME, "remember_me").click()
    sleep(2)
    button = browser.find_element(By.NAME, "submit").click()
    sleep(2)
    #verification
    content = browser.page_source
    assert 'Welcome to Student Assistant Portal!' in content
    assert student2['email'] in content

def test_invalidlogin(browser,student2):
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "email").send_keys(student2['email'])
    sleep(2)
    browser.find_element(By.NAME, "password").send_keys('wrongpassword')
    sleep(2)
    browser.find_element(By.NAME, "remember_me").click()
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    #verification
    content = browser.page_source
    assert 'Invalid email or password' in content
    assert 'Log In' in content

def test_register_section1(browser,instructor2,section2):
    #first login
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "email").send_keys(instructor2['email'])
    browser.find_element(By.NAME, "password").send_keys(instructor2['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    browser.get('http://localhost:5000/instructor/section')
    browser.find_element(By.NAME, "term").send_keys(section2['term'])
    sleep(2)
    browser.find_element(By.NAME, "section_num").send_keys(section2['section_number'])
    sleep(2)
    Select(browser.find_element(By.NAME, "course")).select_by_visible_text(section2['course'])
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    assert 'Section CS2022-02 is created' in content

def test_register_section2(browser,instructor1,section1):
    #first login
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "email").send_keys(instructor1['email'])
    browser.find_element(By.NAME, "password").send_keys(instructor1['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    browser.get('http://localhost:5000/instructor/section')
    browser.find_element(By.NAME, "term").send_keys(section1['term'])
    sleep(2)
    browser.find_element(By.NAME, "section_num").send_keys(section1['section_number'])
    sleep(2)
    Select(browser.find_element(By.NAME, "course")).select_by_visible_text(section1['course'])
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    assert 'Section CS1101-01 is created' in content

def test_register_section_error(browser,instructor1,section1):
    #first login
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "email").send_keys(instructor1['email'])
    browser.find_element(By.NAME, "password").send_keys(instructor1['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    browser.get('http://localhost:5000/instructor/section')
    browser.find_element(By.NAME, "term").send_keys(section1['term'])
    sleep(2)
    browser.find_element(By.NAME, "section_num").send_keys(section1['section_number'])
    sleep(2)
    Select(browser.find_element(By.NAME, "course")).select_by_visible_text(section1['course'])
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    #verification
    content = browser.page_source
    assert 'The section already exists, please choose a different course, section number, or term.' in content

def test_register_position1(browser,instructor2,position2):
    #first login
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "email").send_keys(instructor2['email'])
    browser.find_element(By.NAME, "password").send_keys(instructor2['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    browser.get('http://localhost:5000/instructor/position')
    Select(browser.find_element(By.NAME, "section")).select_by_visible_text(position2['section'])
    sleep(2)
    browser.find_element(By.NAME, "SAnum").send_keys(position2['sa_num'])
    sleep(2)
    browser.find_element(By.NAME, "minGPA").send_keys(position2['min_gpa'])
    sleep(2)
    browser.find_element(By.NAME, "min_grade").send_keys(position2['min_grade'])
    sleep(2)
    require_exp = browser.find_element(By.NAME, "prev_sa_exp").click()
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    #verification
    content = browser.page_source
    assert 'Create SA positions succesfully' in content

def test_register_position2(browser,instructor1,position1):
    #first login
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "email").send_keys(instructor1['email'])
    browser.find_element(By.NAME, "password").send_keys(instructor1['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    browser.get('http://localhost:5000/instructor/position')
    Select(browser.find_element(By.NAME, "section")).select_by_visible_text(position1['section'])
    sleep(2)
    browser.find_element(By.NAME, "SAnum").send_keys(position1['sa_num'])
    sleep(2)
    browser.find_element(By.NAME, "minGPA").send_keys(position1['min_gpa'])
    sleep(2)
    browser.find_element(By.NAME, "min_grade").send_keys(position1['min_grade'])
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    #verification
    content = browser.page_source
    assert 'Create SA positions succesfully' in content

def test_register_position_error(browser,instructor1,position1):
    #first login
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "email").send_keys(instructor1['email'])
    browser.find_element(By.NAME, "password").send_keys(instructor1['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    browser.get('http://localhost:5000/instructor/position')
    Select(browser.find_element(By.NAME, "section")).select_by_visible_text(position1['section'])
    sleep(2)
    browser.find_element(By.NAME, "SAnum").send_keys(position1['sa_num'])
    sleep(2)
    browser.find_element(By.NAME, "minGPA").send_keys('5')
    sleep(2)
    browser.find_element(By.NAME, "min_grade").send_keys(position1['min_grade'])
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    #verification
    content = browser.page_source
    assert 'Number must be between 0 and 4.' in content
    
def test_apply1(browser,student2,application2):
    #first login
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "email").send_keys(student2['email'])
    browser.find_element(By.NAME, "password").send_keys(student2['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    browser.get('http://localhost:5000/student/application/1')
    Select(browser.find_element(By.NAME, "grade")).select_by_visible_text(application2['grade'])
    sleep(2)
    browser.find_element(By.NAME, "year_took_course").send_keys(application2['year'])
    sleep(2)
    Select(browser.find_element(By.NAME, "term_took_course")).select_by_visible_text(application2['term'])
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    #verification
    content = browser.page_source
    assert 'Applied to position' in content
    assert 'Already Applied!' in content

def test_apply2(browser,student1,application1):
    #first login
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "email").send_keys(student1['email'])
    browser.find_element(By.NAME, "password").send_keys(student1['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    browser.get('http://localhost:5000/student/application/2')
    Select(browser.find_element(By.NAME, "grade")).select_by_visible_text(application1['grade'])
    sleep(2)
    browser.find_element(By.NAME, "year_took_course").send_keys(application1['year'])
    sleep(2)
    Select(browser.find_element(By.NAME, "term_took_course")).select_by_visible_text(application1['term'])
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    #verification
    content = browser.page_source
    assert 'Applied to position' in content
    assert 'Already Applied!' in content

def test_apply_error(browser,student2,application2):
    #first login
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "email").send_keys(student2['email'])
    browser.find_element(By.NAME, "password").send_keys(student2['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    browser.get('http://localhost:5000/student/application/2')
    Select(browser.find_element(By.NAME, "grade")).select_by_visible_text(application2['grade'])
    sleep(2)
    browser.find_element(By.NAME, "year_took_course").send_keys('2025')
    sleep(2)
    Select(browser.find_element(By.NAME, "term_took_course")).select_by_visible_text(application2['term'])
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    #verification
    content = browser.page_source
    assert 'This year is not valid' in content

def test_assign(browser,instructor2):
    #first login
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "email").send_keys(instructor2['email'])
    browser.find_element(By.NAME, "password").send_keys(instructor2['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    browser.find_element(By.ID, "sele-assign").click()
    
    browser.get('http://localhost:5000/instructor/student/1/profile')
    
    #verification
    content = browser.page_source
    assert 'CS2022-02: Discrete Mathematics' in content
    
def test_withdraw(browser,student1):
    #first login
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "email").send_keys(student1['email'])
    browser.find_element(By.NAME, "password").send_keys(student1['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    browser.get('http://localhost:5000/student/profile')
    
    browser.find_element(By.ID, "sele-withdraw").click()
    
    browser.get('http://localhost:5000/student/index')
    
    #verification
    content = browser.page_source
    assert 'Already Applied!' not in content
    
if __name__ == "__main__":
    retcode = pytest.main(verbose=2)