def is_correct(state, dimacs):
    # Convert characters to bools & reverse guess
    state = [bool(int(x)) for x in state][::-1]

    for line in dimacs.split('\n'):
        line = line.strip(' 0')
        clause_eval = False
        for literal in line.split(' '):
            if literal in ['p', 'c']:
                clause_eval = True
                break
            if '-' in literal:
                literal = literal.strip('-')
                lit_eval = not state[int(literal) - 1]
            else:
                lit_eval = state[int(literal) - 1]
            clause_eval |= lit_eval
        if clause_eval is False:
            return False
    return True


def verify_circuit_results(circuit_results, dimacs):
    found_ne = False
    ne_list = []
    for state, number_of_measurements in circuit_results.items():
        if number_of_measurements > 150 and is_correct(state, dimacs):
            k = state[::-1]
            ne_list.append(str(k))
            found_ne = True
    if not found_ne:
        print("No NE found")

    return ne_list
