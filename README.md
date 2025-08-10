
# Lifestyle Tracker (CLI)

A simple **Command-Line Interface (CLI)** application designed to help users track their **PCOS/PCOD-related lifestyle habits** — including periods, mood, sleep, and water intake.  
This project is part of my **Python learning journey** and is aimed at building both **practical coding skills** and **health-focused tools**.

---

## 📌 Features

- **Period Tracking** – Log daily period status (yes/no).
- **Mood Tracking** – Record daily mood with predefined or custom moods.
- **Sleep Tracking** – Log daily sleep hours.
- **Water Intake Tracking** – Track daily water intake in liters.
- **Weekly Summary** – View last 7 days’ stats (period days, average sleep, water intake).
- **Visualizations** – Display graphs for mood, sleep, and water intake trends.
- **Help Menu** – Shows available commands.
- **Input Validation** – Ensures correct and meaningful entries.

---

## 🛠️ Installation & Setup
---

## Installation & Setup for **PCOS Lifestyle Tracker CLI**

1. **Clone the repository** to your local machine:

   ```bash
   git clone https://github.com/yourusername/pcos-lifestyle-tracker-cli.git

2. **Navigate into the project folder**:

   ```bash
   cd pcos-lifestyle-tracker-cli
   ```

3. **(Optional but recommended) Create a virtual environment** to keep project dependencies isolated:

   * On Windows:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   * On macOS/Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

4. **Install any dependencies** (if listed in `requirements.txt`). For this CLI app, there might not be extra dependencies, but if there are, run:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application** by executing:

   ```bash
   python tracker.py
   ```

6. **Follow the prompts** in your terminal to start logging your PCOS lifestyle data.

---



---
##  Installation & Setup for Lifestyle Tracker Streamlit App

### Installation and Setup

1. **Clone the repository** to your local machine:

   ```bash
   git clone https://github.com/yourusername/pcos-lifestyle-tracker-streamlit.git

2. **Navigate into the project folder**:

   ```bash
   cd pcos-lifestyle-tracker-streamlit
   ```

3. **(Optional but recommended) Create a virtual environment**:

   * On Windows:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   * On macOS/Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

4. **Install required Python packages** using `pip`:

   * Make sure you have a `requirements.txt` file that includes at least:

     ```
     streamlit
     pandas
     matplotlib
     ```

   * Run:

     ```bash
     pip install -r requirements.txt
     ```

   If you don’t have a `requirements.txt`, just run:

   ```bash
   pip install streamlit pandas matplotlib
   ```

5. **Run the Streamlit app** by executing:

   ```bash
   streamlit run pcos_tracker_app.py
   ```

6. This will open the app in your default web browser.
   If it doesn’t open automatically, look for a URL in the terminal output like:

   ```
   Local URL: http://localhost:8501
   ```

   Open this URL manually in your browser.

---


## 📖 How to Use

When you run the script, you will see a **main menu** with different options.
Choose a number from the menu to perform an action:

* `1` – Log today’s period, mood, sleep, and water intake
* `2` – View last 7 days’ summary
* `3` – Show visualizations (mood chart, sleep chart, water chart)
* `4` – Help menu
* `5` – Exit

**Example:**

Welcome to PCOS Lifestyle Tracker!
1. Add daily entry
2. View weekly summary
3. Show visualizations
4. Help
5. Exit
Enter your choice: 1


## 📂 Project Structure

📦 PCOS-Lifestyle-Tracker

 ┣ 📜 pcos_tracker.py        # Main Python script
 
 ┣ 📜 data.csv               # Stores user data
 
 ┣ 📜 README.md              # Project documentation
 
 ┗ 📜 requirements.txt       # Required libraries


## ✅ Input Validation

* **Period** – Only accepts `yes` or `no`.
* **Sleep Hours** – Must be a positive number (max 24).
* **Water Intake** – Must be a positive number (max 10 liters).
* **Mood** – Choose from given options or enter a custom mood.

---

## 💡 Future Improvements

* Add **BMI tracking** and health tips
* Enable **export to PDF**
* Add **monthly and yearly reports**
* Store data in a database instead of CSV

---

## 🧑‍💻 Author

**Nidhi** – Automation & Robotics Engineering Student

📌 Focus: AI/ML, HealthTech, and practical coding projects


---

## 📜 License

This project is open-source and available under the **MIT License**.

---


