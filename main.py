# Game Colour Palette: https://colorhunt.co/palette/1b262c0f4c753282b8bbe1fa
# Import Libraries
import os
import sys
import pygame
import random
import sqlitecloud

#PyGame Initialisation
pygame.init()
pygame.font.init()

# Connect to db
db = sqlitecloud.connect("sqlitecloud://cjt2v0bqsz.sqlite.cloud:8860?apikey=ScasSsHOWlJMG3JjOK0od5XAf2Bx4RbPvRuvZG8abDg")

# Global Variable Declaration
SCREEN_WIDTH = 1700
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
caption = pygame.display.set_caption("Whack-a-Duck")
clock = pygame.time.Clock()

aldrichFont = pygame.font.Font("fonts/aldrich/Aldrich-Regular.ttf", 30)
running = True
gameState = "start"
cells = []
circles = []
score = 0
cell1 = random.randint(0,8)
cell2 = random.randint(0,8)
startTime = pygame.time.get_ticks()
scoreText = aldrichFont.render("Score: " + str(score), True, (0,0,0))
username = ""
submitted = False

# Timer Set Up
timer = 30
timerInterval = 1000
timerEvent = pygame.USEREVENT + 1
pygame.time.set_timer(timerEvent, timerInterval)
timerText = aldrichFont.render("Time: " + str(timer), True, [0,0,0])

# Creation of gameSprite class
class gameSprite(pygame.sprite.Sprite):
        def __init__(self, img, clicked):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(os.path.join(img))
            self.rect = self.image.get_rect()
            self.clicked = clicked

# Image paths
startImgPath = "images/start_btn.png"
instructionImgPath = "images/instructions_btn.png"
exitImgPath = "images/exit_btn.png"
titleScreenImgPath = "images/title_screen_btn.png"
instructionScreenImgPath = "images/instructions.png"
gridBackgroundPath = "images/gridBackground.png"
lblBackgroundPath = "images/lblBackground.png"
emptyCellPath = "images/emptyCell.png"
plusDuckPath = "images/plusDuck.png"
minusFishPath = "images/minusFish.png"
endScreenBackgroundPath = "images/endScreenBackground.png"
nextImgPath = "images/next_btn.png"
inputFieldPath = "images/inputField.png"

# Creation of sprites using the gameSprite class
startImg = gameSprite(startImgPath, False)
instructionImg = gameSprite(instructionImgPath, False)
exitImg = gameSprite(exitImgPath, False)
titleScreenImg = gameSprite(titleScreenImgPath, False)
instructionScreenImg = gameSprite(instructionScreenImgPath, False)
gridBackground = gameSprite(gridBackgroundPath, False)
lblBackground = gameSprite(lblBackgroundPath, False)
emptyCell = gameSprite(emptyCellPath, False)
plusDuck = gameSprite(plusDuckPath, False)
minusFish = gameSprite(minusFishPath, False)
endScreenBackground = gameSprite(endScreenBackgroundPath, False)
nextImg = gameSprite(nextImgPath, False)
inputFieldImg = gameSprite(inputFieldPath, False)


# Main Function
def main():
    global screen, clock, timer, running, timerText, score, scoreText, gameState, username, submitted
    
    # Main loop for the game
    while running:
        for event in pygame.event.get():
            # If the game is quit, stop the main loop
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If gameState is start, check for collisions on each of the title screen buttons
                if gameState == "start":
                    if startImg.rect.collidepoint(event.pos):
                        gameState = "setup"
                    elif instructionImg.rect.collidepoint(event.pos):
                        gameState = "instructions"
                    elif exitImg.rect.collidepoint(event.pos):
                        gameState = "exit"
                elif gameState == "instructions":
                    if titleScreenImg.rect.collidepoint(event.pos):
                        gameState = "start"
                elif gameState == "scoreInput":
                    if exitImg.rect.collidepoint(event.pos):
                        gameState = "exit"
                # Else if gameState is game, check for collisions for each of the moving sprites in the game
                elif gameState == "game":
                    if plusDuck.rect.collidepoint(event.pos):
                        if plusDuck.clicked == False:
                            score += 1
                            plusDuck.clicked = True
                            scoreText = aldrichFont.render("Score: " + str(score), True, (0,0,0))
                    elif minusFish.rect.collidepoint(event.pos):
                        if minusFish.clicked == False:
                            score -= 1
                            minusFish.clicked = True
                            scoreText = aldrichFont.render("Score: " + str(score), True, (0,0,0))
                elif gameState == "endgame":
                    if nextImg.rect.collidepoint(event.pos):
                        if score > 0:
                            gameState = "scoreInput"
                        else:
                            gameState = "exit"
            elif event.type == pygame.KEYDOWN and gameState == "scoreInput":
                if submitted == False:
                    if event.key == pygame.K_RETURN:
                        submitted = True
                        db.execute("INSERT INTO scores (name, score) VALUES (?,?);", (username, score))
                        db.commit()
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        if (len(username)) < 11:
                            username += event.unicode
            elif event.type == timerEvent and gameState == "game":
                timer -= 1
                timerText = aldrichFont.render("Time: " + str(timer), True, [0,0,0])
                if timer == 0:
                    pygame.time.set_timer(timerEvent, 0)

        # If/Else statement to call the different functions depending on what the gameState is
        if gameState == "start":
            titleScreen()
        elif gameState == "instructions":
            instructionScreen()
        elif gameState == "setup":
            drawGrid()
        elif gameState == "game":
            gameLogic()
        elif gameState == "endgame":
            endScreen()
        elif gameState == "scoreInput":
            scoreInput()
        elif gameState == "exit":
            screen.fill("black")
            pygame.quit()
            sys.exit()
    
        # Updates screen
        pygame.display.flip()
        clock.tick(30)


