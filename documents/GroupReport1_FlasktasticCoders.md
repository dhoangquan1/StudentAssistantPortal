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
* As an instructor, I want to register an instructor account so that I can start creating course sections and SA positions listings

**User stories done by Quan Dinh:**

* As an instructor, I want to add a new course section that I am going to teach so that students can request to be SA in my section
* As an instructor, I want to add a new course section that I am going to teach so that students can request to be SA in my section
----
## 3. Iteration 1 - Sprint Retrospective
* Include the outcome of your `Iteration-1 Scrum retrospective meetings`.
* Mention the changes the team will be doing to improve itself as a result of the
Scrum reflections.

OUTCOME OF SCRUM RETROSPECTIVE MEETINGS:
* Changed the design of the UML diagram
* Error handling and debugging
* Designed the interface

CHANGES TO IMPROVE:
* Communicate more if errors arise
* Try to upload on self-created branches before merging to the main branch
----
## 4. Product Backlog refinement
* Have you made any changes to your `product backlog` after `Iteration-1`? If so,
please explain the changes here.

* Deleted the task of creating Qualifications table and Require_Qualifications relationship: this is to make the model less confusing and redundant.
----
## 5. Iteration 2 - Sprint Backlog
Include a draft of your `Iteration-2 spring backlog`.
* List the user stories you plan to complete in `Iteration-2`. Make sure to break
down the larger user stories into smaller size stories. Mention the team member(s)
who will work on each user story.
* Make sure to update the "issues" on your GitHub repo accordingly.

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
