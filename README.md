# Student Assistant Portal Application (SAP)
*This project is a demo for educational purposes as part of course*

The purpose of SAP web application is to improve the undergraduate Student Assistants (SAs) recruitment process. Computer Science Department can recruit SA for the introductary level courses and lab sections.

The application allow seemless interactions between the instructors and students. Students who are interested in SA positions can create accounts, and enter contact information as well as course preferences. Instructors can choose the student assistants among the students who are interested in their course.

------------------------
## ⚙️ Technologies Used
-----------------------
[![My Skills](https://skillicons.dev/icons?i=js,html,css,flask,aws,docker,selenium,azure,bootstrap,postgres,figma)](https://skillicons.dev)

------------------------
## 🌟 Features
-----------------------
- **Authentication**: Register an account to join the portal.
- **Single Sign-On Service**: Log in to your WPI account quickly with Microsoft Azure SSO.
- **Profile Customization**: Add your GPA, grade, previous courseworks and experiences to your own profile.
- **Course, Section & Position Creation**: Register a course and section that you teaches from a list of CS courses, and create new position listings with specific requirements
- **Position Application**: Apply to a course that you are interested in.
- **Personalized Recommendation**: Recommend positions based on your own skill sets.
- **Sort and Filter**: Check out position listings based on your preference.
- **Status Updates**: Review the status of your applications, or applicants if you are an instructor.
- **All-in-one System**: Manage SAs efficiently with quick assignments, and ensure that students can only be SA exclusively to a section.

------------------------
## 🚀 Getting Started
-----------------------

### Set up dependencies:
- Create a python environment:
    ```
    python -m venv venv
    ```
- Activate the python environment:
    ```
    .\venv\Scripts\activate
    ```
- Download dependencies:
    ```
    pip install -r requirements.txt
    ```

------------------------
## 🖥️ Running the program
-----------------------

### To run this app:
- Start the SAP application with the following command:
    ```
    python application.py
    ```

### To run the tests:
- run the tests for Model (unittest)
    ``` 
    python -m unittest -v tests/test_models.py 
    ```
- run the tests for routes (pytest)
    ```
    python -m pytest -v tests/test_routes_1.py
    ```
- run the selenium tests
    * Download the Chrome webdriver for your Chrome browser version (https://chromedriver.chromium.org/downloads); extract and copy it under `C:\Webdriver` folder.
    * Run the SAP application in a terminal window: 
        ```
            python application.py
        ```
    * Run the selenium tests
        ```
            python tests/test_selenium.py
        ```

------------------------
## 📚 Documentations
-----------------------
For more information on the app development process and design, check out the documentations in /documents to see user stories, web structure, and DB designs in details.

------------------------
## 🙏 Acknowledgements
-----------------------
- Professor Arslan Ay - CS-3733: Software Engineering
- Flask-tasticCoders Team Members  
[![Profile Picture](https://github.com/iamkdao.png)](https://github.com/iamkdao)
[![Profile Picture](https://github.com/dhoangquan1.png)](https://github.com/dhoangquan1)
[![Profile Picture](https://github.com/samnguyen3115.png)](https://github.com/samnguyen3115)
[![Profile Picture](https://github.com/wolflieu201105.png)](https://github.com/wolflieu201105)
