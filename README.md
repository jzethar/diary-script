# Diary

## Purpose
Having a diary is useful, but it's even more beneficial to use Obsidian! You won't forget anything – you can write down your thoughts, work tasks, or even personal stuff in this powerful note-taking app. However, creating files every day could get boring. That's where the genius idea of an automation script comes in!

## How to use it
This repo provides some templates that illustrate which fields the script can use. Mostly they are:
- day1
- day2
- day3
- day4
- day5
- day6
- day7
- week_prev
- week_next
- prev_day
- next_day
- Week
- Day

Before using it be sure that you changed your paths and correctly fulfilled `main` function:
- `week_template_path` – template for a week file
- `daily_template_path` – template for a day file
- `output_folder_path` – replace with your actual path to Obsidian vault's folder for a diary
- `vault_path` – replace with your actual path to Obsidian vault
- `start_from_beginning` – it means that you diary will start exactly from the first week (`True`) or current week (`False`)
- `working_days_per_week` – how much do you work per week, based on this links between days will be created