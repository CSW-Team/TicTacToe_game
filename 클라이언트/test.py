import random
import pygame,sys
from pygame.locals import *
from socket import *

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('118.37.196.194', 8080))
print('연결 확인 됐습니다.')
pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((555,749),0,32)
pygame.display.set_caption("틱텍톡")
WHITE = (255,255,255)
black = (0,0,0)
black2 = (30,30,30)
background = pygame.image.load("check.png")
oimage = pygame.image.load("oo.png")
ximage = pygame.image.load("xx.png")
sf = pygame.font.SysFont("LexiGulim.ttf", 100)
sf1 = pygame.font.SysFont("LexiGulim.ttf", 70)

def forcheck(numbercheck1):
    temporary1 = -1
    check = 0
    allcheck = []
    for i in numbercheck1:
        if i != temporary1:
            temporary1 = i
            allcheck.append(check)
            check = 1
        else:
            check += 1
    allcheck.append(check)
    return max(allcheck)
def wincheck(ox):
    nextcheck = []
    numbercheck1 = []
    numbercheck2 = []
    numbercheck3 = []
    temporary = 0
    for i in range(len(ox)):
        numbercheck1.append(ox[i][0])
        numbercheck2.append(ox[i][1])
        if ox[i][0] == ox[i][1]:
            temporary += 1
        numbercheck3.append(ox[i][0] + ox[i][1])
    numbercheck1.sort()
    numbercheck2.sort()
    if temporary == 3 or numbercheck3.count(2) == 3 or forcheck(numbercheck1) >= 3 or forcheck(numbercheck2) >= 3:
        return 1
    return 0

def turncheck(a,go):
    typecheck = ""
    if a == 1:
        if go % 2 ==1:
            print("O player turn")
            typecheck = "X"
        else:
            print("X player turn")
            typecheck = "O"
    else:
        if go%2 == 1:
            print("X player turn")
            typecheck = "O"
        else:
            print("O player turn")
            typecheck = "X"
    return typecheck
            
def Ninput(a,b,go,x,o,location):
    if go%2 ==1:
            N[location[0]][location[1]] = a
            if a == "O":
                o.append(location)
                finalcheck = "O"
                final = wincheck(o)
            else:
                x.append(location)
                finalcheck = "X"
                final = wincheck(x)
    else:
            N[location[0]][location[1]] = b
            if b == "O":
                o.append(location)
                finalcheck = "O"
                final = wincheck(o)
            else:
                x.append(location)
                finalcheck = "X"
                final = wincheck(x)
    return o,x,finalcheck,final
            
def inputandcheck(N,a,go):
    if a == 1:
        if go % 2 ==1:
            data = clientSock.recv(1024)
            youdata = int(data.decode('utf-8'))
        else:
            youdata = int(input("please one check: "))
            clientSock.send(str(youdata).encode('utf-8'))
    else:
        if go%2 == 1:
            youdata = int(input("please one check: "))
            clientSock.send(str(youdata).encode('utf-8'))
        else:
            data = clientSock.recv(1024)
            youdata = int(data.decode('utf-8'))
    location = []
    check = 0
    for i in range(len(N)):
        for j in range(len(N[i])):
            if N[i][j] == youdata:
                location = [i,j]
                check = 1
    return location,check

N,go = [[1,2,3],[4,5,6],[7,8,9]],1
x,o = [],[]
a = random.randint(1,2)

DISPLAYSURF.fill(WHITE)
DISPLAYSURF.blit(background,(0,0))
if a == 1:
    text = sf1.render("O player turn",True,(0,0,0))
elif a == 2:
    text = sf1.render("X player turn",True,(0,0,0))
DISPLAYSURF.blit(text,(10,600))
pygame.display.update()

while True:
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(background,(0,0))
    for i in N:
        print(i)
    typecheck = turncheck(a,go)
    text = sf1.render(typecheck + " player turn",True,(0,0,0))
    DISPLAYSURF.blit(text,(10,600))
    location,check = inputandcheck(N,a,go)
    if check == 0:
        print("Please try again")
        continue
    go += 1
    if a== 1:
        o,x,finalcheck,final = Ninput("X","O",go,x,o,location)
    elif a == 2:
        o,x,finalcheck,final = Ninput("O","X",go,x,o,location)
    for i in range(len(o)):
        DISPLAYSURF.blit(oimage,(90+((o[i][1]+1) * 80),100+((o[i][0]+1) * 70)))
    for i in range(len(x)):
        DISPLAYSURF.blit(ximage,(90+((x[i][1]+1) * 80),100+((x[i][0]+1) * 70)))
    if final == 1:
        print(finalcheck + " WIN!!!")
        text = sf.render(finalcheck + " WIN!!!",True,(0,0,0))
        DISPLAYSURF.blit(text,(140,60))
        pygame.display.update()
        break
    if go == 10:
        print("DRAW")
        text = sf.render("DRAW",True,(0,0,0))
        DISPLAYSURF.blit(text,(160,60))
        pygame.display.update()
        break
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
clientSocekt.close()
quit()
