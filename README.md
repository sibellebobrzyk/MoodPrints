# **Book recommendation app based on emotional state**

This web application suggests the ideal book for the user based on their emotional state, which is determined through an interactive questionnaire. The system then recommends a book that aligns with the user's mood and feelings.

## **Technologies used**

- **Frontend:** HTML, CSS, and JavaScript to create and style the web form.
- **Backend:** Python for managing book recommendations.
- **Database:** SQL to store information about users and track the percentage of users who received the same book as a recommendation.
- **Docker:** Used to streamline and isolate the frontend application.

## **Docker commands**

To run the frontend with Docker, use the following commands:
- docker build -t moodprints .
- docker run -d -p 8080:80 moodprints
