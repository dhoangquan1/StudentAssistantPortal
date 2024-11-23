# Project Group Report - 1
## Team: `<Flask-tastic Coders>`
List team members and their GitHub usernames
* `<Khoi Dao>`,`<iamkdao>`
* `<Quan Dinh>`,`<dhoangquan1>`
* `<Huy Pham>`,`<wolflieu201105>`
* `<Duc Nguyen>`,`<blackkendiz>`
---
**Course** : CS 3733 - Software Engineering
**Instructor**: Sakire Arslan Ay
----
## 1. Schedule
* Fridays at 6pm
----
## 2. Iteration 1 - Summary

**Iteration-1 accomplishments:**

* Created login and register pages for instructors and students
* Created a form to create sections for a course
* Created a form to create positions for a section

**User stories done by Khoi Dao:**

* As a student, I want to register a student account so that I can start applying for a student assistant position.
* As a student, I want to log in using a student account with WPI email and password
* As an instructor, I want to register an instructor account so that I can start creating course sections and SA positions listings

**User stories done by Quan Dinh:**

* As an instructor, I want to add a new course section that I am going to teach so that students can request to be SA in my section

**User stories done by Huy Pham:**

* As an instructor, I want to log in using an instructor account with WPI email and password

**User stories done by Duc Nguyen:**

* As an instructor, I want to choose my course section and then create SA positions listing for the course so that students knows my course sections needs certain SAs

----
## 3. Iteration 1 - Sprint Retrospective

OUTCOME OF SCRUM RETROSPECTIVE MEETINGS:
* Changed the design of the UML diagram
* Error handling and debugging
* Designed the interface

CHANGES TO IMPROVE:
* Communicate more if errors arise
* Try to upload on self-created branches before merging to the main branch
----
## 4. Product Backlog refinement

* Deleted the task of creating Qualifications table and Require_Qualifications relationship: this is to make the model less confusing and redundant.
* Added the Position table: separate from the Section table.
* Added attributes to the Past_Enrollment table: to store the necessary data of student user.

----
## 5. Iteration 2 - Sprint Backlog

USER STORIES TO BE COMPLETED IN ITERATION 2:
* As a student, I want to view open SA positions so that I can choose my course preferences for student assistantships
* As a student, I want to apply for SA positions so that the instructor can be notified that I want to be SA in their course section
* As an instructor, I want to see the students who has applied to be my course section's SA so that I can assigned some students to be the course's SA

ISSUES + THE PERSON IN CHARGE:

1. [Implementation] Design the student view of open positions and an HTML template for student index view
2. [Implementation] Design the student view of recommended positions and an HTML template for student index view
3. [Implementation] Design the student view of the application form
4. [Implementation] Design the instructor view of a notification page to get notified of student applications
5. [Implementation] Design the instructor view of a page to manage applications
6. [Database Model] Make an "Application" model in database
