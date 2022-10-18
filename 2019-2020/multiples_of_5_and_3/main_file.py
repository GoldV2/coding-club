# Instead of making a hard coded value (1000), I made it a variable, making the code more versatile.
n = int(input("What number will you find the sum of the multiples of 3 and 5 below it?\n\n>> "))
# List with all the numbers between 0, and n none inclusive.
l = list(range(0, n))

# Place holder for all values that are multiples of 3 and 5.
nums = []
for num in l:
	# When num is divided by 3 or 5 and has a remainder of 0 it will be appended to the nums placeholder.
	if num % 3 == 0:
		nums.append(num)
	elif num % 5 == 0:
		nums.append(num)

print(str(sum(nums)) + " Is the sum of all numbers divisible by 3 and 5 under " + str(n))
