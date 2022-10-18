import platform
import os
from random import randint
from time import time

def clear():
    if platform.system() == 'Windows':
        os.system('cls')

    else:
        os.system('clear')

def create_table(f1, f2):
    table = []
    for num1 in range(1, f1+1):
        row = []
        for num2 in range(1, f2+1):
            if num1 == 1:
                row.append(num2)

            elif num2 == 1:
                row.append(num1)

            else:
                row.append('?')

        table.append(row)
    
    return table

def print_table(table):
    result = ''
    for row in table:
        print_row = ''
        for num in row:
            print_row += f'{num:^7}'

        result += print_row + '\n'

    print(result)

def print_results(table, times):
    correct = 0
    incorrect = 0
    for row in table[1:]:
        for num in row[1:]:
            if num == 'X':
                incorrect += 1
                continue

            correct += 1

    if correct:
        ratio = str(round(correct/(correct+incorrect), 3)*100) + '%'

    else:
        print('YOU SUCK, YOU GOT NOTHING CORRECT!')
        return

    times.sort()
    slowest = round(times[-1], 2)
    fastest = round(times[0], 2)
    average = round(sum(times)/len(times), 2)

    cw = 9
    iw = 11
    rw = 7
    sw = 14
    fw = 14
    aw = 14
    w = cw + iw + rw + sw + fw + aw + 5
    
    clear()
    print(f"""
+{'-'*cw}+{'-'*iw}+{'-'*rw}+{'-'*sw}+{'-'*fw}+{'-'*aw}+
|{'Correct':^{cw}}|{'Incorrect':^{iw}}|{'Ratio':^{rw}}|{'Slowest Time':^{sw}}|{'Fastest Time':^{fw}}|{'Average Time':^{aw}}|
+{'-'*cw}+{'-'*iw}+{'-'*rw}+{'-'*sw}+{'-'*fw}+{'-'*aw}+
|{correct:^{cw}}|{incorrect:^{iw}}|{ratio:^{rw}}|{slowest:^{sw}}|{fastest:^{fw}}|{average:^{aw}}|
+{'-'*cw}+{'-'*iw}+{'-'*rw}+{'-'*sw}+{'-'*fw}+{'-'*aw}+
""")

def game():
    f1 = int(input("Please enter the first factor you'd like to be tested on\n\n>>> "))
    f2 = int(input("Please enter the second factor you'd like to be tested on\n\n>>> "))

    table = create_table(f1, f2)

    x = 0
    asked = []
    times = []
    while True:
        clear()
        print_table(table)

        if x == (f1-1)*(f2-1):
            print_results(table, times)
            break

        while True:
            question = (randint(2, f1), randint(2, f2))

            if question not in asked:
                break

        asked.append(question)

        time1 = time()
        while True:
            answer = input(f'What is: {question[0]}x{question[1]}\n\n>>> ')

            if answer.isdigit():
                answer = int(answer)
                if answer == question[0]*question[1]:
                    table[question[0]-1][question[1]-1] = answer
                    times.append(time()-time1)

                else:
                    table[question[0]-1][question[1]-1] = 'X'

                x += 1
                break

            else:
                print('Invalid. Try again')


game()
while True:    
    again = input('Play again? Enter "1" to play again. "0" to quit\n\n>>> ')
    if again == '0':
        print("Please don't leave :( stay and become a multiplication master!")
        break

    elif again == '1':
        game()

    else:
        print("I can't understand what you said, so I think you want to play again :D")
        game()