from math import sin, cos, pi
from tkinter import *




def main():
	root = Tk()
	root.title("rotation_in_3d")
	Canvas.draw_point = draw_point
	WIDTH = 500
	HEIGHT = WIDTH
	HORIZON_POINT = Point(0,0,-300)
	canvas = Canvas(root, height = WIDTH, width = HEIGHT, bg="white")
	points = [
		Point(-50, -50, -50),
		Point(-50, -50, 50),
		Point(-50, 50, -50),
		Point(-50, 50, 50),
		Point(50, -50, -50),
		Point(50, -50, 50),
		Point(50, 50, -50),
		Point(50, 50, 50)
	]

	draw_cube(points, 'cube', HORIZON_POINT, WIDTH, canvas)

	var_y = DoubleVar()
	var_x = DoubleVar()
	var_z = DoubleVar()

	def rotate_cube_by_y(points):
		angle = var_y.get()*pi/360
		rotated_points = copy_points_list(points)
		for p in rotated_points:
			p.apply_rotation(angle, 'y')
		return rotated_points

	def rotate_cube_by_x(points):
		angle = var_x.get()*pi/360
		rotated_points = copy_points_list(points)
		for p in rotated_points:
			p.apply_rotation(angle, 'x')
		return rotated_points


	def rotate_cube_by_z(points):
		angle = var_z.get()*pi/360
		rotated_points = copy_points_list(points)
		for p in rotated_points:
			p.apply_rotation(angle, 'z')
		return rotated_points


	def draw_rotated_cube(self):
		rotated_points = rotate_cube_by_x(rotate_cube_by_y(rotate_cube_by_z(points)))
		canvas.delete('cube')
		draw_cube(rotated_points, 'cube', HORIZON_POINT, WIDTH, canvas)



	scale_y = Scale( root, orient=HORIZONTAL, length=500, from_=0, to=360, variable = var_y, command = draw_rotated_cube )
	scale_x = Scale( root, orient=HORIZONTAL, length=500, from_=0, to=360, variable = var_x, command = draw_rotated_cube )
	scale_z = Scale( root, orient=HORIZONTAL, length=500, from_=0, to=360, variable = var_z, command = draw_rotated_cube )


	canvas.pack(pady=20)
	scale_y.pack()
	scale_x.pack()
	scale_z.pack()
	root.mainloop()



def draw_cube(points, tag, horizon_point, WIDTH, canvas):

	perspectived_points = perspective_points(points, WIDTH, horizon_point)


	converted_points = [Point(0,0,0) for i in range(len(points))]

	for i in range(len(points)):
		converted_points[i] = convert_to_canvas_coords(perspectived_points[i], WIDTH, WIDTH)


	#drawing edges
	connect_points(converted_points[0], converted_points[1], tag, canvas)
	connect_points(converted_points[1], converted_points[3], tag, canvas)
	connect_points(converted_points[3], converted_points[2], tag, canvas)
	connect_points(converted_points[2], converted_points[0], tag, canvas)

	connect_points(converted_points[4], converted_points[5], tag, canvas)
	connect_points(converted_points[5], converted_points[7], tag, canvas)
	connect_points(converted_points[7], converted_points[6], tag, canvas)
	connect_points(converted_points[6], converted_points[4], tag, canvas)

	connect_points(converted_points[0], converted_points[4], tag, canvas)
	connect_points(converted_points[1], converted_points[5], tag, canvas)
	connect_points(converted_points[2], converted_points[6], tag, canvas)
	connect_points(converted_points[3], converted_points[7], tag, canvas)


	for p in converted_points:
		canvas.draw_point(p, tag)


def convert_to_canvas_coords(point, width, height):
	return Point(point.x+width/2, height/2 - point.y,0)


def perspective_points(points, WIDTH, horizont_point):
	perspectived_points = [Point(0,0,0) for i in range(len(points))]
	for p, perspectived_p in zip(points,perspectived_points):
		perspectived_point = perspective_point(p, WIDTH, horizont_point)

		perspectived_p.x = perspectived_point.x
		perspectived_p.y = perspectived_point.y
		perspectived_p.z = perspectived_point.z

	return perspectived_points

def perspective_point(point, WIDTH, horizon_point):
	inside_scale = 1 - point.z/horizon_point.z
	x_from_horizon_point_to_edge = WIDTH/2 + horizon_point.x
	y_from_horizon_point_to_edge = WIDTH/2 - horizon_point.y

	plane_corner = Point(horizon_point.x - inside_scale*x_from_horizon_point_to_edge, horizon_point.y + inside_scale*y_from_horizon_point_to_edge, 0)


	plane_center = Point(plane_corner.x+inside_scale*WIDTH/2, plane_corner.y-inside_scale*WIDTH/2,0)

	rel_x = point.x*inside_scale
	rel_y = point.y*inside_scale

	perspectived_point = Point(plane_center.x+rel_x, plane_center.y+rel_y, 0)
	return perspectived_point


def draw_point(self, point, tag):
	self.create_oval(point.x-5, point.y-5, point.x+5, point.y+5, width = 0, fill = 'black', tags=tag)



def connect_points(point_1, point_2, tag , canvas):
	canvas.create_line(point_1.x, point_1.y, point_2.x, point_2.y, width=5, fill="black", tags=tag)




def copy_points_list(points_list):
	copy_of_list = [0]*len(points_list)
	for i in range(len(points_list)):
		copy_of_list[i] = Point(points_list[i].x, points_list[i].y, points_list[i].z)
	return copy_of_list


class Point:
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z

	def to_2d(self):
		return (self.x, self.y)

	def rotated_z(self, phi):
		rotated_x = self.x*cos(phi) - self.y*sin(phi)
		rotated_y = self.x*sin(phi) + self.y*cos(phi)
		return Point(rotated_x, rotated_y, self.z)

	def rotated_y(self, phi):
		rotated_x = self.x*cos(phi) - self.z*sin(phi)
		rotated_z = self.x*sin(phi) + self.z*cos(phi)
		return Point(rotated_x, self.y, rotated_z)

	def rotated_x(self, phi):
		rotated_y = self.y*cos(phi) - self.z*sin(phi)
		rotated_z = self.y*sin(phi) + self.z*cos(phi)
		return Point(self.x, rotated_y, rotated_z)

	def apply_rotation(self, phi, axis='z'):
		rotated_point = None
		if axis=='x':
			rotated_point = self.rotated_x(phi)
		elif axis=='y':
			rotated_point = self.rotated_y(phi)
		else:
			rotated_point = self.rotated_z(phi)

		self.x = rotated_point.x
		self.y = rotated_point.y
		self.z = rotated_point.z
		return self

	def __str__(self):
		return str((self.x, self.y, self.z))



if __name__ == "__main__":
	main()

