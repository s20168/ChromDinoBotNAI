import cv2
import pyautogui as pag
from func import Object, grabScreen
import time


startTime = time.time()
prevTime = time.time()
speedRate = 1.3

playerIndex = 0
objectIndex = 0
distanceThreshold = 100.0

player = [Object('AvatarImages/dino.png'), Object('AvatarImages/dinoBlack.png')]
objects = [
     [Object('AvatarImages/cactus1.png'), Object('AvatarImages/cactus2.png'), Object('AvatarImages/bird.png')],
     [Object('AvatarImages/cactus1Black.png'), Object('AvatarImages/cactus2Black.png'), Object('AvatarImages/birdBlack.png')],
]

while True:
    img = grabScreen()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if player[0].match(img):
        topleft_x = int(player[0].location[0][0] - player[0].width)
        topleft_y = int(player[0].location[0][1] - 3*player[0].height)
        bottomRight_x = int(player[0].location[1][0] + 14*player[0].width)
        bottomRight_y = int(player[0].location[1][1] + 0.5*player[0].height)
        screenStart = (topleft_x, topleft_y)
        screenEnd = (bottomRight_x, bottomRight_y)
        break

pag.press('space')

while True:
    img_o = grabScreen(bbox=(*screenStart, *screenEnd))
    img = cv2.cvtColor(img_o, cv2.COLOR_BGR2GRAY)

    if player[0].match(img):
        playerIndex = 0
        objectIndex = 0
    elif player[1].match(img):
        playerIndex = 1
        objectIndex = 1
    
    if time.time() - prevTime > 1:
        if time.time() - startTime < 180 and player[playerIndex].location:
            distanceThreshold += speedRate
        
        prevTime = time.time()
    
    if player[playerIndex].location:
        cv2.rectangle(img_o, player[playerIndex].location[0], player[playerIndex].location[1], (255, 0, 0), 2)
    
    for object in objects[objectIndex]:
        if object.match(img):
            cv2.rectangle(img_o, object.location[0], object.location[1], (0, 0, 255), 2)

            if player[playerIndex].location:
                horizontalDistance = object.location[0][0] - player[playerIndex].location[1][0]
                verticalDistance = player[playerIndex].location[0][1] - object.location[1][1]

                if horizontalDistance < distanceThreshold and verticalDistance < 2:
                    pag.press('space')
                    break


    cv2.imshow("Screen ", img_o)

    if cv2.waitKey(1) == ord('q'):
        break