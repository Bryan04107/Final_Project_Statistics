import csv
import os
import json

# Specify the directory containing your files
directory = 'E2'

# Specify the output CSV file
output_csv = 'output2.csv' 
# Initialize a list to store data from all files
all_data = []
message_id = 1

# Iterate through files in the directory
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)

    # Check if the current item is a file and ends with '.txt'
    if os.path.isfile(file_path) and filename.endswith('.txt'):
        # Open and read each file with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.loads(file.read())

            # Process the data and extract required values
            player_data = {}  # Dictionary to store player-related data

            for player in data['players']:
                # Access the "scores" section within each "player"
                scores = player.get('scores', {})

                # Extract kills, deaths, assists, and outcome from "scores"
                kills = int(scores.get('kills', 0))
                deaths = int(scores.get('deaths', 0))
                assists = int(scores.get('assists', 0))
                outcome = player.get('outcome', 0)

                # Store player-related data in the dictionary using player ID as the key
                player_data[player['champion_name']] = {'kills': kills, 'deaths': deaths, 'assists': assists, 'outcome': outcome}

            for chat_entry in data['chat_log']:
                match_id = filename
                champion_name = chat_entry['champion_name']
                time = chat_entry['time']
                sent_to = chat_entry['sent_to']
                message = chat_entry['message']
                association_to_offender = chat_entry['association_to_offender']

                # Retrieve player-related data using champion_name as the key
                player_info = player_data.get(champion_name, {})
                kills = player_info.get('kills', 0)
                deaths = player_info.get('deaths', 0)
                assists = player_info.get('assists', 0)
                outcome = player_info.get('outcome', '')

                label = 0
                kda = round((kills + assists) / (deaths if deaths != 0 else 1), 2)

                # Append the data to the list
                all_data.append([message_id, match_id, champion_name, time, sent_to, message, association_to_offender, kills, deaths, assists, outcome, label, kda])
                message_id += 1

# Write all data to a CSV file with UTF-8 encoding
with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header
    csv_writer.writerow(['message_id', 'match_id', 'champion_name', 'time', 'sent_to', 'message', 'association_to_offender', 'kills', 'deaths', 'assists', 'outcome', 'label', 'kda'])

    # Write data to the CSV file
    csv_writer.writerows(all_data)
