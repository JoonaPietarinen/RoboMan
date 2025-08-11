# TEE PELI TÄHÄN
import pygame
import random

# Alustetaan pygame
pygame.init()

# Näytön asetukset
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Robo's Escape")

# Värit
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
YELLOW = (255, 255, 0)
GREEN = (0, 225, 0)


# Ladataan kuvat
robo_img = pygame.image.load("robo.png")
coin_img = pygame.image.load("kolikko.png")
door_img = pygame.image.load("ovi.png")
monster_img = pygame.image.load("hirvio.png")


# Skaalataan kuvat
TILE_SIZE = 50
robo_img = pygame.transform.scale(robo_img, (TILE_SIZE, TILE_SIZE))
coin_img = pygame.transform.scale(coin_img, (TILE_SIZE, TILE_SIZE))
door_img = pygame.transform.scale(door_img, (TILE_SIZE, TILE_SIZE))
monster_img = pygame.transform.scale(monster_img, (TILE_SIZE, TILE_SIZE))


# Pelikellonaika
clock = pygame.time.Clock()
FPS = 60

# Pelikartta
level = [ 
    "##############O#####",
    "#R.......C#C.....#C#",
    "#.####.#####.#.#.#.#",
    "#.BC#C.M.....#....B#",
    "#.####.#######C###.#",
    "#.#C.............#.#",
    "#.#######B####.#...#",
    "#..#C.M..M#D#C.###.#",
    "##...####..C##.....#",
    "#..###CC#####..#.#M#",
    "O....C..B......#..CO",
    "####################",
    "O............BC###.O",
    "################..C#",
    "#CB............#.###",
    "#B############.#...#",
    "#.#..........#.###.#",
    "#.#.########C#.....#",
    "#...#C........B###C#",
    "##############O#####",
]



# Pelin objektit
player_pos = [1, 1]
monsters = []
coins = []
door = None
walls = []
player_energy = 100
ENERGY_LOSS_PER_MOVE = 1
ENERGY_GAIN_FROM_BATTERY = 30
batteries = []

# Kartan lataus
for row_index, row in enumerate(level):
    for col_index, tile in enumerate(row):
        x, y = col_index * TILE_SIZE, row_index * TILE_SIZE
        if tile == "#":
            walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
        elif tile == "C":
            coins.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
        elif tile == "D":
            door = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        elif tile == "M":
            monsters.append([col_index, row_index, random.choice([-1, 1]), random.choice([-1, 1])])
        elif tile == "R":
            player_pos = [col_index, row_index]
            player_start = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        elif tile == "B":
            batteries.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

