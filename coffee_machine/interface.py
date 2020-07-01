from coffee_machine import models, prompts
from coffee_machine.utils import shutdown_machine


class UserInterface:
    def __init__(self, machine: models.Machine):
        self.machine = machine
        self.machine_active = True
        self.beverage_list = machine.list_beverages()
        self.menu_size = len(self.beverage_list)
        beverage_menu = [prompts.BEVERAGE_DISPLAY_FORMAT.format(number=i + 1, beverage_name=beverage_name)
                         for i, beverage_name in enumerate(self.beverage_list)]
        self.beverage_prompt = prompts.HEADER_PROMPT + "".join(beverage_menu)

    @staticmethod
    def validate_input(inp, n=0):
        try:
            beverage_number = int(inp)
            if n and beverage_number > n:
                return False, prompts.INVALID_PROMPT
            return True, beverage_number
        except ValueError:
            return False, prompts.INVALID_PROMPT

    def start_machine(self):
        print("Machine is starting\n")
        self.main_menu()
        while self.machine_active:
            self.beverage_dispatch()

    def main_menu(self):
        inp = input(prompts.INITIAL_PROMPT)
        valid, inp = self.validate_input(inp)
        if not valid:
            print(inp)
        elif inp == 1:
            return
        elif inp == 2:
            self.view_remaining_ingredients()
        elif inp == 3:
            self.load_ingredients()
        elif inp == 4:
            shutdown_machine(self.machine)
            self.machine_active = False
            print(prompts.SHUTDOWN_MESSAGE)
            return
        self.main_menu()

    def beverage_dispatch(self):
        inp = input(self.beverage_prompt)
        try:
            beverage_number = int(inp)
        except ValueError:
            print(f"{inp} is not in the list of options")
            return
        if beverage_number > self.menu_size:
            print(prompts.SELECT_VALID_DRINK)
            return
        if beverage_number == 0:
            return self.main_menu()
        service = self.machine.serve_drink(self.beverage_list[beverage_number - 1])
        print(service)

    def view_remaining_ingredients(self):
        print(prompts.INGREDIENTS_HEADER)
        for ingredient, quantity in self.machine.available_ingredients.items():
            print(f"{ingredient}: {quantity}")
        print()

    def load_ingredients(self):
        ingredient_name = input(prompts.ENTER_INGREDIENT_NAME)
        quantity = input(prompts.ENTER_INGREDIENT_QUANTITY)
        valid_quantity, quantity = self.validate_input(quantity)
        if valid_quantity:
            self.machine.add_ingredients({ingredient_name: quantity})
            print(prompts.ADDED_INGREDIENT.format(ingredient_name=ingredient_name, quantity=quantity))
        else:
            print(quantity)