def tape_initialization(blanc, input_string):
    tape = [blanc, blanc]
    tape.extend(list(input_string))
    tape.extend([blanc, blanc])
    return tape

def derivation(blanc, initial_state, acceptance_state, delta, tape):
    print("Ejecutando secuencia...")
    delta = delta #transiciones de la máquina
    state = initial_state
    index = 2 #punto de inicio de la cinta
    char_tape = tape[index] #caracter leido actualmente en la cinta

    if char_tape == blanc:
        print("aaaaaaaaaaaaaaaaaa")

    while not (state == acceptance_state and char_tape == blanc):
        changes = delta_transitions(state, char_tape, delta)
        state = changes[0]
        tape[index] = changes[1]
        index += int(changes[2])
        char_tape = tape[index]
    
    tape_result = "".join(tape)
    return tape_result.replace(blanc, "")

def delta_transitions(state, char_input, delta):
    key_value = f"{state}, {char_input}"
    changes = delta.get(key_value, []).copy()
    
    if len(changes) == 0:
        return changes

    # Reemplazar dirección por valor de suma
    if changes[2] == "S":
        changes[2] = "0"
    elif changes[2] == "R":
        changes[2] = "1"
    elif changes[2] == "L":
        changes[2] = "-1"
    
    return changes