def titleScreen():
    # Declare global variables to be used in this function
    global screen, gameState
    # Fills screen with colour
    screen.fill("#1B262C")

    # Calculate the x value needed to place button in middle of screen
    centerX = (SCREEN_WIDTH / 2) - (startImg.image.get_width() / 2)
    
    # Set rect x and y values
    startImg.rect.x = centerX
    instructionImg.rect.x = centerX
    exitImg.rect.x = centerX
    startImg.rect.y = 100
    instructionImg.rect.y = 300
    exitImg.rect.y = 500

    # Add buttons to screen
    screen.blit(startImg.image, [startImg.rect.x, startImg.rect.y])
    screen.blit(instructionImg.image, [instructionImg.rect.x, instructionImg.rect.y])
    screen.blit(exitImg.image, [exitImg.rect.x, exitImg.rect.y])


def instructionScreen():
    global screen

    # Calculates the x value for the button
    titleImgX = (SCREEN_WIDTH / 2) - (titleScreenImg.rect.width / 2)
    instructionImgX = (SCREEN_WIDTH / 2) - (instructionScreenImg.rect.width / 2)
    
    # Fills the screen background
    screen.fill("#1B262C")

    # Initialises the x and y values for the button
    titleScreenImg.rect.x = titleImgX
    titleScreenImg.rect.y = 600
    instructionScreenImg.rect.x = instructionImgX
    instructionScreenImg.rect.y = 70

    # Adds the button to the screen
    screen.blit(instructionScreenImg.image, [instructionScreenImg.rect.x, instructionScreenImg.rect.y])
    screen.blit(titleScreenImg.image, [titleScreenImg.rect.x, titleScreenImg.rect.y])


def drawGrid():
    # Declare global variables to be used in this function
    global screen, gameState

    # Declare local variables
    rect_size = 150
    circle_size = 60

    # Calculate where the x and y values of the grid so it can be centered on the screen
    rect_x = (SCREEN_WIDTH / 2) - ((rect_size * 3) / 2)
    rect_y = (SCREEN_HEIGHT / 2) - ((rect_size * 3) / 2)

    # Assign x and y values to the gridBackground
    gridBackground.rect.x = rect_x
    gridBackground.rect.y = rect_y

    # Fill the screen with a white colour
    screen.fill("#3282B8")
    screen.blit(gridBackground.image, [gridBackground.rect.x, gridBackground.rect.y])
            
    for i in range(3):
        for j in range(3):
            # Creates a Rect object
            rect = pygame.Rect(rect_x, rect_y, rect_size, rect_size)
            # Draws the rect object on the screen
            pygame.draw.rect(screen, (0,0,0), rect, 2)
            # Draws a circle in the center of rect, but the circle is the came colour as the background
            circle = pygame.draw.circle(screen, ("#1B262C"), rect.center, circle_size)
            # Adds rect to cells list
            cells.append(rect)
            # Adds circle to circles list
            circles.append(circle)

            # Increments x value by size variable
            rect_x = (rect_x + rect_size)
        
        #Resets x value
        rect_x = rect_x - (rect_size * 3)
        # Increments y value by size variable
        rect_y = rect_y + rect_size

    # Changes gameState variable to "game"
    gameState = "game"


def gameLogic():
    global screen, timer, gameState, circles, score, timerText, cell1, cell2, startTime, scoreText

    # Add background image to screen
    screen.blit(lblBackground.image, [625, 20])

    # Add timer and score labels to screen
    screen.blit(timerText, [655, 35])
    screen.blit(scoreText, [655, 75])
    
    # Add empty cell images into cells
    for i in circles:
        screen.blit(emptyCell.image, [i.x, i.y])
    
    if timer > 0:
        # Change the position of the sprites every 500ms
        if pygame.time.get_ticks() - startTime > 500:
            cell1 = random.randint(0,8)
            cell2 = random.randint(0,8)
            plusDuck.clicked = False
            minusFish.clicked = False
            # If both cell1 and cell2 are equal get another random value for cell2
            if cell1 == cell2:
                cell2 = random.randint(0,8)
            # If both cell1 and cell two show a different value change the x and y values of the sprites and reset the startTime variable
            else:
                startTime = pygame.time.get_ticks()
                plusDuck.rect.x = circles[cell1].x
                plusDuck.rect.y =  circles[cell1].y
                minusFish.rect.x = circles[cell2].x
                minusFish.rect.y = circles[cell2].y
                
        # Update the sprites position on screen
        screen.blit(plusDuck.image, [plusDuck.rect.x, plusDuck.rect.y])
        screen.blit(minusFish.image, [minusFish.rect.x, minusFish.rect.y])

    # If the timer has run out change the gameState to "endgame"
    elif timer <= 0:
        gameState = "endgame"


