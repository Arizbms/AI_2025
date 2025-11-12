# ------------------------------
# Resolution in First Order Logic
# ------------------------------

from itertools import product

# Helper function: check if a literal is negated
def is_negative(literal):
    return literal.startswith("¬")

# Negate a literal
def negate(literal):
    return literal[1:] if is_negative(literal) else "¬" + literal

# Unification function (basic variable substitution)
def unify(x, y, substitution={}):
    if substitution is None:
        return None
    elif x == y:
        return substitution
    elif isinstance(x, str) and x.islower():  # variable
        return unify_var(x, y, substitution)
    elif isinstance(y, str) and y.islower():
        return unify_var(y, x, substitution)
    elif isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y):
        for a, b in zip(x, y):
            substitution = unify(a, b, substitution)
        return substitution
    else:
        return None

def unify_var(var, x, substitution):
    if var in substitution:
        return unify(substitution[var], x, substitution)
    elif x in substitution:
        return unify(var, substitution[x], substitution)
    else:
        substitution[var] = x
        return substitution

# Resolution algorithm
def resolution(kb, query):
    clauses = kb + [negate(query)]
    new = set()

    print("Initial clauses:")
    for c in clauses:
        print(" -", c)
    print("\nResolution steps:")

    while True:
        pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i + 1, len(clauses))]
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if "" in resolvents:
                print(f"\nContradiction found between {ci} and {cj}")
                print("✅ Therefore, the query is PROVED true.")
                return True
            new = new.union(resolvents)

        if new.issubset(set(clauses)):
            print("\nNo new clauses can be added.")
            print("❌ Query cannot be proved.")
            return False
        for c in new:
            if c not in clauses:
                clauses.append(c)

# Resolve two clauses
def resolve(ci, cj):
    resolvents = set()
    ci_literals = ci.split(" ∨ ")
    cj_literals = cj.split(" ∨ ")

    for di in ci_literals:
        for dj in cj_literals:
            if di == negate(dj):
                new_clause = list(set(ci_literals + cj_literals))
                new_clause.remove(di)
                new_clause.remove(dj)
                resolvent = " ∨ ".join(sorted(set(new_clause)))
                resolvents.add(resolvent)
    return resolvents



if __name__ == "__main__":
    KB = [
        "¬Food(x) ∨ Likes(John, x)",                # John likes all food
        "Food(Apple)",                              # Apple is food
        "Food(Vegetable)",                          # Vegetable is food
        "¬Eats(x, y) ∨ ¬¬Killed(x) ∨ Food(y)",      # Anything anyone eats and not killed is food
        "Eats(Anil, Peanuts)",                      # Anil eats peanuts
        "¬Killed(Anil)",                            # Anil is still alive
        "¬Eats(x, y) ∨ Eats(Harry, y)",             # Harry eats everything Anil eats
        "¬Alive(x) ∨ ¬Killed(x)",                   # Alive ⇒ not killed
        "¬¬Killed(x) ∨ Alive(x)"                    # not killed ⇒ alive
    ]

    QUERY = "Likes(John, Peanuts)"

    resolution(KB, QUERY)
