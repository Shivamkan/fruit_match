class cells:

	def __init__(self, blocked, i, j, screensize, gsize):
		self.blocked = blocked
		self.moving = 0
		self.i, self.j = i, j
		self.size = screensize[0] // gsize[0]
		self.item = 0
		self.point = [0,0]
		self.nextpos = [0, 0]
		self.nextitem = -1

	def draw(self, screen, imgs):
		# if self.blocked == 0:
		# 	screen.blit(imgs['0'], (self.i * self.size, self.j * self.size))
			if self.item != 0:
				screen.blit(imgs[str(self.item - 1)],
				            (self.i * self.size + int(self.point[0]), self.j * self.size + int(self.point[1])))

	def fall(self, grid):
		if not self.moving:
			if self.j <= len(grid) - 2:
				if grid[self.i][self.j].blocked == 0 and grid[self.i][self.j+1].item == 0 and self.item != 0:
					self.move((1, 0),grid[self.i][self.j+1].item)
					grid[self.i][self.j+1].move((-1, 0), self.item)

	def move(self, pos=[0, 0], item=-1):
		if pos != [0, 0]:
			self.nextpos = pos
			self.moving = 1
			self.nextitem = item
			# print('f')
		if self.moving:
			self.point[0] += (self.size / 20) * self.nextpos[1]
			self.point[1] += (self.size / 20) * self.nextpos[0]
			if abs(self.point[1]) >= self.size*abs(self.nextpos[0]) and abs(self.point[0])>= self.size*abs(self.nextpos[1]):
				self.moving = 0
				self.point = [0,0]
				self.nextpos = [0, 0]
				self.item = self.nextitem
				self.nextitem = -1
