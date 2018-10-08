
def create_powerset(input_set):
    subsets = [set()]
    if 1 == len(input_set):
        subset = set()
        subset.add(input_set[0])
        subsets.append(subset)
        return subsets
    else:
        # Remove one item from the input set add it to the current set
        # Recursively call method on subset
        subset = create_powerset(input_set[:len(input_set)-1])
        subsets.append(set(input_set[len(input_set)-1]))
        # Unions subset and subset
        for item in subset:
            if item not in subsets:
                subsets.append(set(item))
        # If the subset does not already exist, add/union the "cut" item to
        # each subset
        test_subset = []
        for item in subsets:
            temp = set(item)
            temp.add(input_set[len(input_set)-1])
            test_subset.append(temp)
        for item in test_subset:
            if item not in subsets:
                subsets.append(item)
    return subsets

test = ['a', 'b', 'c', '1', '4']
#test = ['a']
if(len(create_powerset(test)) == 2**len(test)):
    print("Powerset is valid \n")
print(create_powerset(test))
