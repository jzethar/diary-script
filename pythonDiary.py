import os
import datetime
from datetime import date, timedelta

def is_this_year(today, next_day):
    """
    Check the year for the next day 
    """
    if next_day.year > today.year:
        return False
    return True


def is_today_weekend():
    """
    Checks if today is a weekend (Saturday or Sunday).
    """
    today = datetime.date.today()
    return today.weekday() in (5, 6)


def get_current_week_number(today):
    """
    Returns the current week number based on your definition (starting Monday).
    """
    if is_today_weekend():
        # Adjust for weekend by going back to previous Monday
        today = datetime.date.today() - timedelta(days=today.weekday())
    else:
        today = datetime.date.today()
    return today.isocalendar()[1]


def create_folder(folder_path, week_number):
    """
    Creates a folder with the given name in the specified path.
    """
    folder_name = f"Week {week_number}"
    full_path = os.path.join(folder_path, folder_name)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    return full_path


def create_md_file(file_path, template_path, replacements):
    """
    Creates an MD file from a template, filling in placeholders with values.
    """
    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    for key, value in replacements.items():
        template_content = template_content.replace(f"{{{key}}}", value)

    with open(file_path, "w") as output_file:
        output_file.write(template_content)


def full_week_with_days(monday: date):
    """
    Making list of days in mentioned week
    """
    days_in_week = list()
    for i in range(0, 7, 1):
        days_in_week.append(monday + timedelta(days=monday.weekday() + i))
    return days_in_week

def evaluate_prev_day(today : date, working_days_per_week : int):
    """
    Evaluating previous day by using today date and working days per week
    """
    today_number = today.weekday()
    if today_number == 0:
        # Going to a previous week
        return today - timedelta(days=(7 - working_days_per_week + 1))
    else:
        return today - timedelta(days=1)
    

def evaluate_next_day(today: date, working_days_per_week: int):
    """
    Evaluating next day by using today date and working days per week
    """
    today_number = today.weekday()
    if today_number == (working_days_per_week - 1):
        # Going to a next week
        return today + timedelta(days=(7 - working_days_per_week + 1))
    else:
        return today + timedelta(1)


def main(week_template_path, daily_template_path, output_folder_path, vault_path, start_from_beginning, working_days_per_week):
    """
    Main function that creates folders and files.
    """
    folder_prefix = output_folder_path[len(vault_path):] if vault_path in output_folder_path else output_folder_path
    if folder_prefix[len(folder_prefix) - 1] != '/':
        folder_prefix + "/"

    # Prepare date formatting
    new_weak_day = today = date(datetime.date.today().year, 1, 1) if start_from_beginning else datetime.date.today()
    while is_this_year(today=today, next_day=new_weak_day):
        today = new_weak_day
        actual_week = today.isocalendar()[1]
        
        # Get Monday for this week
        this_monday = today - timedelta(days=today.weekday())
        week_bucket = full_week_with_days(this_monday)
        new_weak_day = week_bucket[len(week_bucket) - 1] + timedelta(days=1)
        week_bucket = week_bucket[0:working_days_per_week]

        # Create folder for a week 
        week_number = today.isocalendar()[1] if actual_week <= today.isocalendar()[1] else exit(0)
        folder_path = create_folder(output_folder_path, week_number)
        folder_prefix_week = folder_prefix + f"Week {week_number}" + "/"
        folder_prefix_week_prev = folder_prefix + f"Week {week_number - 1}" + "/"
        folder_prefix_week_next = folder_prefix + f"Week {week_number + 1}" + "/"

        # Create week file
        week_file_path = os.path.join(folder_path, f"Week {week_number}.md")
        week_replacements = {
            "Week": f"Week {week_number}",
            "day1": folder_prefix_week + week_bucket[0].strftime("%d.%m.%Y"),
            "day2": folder_prefix_week + week_bucket[1].strftime("%d.%m.%Y"),
            "day3": folder_prefix_week + week_bucket[2].strftime("%d.%m.%Y"),
            "day4": folder_prefix_week + week_bucket[3].strftime("%d.%m.%Y"),
            "day5": folder_prefix_week + week_bucket[4].strftime("%d.%m.%Y"),
            "day6": folder_prefix_week + week_bucket[4].strftime("%d.%m.%Y"),
            "day7": folder_prefix_week + week_bucket[4].strftime("%d.%m.%Y"),
            "week_prev": folder_prefix_week_prev + f"Week {week_number - 1}",
            "week_next": folder_prefix_week_next + f"Week {week_number + 1}",
        }
        create_md_file(week_file_path, week_template_path, week_replacements)

        for day in week_bucket:
            # Create daily file
            day_formatted = day.strftime("%d.%m.%Y")
            daily_file_path = os.path.join(folder_path, f"{day_formatted}.md")
            prev_day = evaluate_prev_day(day, working_days_per_week)
            next_day = evaluate_next_day(day, working_days_per_week)
            folder_prefix_week_for_next_day = folder_prefix_week if next_day.isocalendar()[1] == actual_week else folder_prefix_week_next
            folder_prefix_week_for_prev_day = folder_prefix_week if prev_day.isocalendar()[1] == actual_week else folder_prefix_week_prev
            daily_replacements = {
                "Day": day_formatted,
                "Week": folder_prefix_week + f"Week {week_number}",
                "prev_day": folder_prefix_week_for_prev_day + prev_day.strftime("%d.%m.%Y"),
                "next_day": folder_prefix_week_for_next_day + next_day.strftime("%d.%m.%Y"),
            }
            create_md_file(daily_file_path, daily_template_path, daily_replacements)


if __name__ == "__main__":
    week_template_path = "weekTemplate.txt"     # Replace with your actual file
    daily_template_path = "dailyTemplate.txt"   # Replace with your actual file
    output_folder_path = "/output/folder/path"  # Replace with your actual path
    vault_path = "/vault/path"                  # Replace with your actual path
    main(week_template_path, daily_template_path, output_folder_path, vault_path,
         start_from_beginning=False, working_days_per_week=5)
