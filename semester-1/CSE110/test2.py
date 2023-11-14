cart=[]
def test(*something):
    print(something[0])
    if (type(something[0]) is str):
        for i in something:
            cart.append(i)
test("Air Jordan", 2)
print(cart)