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
        mixer.music.load("eating.mp3")  # Eating sound
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


def redraw(window, snake, snack, score):
    """
    Function to redraw the window after every movement.

    :param window: Window that contains the board
    :param snake: The snake on the board
    :param snack: The snack on the board
    :param score: The current score
    """
    window.fill((47, 48, 47))  # Fills background with a GRAY color
    font = pygame.font.Font("8-bit-pusab.ttf", 20)  # Font used to display score
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


def gameOver(window, score):
    run = True

    while run:
        # If user hits the "X" quit button, closes application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        window.fill((47, 48, 47))  # Fills background with a GRAY color

        font = pygame.font.Font("8-bit-pusab.ttf", 40)  # Font used to display score
        font2 = pygame.font.Font("8-bit-pusab.ttf", 21)  # Font used to display score
        font3 = pygame.font.Font("8-bit-pusab.ttf", 18)  # Font used to display score

        gameOverText = font.render("Game Over", True, (255, 255, 255))  # Renders score text
        scoreText = font2.render("Score: " + str(score), True, (255, 255, 255))
        restart = font3.render("Press \"SPACE\" to play again", True, (255, 255, 255))

        window.blit(gameOverText, [120, 240])  # Blit's text to window
        window.blit(restart, [75, 500])
        if score > 99:
            window.blit(scoreText, [205, 310])
        elif score > 9:
            window.blit(scoreText, [215, 310])
        else:
            window.blit(scoreText, [225, 310])

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            run = False

        pygame.display.update()

    main()


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


def main():
    """
    Main loop of the Snake game.

    @author Matt Thompson
    """
    pygame.init()  # Initializes pygame
    window = pygame.display.set_mode((600, 600))  # Creates initial window
    pygame.display.set_caption("Snake -- by @thompmatt")  # Sets caption of window

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
        pygame.time.delay(100)  # Delay between loops, slows game down

        # If user hits the "X" quit button, closes application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        velX, velY, secondSquare = snake.move(velX, velY)  # Calls the snake.move()

        if secondSquare or snakeHit(snake):  # Checks if a Snake has collided with itself
            mixer.music.load("thud.mp3")  # Hit itself sound effect
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

    gameOver(window, score)


main()
