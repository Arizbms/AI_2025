from copy import deepcopy

def standardize_variables(rule, var_count):
    """
    Standardize variables by renaming them with a unique suffix to avoid clashes.
    """
    new_rule = []
    for literal in rule:
        new_literal = []
        for token in literal:
            if token.islower() and token.isalpha():
                new_literal.append(token + str(var_count))
            else:
                new_literal.append(token)
        new_rule.append(tuple(new_literal))
    return new_rule

def unify(x, y, subst={}):
    """
    Unify two literals (tuples) x and y with current substitution subst.
    Returns updated substitution or None if cannot unify.
    """
    if subst is None:
        return None
    elif x == y:
        return subst
    elif isinstance(x, str) and x.islower():
        return unify_var(x, y, subst)
    elif isinstance(y, str) and y.islower():
        return unify_var(y, x, subst)
    elif isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y):
        for a, b in zip(x, y):
            subst = unify(a, b, subst)
        return subst
    else:
        return None

def unify_var(var, x, subst):
    if var in subst:
        return unify(subst[var], x, subst)
    elif x in subst:
        return unify(var, subst[x], subst)
    else:
        subst[var] = x
        return subst

def substitute(sentence, subst):
    """
    Apply substitution subst to a sentence (list of literals).
    """
    new_sentence = []
    for literal in sentence:
        new_literal = []
        for token in literal:
            if token in subst:
                new_literal.append(subst[token])
            else:
                new_literal.append(token)
        new_sentence.append(tuple(new_literal))
    return new_sentence

def fol_fc_ask(KB, alpha):
    """
    Forward chaining algorithm for First Order Logic.

    KB: list of rules in the form [ (premises), conclusion ]
    alpha: query, atomic sentence as a tuple
    """

    var_count = 0
    new = []
    while True:
        new = []
        for (premises, conclusion) in KB:
            # Standardize variables in rule
            var_count += 1
            standardized_premises = standardize_variables(premises, var_count)
            standardized_conclusion = standardize_variables([conclusion], var_count)[0]

            # Try to unify each premise with some sentence in KB or new
            for fact in KB:
                subst = {}
                for premise in standardized_premises:
                    subst = unify(premise, fact[1], subst)
                    if subst is None:
                        break
                if subst is not None:
                    # Apply substitution
                    inferred = substitute([standardized_conclusion], subst)[0]
                    if inferred not in KB and inferred not in new:
                        new.append(inferred)
                    # Check if query is proven
                    subst_alpha = unify(alpha, inferred, {})
                    if subst_alpha is not None:
                        return subst_alpha

        if not new:
            return False
        KB.extend([((), fact) if isinstance(fact, tuple) else fact for fact in new])

# --------------------------------
# Example usage:
# Represent atomic sentences as tuples, e.g. Likes(John, Food) -> ("Likes", "John", "Food")

if __name__ == "__main__":
    # KB: List of rules: (premises, conclusion)
    # premises and conclusion are list/tuple of literals (predicates as tuples)

    KB = [
        # John likes all food: Food(x) => Likes(John, x)
        ( [("Food", "x")], ("Likes", "John", "x") ),

        # Apple and Vegetable are food
        ( [], ("Food", "Apple") ),
        ( [], ("Food", "Vegetable") ),

        # Anything eaten and not killed is food: Eats(x,y) ^ ¬Killed(x) => Food(y)
        ( [("Eats", "x", "y"), ("NotKilled", "x")], ("Food", "y") ),

        # Anil eats peanuts and not killed
        ( [], ("Eats", "Anil", "Peanuts") ),
        ( [], ("NotKilled", "Anil") ),

        # Harry eats everything Anil eats: Eats(Anil,y) => Eats(Harry,y)
        ( [("Eats", "Anil", "y")], ("Eats", "Harry", "y") ),

        # Alive implies not killed: Alive(x) => NotKilled(x)
        ( [("Alive", "x")], ("NotKilled", "x") ),

        # Not killed implies alive: NotKilled(x) => Alive(x)
        ( [("NotKilled", "x")], ("Alive", "x") )
    ]

    # Query: Likes(John, Peanuts)
    query = ("Likes", "John", "Peanuts")

    result = fol_fc_ask(KB, query)
    if result:
        print("Query proved with substitution:", result)
    else:
        print("Query cannot be proved.")
