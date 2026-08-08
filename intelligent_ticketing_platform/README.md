# Intelligent Ticketing Platform
### Machine Learning-Based Online Event Booking and Management System

**Student:** NKEEH FAVOUR GODWIN  
**Matric No:** U2022/5570030  
**Department:** Computer Science, University of Port Harcourt  
**Date:** July 2026

---

## What This Project Does
This is a web application that allows people to:
- Register and login
- Browse and search events
- Get personalized event recommendations (using Machine Learning)
- Book tickets for events
- Allow event organizers to create events and see predicted ticket demand (using Machine Learning)

---

## Project Structure (Simple Explanation)

```
intelligent_ticketing_platform/
│
├── app/                        ← Main application folder
│   ├── __init__.py             ← Starts the Flask app
│   ├── models.py               ← Database tables (Users, Events, Bookings)
│   ├── routes/                 ← Website pages & actions
│   │   ├── auth.py             ← Login & Register
│   │   ├── events.py           ← View & manage events
│   │   ├── bookings.py         ← Book tickets
│   │   ├── recommendations.py  ← ML Recommendations
│   │   └── organizer.py        ← Organizer dashboard + demand prediction
│   ├── ml/                     ← Machine Learning models
│   │   ├── recommender.py      ← Content-Based Filtering
│   │   └── demand_predictor.py ← Linear Regression
│   ├── static/                 ← CSS, JavaScript, Images
│   ├── templates/              ← HTML pages
│   └── utils/                  ← Helper functions
│
├── data/                       ← Sample data & saved ML models
├── database/                   ← Database setup file
├── config.py                   ← App settings
├── run.py                      ← File to start the website
├── requirements.txt            ← List of Python libraries needed
└── README.md                   ← This file
```

---

## How We Will Build It (Step-by-Step Modules)

We will build this project in **clear modules**.  
You only need to follow one module at a time.

**Module 1:** Project Setup & Installation  
**Module 2:** Database Design  
**Module 3:** User Registration & Login  
**Module 4:** Event Management (Create & View Events)  
**Module 5:** Ticket Booking System  
**Module 6:** Machine Learning – Event Recommendation  
**Module 7:** Machine Learning – Ticket Demand Prediction  
**Module 8:** Frontend Design (Beautiful Pages)  
**Module 9:** Testing & Evaluation  
**Module 10:** Final Documentation

---

## Technologies Used
- **Python** + **Flask** → Backend
- **HTML, CSS, JavaScript** → Frontend
- **MySQL** → Database
- **scikit-learn** → Machine Learning
- **pandas & numpy** → Data handling