# Piirtää pelikartan kentän laatat
def draw_level():
    for row_index, row in enumerate(level):
        for col_index, tile in enumerate(row):
            x, y = col_index * TILE_SIZE, row_index * TILE_SIZE
            if tile == "#":
                pygame.draw.rect(screen, DARK_GRAY, (x, y, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.rect(screen, GRAY, (x, y, TILE_SIZE, TILE_SIZE))

# Piirtää pelin objektit
def draw_game():
    draw_level()
    for coin in coins:
        screen.blit(coin_img, coin.topleft)
    draw_batteries()
    draw_energy_bar()
    if door:
        screen.blit(door_img, door.topleft)
    for monster in monsters:
        screen.blit(monster_img, (monster[0] * TILE_SIZE, monster[1] * TILE_SIZE))
    screen.blit(robo_img, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))
    draw_collected_coins() 

# Alustaa pelin
def initialize_game():
    global player_pos, monsters, coins, door, walls, collected_coins, player_energy, batteries


    player_pos = [1, 1]
    monsters = []
    coins = []
    door = None
    walls = []
    collected_coins = 0
    player_energy = 100
    batteries = []


    for row_index, row in enumerate(level):
        for col_index, tile in enumerate(row):
            x, y = col_index * TILE_SIZE, row_index * TILE_SIZE
            if tile == "#":
                walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif tile == "C":
                coins.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif tile == "D":
                door = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            elif tile == "M":
                monsters.append([col_index, row_index, random.choice([-1, 1]), random.choice([-1, 1])])
            elif tile == "R":
                player_pos = [col_index, row_index]
            elif tile == "B":
                batteries.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

# Näyttää kerättyjen kolikoiden määrän
def draw_collected_coins():
    font = pygame.font.SysFont("Arial", 24)
    text = font.render(f"Coins: {collected_coins}/20", True, YELLOW)
    screen.blit(text, (SCREEN_WIDTH - text.get_width() - 10, 10))



# Piirtää akut
def draw_batteries():
    battery_size = TILE_SIZE // 2
    for battery in batteries:
        center_x = battery.x + (TILE_SIZE - battery_size) // 2
        center_y = battery.y + (TILE_SIZE - battery_size) // 2
        pygame.draw.rect(screen, (0, 255, 0), (center_x, center_y, battery_size, battery_size))

# Piirtää energiapalkin
def draw_energy_bar():
    pygame.draw.rect(screen, WHITE, (10, 10, 200, 20), 2) 
    pygame.draw.rect(screen, (0, 255, 0), (10, 10, player_energy * 2, 20))  
    font = pygame.font.SysFont("Arial", 20)
    text = font.render("Energy", True, GREEN)
    text_x = 10 
    text_y = 10 - text.get_height() + 40 
    screen.blit(text, (text_x, text_y))

# Tarkistaa, kerääkö pelaaja akkuja    
def check_battery_collection():
    global batteries, player_energy
    player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    for battery in batteries[:]:
        if player_rect.colliderect(battery):
            player_energy = min(player_energy + ENERGY_GAIN_FROM_BATTERY, 100) 
            batteries.remove(battery)

# Vähentää pelaajan energiaa
def update_energy(moved):
    global player_energy
    if moved:
        player_energy -= ENERGY_LOSS_PER_MOVE
    if player_energy <= 0:
        if game_over_screen("Out of energy! Press R to restart or Q to quit."):
            main_game()


# Hae porttien sijainnit
portals = [(x, y) for y, row in enumerate(level) for x, tile in enumerate(row) if tile == 'O']

# Luo portaaliparit ja määritä portaalien edessä olevat ruudut
portal_pairs = []
portal_exits = {}
while portals:
    portal1 = portals.pop(0)
    for portal2 in portals:
        if portal1[0] == portal2[0] or portal1[1] == portal2[1]:  
            portal_pairs.append((portal1, portal2))
            portals.remove(portal2)
            

            if portal1[0] == portal2[0]:  
                if portal2[1] > portal1[1]:
                    portal_exits[portal2] = (portal2[0], portal2[1] - 1)
                    portal_exits[portal1] = (portal1[0], portal1[1] + 1)
                else:
                    portal_exits[portal2] = (portal2[0], portal2[1] + 1)
                    portal_exits[portal1] = (portal1[0], portal1[1] - 1)
            else:  
                if portal2[0] > portal1[0]:
                    portal_exits[portal2] = (portal2[0] - 1, portal2[1])
                    portal_exits[portal1] = (portal1[0] + 1, portal1[1])
                else:
                    portal_exits[portal2] = (portal2[0] + 1, portal2[1])
                    portal_exits[portal1] = (portal1[0] - 1, portal1[1])

# Tarkistaa, liikkuuko entiteetti portaalin läpi
def handle_portals(entity_x, entity_y):
    for portal_a, portal_b in portal_pairs:
        if (entity_x, entity_y) == portal_a:
            return portal_exits.get(portal_b, (entity_x, entity_y))
        elif (entity_x, entity_y) == portal_b:
            return portal_exits.get(portal_a, (entity_x, entity_y))
    return entity_x, entity_y  

# Lisää hirviön viimeisen liikkeen ajastin
monster_last_move_time = [0] * len(monsters)
MONSTER_MOVE_DELAY = 500  

# Liikuttaa hirviöitä
def move_monsters():
    current_time = pygame.time.get_ticks()
    for i, monster in enumerate(monsters):
        x, y, dx, dy = monster


        if current_time - monster_last_move_time[i] > MONSTER_MOVE_DELAY:
            new_x, new_y = x + dx, y + dy
            monster_rect = pygame.Rect(new_x * TILE_SIZE, new_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            if any(monster_rect.colliderect(wall) for wall in walls):
                if dx != 0:  
                    monster[2] = 0
                    monster[3] = random.choice([-1, 1])  
                elif dy != 0: 
                    monster[3] = 0
                    monster[2] = random.choice([-1, 1]) 

            elif any(monster_rect.colliderect(pygame.Rect(other[0] * TILE_SIZE, other[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                     for j, other in enumerate(monsters) if i != j):
                if dx != 0:  
                    monster[2] = 0
                    monster[3] = random.choice([-1, 1])  

                elif dy != 0:  
                    monster[3] = 0
                    monster[2] = random.choice([-1, 1]) 

            else:
                monster[0], monster[1] = new_x, new_y

            monster[0], monster[1] = handle_portals(monster[0], monster[1])
            monster_last_move_time[i] = current_time




# Pelin päävalikko
def game_over_screen(message):
    font = pygame.font.SysFont("Arial", 36)
    text = font.render(message, True, WHITE)
    screen.fill(BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: 
                    return True
                if event.key == pygame.K_q:  
                    pygame.quit()
                    exit()
        clock.tick(FPS)

# Pääsilmukka
def main_game():
    global player_pos, monsters, coins, door, collected_coins
    initialize_game()  

    running = True
    move_delay = 10  
    move_timer = move_delay

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if move_timer <= 0:
            if keys[pygame.K_UP]:
                dy = -1
                move_timer = move_delay
            if keys[pygame.K_DOWN]:
                dy = 1
                move_timer = move_delay
            if keys[pygame.K_LEFT]:
                dx = -1
                move_timer = move_delay
            if keys[pygame.K_RIGHT]:
                dx = 1
                move_timer = move_delay
        
        move_timer -= 1

        moved = dx != 0 or dy != 0  
        new_x, new_y = player_pos[0] + dx, player_pos[1] + dy
        player_rect = pygame.Rect(new_x * TILE_SIZE, new_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        if not any(player_rect.colliderect(wall) for wall in walls):
            player_pos = [new_x, new_y]

            player_pos[0], player_pos[1] = handle_portals(player_pos[0], player_pos[1])

        collected_coins += sum(1 for coin in coins if player_rect.colliderect(coin))
        coins = [coin for coin in coins if not player_rect.colliderect(coin)]
        if not coins and door and player_rect.colliderect(door):
            if game_over_screen("You win! Press R to restart or Q to quit."):
                main_game()
        update_energy(moved)
        check_battery_collection()
        move_monsters()

        for monster in monsters:
            monster_rect = pygame.Rect(monster[0] * TILE_SIZE, monster[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if monster_rect.colliderect(player_rect):
                if game_over_screen("Game over! Press R to restart or Q to quit."):
                    main_game()

        draw_game()
        pygame.display.flip()
        clock.tick(FPS)

main_game()
pygame.quit()