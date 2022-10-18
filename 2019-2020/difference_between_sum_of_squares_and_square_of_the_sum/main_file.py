# Two liner that allows the user to input a number, somewhat understandable.
l = list(range(1, int(input("Input.\n\n>> "))+1))
print("The difference is: " + str((sum(l)**2) - sum(list(map(lambda x: x**2, l)))))

# One liner that allows the user tro input a number, way too messy because the same number has to be inputted twice.
print("The difference is: " + str((sum(list(range(1, int(input("Input\n>> "))+1)))**2) - sum(list(map(lambda x: x**2, list(range(1, int(input("Input\n>> "))+1)))))))

# One liner using the number 100.
print("The difference is: " + str((sum(list(range(1, 101)))**2) - sum(list(map(lambda x: x**2, list(range(1, 101)))))))
