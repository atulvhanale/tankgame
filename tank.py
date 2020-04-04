import random
import curses
import time
from pygame import mixer

s = curses.initscr()
curses.curs_set(0)
sh, sw = s.getmaxyx()
w = curses.newwin(sh, sw, 0 , 0)
w.keypad(1)
w.timeout(100)

tank_cy = int(sh - sh//8)
tank_cx = int(sw//2)
enemy_y =int(sh//8)
enemy_x =int(random.randint(1, sw-1))
enemy_y2 =int(sh//8)
enemy_x2 =int(random.randint(1, sw-1))

tank_health = 100
tank_score = 0

class Enemy:
	enemy_location=[]
	enemy_health:int
	enemy_shot_origin = []
	hit_area = []

	def __init__(self, location, health, origin):
		self.enemy_location = location
		self.enemy_health = health
		self.enemy_shot_origin = origin


tank = [
	[tank_cy-1,tank_cx-1],
	[tank_cy-1, tank_cx+1],
	[tank_cy,tank_cx],
	[tank_cy+1,tank_cx-1],
	[tank_cy+1,tank_cx+1]
	
]

enemy1_location = [

	[enemy_y-1,enemy_x-1],
	[enemy_y-1, enemy_x+1],
	[enemy_y,enemy_x]	
]

enemy2_location = [

	[enemy_y2-1,enemy_x2-1],
	[enemy_y2-1, enemy_x2+1],
	[enemy_y2,enemy_x2]	
]

enemy1 = Enemy(enemy1_location, 100, [enemy1_location[2][0], enemy1_location[2][1]])
enemy2 = Enemy(enemy2_location, 100, [enemy2_location[2][0], enemy2_location[2][1]])

enemies = [ enemy1, enemy2 ]

for i in range(5):
	w.addch(int(tank[i][0]), int(tank[i][1]), curses.ACS_CKBOARD)

for enemy in enemies:
	for i in range(3):
		w.addch(int(enemy.enemy_location[i][0]), int(enemy.enemy_location[i][1]), curses.ACS_CKBOARD)

key = curses.KEY_RIGHT

tank_shot_position = 1
enemy_shot_position = 1

tank_shot_origin1=[tank[0][0], tank[0][1]]
tank_shot_origin2=[tank[1][0], tank[1][1]]
hit_counter = 0
mixer.init()

while len(enemies)> 0 and tank_health > 0 :
	next_key = w.getch()
	key  = key if next_key == -1 else next_key

	#player +3 enemies here
	for i in range(5):
		w.addch(int(tank[i][0]), int(tank[i][1]), ' ')

	#erase enemy
	for enemy in enemies:
		for i in range(3):
			w.addch(int(enemy.enemy_location[i][0]), int(enemy.enemy_location[i][1]), ' ')

	for enemy in enemies:
		if random.randint(1,100)>50:
			for e in enemy.enemy_location:
				e[1] += 1
		else:
			for e in enemy.enemy_location:
				e[1] -= 1

	#erase 2 shots that keep propogating
	w.addch(int(tank_shot_origin1[0]-(tank_shot_position-1)), int(tank_shot_origin1[1]), ' ')
	w.addch(int(tank_shot_origin2[0]-(tank_shot_position-1)), int(tank_shot_origin2[1]), ' ')

	#enemy shots erase
	for enemy in enemies:
		w.addch(int(enemy.enemy_shot_origin[0]+(enemy_shot_position-1)), int(enemy.enemy_shot_origin[1]), ' ')

	#erase health of player
	w.addstr(sh-2, sw-15, '                  ')

	if key == curses.KEY_RIGHT:
		for t in tank:
			t[1]+=1

	elif key == curses.KEY_LEFT:
		for t in tank:
			t[1]-=1
	else:
		curses.endwin()

	#round box tank and enemy below	
	for enemy in enemies:
		if enemy.enemy_location[0][1] < 0:
			enemy.enemy_location = [[enemy.enemy_location[0][0], sw-3], [enemy.enemy_location[1][0],sw-1], [enemy.enemy_location[2][0], sw-2]]

		elif enemy.enemy_location[1][1] >= sw:
			enemy.enemy_location = [[enemy.enemy_location[0][0], 0], [enemy.enemy_location[1][0], 2], [enemy.enemy_location[2][0], 1]]

	if tank[0][1] < 0:
		tank = [[tank[0][0], sw-3], [tank[1][0],sw-1], [tank[2][0], sw-2], [tank[3][0], sw-3], [tank[4][0], sw-1]]

	elif tank[1][1] >= sw:
		tank = [[tank[0][0], 0], [tank[1][0], 2], [tank[2][0], 1], [tank[3][0], 0], [tank[4][0], 2]]

	for i in range(5):
		w.addch(int(tank[i][0]), int(tank[i][1]), curses.ACS_CKBOARD)

	for enemy in enemies:
		for i in range(3):
			w.addch(int(enemy.enemy_location[i][0]), int(enemy.enemy_location[i][1]), curses.ACS_CKBOARD)

	#emit 2 shots that keep propogating
	shot_starting = [tank[0][0], tank[0][1]]
	enemy_shot_starting = []
	for enemy in enemies:
		enemy_shot_starting.append([enemy.enemy_location[0][0], enemy.enemy_location[0][1]])

	if (int(tank[0][0])-tank_shot_position) < 0:
		tank_shot_position=1

	if (int(enemies[0].enemy_location[0][0] + enemy_shot_position)) > sh-2:
		enemy_shot_position=1

	if enemy_shot_position == 1:
		# enemy_shot_origin.clear()
		for enemy in enemies:
			enemy.enemy_shot_origin.clear()
			enemy.enemy_shot_origin = [enemy.enemy_location[2][0], enemy.enemy_location[2][1]]

	if (tank_shot_position) == 1:
		tank_shot_origin1=[tank[0][0], tank[0][1]]
		tank_shot_origin2=[tank[1][0], tank[1][1]]

	w.addch(int(tank_shot_origin1[0]-tank_shot_position), int(tank_shot_origin1[1]), curses.ACS_PI)
	w.addch(int(tank_shot_origin2[0]-tank_shot_position), int(tank_shot_origin2[1]), curses.ACS_PI)
	
	#enemy shots
	for enemy in enemies:
		w.addch(int( enemy.enemy_shot_origin[0] + enemy_shot_position ), int(enemy.enemy_shot_origin[1]), curses.ACS_PI)

	#tank_target_dimentions are first layer of tank for convenience simillarly for enemies
	for enemy in enemies:
		enemy.hit_area.clear()
		center_loc = enemy.enemy_location[2]

		enemy.hit_area = [
			[center_loc[0]-1, center_loc[1]-1],
			center_loc,
			[center_loc[0]-1, center_loc[1]+1]
		]

	tank_target_dimentions = tank[:2]
	tank_target_dimentions.insert(1, [tank[2][0]-1,tank[2][1]])
	
	#attack on enemies
	for enemy in enemies:
		if [int(tank_shot_origin1[0]-tank_shot_position ), int(tank_shot_origin1[1])] in enemy.hit_area or [int(tank_shot_origin2[0]-tank_shot_position ), int(tank_shot_origin2[1])] in enemy.hit_area:
			enemy.enemy_health -= 50
			w.refresh()
			mixer.music.load('enemy_dead.mp3')
			mixer.music.play(0)
			w.refresh()
		if enemy.enemy_health <= 0:
			for i in range(3):
				w.addch(int(enemy.enemy_location[i][0]), int(enemy.enemy_location[i][1]), ' ')
			w.addch(int(enemy.enemy_shot_origin[0]+(enemy_shot_position)), int(enemy.enemy_shot_origin[1]), ' ')
			enemies.remove(enemy)

	# attack on tank
	if len(enemies) > 0:
		for enemy in enemies:
			if [int(enemy.enemy_shot_origin[0]+enemy_shot_position), int(enemy.enemy_shot_origin[1])] in tank_target_dimentions:
				tank_health = tank_health - 25
				mixer.music.load('enemy_dead.mp3')
				mixer.music.play(0)
				hit_counter+=1

	tank_shot_position+=1
	enemy_shot_position+=1

	#display current health
	w.addstr(sh-2, sw-15, "Your Health:{}".format(tank_health))
	w.refresh()

if len(enemies) > 0:
	w.clear()
	w.refresh()
	w.addstr(sh//2, sw//2, "You Lost!" )
	w.refresh()
	mixer.music.load('lost.mp3')
	mixer.music.play(0)

else:
	w.clear()
	w.refresh()
	w.addstr(sh//2, sw//2, "You Won!")
	w.refresh()
	mixer.music.load('win.mp3')
	mixer.music.play(0)

time.sleep(50)
curses.endwin()
quit()
