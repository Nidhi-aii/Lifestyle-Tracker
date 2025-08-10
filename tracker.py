import csv
import os
from datetime import date
import matplotlib.pyplot as plt
import json
import os
import calendar

def load_config():
    config_file = 'config.json'

    # Check if config file exists
    if os.path.isfile(config_file):
        print("📂 Loading existing config...")
        try:
            with open(config_file, 'r') as file:
                config = json.load(file)
                print(f"✅ Config loaded: Sleep ≥ {config['sleep_goal']} hrs, Water ≥ {config['water_goal']} L")
                return config
        except Exception as e:
            print(f"⚠️ Error reading config file: {e}")
            print("Proceeding to recreate it...")

    # If not found or unreadable, create a new one
    print("\n🔧 Let's set up your PCOS Tracker goals 🎯")

    while True:
        try:
            sleep_goal = float(input("Enter your daily sleep goal (hours, e.g., 7): "))
            water_goal = float(input("Enter your daily water goal (litres, e.g., 2): "))
            break
        except ValueError:
            print("! Invalid input. Please enter numeric values.")

    config = {
        'sleep_goal': sleep_goal,
        'water_goal': water_goal
    }

    try:
        with open(config_file, 'w') as file:
            json.dump(config, file, indent=4)
        print("✅ Config file saved at:", os.path.abspath(config_file))
    except Exception as e:
        print(f"❌ Failed to save config: {e}")

    return config

def update_goals():
    global config
    config_file = 'config.json'

    print("\n🔧 Update Your PCOS Tracker Goals")

    while True:
        try:
            sleep_goal = float(input(f"Enter new sleep goal (current: {config['sleep_goal']}): "))
            water_goal = float(input(f"Enter new water goal (current: {config['water_goal']}): "))
            break
        except ValueError:
            print("! Please enter valid numbers.")

    config['sleep_goal'] = sleep_goal
    config['water_goal'] = water_goal

    try:
        with open(config_file, 'w') as file:
            json.dump(config, file, indent=4)
        print("✅ Goals updated successfully!")
    except Exception as e:
        print(f"❌ Failed to update config: {e}")


def get_daily_input():
    print('\nWelcome to PCOS Tracker!!')
    today = date.today().isoformat()

    while True:
        period = input("Did you get your period today? (yes/no): ").strip().lower()
        if period in ['yes', 'no']:
            break
        else:
            print("! Please enter 'yes' or 'no'.")


    while True:
        try:
            sleep = float(input('How many hours did you sleep😴 : '))
            if sleep < 0:
                print("! Please enter a positive number.")
                continue
            break
        except ValueError:
            print('! Invalid input. Please enter a number.')

    while True:
        mood = input('Happy😁 / Neutral🙂 / Low🙁 : ').capitalize()
        if mood not in ['Happy', 'Neutral', 'Low']:
            print("! Invalid mood. Please enter Happy, Neutral, or Low.")
            continue
        break

    while True:
        try:
            water_intake = float(input('How many litres of water did you drink💧: '))
            if water_intake < 0:
                print("! Please enter a positive number.")
                continue
            break
        except ValueError:
            print('! Invalid input. Please enter a number.')

    notes = input('Write anything: ')

    filename = 'tracker_data.csv'
    file_exists = os.path.isfile(filename)

    # Create file with correct header if it doesn't exist
    if not file_exists:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['date', 'sleep', 'mood', 'water_intake', 'period', 'notes'])

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([today, sleep, mood, water_intake, period, notes])

    print('✅ Your entry has been saved!')


def view_last_entries():
    filename = 'tracker_data.csv'
    if not os.path.isfile(filename):
        print('No entries found yet. Please add data first.')
        return

    with open(filename, 'r') as file:
        reader = list(csv.reader(file))
        header = reader[0]
        data = reader[1:]

        if not data:
            print('No data available.')
            return

        last_entries = data[-5:]
        print('\nLast 5 entries:')
        print(', '.join(header))
        for row in last_entries:
            print(', '.join(row))


