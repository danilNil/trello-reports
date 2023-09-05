import json
import csv

# Load the Trello board JSON data from a file
with open('board.json', 'r') as json_file:
    data = json.load(json_file)

# Open a CSV file for writing
with open('trello_board.csv', 'w', newline='') as csv_file:
    # Define the CSV writer
    csv_writer = csv.writer(csv_file)

    # Write the header row
    csv_writer.writerow(['ID', 'Subject', 'Assignee', 'Finish date', 'Start date', 'Description', ])

    # Loop through the Trello cards
    for card in data['cards']:
        card_id = card['id']
        subject = card['name']
        assignee = card.get('idMembers', [])
        finish_date = card.get('due', '')
        start_date = card.get('start', '')
        description = card.get('desc', '')

        status = ''
        for list_info in data['lists']:
            if list_info['id'] == card['idList']:
                status = list_info['name']
                break


        # Write the card data to the CSV file
        csv_writer.writerow([card_id, subject, assignee, finish_date, start_date, description])

print("Conversion completed. CSV file saved as 'trello_board.csv'.")
