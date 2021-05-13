import sys
from os import listdir
from os.path import isfile, join
from random import randint

import pygame

import cells

pygame.init()
size = (600, 600)
screen = pygame.display.set_mode(size)
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, size)
gridsize = [10, 10]
pygame.mixer.music.load(r"music/CleytonRX - Mystical Enigmatic Background Music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1.0)
# print(pygame.mixer.music.get_volume())
destroyS = []
for filename in [f for f in listdir(r"sounds/") if isfile(join("sounds/", f))]:
	filename = "sounds/" + filename
	destroyS.append(pygame.mixer.Sound(filename))
	pygame.mixer.Sound.set_volume(destroyS[-1],0.2)


def mapThis(current, min1, max1, min2, max2):
	x = min1
	max1 -= x
	current -= x
	x = min2
	max2 -= x
	out = (current / max1) * max2
	out += x + 1
	max2 += x
	if out < min2:
		out = min2
	elif out > max2:
		out = max2
	return out


def listdif(list1, list2):
	return (list1[0] - list2[0], list1[1] - list2[1])


def handleInput():
	global sel
	poses = [(0, 1), (1, 0), (0, -1), (-1, 0)]
	mousepos = pygame.mouse.get_pos()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			pos = (mousepos[0] // (size[0] // gridsize[0]), mousepos[1] // (size[1] // gridsize[1]))
			if len(sel):
				if listdif(sel[0], pos) in poses:
					sel.append(pos)
				else:
					sel = []
			else:
				sel.append(pos)

class main:
	def __init__(self):
		self.grid = self.gridmake(gridsize)
		self.imgs = self.load()
		self.undo = []

	def load(self):
		imgs = {}
		for filename in [f for f in listdir(r"sprits/") if isfile(join("sprits/", f))]:
			x = filename
			filename = "sprits/" + filename
			if filename == "sprits/0.png":
				temp = pygame.image.load(filename).convert_alpha()
				temp.set_alpha(105)
				imgs["0"] = (pygame.transform.scale(temp, (size[0] // len(self.grid[0]), size[1] // len(self.grid))))
				print("got it")
			else:
				temp = pygame.image.load(filename)
				imgs[str(x.replace(".png", ""))] = (
					pygame.transform.scale(temp, (size[0] // len(self.grid[0]), size[1] // len(self.grid))))
		return imgs

	def gridmake(self, ssize):
		grid = []
		for x in range(ssize[0]):
			row = []
			for y in range(ssize[1]):
				# if randint(0,10) >= 1:
				row.append(cells.cells(0, x, y, size, ssize))
			# else:
			# 	row.append(cells.cells(1, x, y, size, ssize))
			grid.append(row)
		return grid

	def spawn(self):
		for y in range(len(self.grid)):
			# for x in range(len(self.grid)):
			if self.grid[y][0].item == 0 and not self.grid[y][0].blocked:
				self.grid[y][0].item = randint(2, len(self.imgs))

	def draw(self):
		screen.fill((30, 30, 30))
		screen.blit(background, (0, 0))
		for x in range(len(self.grid)):
			for y in range(len(self.grid[0])):
				tsize = size[0] // len(self.grid)
				if self.grid[x][y].blocked == 0:
					screen.blit(self.imgs["0"], (tsize * x, tsize * y))
		for x in sel:
			tsize = size[0] // len(self.grid)
			if self.grid[x[0]][x[1]].blocked == 0:
				screen.blit(self.imgs["0"], (tsize * x[0], tsize * x[1]))
				screen.blit(self.imgs["0"], (tsize * x[0], tsize * x[1]))
		for x in range(len(self.grid)):
			for y in range(len(self.grid[0])):
				self.grid[x][y].draw(screen, self.imgs)

	def move(self):
		for x in range(len(self.grid)):
			for y in range(len(self.grid[0])):
				self.grid[x][y].move()

	def fall(self):
		temp = False
		for x in range(len(self.grid), 0, -1):
			for y in range(len(self.grid[0]), 0, -1):
				self.grid[x - 1][y - 1].fall(self.grid)

	def cheakmove(self):
		global sel
		# print(len(sel))
		if len(sel) == 2:
			if not self.grid[sel[0][0]][sel[0][1]].moving and not self.undo:
				dif = listdif(sel[1], sel[0])
				self.grid[sel[0][0]][sel[0][1]].move((dif[1], dif[0]), self.grid[sel[1][0]][sel[1][1]].item)
				dif = listdif(sel[0], sel[1])
				self.grid[sel[1][0]][sel[1][1]].move((dif[1], dif[0]), self.grid[sel[0][0]][sel[0][1]].item)
				self.undo = sel
		if len(self.undo) == 2:
			if not self.grid[self.undo[0][0]][self.undo[0][1]].moving:
				if self.destroy():
					self.undo = []
					sel=[]
				else:
					tsel = self.undo
					dif = listdif(tsel[1], tsel[0])
					self.grid[self.undo[0][0]][self.undo[0][1]].move((dif[1], dif[0]), self.grid[tsel[1][0]][tsel[1][1]].item)
					dif = listdif(tsel[0], tsel[1])
					self.grid[tsel[1][0]][tsel[1][1]].move((dif[1], dif[0]), self.grid[tsel[0][0]][tsel[0][1]].item)
					self.undo=[]
					sel = []

	def destroy(self):
		toremove = []
		for x in range(len(self.grid)):
			for y in range(len(self.grid[0])):
				a = self.grid[x][y].item
				if x < len(self.grid) - 2:
					for z in range(1, 3):
						if self.grid[x + z][y].item != a:
							break
						if z == 2:
							toremove.append((x, y))
							toremove.append((x + 1, y))
							toremove.append((x + 2, y))
				if y < len(self.grid[0]) - 2:
					for z in range(1, 3):
						if self.grid[x][y+z].item != a:
							break
						if z == 2:
							toremove.append((x, y))
							toremove.append((x, y+1))
							toremove.append((x, y+2))
		i = False
		for x in toremove:
			if not self.grid[x[0]][x[1]].moving:
				if i == False:
					pygame.mixer.Sound.play(destroyS[randint(0,1)])
				self.grid[x[0]][x[1]].item = 0
				i = True
		return toremove

main = main()
main.spawn()
clock = pygame.time.Clock()
sel = []
while True:
	clock.tick(60)
	handleInput()
	main.draw()
	main.move()
	main.fall()
	main.spawn()
	main.cheakmove()
	main.destroy()
	pygame.display.flip()
