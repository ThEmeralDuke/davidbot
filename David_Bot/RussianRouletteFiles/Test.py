import random
Bullets=[]
Players=""
game=[]
def BulletCreation():
    global Players
    global Bullets
    Players= random.randint(1,5)
    global Bullets
    Bullets= ["1"]
    for i in range(random.randint(1,5)):
        Bullets.append("0")
    random.shuffle(Bullets)
    Bullets= "|".join(Bullets)
    print(Players, Bullets)


i= 0
for o in range(5):
    BulletCreation()
    temp= []
    temp.append(Players)
    temp.append(Bullets)
    game.append(temp)
    Bullets=[]
    Players=""
    i= i+1


number= random.randint(1,5)
print(game[number][0],game[number][1])