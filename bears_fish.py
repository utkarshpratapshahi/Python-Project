import random
import time
from typing import Optional


class Animal:
    symbol = "?"

    def __init__(self):
        self.acted = False


class Bear(Animal):
    symbol = "B"


class Fish(Animal):
    symbol = "F"


class River:
    def __init__(self, size=40, n_bears=10, n_fishes=15, seed=None):
        if n_bears + n_fishes > size:
            raise ValueError("Too many animals in river")

        if seed is not None:
            random.seed(seed)

        self.size = size
        self.cells: list[Optional[Animal]] = [None] * size

        spots = random.sample(range(size), n_bears + n_fishes)
        for i in spots[:n_bears]:
            self.cells[i] = Bear()
        for i in spots[n_bears:]:
            self.cells[i] = Fish()

    def empty_indices(self):
        return [i for i, c in enumerate(self.cells) if c is None]

    def spawn(self, animal_type):
        #Place a new animal of the given type in a random empty cell.
        empties = self.empty_indices()
        if not empties:
            return False
        baby = animal_type()
        baby.acted = True  # newborns don't act in the step they are born
        self.cells[random.choice(empties)] = baby
        return True

    def counts(self):
        bears = sum(isinstance(c, Bear) for c in self.cells)
        fishes = sum(isinstance(c, Fish) for c in self.cells)
        return bears, fishes

    def step(self):
        # reset every animal's "acted" flag at the start of the step
        for animal in self.cells:
            if animal is not None:
                animal.acted = False

        # process cells in random order
        order = list(range(self.size))
        random.shuffle(order)

        for i in order:
            animal = self.cells[i]
            if animal is None or animal.acted:
                continue
            animal.acted = True

            target = i + random.choice((-1, 0, 1))
            if target == i or not (0 <= target < self.size):
                continue  # stays where it is

            other = self.cells[target]

            if other is None:
                # move into empty cell
                self.cells[target] = animal
                self.cells[i] = None

            elif type(other) is type(animal):
                # same species: both stay put, a baby is born
                self.spawn(type(animal))

            elif isinstance(animal, Bear):
                # bear moves onto fish: fish is eaten
                self.cells[target] = animal
                self.cells[i] = None

            else:
                # fish moves onto bear: fish is eaten
                self.cells[i] = None

    def __str__(self):
        return "".join(c.symbol if c is not None else "." for c in self.cells)


def run(steps=50, size=40, n_bears=5, n_fishes=10, delay=0.0, seed=None):
    river = River(size, n_bears, n_fishes, seed)
    b, f = river.counts()
    print(f"Step {0:3d} | {river} | Bears: {b:2d} Fish: {f:2d}")

    for t in range(1, steps + 1):
        river.step()
        b, f = river.counts()
        print(f"Step {t:3d} | {river} | Bears: {b:2d} Fish: {f:2d}")
        if delay:
            time.sleep(delay)
        if b == 0 and f == 0:
            print("Everything has died out.")
            break


if __name__ == "__main__":
    run(steps=20, size=120, n_bears=20, n_fishes=40, delay=0.1)