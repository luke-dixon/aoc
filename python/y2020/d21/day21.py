from collections import defaultdict

from lib import puzzle


class Food:
    def __init__(self, ingredients, allergens):
        self.ingredients = ingredients
        self.allergens = allergens

    def __repr__(self):
        return f'Food({self.ingredients}, {self.allergens})'


class Day21(puzzle.Puzzle):
    year = '2020'
    day = '21'

    def get_data(self):
        orig_data = self.input_data.splitlines()

        data = '''\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)'''.splitlines()
        data = orig_data

        foods = []
        for line in data:
            line.split(' ')
            ingredients = []
            allergens = []

            allergens_seen = False
            for word in line.split(' '):
                if word.startswith('('):
                    allergens_seen = True
                if allergens_seen:
                    word = word.lstrip('(').rstrip(')').rstrip(',')
                    if word != 'contains':
                        allergens.append(word)
                else:
                    ingredients.append(word)
            foods.append(Food(set(ingredients), set(allergens)))
        return foods

    def part1(self):
        foods = self.get_data()

        ingredients = set()
        for food in foods:
            for ingredient in food.ingredients:
                ingredients.add(ingredient)

        foods_by_allergen = defaultdict(set)
        for food in foods:
            for allergen in food.allergens:
                foods_by_allergen[allergen].add(food)
        foods_by_allergen = dict(foods_by_allergen)

        ingredients_by_allergen = {}
        for allergen in foods_by_allergen:
            for food in foods_by_allergen[allergen]:
                if allergen not in ingredients_by_allergen:
                    ingredients_by_allergen[allergen] = set(food.ingredients)
                else:
                    ingredients_by_allergen[allergen] &= set(food.ingredients)

        possible_allergens = set()
        for allergens in ingredients_by_allergen.values():
            possible_allergens |= allergens

        non_allergens = ingredients - possible_allergens
        total = 0
        for food in foods:
            for ingredient in food.ingredients:
                if ingredient in non_allergens:
                    total += 1

        return total

    def part2(self):
        foods = self.get_data()

        allergens = set()
        for food in foods:
            for allergen in food.allergens:
                allergens.add(allergen)

        ingredients = set()
        for food in foods:
            for ingredient in food.ingredients:
                ingredients.add(ingredient)

        foods_by_allergen = defaultdict(set)
        for food in foods:
            for allergen in food.allergens:
                foods_by_allergen[allergen].add(food)
        foods_by_allergen = dict(foods_by_allergen)

        ingredients_by_allergen = {}
        for allergen in foods_by_allergen:
            for food in foods_by_allergen[allergen]:
                if allergen not in ingredients_by_allergen:
                    ingredients_by_allergen[allergen] = set(food.ingredients)
                else:
                    ingredients_by_allergen[allergen] &= set(food.ingredients)
        possible_allergens = set()
        for allergens in ingredients_by_allergen.values():
            possible_allergens |= allergens

        non_allergens = ingredients - possible_allergens
        total = 0
        for food in foods:
            for ingredient in food.ingredients:
                if ingredient in non_allergens:
                    total += 1

        while len(
            [x for x in ingredients_by_allergen if len(ingredients_by_allergen[x]) == 1]
        ) != len(ingredients_by_allergen):
            for allergen in [
                x
                for x in ingredients_by_allergen
                if len(ingredients_by_allergen[x]) == 1
            ]:
                (ingredient,) = ingredients_by_allergen[allergen]
                for other_allergen in ingredients_by_allergen:
                    if allergen == other_allergen:
                        continue
                    if ingredient in ingredients_by_allergen[other_allergen]:
                        ingredients_by_allergen[other_allergen].remove(ingredient)

        ingredients_by_allergen_flattened = {}
        for allergen in ingredients_by_allergen:
            (ingredient,) = ingredients_by_allergen[allergen]
            ingredients_by_allergen_flattened[allergen] = ingredient

        return ','.join(
            [
                ingredients_by_allergen_flattened[allergen]
                for allergen in sorted(ingredients_by_allergen_flattened)
            ]
        )

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
