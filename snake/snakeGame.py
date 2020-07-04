import random
import pygame
from pygame import mixer
from copy import deepcopy


class Square(object):
    """
    This class constructs a Square object, which is used to the display the Snake's parts and the snack.
    """

    def __init__(self, posX, posY, color):
        """
        Creates a Square object.

        :param posX: The X coordinate for the Square
        :param posY: The Y coordinate for the Square
        :param color: The Square's color
        """
        self.width = 20  # Width of the square (20x20)
        self.height = 20  # Height of the square (20x20)
        self.color = color  # Sets the color to the parameterized color
        self.posX = posX  # Sets the X position to the position indicated by the posX parameter
        self.posY = posY  # Sets the Y position to the position indicated by the posX parameter
        self.dirRight = 1  # Square is facing right
        self.dirLeft = 0  # Square is facing left
        self.dirDown = 0  # Square is facing downwards
        self.dirUp = 0  # Square is facing upwards

    def move(self, posX, posY, dirRight, dirLeft, dirUp, dirDown):
        """
        Move function to update a Square's position.

        :param posX: The new X coordinate
        :param posY: The new Y coordinate
        :param dirRight: 1 if facing right, 0 otherwise
        :param dirLeft: 1 if facing left, 0 otherwise
        :param dirUp: 1 if facing upwards, 0 otherwise
        :param dirDown: 1 if facing downwards, 0 otherwise
        """
        self.posX = posX
        self.posY = posY
        self.dirRight = dirRight
        self.dirLeft = dirLeft
        self.dirUp = dirUp
        self.dirDown = dirDown


