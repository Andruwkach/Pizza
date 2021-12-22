from random import randint

import click


def log(pattern):
    def sub_log(function):
        def sub_sub_log(self):
            function(self)
            cooking_time = randint(1, 100)
            print(pattern.format(cooking_time))

        return sub_sub_log

    return sub_log


class PizzaInfo:
    """Класс, в котором содержится техническая информация о пиццах"""

    recipes = {
        "margherita": ["tomato sauce", "mozzarella", "tomatoes"],
        "pepperoni": ["tomato sauce", "mozzarella", "pepperoni"],
        "hawaiian": ["tomato sauce", "mozzarella", "chicken", "pineapples"],
    }
    emojies = {"margherita": "🧀", "pepperoni": "🍕", "hawaiian": "🍍"}
    facts = {
        "margherita": "Первые упоминания датируются 1796 - 1810 годами (Неаполь)",
        "pepperoni": "Это американская пицца, на итальянском - pizza alla diavola",
        "hawaiian": "Один из самый молодых видов пицц: придумана в Канаде в 1962",
    }
    possible_sizes = {"L", "XL"}

    @staticmethod
    def dict() -> None:
        print(recipes)


class Pizza:
    """класс для создания и оперирование объектом пицца"""

    def __init__(self, pizza_type: str, pizza_size: str = "L"):
        pizza_size = pizza_size.upper()
        pizza_type = pizza_type.lower()
        assert pizza_type in PizzaInfo.recipes, "такой пиццы в меню нет!"
        assert pizza_size in PizzaInfo.possible_sizes, "такого размера нет!"
        self.pizza_type = pizza_type
        self.ingredients = PizzaInfo.recipes.get(pizza_type)
        self.emoji = PizzaInfo.emojies.get(pizza_type)
        self.size = pizza_size
        self.status = "raw"

    def __str__(self) -> str:
        beauty_ingredients = ", ".join(self.ingredients)
        return f"- {self.pizza_type} {self.emoji}: {beauty_ingredients}"

    def __eq__(self, other) -> bool:
        if (self.pizza_type == other.pizza_type) and (self.size == other.size):
            return True
        return False

    def __ne__(self, other) -> bool:
        return not __eq__(self, other)

    def print_fact(self) -> None:
        print(
            PizzaInfo.facts.get(self.pizza_type, "ничего интересного, скучная пицца(")
        )

    @log("Доставили за {}с!")
    def delivery(self) -> None:
        """Доставляет пиццу"""
        assert self.status == "backed", "пицца ещё не готова, либо уже доставлена"
        self.status = "delivered"

    @log("Забрали за {}с!")
    def pickup(self) -> None:
        """Самовывоз"""
        assert self.status == "backed", "пицца ещё не готова, либо уже доставлена"
        self.status = "pickuped"

    @log("Приготовили за {}с! А чего добился ты?")
    def bake(self) -> None:
        """Готовит пиццу"""
        assert self.status == "raw", "пицца уже готова!"
        self.status = "backed"


@click.group()
def cli():
    pass


@cli.command()
@click.argument("pizza", nargs=1)
@click.option("--delivery", default=False, is_flag=True)
@click.option("--size", default="L")
def order(pizza: str, size: str, delivery: bool) -> None:
    """Готовит и доставляет пиццу"""
    current_pizza = Pizza(pizza, size)
    current_pizza.bake()
    if delivery:
        current_pizza.delivery()
    else:
        current_pizza.pickup()


@cli.command()
def menu() -> None:
    """Выводит меню"""
    print("Сегодня в меню нашего ресторана:")
    for piza_type in PizzaInfo.recipes:
        print(Pizza(piza_type))
    print("Для заказа выберети тип пиццы")


if __name__ == "__main__":
    cli()
