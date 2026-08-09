# Antaranga - Tour Management & Recommendation System

**Antaranga** is a web-based tour management and recommendation system designed to help users plan their perfect journey in Nepal. By understanding user preferences through an interactive questionnaire, the platform provides personalized destination recommendations tailored to their ideal travel experience.

## 🚀 Features

* **Interactive Questionnaire:** Collects user preferences based on:

  * Adventure
  * Culture
  * Altitude
  * Natural Beauty

* **Smart Recommendation Engine:** Analyzes questionnaire responses and recommends destinations across Nepal that best match the user's preferences.

* **Personalized Travel Recommendations:** Helps users discover destinations based on their preferred type of travel experience.

* **Comprehensive Location Insights:** Provides useful information about recommended destinations, including:

  * Local cuisine and traditional foods
  * Altitude
  * Average temperature
  * Best months to visit

## 🛠️ Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML5, CSS3, JavaScript
* **Database:** MySQL

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/pokharelayam1/Antaranga.git
cd Antaranga
```

### 2. Set Up a Virtual Environment

It is recommended to use a virtual environment for the project.

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install Django and the required MySQL client:

```bash
pip install django mysqlclient
```

If the project contains a `requirements.txt` file, you can install all dependencies using:

```bash
pip install -r requirements.txt
```

### 4. Database Configuration

Antaranga uses **MySQL** as its database.

1. Start your MySQL server.
2. Create a database for the project.
3. Import the provided SQL database dump:

```bash
mysql -u your_username -p your_database_name < mysql.sql
```

4. Open:

```text
project/settings.py
```

5. Update the `DATABASES` configuration with your MySQL credentials.

Example:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Run Database Migrations

After configuring the database, run:

```bash
python manage.py migrate
```

### 6. Start the Development Server

Run the Django development server:

```bash
python manage.py runserver
```

The application will normally be available at:

```text
http://127.0.0.1:8000/
```

Open the URL in your web browser to access Antaranga.

## 🎯 How It Works

1. The user starts the Antaranga platform.
2. The system presents an interactive questionnaire.
3. The user provides preferences related to adventure, culture, altitude, and natural beauty.
4. The recommendation engine analyzes the responses.
5. Suitable destinations in Nepal are selected based on the user's preferences.
6. The recommended destinations are displayed with useful location information.
7. Users can explore details such as local food, altitude, temperature, and the best time to visit.

## 🌄 Purpose

Antaranga aims to make travel planning in Nepal easier and more personalized by connecting travelers with destinations that match their interests and preferred travel experiences.

## 📌 Future Improvements

* User authentication and personalized profiles
* Interactive maps and location tracking
* Weather API integration
* Hotel and accommodation recommendations
* Transportation information
* Online tour booking
* AI-based travel recommendations
* Multi-day personalized itinerary generation
