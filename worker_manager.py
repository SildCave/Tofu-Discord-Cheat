from tinydb import TinyDB, where
import os

if not os.path.exists('workers.json'):
    open('workers.json', 'w').close()
    
db = TinyDB('workers.json', indent=4)
db = db.table('workers')
opt_list = []

def option_1():
    worker_personal_token = input('dc_personal_token: ')
    worker_friendly_name = input('worker_friendly_name: ')
    worker_id = input('worker_id: ')
    
    stats = {
        'summon': 0,
        'minigame': 0,
        'daily': 0,
        'grab': 0,
        'fusion_tokens_used': 0
    }

    db.insert({'worker_friendly_name': worker_friendly_name, 'worker_personal_token': worker_personal_token, 'worker_id': worker_id, 'worker_stats': stats})

    print('\n')

def option_2():
    friendly_name = input('friendly_name: ')
    db.remove(where('worker_friendly_name') == friendly_name)
    print('REMOVED')

def option_3():
    quit()

opt_list.append(option_1)
opt_list.append(option_2)
opt_list.append(option_3)

while True:
    print('option_1: append_worker')
    print('option_2: delete_worker')
    print('option_3: quit')
    print('\n')
    choice = input('select option: ')
    print("\033[A                             \033[A")
    opt_list[int(choice) - 1]()
