a=int(raw_input("please enter first number"))
b=int(raw_input("please enter second number"))
c=int(raw_input("please enter third number"))
print a,b,c
if a > b and a > c:
    print(" a is greatest ")
elif b > a and b > c:
    print("b is greatest")
elif c > a and c > b:
    print("c is greatest")
else:
    print("incorrect output")