# Project Title: Right 2 Ya

## Overview
I made this app from a Template and added more components as well a Dashboard. This app consists of 3 apps. The is a Customer app that creates a delivery job. A courier app that can take orders and deliver them. The last app is the Dispatcher dashboard that tracks drivers and here you can release jobs to available drivers.

## Technologies Used
- Django
- HTML/CSS/Bootstrap
- JavaScript 
- Python
- DRF
- Channels
- Redis
- Nginx
- Paypal API - For courier payouts
- Stripe API - to charge customers
- Twilio API - order updates
- Google Maps/Directions/Places API
- AWS S3
- Postgres

## Screenshots (if applicable)


## Demo
N/A

## Installation
1. **Download the repository:**

2. **Set up a virtual environment or install dependencies:**
- Create a virtual environment:
  ```
  python3 -m venv env
  ```
- Activate the virtual environment:
  - On Windows:
    ```
    env\Scripts\activate
    ```
  - On macOS and Linux:
    ```
    source env/bin/activate
    ```
- Install dependencies:
  ```
  pip3 install -r requirements.txt
  ```

## Database Setup
 **Run migrations:**
 ```
  python3 manage.py makemigrations
  python3 manage.py migrate
 ```


## Usage
1. **Run the development server:**


2. **Access the project in your web browser at `http://localhost:8000`**

## What I Learned
I learned how to use GPS for tracking. Redis and Channels to relay updates to other parts of the application. I learned how to put this kind of application online in a production setting. I also learned how to use Stripe and Paypal for receiving and sending payments.

## Challenges Faced
This app was very difficult and I worked on this for the whole 2023. While working on the tutorial I came across alot of errors and mistakes. I was forced to scour through reddit and stackoverflow to overcome numerous pitfalls. I was unfamiliar with most of these API and had to learn how to get and disregard certain data if it was not needed. I also wanted to have this work online so I used Digital Ocean to host this project. As I was not familiar with the server side I had to do alot of research on Redis and Channels and Nginx. There was alot of challenges on each part of these apps and alot to list but it was an exciting year and many obstacles to overcome.

## Future Improvements
No plans at this time.

## License
n/a

## Contact Information

tyraineytech@gmail.com




#  This part might be needed depending on what errors you may occur while trying to load this project. I will be fixing this soon

Remove all social connections to app
setup database: https://github.com/mitchtabian/HOWTO-django-channels-daphne

# To set up the project
pip3 install -r requirements.txt