class Snake(object):
    """
    This class constructs a Snake object, which is represented as a list (self.body) of Squares.
    """

    def __init__(self):
        """
        Default constructor for the Snake.
        """
        self.body = []  # Sets the body to an empty list
        self.head = Square(100, 300, (255, 255, 255))  # Creates head
        self.body.append(self.head)  # Appends head to body

    def reset(self, posX, posY):
        """
        Resets the snake to size 1
        :param posX: The X coordinate where snake should start again
        :param posY: The Y coordinate where snake should start again
        """
        self.body = []
        self.head = Square(posX, posY, (255, 255, 255))
        self.body.append(self.head)

    def move(self, vX, vY):
        """
        Move function for the Snake. Utilizes the arrow keys for snake movement.

        :param vX: Snake's current velocity of X coordinate
        :param vY: Snake's current velocity of Y coordinate
        :return vX, vY, flag
        """
        keys = pygame.key.get_pressed()  # Reads if a key has been pressed
        flag = False  # Flag to check if a Snake of len 2 has backed into its tail
        lastX = self.body[-1].posX  # Initial X position of tail
        lastY = self.body[-1].posY  # Initial Y position of tail
        self.reorganize()  # Reorganizes the whole snake, leaving only the head to be changed

        if keys[pygame.K_w] or keys[pygame.K_UP]:  # If the "W" or "UP" key is pressed, changes the head's direction
            # upwards
            self.head.dirRight = 0
            self.head.dirLeft = 0
            self.head.dirDown = 0
            self.head.dirUp = 1
            vX = 0
            vY = -20

        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:  # If the "A" or "LEFT" key is pressed, changes the head's
            # direction to the left
            self.head.dirRight = 0
            self.head.dirLeft = 1
            self.head.dirDown = 0
            self.head.dirUp = 20
            vX = -20
            vY = 0

        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:  # If the "S" or "DOWN" key is pressed, changes the head's
            # direction downwards
            self.head.dirRight = 0
            self.head.dirLeft = 0
            self.head.dirDown = 1
            self.head.dirUp = 0
            vX = 0
            vY = 20

        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # If the "D" or "RIGHT" key is pressed, changes the head's
            # direction to the right
            self.head.dirRight = 1
            self.head.dirLeft = 0
            self.head.dirDown = 0
            self.head.dirUp = 0
            vX = 20
            vY = 0

        self.head.posX += vX  # Alters the vX value if movement is left or right
        self.head.posY += vY  # Alters the vY value if movement is upwards or downwards

        # These four if/elif statements control the boundaries, so the snake does not disappear out of screen.
        if self.head.posX >= 600:  # If the head's position is too far right, it will reappear in left side.
            self.head.posX = 0
        elif self.head.posX < 0:  # If the head's position is too far left, it will reappear in the right side.
            self.head.posX = 580
        elif self.head.posY >= 600:  # If the head's position is too low, it will reappear in the top.
            self.head.posY = 0
        elif self.head.posY < 0:  # If the head's position is too high, it will reappear in the bottom.
            self.head.posY = 580

        if self.head.posX == lastX and self.head.posY == lastY:  # Checks if snake has backed into its tail
            flag = True

        return vX, vY, flag

    def reorganize(self):
        """
        Reorganizes the snake. Utilizing a copy of the body list, every Square (except the head) is updated to the
        values of the Square before it.
        """
        newBody = deepcopy(self.body)  # Makes a deepcopy of the body (Will be used to make the changes to self.body)

        # For every square in the self.body array, its position will be updated to the square before it.
        for index, square in enumerate(self.body):
            if square == self.body[0]:  # Skips the head
                continue
            else:
                self.body[index].move(newBody[index - 1].posX, newBody[index - 1].posY,
                                      newBody[index - 1].dirRight,
                                      newBody[index - 1].dirLeft, newBody[index - 1].dirUp,
                                      newBody[index - 1].dirDown)

    def addSquare(self):
        """
        Adds a Square to the tail of the snake.
        """
        mixer.music.load("data/eating.wav")  # Eating sound
        mixer.music.set_volume(0.05)  # Reduces eating sound volume
        mixer.music.play()  # Plays eating sound
        tail = self.body[-1]  # Tail of the current snake

        if tail.dirDown == 1:  # If the tail's direction is facing down, adds a new Square above the current tail
            newTail = Square(tail.posX, tail.posY - 20, (255, 255, 255))
            newTail.dirDown = 1
            newTail.dirRight = 0
            self.body.append(newTail)

        elif tail.dirUp == 1:  # If the tail's direction is facing down, adds a new Square below the tail
            newTail = Square(tail.posX, tail.posY + 20, (255, 255, 255))
            newTail.dirUp = 1
            newTail.dirRight = 0
            self.body.append(newTail)

        elif tail.dirRight == 1:  # If the tail's direction is facing down, adds a new Square to the left of the tail
            newTail = Square(tail.posX - 20, tail.posY, (255, 255, 255))
            self.body.append(newTail)

        elif tail.dirLeft == 1:  # If the tail's direction is facing left, adds a new Square to the right of the tail
            newTail = Square(tail.posX + 20, tail.posY, (255, 255, 255))
            newTail.dirLeft = 1
            newTail.dirRight = 0
            self.body.append(newTail)

    def draw(self, window):
        """
        Draws the snake

        :param window: Window which contains the board
        """
        for i, square in enumerate(self.body):
            pygame.draw.rect(window, square.color, (square.posX, square.posY, square.width, square.height))


class Button:
    """
    Button class that creates the buttons for various seen in different screens, i.e. main menu
    """

    def __init__(self, x, y, width, height, text):
        """
        Parameterized constructor for a button.

        :param x: X-coordinate location for the button
        :param y: Y-coordinate location for the button
        :param width: The width of the button
        :param height: The height of the button
        :param text: Text (if any) to be written onto button
        """
        self.color = (107, 199, 107)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, window):
        """
        Draw function for Button.

        :param window: Window to draw the button onto
        """
        pygame.draw.rect(window, (25, 79, 41), (self.x - 3, self.y - 3, self.width + 6, self.height + 6), 0)
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)
        font = pygame.font.Font("data/8-bit-pusab.ttf", 20)
        buttonText = font.render(self.text, False, (255, 255, 255))
        window.blit(buttonText, (self.x + (self.width / 2 - buttonText.get_width() / 2),
                                 self.y + (self.height / 2 - buttonText.get_height() / 2)))

    def hover(self, pos):
        """
        Checks if the mouse position is above the button.

        :param pos: Position of mouse
        :return: True if mouse is on button, False otherwise
        """
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


