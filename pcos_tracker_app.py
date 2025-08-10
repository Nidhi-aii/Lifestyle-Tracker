# pcos_tracker_app.py
import streamlit as st
import csv
import os
import json
import calendar
from datetime import date, datetime, timedelta
from collections import Counter

# -----------------------
# File names & config
# -----------------------
DATA_FILE = "tracker_data.csv"
PROFILE_FILE = "profile.json"
CONFIG_FILE = "config.json"

st.set_page_config(page_title="Lifestyle Tracker", layout="wide")

# -----------------------
# Helpers: file & config
# -----------------------
def ensure_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['date','sleep','mood','water_intake','period','notes'])

def read_all_entries():
    ensure_data_file()
    with open(DATA_FILE, "r", newline="") as f:
        rows = list(csv.reader(f))
        if not rows:
            return []
        return rows[1:]  # skip header

def write_all_entries(rows):
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['date','sleep','mood','water_intake','period','notes'])
        writer.writerows(rows)

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    cfg = {"sleep_goal": 7.0, "water_goal": 2.0}
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)
    return cfg

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)

config = load_config()

def load_profile():
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def save_profile(profile):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile, f, indent=4)

def calculate_age(dob_iso):
    try:
        b = datetime.fromisoformat(dob_iso).date()
        today = date.today()
        return today.year - b.year - ((today.month, today.day) < (b.month, b.day))
    except Exception:
        return None

def parse_float_safe(val, default=0.0):
    try:
        return float(val)
    except Exception:
        return default

def group_period_streaks(period_dates):
    if not period_dates:
        return []
    dates = sorted([datetime.fromisoformat(d).date() for d in period_dates])
    streaks = []
    cur = [dates[0]]
    for i in range(1, len(dates)):
        if (dates[i] - dates[i-1]).days == 1:
            cur.append(dates[i])
        else:
            streaks.append(cur)
            cur = [dates[i]]
    streaks.append(cur)
    return streaks

# -----------------------
# UI: Profile / Dashboard
# -----------------------

# create session state keys
if "page" not in st.session_state:
    st.session_state.page = "dashboard"  # or "profile_setup" if no profile yet
if "profile_edit_open" not in st.session_state:
    st.session_state.profile_edit_open = False

profile = load_profile()
if profile is None:
    # force the profile setup first time
    st.session_state.page = "profile_setup"

# Top title
st.markdown("<h1 style='text-align:center'>🌸 Lifestyle Tracker</h1>", unsafe_allow_html=True)
st.write("")  # small spacer

# Layout: left profile card (1/4), main area (3/4)
main_col = st.container()

with st.sidebar:
    # --- Start Profile Card (moved here) ---
    st.markdown("<div style='padding:8px;border-radius:10px;background:#ffe9e6'>", unsafe_allow_html=True)
    if profile:
        age = calculate_age(profile.get("dob")) or "-"
        name = profile.get("name", "Your Name")
        cycle_len = profile.get("cycle_length", "")
        st.markdown(f"<h3 style='color:#b82b2b; margin:4px 0;'>👋 {name}</h3>", unsafe_allow_html=True)
        st.write(f"*Age:* {age}")
        st.write(f"*Cycle length:* {cycle_len} days" if cycle_len else "*Cycle length:* -")
        rows = read_all_entries()
        total_entries = len(rows)
        avg_sleep = None
        avg_water = None
        if total_entries:
            sleeps = [parse_float_safe(r[1]) for r in rows if r[1] != ""]
            waters = [parse_float_safe(r[3]) for r in rows if r[3] != ""]
            if sleeps:
                avg_sleep = sum(sleeps)/len(sleeps)
            if waters:
                avg_water = sum(waters)/len(waters)
        st.write(f"*Total entries:* {total_entries}")
        st.write(f"*Avg sleep:* {avg_sleep:.1f} hrs" if avg_sleep is not None else "*Avg sleep:* -")
        st.write(f"*Avg water:* {avg_water:.1f} L" if avg_water is not None else "*Avg water:* -")
        st.write("")
        if st.button("Edit Profile"):
            st.session_state.profile_edit_open = True
            st.session_state.page = "profile_setup"
            st.rerun()
    else:
        st.write("No profile found.")
        if st.button("Create Profile"):
            st.session_state.page = "profile_setup"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    # --- End Profile Card ---