def endScreen():
    global screen, score

    # Initalise Rect - to be used for subsurface
    finalScreenRect = pygame.Rect(0,0, 300, 100)

    # Calculates the x values of each component to ensure they are in the center of the screen
    finalScreenX = (SCREEN_WIDTH / 2) - (finalScreenRect.width/ 2)
    btnImageX = (SCREEN_WIDTH / 2) - (nextImg.rect.width / 2)
    bgImageX = (SCREEN_WIDTH / 2) - (endScreenBackground.rect.width / 2)

    # Assign x and y values
    finalScreenRect.x = finalScreenX
    finalScreenRect.y = 260
    nextImg.rect.x = btnImageX
    nextImg.rect.y = 600
    exitImg.rect.x = btnImageX
    exitImg.rect.y = 600
    endScreenBackground.rect.x = bgImageX
    endScreenBackground.rect.y = 150

    # Creates subsurface
    finalScreen = screen.subsurface(finalScreenRect)

    # Change colour of background and add background image to screen
    screen.fill("#1B262C")
    screen.blit(endScreenBackground.image, [endScreenBackground.rect.x, endScreenBackground.rect.y])

    # If the score is greater than 0 display the success message
    if score > 0:
        successText = aldrichFont.render("Congratulations!", True, (0,0,0))
        centerTextX = (finalScreenRect.width / 2) - (successText.get_width() / 2)
        finalScreen.blit(successText, [centerTextX, 10])
        screen.blit(nextImg.image, [nextImg.rect.x, nextImg.rect.y])
    # If the score is 0 or less display the failure message
    elif score <= 0:
        failText = aldrichFont.render("Game Over!", True, (0,0,0))
        centerTextX = (finalScreenRect.width / 2) - (failText.get_width() / 2)
        finalScreen.blit(failText, [centerTextX, 10])
        screen.blit(exitImg.image, [exitImg.rect.x, exitImg.rect.y])

    # Display the score
    finalScoreText = aldrichFont.render("Your Score: " + str(score), True, (0,0,0))
    centerTextX = (finalScreenRect.width / 2) - (finalScoreText.get_width() / 2)
    finalScreen.blit(finalScoreText, [centerTextX, 50])


def scoreInput():
    global screen, score, gameState

    # Fills screem with background colour
    screen.fill("#1B262C")

    # Creates Rect for user input field
    userInputRect = pygame.Rect(0, 0, 250, 40)

    # Define text to be rendered
    usernameText1 = aldrichFont.render("Please enter your name", True, (0,0,0))
    usernameText2 = aldrichFont.render("and press enter:", True, (0,0,0))
    usernameInput = aldrichFont.render(username, True, (0,0,0))
    submitMsg = aldrichFont.render("Username submitted", True, (0,0,0))

    # Calculate center x values for all screen components
    backgroundX = (SCREEN_WIDTH / 2) - (endScreenBackground.rect.width / 2)
    usernameTextX = (SCREEN_WIDTH / 2) - (usernameText1.get_width() / 2)
    userInputX = (SCREEN_WIDTH / 2) - (userInputRect.width / 2)
    inputImgX = (SCREEN_WIDTH / 2) - (inputFieldImg.rect.width / 2)
    submitMsgX = (SCREEN_WIDTH / 2) - (submitMsg.get_width() / 2)
    exitBtnX = (SCREEN_WIDTH / 2) - (exitImg.rect.width / 2)

    # Assign x and y values to screen components
    endScreenBackground.rect.x = backgroundX
    endScreenBackground.rect.y = 150
    userInputRect.x = userInputX
    userInputRect.y = 300
    inputFieldImg.rect.x = inputImgX
    inputFieldImg.rect.y = 300
    exitImg.rect.x = exitBtnX
    exitImg.rect.y = 600

    # Creates a subsurface for the user input
    userInputScreen = screen.subsurface(userInputRect)
    
    # Adds components to the screen
    screen.blit(endScreenBackground.image, [endScreenBackground.rect.x, endScreenBackground.rect.y])
    screen.blit(usernameText1, [usernameTextX, 200])
    screen.blit(usernameText2, [usernameTextX, 230])
    userInputScreen.fill("white")
    screen.blit(inputFieldImg.image, [inputFieldImg.rect.x, inputFieldImg.rect.y])
    userInputScreen.blit(usernameInput, [5, 12])

    # Components added to screen after the username has been submitted
    if (submitted == True):
        screen.blit(endScreenBackground.image, [endScreenBackground.rect.x, endScreenBackground.rect.y])
        screen.blit(submitMsg, [submitMsgX, 290])
        screen.blit(exitImg.image, [exitImg.rect.x, exitImg.rect.y])
        

# Run main() function
if __name__ == "__main__":
    main()

