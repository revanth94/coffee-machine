from typing import List, Dict
from collections import defaultdict
from threading import Thread
import time
from . import prompts


class Machine:
    def __init__(self, outlets: dict, total_items_quantity: Dict[str, int], beverages: Dict[str, Dict[str, int]]):
        self.outlets = outlets.get("count_n")
        self.available_ingredients = defaultdict(int)
        self.available_ingredients.update(total_items_quantity)
        self.beverages = beverages
        self.serving_time = 5  # seconds
        self.taps = [True] * self.outlets
        self.free_tap = 0

    def list_beverages(self) -> List[str]:
        return [beverage_name for beverage_name in self.beverages]

    def add_ingredients(self, ingredients: Dict[str, int]) -> None:
        for ingredient, quantity in ingredients.items():
            self.available_ingredients[ingredient] += quantity

    def check_and_deduct_ingredients(self, beverage_ingredients: Dict[str, int]) -> dict:
        for ingredient, required_quantity in beverage_ingredients.items():
            if ingredient not in self.available_ingredients:
                return dict(served_drink=False, ingredient=ingredient, problem="not available")
            if self.available_ingredients.get(ingredient, 0) < required_quantity:
                return dict(served_drink=False, ingredient=ingredient, problem="not sufficient")
        for ingredient, required_quantity in beverage_ingredients.items():
            self.available_ingredients[ingredient] -= required_quantity
        return dict(served_drink=True)

    @staticmethod
    def get_message(beverage_name: str, response: dict) -> str:
        if response['served_drink']:
            return prompts.BEVERAGE_BEING_PREPARED.format(beverage=beverage_name)
        return prompts.BEVERAGE_INGREDIENT_ISSUE.format(beverage=beverage_name, ingredient=response['ingredient'],
                                                        problem=response['problem'])

    def run_tap(self):
        self.taps[self.free_tap] = False
        x = self.free_tap
        self.free_tap += 1
        print(prompts.SERVING_DRINK_ON_TAP.format(tap=self.free_tap))
        self.free_tap %= self.outlets
        time.sleep(self.serving_time)
        self.taps[x] = True

    def serve_drink(self, beverage: str):
        if beverage not in self.beverages:
            return prompts.BEVERAGE_NOT_AVAILABLE.format(beverage=beverage)
        if self.taps[self.free_tap] is False:
            return prompts.NO_FREE_TAP
        drink_status = self.check_and_deduct_ingredients(self.beverages[beverage])
        if drink_status.get("served_drink"):
            Thread(target=self.run_tap).start()
        return self.get_message(beverage, drink_status)
