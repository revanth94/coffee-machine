import coffee_machine.interface
from coffee_machine import models, utils

machine_data = utils.get_last_saved_state()
c_machine = models.Machine(**machine_data)
ui = coffee_machine.interface.UserInterface(c_machine)
ui.start_machine()