def redraw(window, snake, snack, score):
    """
    Function to redraw the window after every movement.

    :param window: Window that contains the board
    :param snake: The snake on the board
    :param snack: The snack on the board
    :param score: The current score
    """
    window.fill((47, 48, 47))  # Fills background with a GRAY color
    font = pygame.font.Font("data/8-bit-pusab.ttf", 20)  # Font used to display score
    scoreText = font.render(str(score), True, (255, 255, 255))  # Renders score text

    if score > 99:
        window.blit(scoreText, [535, 10])
    elif score > 9:
        window.blit(scoreText, [550, 10])
    else:
        window.blit(scoreText, [565, 10])  # Blit's text to window depending on current score

    snake.draw(window)  # Calls the snake's draw function
    drawSnack(window, snack, snack.color)  # Draws snack
    pygame.display.update()


def goodSnackPos(snake, pX, pY):
    """
    Checks if generated coordinates for the snack are not in a place where the snake is.

    :param snake: The snake on the board
    :param pX: X value of the snack
    :param pY: Y value of the snack
    :return: True if the coordinates are OK, false otherwise
    """
    # For every Square in the snake's body, compares its posX and posY values to the snack's posX and posY values.
    for index, square in enumerate(snake.body):
        if square.posX == pX and square.posY == pY:  # If posX and posY are both equal
            return False

    return True


def newSnack():
    """
    Randomly generates coordinates for a potential new snack.
    :return a list with the X and Y coordinates
    """
    posX = random.randint(1, 28)  # Generates a number for posX (Not including borders)
    posY = random.randint(1, 28)  # Generates a number for posY (Not including borders)
    posX = posX * 20  # Multiplies X by the width of a cube
    posY = posY * 20  # Multiplies Y by the height of a cube

    return [posX, posY]


def drawSnack(window, snack, snackColor):
    """
    Draws the snack onto the window

    :param window: Screen where game is displayed
    :param snack: Snack to be drawn
    :param snackColor: Color of the snack
    """
    pygame.draw.rect(window, snackColor, (snack.posX, snack.posY, 20, 20))


def snakeHit(snake):
    """
    Function that checks if Snake's head has collided with one of its body parts, or if it goes backwards onto itself

    :param snake: The snake on the board
    :return: True if Snake has collided, False otherwise
    """
    for index, square in enumerate(snake.body):
        if index == 0:  # Skips over the head
            continue
        elif snake.head.posX == square.posX and snake.head.posY == square.posY:  # Compares the head to the body part
            return True

    return False


def helpWindow(window):
    """
    helpWindow displays a new window that contains the controls, instructions, and objective for players to see.
    :param window:
    :return:
    """
    run = True
    font = pygame.font.Font("data/8-bit-pusab.ttf", 18)  # Font used to display score
    controls = font.render("To move the snake, use \"WASD\"", True, (255, 255, 255))
    controls2 = font.render("or the arrow keys!", True, (255, 255, 255))
    objective = font.render("Eat food and the snake will grow...", True, (255, 255, 255))
    objective2 = font.render("but do not eat yourself!", True, (255, 255, 255))
    back = Button(150, 400, 300, 75, "Back to Menu")

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.hover(mousePos):
                    run = False

        mousePos = pygame.mouse.get_pos()
        window.fill((47, 48, 47))  # Fills background with a GRAY color
        window.blit(controls, (60, 150))
        window.blit(controls2, (150, 190))
        window.blit(objective, (30, 270))
        window.blit(objective2, (120, 310))
        back.draw(window)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            run = False

        if pygame.MOUSEMOTION:
            if back.hover(mousePos):
                back.color = (124, 230, 124)
            else:
                back.color = (107, 199, 107)

        pygame.display.update()

    mainMenu()


