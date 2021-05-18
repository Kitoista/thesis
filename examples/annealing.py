temperature = TEMPERATURE_START
state = START()
cost = COST(state)

while CONTINUE():
    newState = NEIGHBOUR(state)
    newCost = COST(newState)

    if newCost < cost or ACCEPTABLE(cost, newCost, temperature):
        cost = newCost
        state = newState

    temperature -= TEMPERATURE_ALPHA
