
# PCOS Lifestyle Tracker (CLI)

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

1. **Clone the Repository**
   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>


2. **Install Dependencies**
   Make sure you have **Python 3.x** installed. Then install the required libraries:

   ```bash
   pip install matplotlib
   ```

3. **Run the Application**

   ```bash
   python pcos_tracker.py

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
```


## 📂 Project Structure

```
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


