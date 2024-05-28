import os
import sys
from prettytable import PrettyTable

def input_tasks():
    tasks = dict()
    print("Masukkan data tugas (misal: A,3 atau B,3,A). Ketik 'selesai' jika sudah selesai atau 'exit' untuk keluar.")
    while True:
        line = input()
        if line.lower() == 'selesai':
            break
        if line.lower() == 'exit':
            return 'exit'
        singleElement = line.split(',')
        task_id = singleElement[0]
        durasi = singleElement[1]
        dependencies = singleElement[2].strip().split(';') if len(singleElement) > 2 else ['-1']

        tasks[task_id] = {
            'id': task_id,
            'durasi': int(durasi),
            'dependencies': dependencies,
            'ES': 0,
            'EF': 0,
            'LS': 0,
            'LF': 0,
            'slack': 0,
            'isCritical': False
        }
    return tasks

def forward_pass(tasks):
    for task_id, task in tasks.items():
        if '-1' in task['dependencies']:
            task['ES'] = 1
            task['EF'] = task['ES'] + task['durasi'] - 1
        else:
            for dep in task['dependencies']:
                if dep in tasks:
                    dep_task = tasks[dep]
                    task['ES'] = max(task['ES'], dep_task['EF'] + 1)
                    task['EF'] = task['ES'] + task['durasi'] - 1

def backward_pass(tasks):
    all_tasks = list(tasks.keys())
    all_tasks.reverse()

    for task_id in all_tasks:
        task = tasks[task_id]
        if all_tasks.index(task_id) == 0:
            task['LF'] = task['EF']
            task['LS'] = task['ES']

        for dep in task['dependencies']:
            if dep != '-1':
                dep_task = tasks[dep]
                if dep_task['LF'] == 0:
                    dep_task['LF'] = task['LS'] - 1
                    dep_task['LS'] = dep_task['LF'] - dep_task['durasi'] + 1
                    dep_task['slack'] = dep_task['LF'] - dep_task['EF']
                if dep_task['LF'] > task['LS'] - 1:
                    dep_task['LF'] = task['LS'] - 1
                    dep_task['LS'] = dep_task['LF'] - dep_task['durasi'] + 1
                    dep_task['slack'] = dep_task['LF'] - dep_task['EF']

def print_tasks(tasks):
    table = PrettyTable()
    table.field_names = ["ID Kegitan", "Durasi", "ES", "EF", "LS", "LF", "Slack", "Is Critical"]

    for task_id, task in tasks.items():
        task['isCritical'] = task['slack'] == 0
        table.add_row([task['id'], task['durasi'], task['ES'], task['EF'], task['LS'], task['LF'], task['slack'], task['isCritical']])
    
    print(table)

def main():
    while True:
        tasks = input_tasks()
        if tasks == 'exit':
            break
        forward_pass(tasks)
        backward_pass(tasks)
        print_tasks(tasks)
        user_input = input("Tekan Enter untuk memulai lagi atau ketik 'exit' untuk berhenti: ")
        if user_input.lower() == 'exit':
            break

if __name__ == "__main__":
    main()
