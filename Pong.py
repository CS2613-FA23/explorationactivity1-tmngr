import pygame

pygame.init() ##Initialize all imported pygame modules.

font = pygame.font.SysFont("Comic Sans", 20)

##Setting up the screen

w, h = 900, 600 ##Width and height that will be used to create screen.
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()
FPS = 30

##Let's make a class for the ball that we will have

class Ball:
    ##This is an instead method that initializes a newly created object.
    ##It takes the object as its first argument followed by additional arguments. 
    def __init__(self, xpos, ypos, radius, speed, colour):
        self.xpos = xpos
        self.ypos = ypos
        self.radius = radius
        self.speed = speed
        self.colour = colour
        self.xFac = 1 ##The direction it will be moving
        self.yFac = -1 ##The direction it will be moving
        self.ball = pygame.draw.circle(screen, self.colour, (self.xpos, self.ypos), self.radius)
        self.firstTime = 1

    ##Used to display the ball on the screen
    def display(self):
        self.ball = pygame.draw.circle(screen, self.colour, (self.xpos, self.ypos), self.radius)

    ##Let's add an update method that will use to change the ball's position
    def update(self):
        self.xpos += self.speed*self.xFac ##Changing the position with simple displacement equation.
        self.ypos += self.speed*self.yFac

        ##This first if statement is used to change the direction it's moving
        ##When it hits the top or the bottom of the screen
        if self.ypos <= 0 or self.ypos >= h:
            self.yFac *= -1

        ##These if, elif and else statements will check if the ball passed the min and the max of the width of the screen.
        ##If it has passed the min, return 1 so it can be used to determine that player 2 scored.
        ##If it has passed the max, return -1 so it can be used to determine that player 1 scored.
        ##If neither is the case, return 0 which means that ball is still in the screen.
        if self.xpos <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.xpos >= w and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0
    
    ##This will be used to reset the position of the ball to the middle of the screen
    ##It will also change the direction it was moving to the opposite direction.
    def reset(self):
        self.xpos = w//2
        self.ypos = h//2
        self.xFac *= -1
        self.firstTime = 1

    ##If the ball hits to one of the players, change it's x direction by -1
    def hit(self):
        self.xFac *= -1
    
    ##This is used when the ball collides with the player
    def getRect(self):
        return self.ball

##Now that we have a ball in the game, let's make player class.
##This player class will be an rectangle board that can move along the y-axes
##And collide with the ball to change it's direction.

class Player:
    ##Same method as the ball to create a player.
    def __init__(self, xpos, ypos, width, height, speed, colour):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.speed = speed
        self.colour = colour

        ##Since both the ball and player has to be objects that collide,
        ##This will help control the position and the collisions.
        self.playerRect = pygame.Rect(xpos, ypos, width, height)

        ##Object that is blit on the screen
        self.player = pygame.draw.rect(screen, self.colour, self.playerRect)

    ##Used to display the object on the screen
    def display(self):
        self.player = pygame.draw.rect(screen, self.colour, self.playerRect)

    ##Update the players direction
    def update(self, yFac):
        self.ypos += self.speed*yFac

        ##If ypos of the player (The bottom part of the rectangle) is equal to or small than 0, equal it to zero to stop it.
        if self.ypos <= 0:
            self.ypos = 0
        ##If the ypos + height of the rectangle (The top part of the rectangle) is equal or higher than the height of the screen,
        ##Stop it at the height of the screen - player height
        elif self.ypos + self.height >= h:
            self.ypos = h - self.height

        # Updating the rect with the new values
        self.playerRect = (self.xpos, self.ypos, self.width, self.height)

    ##The player class will also need to have their score to be displayed.
    ##This method will help us do that in a specified coordinates.
    def displayScore(self, text, score, x, y, colour):
        text = font.render(text+str(score), True, colour)
        textRect = text.get_rect()
        textRect.center = (x, y)
 
        screen.blit(text, textRect)

    def getRect(self):
        return self.playerRect
    
##The main method that will have the code to actually run the game.
def main():
    running = True

    ##Define the players and the ball.
    ##Picked the colour red for the players -> (255, 0, 0)
    ##And the colour white for the ball -> (255, 255, 255)
    player1 = Player(20, 0, 10, 100, 10, (255, 0, 0))
    player2 = Player(w-30, 0, 10, 100, 10, (255, 0, 0))
    ball = Ball(w//2, h//2, 7, 7, (255, 255, 255))

    ##Put the players in an array to make some of the functions easier
    Players = [player1, player2]
    
    ##Player initial scores and directions.
    player1Score, player2Score = 0, 0
    player1YFac, player2YFac = 0, 0

    while running:
        screen.fill((0, 0, 0)) ## Black -> (0, 0, 0)

        ##This for loop will handle the events
        for event in pygame.event.get():
            ##If the quit button has been pressed, close the game
            if event.type == pygame.QUIT:
                running = False
            ##Check if any keyboard buttons have been pressed
            if event.type == pygame.KEYDOWN:
                ##If up arrow has been pressed, change player 2 direction to -1
                if event.key == pygame.K_UP:
                    player2YFac = -1
                ##If down arrow has been pressed, change player 2 direction to 1
                if event.key == pygame.K_DOWN:
                    player2YFac = 1
                ##If the letter w has been pressed, change player 1 direction to -1
                if event.key == pygame.K_w:
                    player1YFac = -1
                ##If the letter s has been pressed, change player 1 direction to 1
                if event.key == pygame.K_s:
                    player1YFac = 1
            ##This if statement is here to make sure the player does not continue moving after the key buttons are released.
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player2YFac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player1YFac = 0

        ##This will check for collision for both of the players.
        ##This is where the array comes in handy, without the array there would have to be two if statements
        for player in Players:
            if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                ball.hit()

        ##Updating the players and the ball.
        player1.update(player1YFac)
        player2.update(player2YFac)
        ##Put the ball update in a var called point, because ball.update() returns a number that tells us which player has scored.
        point = ball.update()

        # -1 -> player1 has scored
        # +1 -> player2 has scored
        #  0 -> None of them scored
        if point == -1:
            player1Score += 1
        elif point == 1:
            player2Score += 1

        ##If someone has scored and point has been changed, the ball will be out of bounds so it has to be reseted.
        if point:   
            ball.reset()

        ##Display the players and the ball on the screen.
        player1.display()
        player2.display()
        ball.display()

        # Displaying the scores of the players
        player1.displayScore("Player1: ", player1Score, 100, 20, (255, 255, 255))
        player2.displayScore("Player2: ", player2Score, w-100, 20, (255, 255, 255))
        
        pygame.display.update() 
        clock.tick(FPS)

if __name__ == "__main__":
    main()
    pygame.quit()