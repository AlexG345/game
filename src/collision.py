def point_to_circle(x1, y1, x2, y2, r):
	return (x1 - x2) ** 2 + (y1 - y2) ** 2 < r*r

def circle_to_circle(x1, y1, r1, x2, y2, r2):
	return (x1 - x2) ** 2 + (y1 - y2) ** 2 < (r1+r2)**2
