from actions.list_of_actions import LIST_OF_ACTIONS

def do(actions_list: list[dict]):
    results = []
    for call in actions_list:
        result = LIST_OF_ACTIONS[call["action"]](*call["params"])
        results.append(result)
    if len(results) == 1:
        return results[0]
    return results

