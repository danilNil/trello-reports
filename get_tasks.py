import json
import csv
import re
from datetime import datetime

def extract_tasks_from_trello(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    tasks = []
    for card in data['cards']:

        # Skip cards with the label 'infra'
        labels = [label['name'] for label in card['labels']]
        if 'infra' in labels:
            continue

        if 'Frontend' in labels:
            continue

        task = {'name': card['name'], 'description': card['desc'],
                'labels': [label['name'] for label in card['labels']],
                'due_date': card['due'] if 'due' in card else None, 'short_url': card['shortUrl'],
                'closed': card['closed'], 'complete_date':'', 'estimate':0}

        # Check if list ID matches and set 'done' field accordingly
        if check_if_done(card['idList']):
            task['done'] = True
        else:
            task['done'] = False

        # Extract estimate from card name using regular expression
        match = re.search(r'\[(\d+)\]', task['name'])
        if match:
            task['estimate'] = int(match.group(1))
        else:
            task['estimate'] = None

        # Find the first action where the task was moved to the desired list

        for action in data['actions']:
            if action['type'] == 'updateCard' and action['data']['card']['id'] == card['id']:
                if 'listAfter' in action['data']:
                    print(task['name'], action['data']['listAfter']['name'], datetime.strptime(action['date'], "%Y-%m-%dT%H:%M:%S.%fZ"))
                    print("/n")
                    if check_if_ready_for_demo(action['data']['listAfter']['id']):
                        move_date = datetime.strptime(action['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
                        task['complete_date'] = move_date.strftime("%Y-%m-%d %H:%M:%S")
                        print('--')
                        print(task['name'], task['complete_date'])
                        print("--")
                        # break

        if task['complete_date'] == '':
            for action in data['actions']:
                if action['type'] == 'updateCard' and action['data']['card']['id'] == card['id']:
                    if 'listAfter' in action['data']:
                        if check_if_done(action['data']['listAfter']['id']):
                            move_date = datetime.strptime(action['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
                            task['complete_date'] = move_date.strftime("%Y-%m-%d %H:%M:%S")
                            print('--')
                            print(task['name'], task['complete_date'])
                            print("--")
                            # break

        tasks.append(task)

    return tasks

def check_if_ready_for_demo(listId):
    listDoneId1 = '642c5aedd95db65295aa3200' #готово к демо
    # listDoneId2 = '642c5aedd95db65295aa3201' #Done

    return listId == listDoneId1

def check_if_done(listId):
    # listDoneId1 = '642c5aedd95db65295aa3200' #готово к демо
    listDoneId2 = '642c5aedd95db65295aa3201' #Done

    return listId == listDoneId2

def save_tasks_to_csv(tasks, csv_file):
    fieldnames = ['Task Name', 'URL', 'Archived', 'Complete Date', 'Estimate']

    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            writer.writerow({
                'Task Name': task['name'],
                'URL': task['short_url'],
                'Archived': task['closed'],
                'Complete Date': task['complete_date'],
                'Estimate': task['estimate'],
            })



json_file = 'board.json'
csv_file = 'tasks.csv'

tasks = extract_tasks_from_trello(json_file)
save_tasks_to_csv(tasks, csv_file)