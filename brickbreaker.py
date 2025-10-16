import pygame
import random
import sys

# --- Settings ---
WIDTH, HEIGHT = 800, 600
FPS = 60
PADDLE_W, PADDLE_H = 120, 14
BALL_RADIUS = 8
BRICK_COLS = 10
BRICK_ROWS = 5
BRICK_W = (WIDTH - 100) // BRICK_COLS
BRICK_H = 22
LIVES = 3

# --- Colors ---
WHITE = (245, 245, 245)
BG = (18, 18, 20)
PADDLE_COLOR = (40, 120, 200)
BALL_COLOR = (180, 230, 140)
BRICK_COLORS = [
    (240, 100, 100),
    (240, 160, 60),
    (240, 220, 80),
    (120, 200, 180),
    (140, 140, 240),
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 48)

class Paddle:
    def __init__(self):
        self.w = PADDLE_W
        self.h = PADDLE_H
        self.x = (WIDTH - self.w) / 2
        self.y = HEIGHT - 50
        self.speed = 7

    def move(self, dir_x):
        self.x += dir_x * self.speed
        if self.x < 0: self.x = 0
        if self.x + self.w > WIDTH: self.x = WIDTH - self.w

    def draw(self, surf):
        pygame.draw.rect(surf, PADDLE_COLOR, (self.x, self.y, self.w, self.h), border_radius=6)

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2 + 60
        angle = random.uniform(-1.0, 1.0)
        speed = 5.0
        self.vx = speed * angle
        self.vy = -speed
        self.radius = BALL_RADIUS
        self.stuck = True

    def update(self):
        if not self.stuck:
            self.x += self.vx
            self.y += self.vy

        # wall collisions
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx *= -1
        if self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
            self.vx *= -1
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy *= -1

    def draw(self, surf):
        pygame.draw.circle(surf, BALL_COLOR, (int(self.x), int(self.y)), self.radius)

class Brick:
    def __init__(self, x, y, w, h, color, hits=1):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.hits = hits

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=4)
        pygame.draw.rect(surf, (20,20,20), self.rect, 2, border_radius=4)

def make_bricks(rows, cols):
    bricks = []
    offset_x = 50
    offset_y = 80
    for r in range(rows):
        for c in range(cols):
            x = offset_x + c * BRICK_W
            y = offset_y + r * (BRICK_H + 6)
            color = BRICK_COLORS[r % len(BRICK_COLORS)]
            hits = 1 + (r // 3)  # higher rows tougher
            bricks.append(Brick(x, y, BRICK_W - 6, BRICK_H, color, hits))
    return bricks

def draw_text(surf, text, size, x, y, center=False):
    if size == "big":
        txt = big_font.render(text, True, WHITE)
    else:
        txt = font.render(text, True, WHITE)
    rect = txt.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surf.blit(txt, rect)

def main():
    paddle = Paddle()
    ball = Ball()
    bricks = make_bricks(BRICK_ROWS, BRICK_COLS)
    score = 0
    lives = LIVES
    running = True
    move_left = move_right = False
    level = 1

    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a): move_left = True
                if event.key in (pygame.K_RIGHT, pygame.K_d): move_right = True
                if event.key == pygame.K_SPACE:
                    if ball.stuck:
                        ball.stuck = False
                    else:
                        # quick nudge upward if needed
                        pass
                if event.key == pygame.K_r:
                    # restart
                    bricks = make_bricks(BRICK_ROWS, BRICK_COLS)
                    ball.reset()
                    paddle = Paddle()
                    score = 0
                    lives = LIVES
                    level = 1
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_a): move_left = False
                if event.key in (pygame.K_RIGHT, pygame.K_d): move_right = False

        # input -> move paddle
        dir_x = 0
        if move_left: dir_x -= 1
        if move_right: dir_x += 1
        paddle.move(dir_x)

        # stick ball to paddle before launch
        if ball.stuck:
            ball.x = paddle.x + paddle.w / 2
            ball.y = paddle.y - ball.radius - 2

        ball.update()

        # paddle collision
        paddle_rect = pygame.Rect(paddle.x, paddle.y, paddle.w, paddle.h)
        ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius*2, ball.radius*2)
        if ball_rect.colliderect(paddle_rect) and ball.vy > 0:
            overlap = (ball.x - (paddle.x + paddle.w / 2)) / (paddle.w / 2)
            ball.vx = overlap * 6
            ball.vy *= -1
            # small speed increase
            speed = min(9 + level * 0.5, (ball.vx**2 + ball.vy**2)**0.5 + 0.3)
            ang = (ball.vx**2 + ball.vy**2)**0.5
            if ang != 0:
                factor = speed / ang
                ball.vx *= factor
                ball.vy *= factor

        # brick collisions
        for brick in bricks[:]:
            if ball_rect.colliderect(brick.rect):
                # determine collision side
                bx, by = ball.x, ball.y
                if bx < brick.rect.left or bx > brick.rect.right:
                    ball.vx *= -1
                else:
                    ball.vy *= -1

                brick.hits -= 1
                if brick.hits <= 0:
                    bricks.remove(brick)
                    score += 10
                else:
                    score += 5
                break

        # bottom miss
        if ball.y - ball.radius > HEIGHT:
            lives -= 1
            if lives <= 0:
                # game over screen
                screen.fill(BG)
                draw_text(screen, "GAME OVER", "big", WIDTH/2, HEIGHT/2 - 40, center=True)
                draw_text(screen, f"Score: {score}", None, WIDTH/2, HEIGHT/2 + 10, center=True)
                draw_text(screen, "Press R to restart or Close window to quit", None, WIDTH/2, HEIGHT/2 + 60, center=True)
                pygame.display.flip()
                ball.stuck = True
                # wait until restart or quit
                waiting = True
                while waiting:
                    for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                            bricks = make_bricks(BRICK_ROWS, BRICK_COLS)
                            ball.reset()
                            paddle = Paddle()
                            score = 0
                            lives = LIVES
                            level = 1
                            waiting = False
                    clock.tick(15)
            else:
                ball.reset()

        # level up when bricks cleared
        if not bricks:
            level += 1
            BRICK_ROWS_local = min(6, BRICK_ROWS + level - 1)
            # create denser bricks for next level
            bricks = make_bricks(BRICK_ROWS_local, BRICK_COLS)
            # speed up ball a touch
            ball.vx *= 1.1
            ball.vy *= 1.1
            ball.stuck = True

        # draw
        screen.fill(BG)
        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)

        # HUD
        draw_text(screen, f"Score: {score}", None, 12, 10)
        draw_text(screen, f"Lives: {lives}", None, WIDTH - 100, 10)
        draw_text(screen, f"Level: {level}", None, WIDTH//2 - 30, 10)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