def highScoreWin(window):
    """
    Window in which the user's high scores are displayed.
    :param window:
    :return:
    """
    run = True
    back = Button(150, 462, 300, 75, "Back to Menu")
    resetEasy = Button(400, 200, 40, 40, "")  # Button to reset Easy mode
    resetNormal = Button(400, 275, 40, 40, "")  # Button to reset Normal mode
    resetHard = Button(400, 350, 40, 40, "")  # Button to reset Hard mode
    titleFont = pygame.font.Font("data/8-bit-pusab.ttf", 36)
    font = pygame.font.Font("data/8-bit-pusab.ttf", 24)
    resetFont = pygame.font.Font("data/8-bit-pusab.ttf", 14)
    HSTitle = titleFont.render("High Scores:", True, (255, 255, 255))
    resetText = resetFont.render("Reset", True, (255, 255, 255))
    resetIcon = pygame.image.load("data/resetIcon.png")
    resetIcon = pygame.transform.scale(resetIcon, (35, 35))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.hover(mousePos):
                    run = False
                elif resetEasy.hover(mousePos):
                    file = open("data/highscores.txt")
                    lines = file.readlines()
                    lines[0] = "0\n"
                    file = open("data/highscores.txt", "w")
                    file.writelines(lines)
                    file.close()
                elif resetNormal.hover(mousePos):
                    file = open("data/highscores.txt")
                    lines = file.readlines()
                    lines[1] = "0\n"
                    file = open("data/highscores.txt", "w")
                    file.writelines(lines)
                    file.close()
                elif resetHard.hover(mousePos):
                    file = open("data/highscores.txt")
                    lines = file.readlines()
                    lines[2] = "0"
                    file = open("data/highscores.txt", "w")
                    file.writelines(lines)
                    file.close()

        window.fill((47, 48, 47))
        HSFile = open("data/highscores.txt")
        lines = HSFile.readlines()
        HSFile.close()
        easy = font.render("Easy: " + lines[0].strip(), True, (255, 255, 255))
        normal = font.render("Normal: " + lines[1].strip(), True, (255, 255, 255))
        hard = font.render("Hard: " + lines[2].strip(), True, (255, 255, 255))
        mousePos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        back.draw(window)
        resetEasy.draw(window)
        resetNormal.draw(window)
        resetHard.draw(window)
        window.blit(HSTitle, (100, 75))
        window.blit(easy, (130, 200))
        window.blit(normal, (130, 275))
        window.blit(hard, (130, 350))
        window.blit(resetText, (385, 165))
        window.blit(resetIcon, (402, 202))
        window.blit(resetIcon, (402, 277))
        window.blit(resetIcon, (402, 352))

        if keys[pygame.K_SPACE]:
            run = False

        if pygame.MOUSEMOTION:
            if back.hover(mousePos):
                back.color = (124, 230, 124)
            elif resetEasy.hover(mousePos):
                resetEasy.color = (124, 230, 124)
            elif resetNormal.hover(mousePos):
                resetNormal.color = (124, 230, 124)
            elif resetHard.hover(mousePos):
                resetHard.color = (124, 230, 124)
            else:
                back.color = (107, 199, 107)
                resetEasy.color = (107, 199, 107)
                resetNormal.color = (107, 199, 107)
                resetHard.color = (107, 199, 107)

        pygame.display.update()

    mainMenu()


