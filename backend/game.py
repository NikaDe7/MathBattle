import random

def generate_math_problem(level: int):
    level = int(level)

    # 1 клас
    if level == 1:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        if random.random() < 0.5:
            return f"{a} + {b}", a + b
        else:
            if a < b: a, b = b, a
            return f"{a} - {b}", a - b

    # 2 клас
    elif level == 2:
        a = random.randint(10, 50)
        b = random.randint(1, 30)
        c = random.randint(1, 20)

        pattern = random.choice([
            "a + b - c",
            "(a + b) - c",
            "a - b + c"
        ])

        if pattern == "a + b - c":
            return f"{a} + {b} - {c}", a + b - c
        elif pattern == "(a + b) - c":
            return f"({a} + {b}) - {c}", (a + b) - c
        else:
            return f"{a} - {b} + {c}", a - b + c

    # 3 клас
    elif level == 3:
        a = random.randint(2, 10)
        b = random.randint(2, 10)
        c = random.randint(1, 20)

        pattern = random.choice([
            "a * b",
            "a * b + c",
            "(a + b) * c"
        ])

        if pattern == "a * b":
            return f"{a} × {b}", a * b
        elif pattern == "a * b + c":
            return f"{a} × {b} + {c}", a * b + c
        else:
            return f"({a} + {b}) × {c}", (a + b) * c

    # 4 клас
    elif level == 4:
        a = random.randint(10, 100)
        b = random.randint(2, 10)

        pattern = random.choice([
            "mul",
            "div",
            "mixed"
        ])

        if pattern == "mul":
            return f"{a} × {b}", a * b
        elif pattern == "div":
            result = random.randint(2, 20)
            return f"{result * b} ÷ {b}", result
        else:
            c = random.randint(1, 50)
            return f"{a} × {b} + {c}", a * b + c

    # 5 клас
    elif level == 5:
        a = random.randint(10, 50)
        b = random.randint(2, 10)
        c = random.randint(1, 30)

        pattern = random.choice([
            "brackets",
            "multi_step",
            "division"
        ])

        if pattern == "brackets":
            return f"{a} × ({b} + {c})", a * (b + c)
        elif pattern == "multi_step":
            return f"{a} × {b} - {c}", a * b - c
        else:
            result = random.randint(2, 20)
            return f"{result * b} ÷ {b} + {c}", result + c

    # 6 клас
    elif level == 6:
        a = random.randint(2, 15)
        b = random.randint(2, 15)
        c = random.randint(1, 20)

        pattern = random.choice([
            "two_brackets",
            "square",
            "mixed"
        ])

        if pattern == "two_brackets":
            return f"({a} + {b}) × ({b} + {c})", (a + b) * (b + c)
        elif pattern == "square":
            return f"{a}²", a * a
        else:
            return f"{a} × {b} + {c}²", a * b + c * c

    # 7 клас
    elif level == 7:
        a = random.randint(5, 20)
        b = random.randint(1, 10)

        pattern = random.choice([
            "square_diff",
            "linear",
            "mixed"
        ])

        if pattern == "square_diff":
            return f"{a}² - {b}²", a*a - b*b
        elif pattern == "linear":
            x = random.randint(1, 20)
            return f"{x} + {a}", x + a
        else:
            return f"{a} × {b} + {b}²", a * b + b * b

    # 8 клас
    elif level == 8:
        a = random.randint(2, 10)
        b = random.randint(2, 10)

        pattern = random.choice([
            "identity",
            "expand",
            "mixed"
        ])

        if pattern == "identity":
            return f"({a} + {b})²", (a + b) ** 2
        elif pattern == "expand":
            return f"({a} - {b})²", (a - b) ** 2
        else:
            return f"{a}² + 2×{a}×{b} + {b}²", (a + b) ** 2

    # 9 клас
    else:
        a = random.randint(2, 10)
        b = random.randint(1, 10)
        c = random.randint(1, 10)

        pattern = random.choice([
            "quadratic_like",
            "difference",
            "complex"
        ])

        if pattern == "quadratic_like":
            return f"{a}² + {b}² + {c}²", a*a + b*b + c*c
        elif pattern == "difference":
            return f"({a} + {b}) × ({a} - {b})", (a + b) * (a - b)
        else:
            return f"{a} × {b} + {c}² - {b}", a*b + c*c - b