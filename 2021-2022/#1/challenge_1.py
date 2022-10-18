# Rule is: the sum of the first eight digits is equal to the last two digits
# Take a look at Discord for my opinion on this problem

def is_valid(n):
    if not n.isdigit():
        print("All characters must be digits.")
        
    elif len(n) > 10:
        print("Number cannot have more than ten digits.")

    else:
        print("Valid" if sum([int(d) for d in n[:8]]) == int(n[-2]) + int(n[-1]) else "Invalid")

while True:
    n = input("Enter a ten-digit number\n>>> ")
    is_valid(n)

    do = input("Enter 1 to try another, enter 0 to exit\n>>> ")
    if do == '0':
        print('Bye!')
        exit()
        
    elif do == '1':
        pass

    else:
        print('I don\'t understand that, so I assume you want to try another!')