def mainMenu():
    """
    Main menu window.
    :return:
    """
    pygame.init()  # Initializes Pygame
    window = pygame.display.set_mode((600, 600))  # Creates initial window
    pygame.display.set_caption("Snake — by @thompmatt")  # Sets caption of window
    icon = pygame.image.load("data/snakeicon.png")
    icon = pygame.transform.scale(icon, (32, 32))
    pygame.display.set_icon(icon)
    easy = Button(200, 250, 200, 75, "Easy")
    normal = Button(200, 362.5, 200, 75, "Normal")
    hard = Button(200, 475, 200, 75, "Hard")
    helpButton = Button(540, 20, 40, 40, "")
    hsButton = Button(485, 20, 40, 40, "")
    helpCalled = False
    hsCalled = False

    # Reads High Scores
    HSFile = open("data/highscores.txt", "r+")
    HSFileLines = HSFile.readlines()
    highScores = []

    for i in range(0, 3):
        highScores.append(HSFileLines[i])

    HSFile.close()

    run = True

    while run:
        # If user hits the "X" quit button, closes application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy.hover(mousePos):
                    diff = 125
                    high = highScores[0]
                    run = False
                elif normal.hover(mousePos):
                    diff = 100
                    high = highScores[1]
                    run = False
                elif hard.hover(mousePos):
                    diff = 75
                    high = highScores[2]
                    run = False
                elif helpButton.hover(mousePos):
                    helpCalled = True
                    run = False
                elif hsButton.hover(mousePos):
                    hsCalled = True
                    run = False

        window.fill((47, 48, 47))  # Fills background with a GRAY color
        font = pygame.font.Font("data/8-bit-pusab.ttf", 60)  # Font used to display score
        font2 = pygame.font.Font("data/8-bit-pusab.ttf", 16)  # Font used to display score
        titleText = font.render("Snake", True, (255, 255, 255))  # Renders score text
        author = font2.render("by @THOMPMATT", False, (255, 255, 255))
        window.blit(titleText, (110, 80))  # Blit's text to window
        window.blit(author, (275, 180))
        easy.draw(window)
        normal.draw(window)
        hard.draw(window)
        helpButton.draw(window)
        hsButton.draw(window)
        qMark = pygame.image.load("data/qMark.png")
        qMark = pygame.transform.scale(qMark, (32, 32))
        trophy = pygame.image.load("data/trophy.png")
        trophy = pygame.transform.scale(trophy, (35, 35))
        window.blit(qMark, (543, 23))
        window.blit(trophy, (487, 22))
        mousePos = pygame.mouse.get_pos()

        if pygame.MOUSEMOTION:
            if easy.hover(mousePos):
                easy.color = (124, 230, 124)
            elif normal.hover(mousePos):
                normal.color = (124, 230, 124)
            elif hard.hover(mousePos):
                hard.color = (124, 230, 124)
            elif helpButton.hover(mousePos):
                helpButton.color = (124, 230, 124)
            elif hsButton.hover(mousePos):
                hsButton.color = (124, 230, 124)
            else:
                easy.color = (107, 199, 107)
                normal.color = (107, 199, 107)
                hard.color = (107, 199, 107)
                helpButton.color = (107, 199, 107)
                hsButton.color = (107, 199, 107)

        pygame.display.update()

    if helpCalled:
        helpWindow(window)
    elif hsCalled:
        highScoreWin(window)
    else:
        main(window, diff, high)


def main(window, diff, high):
    """
    Main loop of the Snake game.

    :param diff:
    :param window: Window to be drawn on.
    """

    snake = Snake()  # Creates the Snake object
    snackColor = (111, 201, 129)  # Color of snack (GREEN)
    snackPos = newSnack()  # Generates coordinates for possible snack

    # Continuously checks if snack has same coordinates as the head. If so, it regenerates a new snack.
    while not goodSnackPos(snake, snackPos[0], snackPos[1]):
        snackPos = newSnack()

    snack = Square(snackPos[0], snackPos[1], snackColor)  # Creates snack

    score = 0
    velX = 20  # Initial X velocity, used for continuous movement
    velY = 0  # Initial Y velocity, used for continuous movement
    run = True
    redraw(window, snake, snack, score)

    # Main loop
    while run:
        pygame.time.delay(diff)  # Delay between loops, slows game down

        # If user hits the "X" quit button, closes application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        velX, velY, secondSquare = snake.move(velX, velY)  # Calls the snake.move()

        if secondSquare or snakeHit(snake):  # Checks if a Snake has collided with itself
            mixer.music.load("data/thud.wav")  # Hit itself sound effect
            mixer.music.play()
            run = False

        if snake.head.posX == snack.posX and snake.head.posY == snack.posY:  # If the snake's head collides with a snack
            snake.addSquare()  # Adds a square to the snake
            score += 1  # Adds 1 to score
            snackPos = newSnack()  # Creates new snack coordinates

            # Checks whether coordinates are not on snake
            while not goodSnackPos(snake, snackPos[0], snackPos[1]):
                snackPos = newSnack()

            snack = Square(snackPos[0], snackPos[1], snackColor)  # Adds snack to the window

        redraw(window, snake, snack, score)  # Redraws window

    gameOver(window, score, diff, high)