with main_col:
    # PROFILE SETUP / EDIT
    if st.session_state.page == "profile_setup":
        st.header("👤 Profile Setup")
        # load values if present
        name_val = profile.get("name") if profile else ""
        dob_val = datetime.fromisoformat(profile["dob"]).date() if profile and profile.get("dob") else date(1995,1,1)
        cycle_val = profile.get("cycle_length") if profile else 28

        with st.form("profile_form"):
            name = st.text_input("Full name", value=name_val)
            dob = st.date_input("Date of birth", value=dob_val)
            cycle_length = st.number_input("Average cycle length (days)", min_value=18, max_value=45, value=int(cycle_val))
            savep = st.form_submit_button("Save Profile")

        if savep:
            profile_data = {
                "name": name,
                "dob": dob.isoformat(),
                "cycle_length": int(cycle_length)
            }
            save_profile(profile_data)
            st.success("Profile saved. Reloading...")
            st.session_state.profile_edit_open = False
            st.session_state.page = "dashboard"
            st.rerun()

    # DASHBOARD (default)
    elif st.session_state.page == "dashboard":
        st.header("Dashboard")
        st.markdown("### Quick Actions")
        a, b, c, d = st.columns(4)
        if a.button("➕ Add Entry", use_container_width=True):
            st.session_state.page = "add_entry"
            st.rerun()
        if b.button("📅 Period Calendar", use_container_width=True):
            st.session_state.page = "period_calendar"
            st.rerun()
        if c.button("📖 All Entries", use_container_width=True):
            st.session_state.page = "view_all"
            st.rerun()
        if d.button("📊 Weekly Summary", use_container_width=True):
            st.session_state.page = "weekly_summary"
            st.rerun()

        st.markdown("---")
        st.subheader("Quick Stats")
        rows = read_all_entries()
        if not rows:
            st.info("No entries yet — add your first entry.")
        else:
            last = rows[-7:]
            sleeps = [parse_float_safe(r[1]) for r in last if r[1] != ""]
            waters = [parse_float_safe(r[3]) for r in last if r[3] != ""]
            moods = [r[2] for r in last]
            st.write(f"- Entries (last 7): {len(last)}")
            if sleeps:
                st.write(f"- Avg sleep (last 7): {sum(sleeps)/len(sleeps):.1f} hrs")
            if waters:
                st.write(f"- Avg water (last 7): {sum(waters)/len(waters):.1f} L")
            mood_counts = Counter(moods)
            col1, col2, col3 = st.columns(3)
            col1.metric("😊 Happy", mood_counts.get("Happy", 0))
            col2.metric("😐 Neutral", mood_counts.get("Neutral", 0))
            col3.metric("😞 Low", mood_counts.get("Low", 0))

    # -------- Page: ADD ENTRY ----------
    elif st.session_state.page == "add_entry":
        st.header("➕ Add Daily Entry")
        today_iso = date.today().isoformat()
        with st.form("daily_form"):
            st.write(f"Date: *{today_iso}*")
            period_val = st.radio("Did you get your period today?", ["yes","no"], index=1)
            sleep = st.number_input("How many hours did you sleep? 😴", min_value=0.0, step=0.5)
            mood = st.selectbox("Mood today", ["😊 Happy", "😐 Neutral", "😞 Low"])
            water = st.number_input("How many litres of water did you drink? 💧", min_value=0.0, step=0.1)
            notes = st.text_area("Notes (optional)")
            submit = st.form_submit_button("Submit Entry")
        if submit:
            rows = read_all_entries()
            rows = [r for r in rows if r[0] != today_iso]
            rows.append([today_iso, sleep, mood.split()[1], water, period_val, notes])
            write_all_entries(rows)
            st.success("Entry saved.")
            st.session_state.page = "dashboard"

    # -------- Page: VIEW ALL ----------
    elif st.session_state.page == "view_all":
        st.header("📖 All Entries")
        rows = read_all_entries()
        if not rows:
            st.info("No entries yet.")
        else:
            st.table([['date','sleep','mood','water_intake','period','notes']] + rows)

    # -------- Page: WEEKLY SUMMARY ----------
    elif st.session_state.page == "weekly_summary":
        st.header("📊 Weekly Summary (last 7 entries)")
        rows = read_all_entries()
        if not rows:
            st.info("No data.")
        else:
            last7 = rows[-7:]
            valid = [(parse_float_safe(r[1]), parse_float_safe(r[3]), r[2], r[4]) for r in last7]
            if not valid:
                st.info("No numeric data.")
            else:
                sleep_avg = sum(v[0] for v in valid)/len(valid)
                water_avg = sum(v[1] for v in valid)/len(valid)
                mood_counts = Counter(v[2] for v in valid)
                st.write(f"*Average sleep:* {sleep_avg:.1f} hrs")
                st.write(f"*Average water:* {water_avg:.1f} L")
                st.write("*Mood counts:*")
                st.table([["😊 Happy", mood_counts.get("Happy",0)],
                          ["😐 Neutral", mood_counts.get("Neutral",0)],
                          ["😞 Low", mood_counts.get("Low",0)]])

    # -------- Page: EDIT/DELETE ----------
    elif st.session_state.page == "edit_delete":
        st.header("✏ Edit/Delete Entry")
        rows = read_all_entries()
        if not rows:
            st.info("No entries.")
        else:
            dates = [r[0] for r in rows]
            sel = st.selectbox("Select date", dates)
            row = next((r for r in rows if r[0]==sel), None)
            if row:
                new_sleep = st.number_input("Sleep (hrs)", value=parse_float_safe(row[1]), step=0.5)
                new_mood = st.selectbox("Mood", ["Happy","Neutral","Low"], index=["Happy","Neutral","Low"].index(row[2]) if row[2] in ["Happy","Neutral","Low"] else 1)
                new_water = st.number_input("Water (L)", value=parse_float_safe(row[3]), step=0.1)
                new_period = st.radio("Period?", ["yes","no"], index=["yes","no"].index(row[4].strip().lower()) if row[4] else 1)
                new_notes = st.text_area("Notes", value=row[5] if len(row)>=6 else "")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Save changes"):
                        for i in range(len(rows)):
                            if rows[i][0] == sel:
                                rows[i] = [sel, new_sleep, new_mood, new_water, new_period, new_notes]
                                break
                        write_all_entries(rows)
                        st.success("Updated.")
                with c2:
                    if st.button("Delete entry"):
                        rows = [r for r in rows if r[0] != sel]
                        write_all_entries(rows)
                        st.warning("Deleted.")

    # -------- Page: PERIOD CALENDAR ----------
   # -------- Page: PERIOD CALENDAR ----------
    elif st.session_state.page == "period_calendar":
        st.header("📅 Period Calendar")

        rows = read_all_entries()
        period_days = {r[0] for r in rows if len(r) >= 5 and r[4].strip().lower() == "yes"}
        streaks = group_period_streaks(period_days)

        today = date.today()
        years = list(range(2020, today.year + 3))
        c1, c2 = st.columns([2, 1])
        with c1:
            sel_month = st.selectbox("Month", list(calendar.month_name)[1:], index=today.month - 1)
        with c2:
            sel_year = st.selectbox("Year", years, index=years.index(today.year))

        month = list(calendar.month_name).index(sel_month)
        year = sel_year

        # Make sure Monday is the first day (matches week_days order)
        calendar.setfirstweekday(calendar.MONDAY)
        cal = calendar.monthcalendar(year, month)

        # weekday header using columns for alignment
        header_cols = st.columns(7)
        week_days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        for i, wd in enumerate(week_days):
            header_cols[i].markdown(
                f"<div style='text-align:center;font-weight:700'>{wd}</div>",
                unsafe_allow_html=True
            )

        # render grid with placeholders for empty days
        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                if day == 0:
                    # Blank but same height as buttons
                    cols[i].markdown(
                        "<div style='height:38px;'></div>",
                        unsafe_allow_html=True
                    )
                else:
                    day_str = f"{year}-{month:02d}-{day:02d}"
                    is_today = day_str == today.isoformat()
                    is_period = day_str in period_days
                    in_streak = any(datetime.fromisoformat(day_str).date() in s for s in streaks)

                    label = f"{day}"
                    if is_today:
                        label += " 🔸"
                    if is_period:
                        label += "🩸 "
                    elif in_streak:
                        label += "◻️ "

                    if cols[i].button(label, key=f"pcal_{day_str}"):
                        # toggle
                        if day_str in period_days:
                            for r in rows:
                                if r[0] == day_str:
                                    r[4] = "no"
                                    break
                            period_days.discard(day_str)
                        else:
                            found = False
                            for r in rows:
                                if r[0] == day_str:
                                    r[4] = "yes"
                                    found = True
                                    break
                            if not found:
                                rows.append([day_str, "", "", "", "yes", ""])
                            period_days.add(day_str)
                        write_all_entries(rows)
                        st.rerun()

    # -------- Page: STREAK CHART ----------
    elif st.session_state.page == "streak_chart":
        st.header("🏆 Streak Chart")
        rows = read_all_entries()
        if not rows:
            st.info("No data.")
        else:
            sleep_goal = float(config.get("sleep_goal", 7))
            water_goal = float(config.get("water_goal", 2))
            seq_sleep = [parse_float_safe(r[1]) >= sleep_goal for r in rows]
            seq_water = [parse_float_safe(r[3]) >= water_goal for r in rows]

            def calc(seq):
                curr = 0; temp = 0; longest = 0
                for v in seq:
                    if v:
                        temp += 1; longest = max(longest, temp)
                    else:
                        temp = 0
                curr = temp
                return curr, longest

            sc, sl = calc(seq_sleep)
            wc, wl = calc(seq_water)
            st.write(f"Sleep streak: *{sc}* (longest {sl}) — goal ≥ {sleep_goal:.1f} hrs")
            st.write(f"Water streak: *{wc}* (longest {wl}) — goal ≥ {water_goal:.1f} L")



    # -------- Page: GOALS ----------
    elif st.session_state.page == "goals":
        st.header("⚙ Goals")
        sg = st.number_input("Sleep goal (hrs)", value=float(config.get("sleep_goal",7)), step=0.5)
        wg = st.number_input("Water goal (L)", value=float(config.get("water_goal",2)), step=0.1)
        if st.button("Save goals"):
            config["sleep_goal"] = sg
            config["water_goal"] = wg
            save_config(config)
            st.success("Goals saved.")

    # -------- Export Weekly Summary ----------
    elif st.session_state.page == "export":
        st.header("📁 Export Weekly Summary")
        rows = read_all_entries()
        if not rows:
            st.info("No data.")
        else:
            total_sleep = total_water = 0.0
            mood_counts = Counter()
            count = 0
            for r in rows:
                try:
                    total_sleep += parse_float_safe(r[1])
                    total_water += parse_float_safe(r[3])
                    mood_counts[r[2]] += 1
                    count += 1
                except:
                    continue
            if count == 0:
                st.info("No numeric data.")
            else:
                import io
                buf = io.StringIO()
                writer = csv.writer(buf)
                writer.writerow(['avg_sleep','avg_water','happy','neutral','low'])
                writer.writerow([total_sleep/count, total_water/count, mood_counts.get('Happy',0), mood_counts.get('Neutral',0), mood_counts.get('Low',0)])
                st.download_button("Download weekly_summary.csv", buf.getvalue(), file_name='weekly_summary.csv', mime='text/csv')

    # -------- Reset ----------
    elif st.session_state.page == "reset":
        st.header("🗑 Reset Tracker")
        if st.button("Reset all data (this will delete entries)"):
            write_all_entries([])
            st.success("Tracker reset.")

    # -------- Help ----------
    elif st.session_state.page == "help":
        st.header("❓ Help & About")
        st.markdown("""
        *Lifestyle Tracker* — quick guide

        - Use *Add Entry* on the dashboard to log your day.
        - Click *Period Calendar* to mark/unmark period days instantly.
        - *View All Entries* lists your CSV.
        - *Edit/Delete Entry* lets you update any row.
        - *Goals* sets sleep/water targets used in streaks.
        - *Export* downloads a CSV summary.
        - *Reset Tracker* clears all data (header preserved).
        """)

# -----------------------
# Sidebar: less important actions (persistent)
# -----------------------
with st.sidebar:
    st.title("Menu")
    if st.button("Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
    if st.button("Add Entry"):
        st.session_state.page = "add_entry"
        st.rerun()
    if st.button("All Entries"):
        st.session_state.page = "view_all"
        st.rerun()
    if st.button("Weekly Summary"):
        st.session_state.page = "weekly_summary"
        st.rerun()
    if st.button("Edit/Delete Entry"):
        st.session_state.page = "edit_delete"
        st.rerun()
    if st.button("Period Calendar"):
        st.session_state.page = "period_calendar"
        st.rerun()
    st.markdown("---")
    if st.button("Streak Chart"):
        st.session_state.page = "streak_chart"
        st.rerun()
    if st.button("Goals"):
        st.session_state.page = "goals"
        st.rerun()
    if st.button("Export Summary"):
        st.session_state.page = "export"
        st.rerun()
    if st.button("Reset Tracker"):
        st.session_state.page = "reset"
        st.rerun()
    st.markdown("---")
    if st.button("Help"):
        st.session_state.page = "help"
        st.rerun()
    st.markdown(" ")
    st.markdown("Made with ❤ ")