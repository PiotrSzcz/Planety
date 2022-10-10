import pygame
import math
pygame.init()

W, H =  800, 800
Okno = pygame.display.set_mode((W, H))
pygame.display.set_caption("Symulacja")

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
	AU = 149.6e6 * 1000
	G = 6.67428e-11
	Skala = 250 / AU  
	Czas = 3600*24

	def __init__(self, x, y, orbita, kolor, masa):
		self.x = x
		self.y = y
		self.radius = orbita
		self.color = kolor
		self.mass = masa

		self.orbit = []
		self.isSlonce = False
		self.odleglosc_slonce = 0

		self.x_vel = 0
		self.y_vel = 0

	def draw(self, win):
		x = self.x * self.Skala + W / 2
		y = self.y * self.Skala + H / 2

		if len(self.orbit) > 2:
			punkty_orb = []
			for point in self.orbit:
				x, y = point
				x = x * self.Skala + W / 2
				y = y * self.Skala + H / 2
				punkty_orb.append((x, y))

			pygame.draw.lines(win, self.color, False, punkty_orb, 2)

		pygame.draw.circle(win, self.color, (x, y), self.radius)
		
		if not self.isSlonce:
			distance_text = FONT.render(f"{round(self.odleglosc_slonce/1000, 1)}km", 1, (227,230,228))
			win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

	def attraction(self, other):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

		if other.isSlonce:
			self.odleglosc_slonce = distance

		force = self.G * self.mass * other.mass / distance**2
		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force
		return force_x, force_y

	def update_position(self, planets):
		total_fx = total_fy = 0
		for planet in planets:
			if self == planet:
				continue

			fx, fy = self.attraction(planet)
			total_fx += fx
			total_fy += fy

		self.x_vel += total_fx / self.mass * self.Czas
		self.y_vel += total_fy / self.mass * self.Czas

		self.x += self.x_vel * self.Czas
		self.y += self.y_vel * self.Czas
		self.orbit.append((self.x, self.y))
		if len(self.orbit)>50:
			self.orbit.pop(0)


def main():
	run = True
	clock = pygame.time.Clock()

	Slonce = Planet(0, 0, 30, (252,223,3), 1.98892 * 10**30)
	Slonce.isSlonce = True

	Ziemia = Planet(-1 * Planet.AU, 0, 16, (53,252,3), 5.9742 * 10**24)
	Ziemia.y_vel = 29.783 * 1000 

	Mars = Planet(-1.524 * Planet.AU, 0, 12, (252,40,3), 6.39 * 10**23)
	Mars.y_vel = 24.077 * 1000

	Merkury = Planet(0.387 * Planet.AU, 0, 8, (141,145,142), 3.30 * 10**23)
	Merkury.y_vel = -47.4 * 1000

	Wenus = Planet(0.723 * Planet.AU, 0, 14, (227,230,228), 4.8685 * 10**24)
	Wenus.y_vel = -35.02 * 1000

	Planety = [Slonce, Ziemia, Mars, Merkury, Wenus]

	while run:
		clock.tick(30)
		Okno.fill((0, 0, 0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		for planet in Planety:
			planet.update_position(Planety)
			planet.draw(Okno)

		pygame.display.update()

	pygame.quit()

main()