def gameOver(window, score, diff, high):
    high = int(high)
    newHS = False
    run = True
    menu = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.hover(mousePos):
                    menu = True
                    run = False

        if score > high:
            newHS = True
            high = score  # Sets new score as the highest
            HSFile = open("data/highscores.txt", "r")
            lines = HSFile.readlines()

            if diff == 125:
                lines[0] = str(score) + "\n"  # Edits Easy high score
            elif diff == 100:
                lines[1] = str(score) + "\n"  # Edits Normal high score
            elif diff == 75:
                lines[2] = str(score)  # Edits Hard high score

            HSFile = open("data/highscores.txt", "w")
            HSFile.writelines(lines)
            HSFile.close()

        window.fill((47, 48, 47))  # Fills background with a GRAY color
        mousePos = pygame.mouse.get_pos()
        font = pygame.font.Font("data/8-bit-pusab.ttf", 40)  # Font used to display score
        font2 = pygame.font.Font("data/8-bit-pusab.ttf", 21)  # Font used to display score
        font3 = pygame.font.Font("data/8-bit-pusab.ttf", 18)  # Font used to display score
        gameOverText = font.render("Game Over", True, (255, 255, 255))  # Renders score text
        scoreText = font2.render("Score: " + str(score), True, (255, 255, 255))
        back = Button(20, 20, 40, 40, "")
        back.draw(window)
        arrow = pygame.image.load("data/back.png")
        arrow = pygame.transform.scale(arrow, (25, 25))
        window.blit(arrow, (26, 27))
        keys = pygame.key.get_pressed()
        HSFile = open("data/highscores.txt")
        lines = HSFile.readlines()

        if diff == 125:
            highScoreNum = lines[0].strip()
            highScoreText = font2.render("High Score: " + highScoreNum, True, (255, 255, 255))
        elif diff == 100:
            highScoreNum = lines[1].strip()
            highScoreText = font2.render("High Score: " + highScoreNum, True, (255, 255, 255))
        elif diff == 75:
            highScoreNum = lines[2].strip()
            highScoreText = font2.render("High Score: " + highScoreNum, True, (255, 255, 255))

        restart = font3.render("Press \"SPACE\" to play again", True, (255, 255, 255))
        window.blit(gameOverText, [120, 240])  # Blit's text to window
        window.blit(restart, [75, 500])

        # Displays score to screen
        if score > 99:
            window.blit(scoreText, [205, 310])
        elif score > 9:
            window.blit(scoreText, [215, 310])
        else:
            window.blit(scoreText, [225, 310])

        # Displays high score to screen
        if int(highScoreNum) > 99:
            window.blit(highScoreText, [150, 350])
        elif int(highScoreNum) > 9:
            window.blit(highScoreText, [160, 350])
        else:
            window.blit(highScoreText, [170, 350])

        if newHS:
            newHSText = font2.render("New High Score!", True, (255, 255, 255))
            window.blit(newHSText, [150, 100])

        if keys[pygame.K_SPACE]:
            run = False

        if pygame.MOUSEMOTION:
            if back.hover(mousePos):
                back.color = (124, 230, 124)
            else:
                back.color = (107, 199, 107)

        pygame.display.update()

    if menu:
        mainMenu()
    else:
        main(window, diff, high)


mainMenu()