def view_weekly_summary():
    from datetime import datetime

    filename = 'tracker_data.csv'
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        rows = [row for row in reader if len(row) >= 6]

    entries = []
    mood_counts = {'Happy': 0, 'Neutral': 0, 'Low': 0}
    total_sleep = 0
    total_water = 0
    period_count = 0
    entry_count = 0

    for row in rows:
        try:
            entry_date = datetime.strptime(row[0], "%Y-%m-%d").date()
            sleep = float(row[1])
            mood = row[2]
            water = float(row[3])
            period = row[4].strip().lower()
            entries.append((entry_date, sleep, water))
            total_sleep += sleep
            total_water += water
            mood_counts[mood] += 1
            entry_count += 1
            if period == 'yes':
                period_count += 1
        except:
            continue

    if entry_count == 0:
        print("No valid data found.")
        return

    print(f'\nAverage Sleep: {total_sleep / entry_count:.1f} hrs')
    print(f'Average Water Intake: {total_water / entry_count:.1f} L')
    print(f'Mood Counts: {mood_counts}')
    print(f'Period days this week: {period_count}')

    # --- Streak Logic Begins ---
    def calculate_streaks(values, condition):
        current_streak = 0
        longest_streak = 0
        temp_streak = 0
        for val in values:
            if condition(val):
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 0
        current_streak = temp_streak
        return current_streak, longest_streak

    # Extract sequences
    sleep_values = [sleep for (_, sleep, _) in entries]
    water_values = [water for (_, _, water) in entries]

    # Streaks
    sleep_current, sleep_longest = calculate_streaks(sleep_values, lambda x: x >= config['sleep_goal'])
    water_current, water_longest = calculate_streaks(water_values, lambda x: x >= config['water_goal'])

    print(f"\n🎯 Sleep streak: {sleep_current} day(s) with ≥{config['sleep_goal']} hrs sleep (Longest: {sleep_longest})")
    print(f"💧 Water streak: {water_current} day(s) with ≥{config['water_goal']}L water (Longest: {water_longest})")


