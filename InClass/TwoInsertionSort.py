from copy import deepcopy

def isort(A):
    c1 = 0
    c2s = []
    for i in range(1, len(A)):
        v = A[i]
        j = i - 1
        c1 += 1
        c2 = 0
        while(j >= 0) and (A[j]>v):
            c2 += 1
            A[j+1]=A[j]
            j=j-1
            A[j+1] = v
            print(A)
        c2s.append(c2)
    print(max(c2s))
    print(c1)
    print()
    return A

def isort2(B):
    c1 = 0
    c2s = []
    for i in range(1, len(B)):
        j = i - 1
        c1 += 1
        c2 = 0
        while(j >= 0) and (B[j] > B[j+1]):
            temp = B[j+1]
            B[j+1] = B[j]
            B[j] = temp
            c2 += 1
            print(B)
            j = j-1
        c2s.append(c2)
    print(max(c2s))
    print(c1)
    print()
    return B

test = [5, 4, 3, 1]
test2 = [5, 4, 3, 1]
print(test)


print("Worst Cases")
print(isort(test))
print()
print(isort2(test2))
print()
print()
print("Best Cases")
test2 = [1, 3, 4, 5]
test = [1, 3, 4, 5]
print(isort(test))
print(isort2(test2))
test = [5, 2, 1, 4, 0]
test2 = [5, 2, 1, 4, 0]
print(isort(test))
print(isort2(test2))



