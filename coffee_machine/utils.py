import os
import json


def get_last_saved_state(folder: str = "coffee_machine"):
    initial_file_name = folder + "/factory_reset.json"
    last_saved_file_name = folder + "/last_saved.json"
    file_name = last_saved_file_name if os.path.exists(last_saved_file_name) else initial_file_name
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data.get("machine")


def shutdown_machine(machine):
    data = dict(
        machine=dict(
            outlets=dict(count_n=machine.outlets),
            total_items_quantity=machine.available_ingredients,
            beverages=machine.beverages
        )
    )
    last_save_file_name = "coffee_machine/last_saved.json"
    with open(last_save_file_name, 'w+') as f:
        json.dump(data, f)
