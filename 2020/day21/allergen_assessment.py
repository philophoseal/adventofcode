import aoc


def parse(food_str: str) -> tuple[set[str], set[str]]:
    ingredients, allergens = food_str[:-1].split('(')
    ingredients = ingredients.strip().split(' ')
    allergens = [x.strip() for x in allergens.replace('contains', '').split(',')]
    return set(ingredients), set(allergens)

def build_allergen_dict(foods: tuple) -> dict[str, set[str]]:
    allergen_dict = {}
    for ingredients, _allergens in foods:
        for allergen in _allergens:
            allergen_dict[allergen] = allergen_dict.get(allergen, ingredients) & ingredients
    return allergen_dict


def main():
    aoc.setup(__file__)
    foods = [parse(line) for line in aoc.read_lines()]
    allergen_dict = build_allergen_dict(foods)

    all_ingredients = set.union(*[f[0] for f in foods])
    possible_allergens = set.union(*[v for v in allergen_dict.values()])
    non_allergens = all_ingredients - possible_allergens
    aoc.answer(1, sum([len(food[0] & non_allergens) for food in foods]))

    solved = {}
    while allergen_dict:
        solved_allergens = [k for k,v in allergen_dict.items() if len(v) == 1]
        for allergen in solved_allergens:
            ingredient = allergen_dict.pop(allergen)
            solved[allergen] = list(ingredient)[0]
            allergen_dict = {k: v - ingredient for k, v in allergen_dict.items()}
    dangerous = [solved[x] for x in sorted(solved.keys())]
    aoc.answer(2, ",".join(dangerous))

if __name__ == '__main__':
    main()
