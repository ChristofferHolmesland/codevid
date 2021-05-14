import os
import glob
import subprocess

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

code = []
images = []
frames_per_token = 1

with open("./code_to_vid.py", "r") as f:
	code = f.readlines()
	
for file in glob.glob("./out/*.png"):
	os.remove(file)
	
fnt = ImageFont.truetype("./CodeNewRoman.otf", size=20)

class VisibleLines:
	def __init__(self):
		self.max_lines = 20
		self.lines = []
	
	def add_line(self, line):
		if len(self.lines) == self.max_lines:
			self.lines.pop(0)
		self.lines.append(line)
		
	def add_token(self, token):
		self.lines[-1] += token
		
vlines = VisibleLines()

num_lines_digits = len(str(len(code)))

for i, line in enumerate(code):
	vlines.add_line(str(i+1).rjust(num_lines_digits, " ") + ". ")
	
	if len(line) == 0:
		continue
	
	for token in line:
		vlines.add_token(token)
		img = Image.new("RGB", (1920, 1080))
		d = ImageDraw.Draw(img)
		for j, vline in enuerate(vlines.lines):
			d.text((10, j * 20), vline.replace("\t, "    "), fill=(238, 238, 238), font=fnt)
		images.extend([img] * frames_per_token)
		
for i in range(len(images)):
	images[i].save(f"./out/{i}.png", "png")
	
subprocess.run("ffmpeg.exe -framerate 24 -i ./out/%d.png -y -vf format=yuv420p out.mp4")