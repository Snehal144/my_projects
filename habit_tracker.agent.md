
---
name: Habit Tracker
description: "Track daily habits with a Streamlit app, store progress in DB, and visualize streaks."
tools: [read, edit, search, execute]
user-invocable: true
---

# Habit Tracker

This project is a Habit Tracker application built using Streamlit. It allows users to track their habits over a week, marking them as completed or not, and provides a user-friendly interface for managing their habits.

## Features

- Track multiple habits.
- Edit a Monday-to-Sunday calendar for all your habits.
- Save and load both completed and not-completed statuses for each day.
- Simple and intuitive user interface.

## Installation

To set up the project, follow these steps:

1. Clone the repository:

   ```
   git clone <repository-url>
   cd habit-tracker
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the application, execute the following command:

```
streamlit run app.py
```

This will start the Streamlit server and open the application in your default web browser.

## Usage

- Add habits using the **Add Habits** tab.
- Open **Track Habits** and check the days when each habit was completed. Leave
  a checkbox unchecked to record that it was not completed.
- Click **Save this week's progress** to save all seven days. The table shows
  the current Monday-to-Sunday week.
- View recent completion counts and habit totals in the **Progress** tab.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.