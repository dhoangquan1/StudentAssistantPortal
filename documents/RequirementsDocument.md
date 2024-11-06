# Software Requirements and Use Cases

## CS 3733 - 2024 B Term Project
--------
Prepared by:

* `Khoi Dao`,`Flask-tasticCoders`
* `Gia Huy Pham`,`Flask-tasticCoders`
* `Tran Nguyen`,`Flask-tasticCoders`
* `Quan Dinh`,`Flask-tasticCoders`

---

**Course** : CS 3733 - Software Engineering

**Instructor**: Sakire Arslan Ay

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Requirements Specification](#2-requirements-specification)
  - [2.1 Customer, Users, and Stakeholders](#21-customer-users-and-stakeholders)
  - [2.2 User Stories](#22-user-stories)
  - [2.3 Use Cases](#23-use-cases)
- [3. User Interface](#3-user-interface)
- [4. Product Backlog](#4-product-backlog)
- [4. References](#4-references)
- [Appendix: Grading Rubric](#appendix-grading-rubric)

<a name="revision-history"> </a>

## Document Revision History

| Name | Date | Changes | Version |
| ------ | ------ | --------- | --------- |
|Revision 1 |2024-11-07 |Initial draft | 1.0        |
|      |      |         |         |
|      |      |         |         |

----
# 1. Introduction

Provide a short description of the software being specified. Describe its purpose, including relevant benefits, objectives, and goals.

The purpose of this web application is to improve the undergraduate Student Assistants (SAs) recruitment process. Computer Science Department can recruit SA for the introductary level courses and lab sections.

The application allow seemless interactions between the instructors and students. Students who are interested in SA positions can create accounts, and enter contact information as well as course preferences. Instructors can choose the student assistants among the students who are interested in their course.

----
# 2. Requirements Specification

This section specifies the software product's requirements. Specify all of the software requirements to a level of detail sufficient to enable designers to design a software system to satisfy those requirements, and to enable testers to test that the software system satisfies those requirements.

## 2.1 Customer, Users, and Stakeholders

A brief description of the customer, stakeholders, and users of your software.

The users of this software includes 
- Undergraduate students who are interested in SA positions
- Computer Science instructors who need SAs for their courses

----
## 2.2 User Stories
This section will include the user stories you identified for your project. Make sure to write your user stories in the form : 
"As a **[Role]**, I want **[Feature]** so that **[Reason/Benefit]** "

1. "As a **[student]**, I want **[to register a student account]** so that **[I can start applying for a student assistant position ]**. I want to be able to enter my WPI email as username, password, contact information (name, last name, WPI ID, email, phone), additional information (major, cumulative GPA, expected graduation date, etc.), and select courses that I have served as SA before "
2. "As a **[student]**, I want **[to log in using a student account with WPI email and password or with Azure Single Sign-On service]** "
3. "As a **[student]**, I want **[to view open SA positions]** so that **[I can choose my course preferences for student assistantships]**. I want to view various information such as course number, section, title, term, instructor's name and contact information, and qualifications needed for the SA position "
4. "As a **[student]**, I want **[to see recommended SA positions]** so that **[I see which courses I have served as an SA before or if I took those course and got an A]** "
5. "As a **[student]**, I want **[to apply to SA positions]** so that **[I can become an SA]**. I want to apply to various positions. Also, I want to be able to enter my grade for the course, the year and term when I took the course, and the year and term that I want to start the SAship for each of the position I apply to."
6. "As a **[student]**, I want **[to view and check statuses of the SA positions I've applied to]** so that **[I can keep track of them]**. I want to see submitted applications as "Pending", and if a professor has accepted a position I should see it as "Assigned". "
7. "As a **[student]**, I want **[to withdraw my pending SA applications]** so that **[I don't have to be considered for jobs I'm not interested in anymore]**.  "
8. "As an **[instructor]**, I want **[]** so that **[]** "
9. "As an **[instructor]**, I want **[]** so that **[]** "
10. "As an **[instructor]**, I want **[]** so that **[]** "
11. "As an **[instructor]**, I want **[]** so that **[]** "
12. "As an **[instructor]**, I want **[]** so that **[]** "
13. "As an **[instructor]**, I want **[]** so that **[]** "
14. "As an **[instructor]**, I want **[]** so that **[]** "
15. "As an **[instructor]**, I want **[]** so that **[]** "
16. "As an **[instructor]**, I want **[]** so that **[]** "

----
## 2.3 Use Cases

This section will include the specification for your project in the form of use cases. 

Group the related user stories and provide a use case for each user story group. You don't need to draw the use-case diagram for the use cases; you will only provide the textual descriptions.  **Also, you don't need to include the use cases for "registration" and "login" use cases for both student and faculty users.**

  * First, provide a short description of the actors involved (e.g., regular user, administrator, etc.) and then follow with a list of the use cases.
  * Then, for each use case, include the following:

    * Name,
    * Participating actors,
    * Entry condition(s) (in what system state is this use case applicable),
    * Exit condition(s) (what is the system state after the use case is done),
    * Flow of events (how will the user interact with the system; list the user actions and the system responses to those),
    * Alternative flow of events (what are the exceptional cases in the flow of events and they will be handles)
    * Iteration # (which sprint do you plan to work on this use case) 

Each use case should also have a field called "Iteration" where you specify in which iteration you plan to implement this feature.

You may use the following table template for your use cases. Copy-paste this table for each use case you will include in your document.

| Use case # 1      |   |
| ------------------ |--|
| Name              | "enter your reponse here"  |
| Participating actor  | "enter your reponse here"  |
| Entry condition(s)     | "enter your reponse here"  |
| Exit condition(s)           | "enter your reponse here"  |
| Flow of events | "enter your reponse here"  |
| Alternative flow of events    | "enter your reponse here"  |
| Iteration #         | "enter your reponse here"  |

----------------------------------------------------------------------------------------
On the student page, a student user can:
| Use case # 1 (3-4)     |   |
| ------------------ |--|
| Name              | View open SA positions  |
| Participating actor  | Student  |
| Entry condition(s)     | Student is registered and logged in  |
| Exit condition(s)           | The software display all available SA positions |
| Flow of events | 1. User go to the home page </br> 2. Software displays all available SA positions with various information: course number, section, title, term, instructor's name and contact information, and qualifications needed for the SA position |
| Alternative flow of events    | If there are no SA positions available, the software will display a message to tell the user that no positions are opened.  |
| Iteration #         | Iteration X  |

| Use case # 2 (3)     |   |
| ------------------ |--|
| Name              | View recommended SA positions  |
| Participating actor  | Student  |
| Entry condition(s)     | Student is registered and logged in  |
| Exit condition(s)           | The software display recommended SA positions based on matching criterias |
| Flow of events | 1. User go to the home page </br> 2. Software displays open SA positions sorted by if the user has served as an SA for the course before, or if the user has taken the course before and had an A, or both </br> 3. Software displays what criterias are met |
| Alternative flow of events    | If there are no SA recommendations available, the software will display a message to tell the user that there are no recommendations.  |
| Iteration #         | Iteration X  |

| Use case # 3 (5)     |   |
| ------------------ |--|
| Name              | Apply for SA positions  |
| Participating actor  | "enter your reponse here"  |
| Entry condition(s)     | "enter your reponse here"  |
| Exit condition(s)           | "enter your reponse here"  |
| Flow of events | "enter your reponse here"  |
| Alternative flow of events    | "enter your reponse here"  |
| Iteration #         | "enter your reponse here"  |

| Use case # 4 (6)     |   |
| ------------------ |--|
| Name              | Check SA applications status  |
| Participating actor  | "enter your reponse here"  |
| Entry condition(s)     | "enter your reponse here"  |
| Exit condition(s)           | "enter your reponse here"  |
| Flow of events | "enter your reponse here"  |
| Alternative flow of events    | "enter your reponse here"  |
| Iteration #         | "enter your reponse here"  |

| Use case # 5 (7)     |   |
| ------------------ |--|
| Name              | Withdraw pending SA applications  |
| Participating actor  | "enter your reponse here"  |
| Entry condition(s)     | "enter your reponse here"  |
| Exit condition(s)           | "enter your reponse here"  |
| Flow of events | "enter your reponse here"  |
| Alternative flow of events    | "enter your reponse here"  |
| Iteration #         | "enter your reponse here"  |

On the instructor page, a faculty user can:
| Use case # 6 (3)     |   |
| ------------------ |--|
| Name              | Add course sections  |
| Participating actor  | Faculty user  |
| Entry condition(s)     | "enter your reponse here"  |
| Exit condition(s)           | "enter your reponse here"  |
| Flow of events | "enter your reponse here"  |
| Alternative flow of events    | "enter your reponse here"  |
| Iteration #         | "enter your reponse here"  |

| Use case # 7 (4)     |   |
| ------------------ |--|
| Name              | Create SA positions  |
| Participating actor  | Faculty user  |
| Entry condition(s)     | "enter your reponse here"  |
| Exit condition(s)           | "enter your reponse here"  |
| Flow of events | "enter your reponse here"  |
| Alternative flow of events    | "enter your reponse here"  |
| Iteration #         | "enter your reponse here"  |

| Use case # 8 (5)     |   |
| ------------------ |--|
| Name              | View students applications  |
| Participating actor  | Faculty user  |
| Entry condition(s)     | "enter your reponse here"  |
| Exit condition(s)           | "enter your reponse here"  |
| Flow of events | "enter your reponse here"  |
| Alternative flow of events    | "enter your reponse here"  |
| Iteration #         | "enter your reponse here"  |

| Use case # 9 (6)     |   |
| ------------------ |--|
| Name              | View students qualifications  |
| Participating actor  | Faculty user  |
| Entry condition(s)     | "enter your reponse here"  |
| Exit condition(s)           | "enter your reponse here"  |
| Flow of events | "enter your reponse here"  |
| Alternative flow of events    | "enter your reponse here"  |
| Iteration #         | "enter your reponse here"  |

| Use case # 10 (7-8-9)      |   |
| ------------------ |--|
| Name              | Assign student to SA position  |
| Participating actor  | Faculty user  |
| Entry condition(s)     | "enter your reponse here"  |
| Exit condition(s)           | "enter your reponse here"  |
| Flow of events | "enter your reponse here"  |
| Alternative flow of events    | "enter your reponse here"  |
| Iteration #         | "enter your reponse here"  |

----
# 3. User Interface

Here you should include the sketches or mockups for the main parts of the interface.
You may use Figma to design your interface:

  Example image. The image file is in the `./images` directory.
  <kbd>
      <img src="images/figma.jpg"  border="2">
  </kbd>
  
----
# 4. Product Backlog

Here you should include a link to your GitHub repo issues page, i.e., your product backlog. Make sure to create an issue for each user story.  

----
# 5. References

Cite your references here.

For the papers you cite give the authors, the title of the article, the journal name, journal volume number, date of publication and inclusive page numbers. Giving only the URL for the journal is not appropriate.

For the websites, give the title, author (if applicable) and the website URL.

----
----
# Appendix: Grading Rubric
(Please remove this part in your final submission)

These is the grading rubric that we will use to evaluate your document. 

| Max Points  | **Content** |
| ----------- | ------- |
| 4          | Do the requirements clearly state the customers’ needs? |
| 2          | Do the requirements avoid specifying a design (note: customer-specified design elements are allowed)? |
| | |  
|    | **Completeness** |
| 14 | Are user stories complete? Are all major user stories included in the document?  |
| 5 | Are user stories written in correct form? | 
| 14 |  Are all major use cases (except registeration and login) included in the document? |
| 15 | Are use cases written in sufficient detail to allow for design and planning? Are the "flow of events" in use case descriptions written in the form of "user actions and system responses to those"? Are alternate flow of events provided (when applicable)? | 
| 6 |  Are the User Interface Requirements given with some detail? Are there some sketches, mockups?  |
| | |  
|   | **Clarity** |
| 5 | Is the document carefully written, without typos and grammatical errors? <br> Is each part of the document in agreement with all other parts? <br> Are all items clear and not ambiguous? |
| | |
|**65**|**TOTAL**|