def view_all_entries():
    with open('tracker_data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        print('\nAll Tracked Entries:')
        for row in reader:
            print(', '.join(row))


def reset_tracker():
    while True:
        confirm = input("Are you sure you want to reset all data? (yes/no): ").strip().lower()
        if confirm in ['yes', 'no']:
            break
        else:
            print("! Please enter 'yes' or 'no'.")

    if confirm == 'yes':
        with open('tracker_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['date', 'sleep', 'mood', 'water_intake', 'period', 'notes'])  # fixed header
        print("🗑️ Tracker has been reset successfully.")
    else:
        print("❎ Reset cancelled.")


def export_weekly_summary():
    with open('tracker_data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        total_sleep = 0
        total_water = 0
        mood_counts = {'Happy': 0, 'Neutral': 0, 'Low': 0}
        entry_count = 0

        for row in reader:
            if len(row) < 6:
                continue

            sleep = float(row[1])
            mood = row[2]
            water = float(row[3])

            total_sleep += sleep
            total_water += water
            entry_count += 1
            mood_counts[mood] += 1

    if entry_count == 0:
        print("No data to export.")
        return

    filename = 'export_weekly_summary.csv'
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['avg_sleep', 'avg_water', 'happy_count', 'neutral_count', 'low_count'])

        writer.writerow([
            total_sleep / entry_count,
            total_water / entry_count,
            mood_counts['Happy'],
            mood_counts['Neutral'],
            mood_counts['Low']
        ])

    print("📁 Your weekly summary has been exported successfully!")


def view_period_days():
    with open('tracker_data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        period_dates = [row[0] for row in reader if len(row) >= 6 and row[4].strip().lower() == 'yes']

    print("\n🩸 Period days tracked:")
    if not period_dates:
        print("No period days recorded.")
    for date in period_dates:
        print(f"- {date}")

def show_help():
    print("\n===== Help Menu =====")
    print("1 - Add today's health log")
    print("2 - View last 5 entries")
    print("3 - View weekly summary")
    print("4 - View all entries")
    print("5 - Reset tracker")
    print("6 - Export weekly summary to CSV")
    print("7 - Show weekly mood/sleep/water trends (graph)")
    print("8 - View period days")
    print("9 - Exit the tracker")
    print("h or ? - Show this help menu")
    print("======================\n")




def plot_weekly_trends():
    with open('tracker_data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        mood_counts = {'Happy': 0, 'Neutral': 0, 'Low': 0}
        total_sleep = 0
        total_water = 0
        entry_count = 0

        for row in reader:
            if len(row) < 6:
                continue
            sleep = float(row[1])
            mood = row[2]
            water = float(row[3])

            total_sleep += sleep
            total_water += water
            mood_counts[mood] += 1
            entry_count += 1

    if entry_count == 0:
        print("No data to plot.")
        return

    avg_sleep = total_sleep / entry_count
    avg_water = total_water / entry_count

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    axs[0].bar(mood_counts.keys(), mood_counts.values(), color='plum')
    axs[0].set_title('Mood Trends')
    axs[0].set_ylabel('Count')

    axs[1].bar(['Avg Sleep', 'Avg Water'], [avg_sleep, avg_water], color=['skyblue', 'lightgreen'])
    axs[1].set_title('Weekly Averages')
    axs[1].set_ylabel('Values')

    plt.tight_layout()
    plt.show()


def manage_entries():
    filename = 'tracker_data.csv'
    if not os.path.isfile(filename):
        print("⚠️ No data file found.")
        return

    with open(filename, 'r') as file:
        reader = list(csv.reader(file))
        header = reader[0]
        raw_rows = reader[1:]

    # Filter out bad/empty rows
    rows = [row for row in raw_rows if len(row) == len(header)]

    if not rows:
        print("⚠️ No valid entries to edit or delete.")
        return

    # Show entries with indexes
    print("\n📋 Tracked Entries:")
    for i, row in enumerate(rows):
        print(f"{i + 1}. {', '.join(row)}")

    try:
        choice = int(input("\nEnter entry number to modify (or 0 to cancel): "))
        if choice == 0:
            return
        if choice < 1 or choice > len(rows):
            print("❌ Invalid choice.")
            return
        index = choice - 1
    except ValueError:
        print("❌ Please enter a number.")
        return

    selected = rows[index]
    print("\nSelected Entry:")
    print(', '.join(selected))

    action = input("Type 'e' to edit, 'd' to delete, or 'c' to cancel: ").strip().lower()
    if action == 'e':
        print("\nEditing Entry. Press Enter to keep original value.")
        new_row = []
        for i, field in enumerate(header):
            value = input(f"{field} [{selected[i]}]: ").strip()
            new_row.append(value if value else selected[i])
        rows[index] = new_row
        print("✅ Entry updated.")
    elif action == 'd':
        confirm = input("Are you sure you want to delete this entry? (yes/no): ").strip().lower()
        if confirm == 'yes':
            del rows[index]
            print("🗑️ Entry deleted.")
        else:
            print("❎ Deletion cancelled.")
            return
    else:
        print("❎ Cancelled.")
        return

    # Save cleaned + updated data
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)
    print("💾 Changes saved to file.")

def show_period_calendar_interactive():
    import calendar
    from datetime import datetime, date

    filename = 'tracker_data.csv'
    today = date.today()
    year = today.year
    month = today.month

    # Step 1: Load existing entries
    rows = []
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            reader = list(csv.reader(file))
            header = reader[0]
            rows = reader[1:]
    else:
        header = ['date', 'sleep', 'mood', 'water_intake', 'period', 'notes']

    # Step 2: Build a dict of entries
    entries = {row[0]: row for row in rows if len(row) >= 6}

    # Step 3: Build calendar & period markers
    period_days = set()
    for row in entries.values():
        try:
            entry_date = datetime.strptime(row[0], "%Y-%m-%d").date()
            if entry_date.year == year and entry_date.month == month and row[4].strip().lower() == 'yes':
                period_days.add(entry_date.day)
        except:
            continue

    print(f"\n📅 Period Calendar - {calendar.month_name[month]} {year}")
    print("🩸 = Period day | T = Today\n")
    print("Mo Tu We Th Fr Sa Su")

    cal = calendar.Calendar()
    for week in cal.monthdayscalendar(year, month):
        line = ""
        for day in week:
            if day == 0:
                line += "   "
            elif day == today.day:
                line += " T "
            elif day in period_days:
                line += "🩸 "
            else:
                line += f"{day:2d} "
        print(line)

    # Step 4: Ask user to select a day
    selected = input("\nSelect a day to update period status (1-31), or press Enter to skip: ").strip()
    if not selected:
        return

    try:
        selected_day = int(selected)
        selected_date = date(year, month, selected_day).isoformat()
    except:
        print("❌ Invalid day selected.")
        return

    # Step 5: Check if entry exists
    if selected_date in entries:
        row = entries[selected_date]
        print(f"\nCurrent period status for {selected_date}: {row[4]}")
        new_status = input("Set period status to (yes/no): ").strip().lower()
        if new_status in ['yes', 'no']:
            row[4] = new_status
            entries[selected_date] = row
            print("✅ Period status updated.")
        else:
            print("❌ Invalid input. Use 'yes' or 'no'.")
            return
    else:
        print(f"\nNo entry found for {selected_date}.")
        new_status = input("Do you want to create a new entry for this date? (yes/no): ").strip().lower()
        if new_status != 'yes':
            return
        period = input("Set period status (yes/no): ").strip().lower()
        if period not in ['yes', 'no']:
            print("❌ Invalid input.")
            return
        # Fill with default values
        new_row = [selected_date, '', '', '', period, '']
        entries[selected_date] = new_row
        print("✅ New entry created and period marked.")

    # Step 6: Write back to CSV
    all_rows = list(entries.values())
    all_rows.sort()  # by date

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(all_rows)

    print("💾 Changes saved successfully!")




def plot_streak_chart():
    import matplotlib.pyplot as plt
    from datetime import datetime

    filename = 'tracker_data.csv'
    if not os.path.isfile(filename):
        print("No data found.")
        return

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        rows = [row for row in reader if len(row) >= 6]

    entries = []
    for row in rows:
        try:
            entry_date = datetime.strptime(row[0], "%Y-%m-%d").date()
            sleep = float(row[1])
            water = float(row[3])
            entries.append((entry_date, sleep, water))
        except:
            continue

    if not entries:
        print("No valid entries to display.")
        return

    entries.sort()  # oldest to newest

    dates = []
    status = []  # 0 = missed both, 1 = met one, 2 = met both

    for entry_date, sleep, water in entries:
        goal_hit = 0
    if sleep >= config['sleep_goal']:
        goal_hit += 1
    if water >= config['water_goal']:
        goal_hit += 1


        dates.append(entry_date.strftime("%b %d"))
        status.append(goal_hit)

    # Plotting
    colors = {0: 'lightcoral', 1: 'gold', 2: 'lightgreen'}
    bar_colors = [colors[val] for val in status]

    plt.figure(figsize=(12, 5))
    plt.bar(dates, status, color=bar_colors, edgecolor='black')
    plt.xticks(rotation=45)
    plt.ylim(0, 2.5)
    plt.yticks([0, 1, 2], ['Missed Both', 'One Goal', 'Both Goals'])
    plt.title(f'📊 Daily Goal Streaks (Sleep ≥ {config["sleep_goal"]}h, Water ≥ {config["water_goal"]}L)')
    plt.xlabel('Date')
    plt.ylabel('Goals Met')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.show()

# Load goals from config file
config = load_config()

# Start the tracker app



def main_menu():
    while True:
        print("\n1. Add daily entry")
        print("2. View last 5 entries")
        print("3. View weekly summary")
        print("4. View all entries")
        print("5. Reset tracker")
        print("6. Export weekly summary")
        print("7. Show weekly trends")
        print("8. View period days")
        print("h or ? - Help menu")
        print("9. Exit")
        print("10. View streak chart")
        print("11. Update your goals")
        print("12. Edit or delete an entry")
        print("13. Show period calendar (and update)")


        choice = input("Enter your choice (1-10, h, ?): ").strip().lower()

        if choice == '1':
            get_daily_input()
        elif choice == '2':
            view_last_entries()
        elif choice == '3':
            view_weekly_summary()
        elif choice == '4':
            view_all_entries()
        elif choice == '5':
            reset_tracker()
        elif choice == '6':
            export_weekly_summary()
        elif choice == '7':
            plot_weekly_trends()
        elif choice == '8':
            view_period_days()
        elif choice == '9':
            print("👋 Exiting the tracker. Stay healthy!")
        elif choice == '10':
            plot_streak_chart()
        elif choice == '11':
            update_goals()
        elif choice == '12':
            manage_entries()
        elif choice == '13':
            show_period_calendar_interactive()
        elif choice in ['h', '?']:
            show_help()
        else:
            print("❌ Invalid input. Please try again.")


# Start the app
main_menu()
