import shutil, os, psutil, copy, sys, subprocess
from termcolor import colored
from itertools import zip_longest

size = shutil.get_terminal_size()

col = size.columns
lin = size.lines

tl = "\u2554"
tr = "\u2557"
top = "\u2550"
side = "\u2551"
bl = "\u255A"
br = "\u255D"

headcol = "cyan"
bodycol = "white"
osname = os.name
logo = __import__(f"logo.{osname}", fromlist=[None])

match osname:
	case "nt":
		def clear():
			subprocess.run("cls", shell=True)
	case "posix":
		def clear(): 
			os.system("clear")

vtb = [[("", "white", None)]]
def buffer(text, fg="white", bg=None):
	global vtb
	vtb[-1].append((text, fg, bg))

def clearvtb():
	global vtb
	vtb = [[("", "white", None)]]

def newline():
	global vtb
	vtb.append([("", "white", None)])

def printvtb():
	global vtb, col, lin, tl, top, tr, bl, br, side
	buf = ""
	buf += tl + (col-2)*top + tr + "\n"
	lins = 0
	for i in vtb:
		lins += 1
		if lins >= lin-2:
			break

		buf += side + "  "
		lent = 0
		for j in i:
			lent += len(j[0])
			if lent <= col-6:
				buf += colored(j[0], color=j[1], on_color=j[2])
			else:
				lent -= len(j[0])

		buf += " "*(col-6-lent) + "  "
		buf += side + "\n"

	if lin - lins > 0:
		for i in range(lin - 2 - lins):
			buf += side + (col-2)*" " + side + "\n"

	buf += bl + (col-2)*top + br
	clear()
	sys.stdout.write(buf)
	sys.stdout.flush()

ram = psutil.virtual_memory()
info = [
	[("CPU USAGE: ", headcol, None), (f"{psutil.cpu_percent(interval=0.4)} %", bodycol, None)],
	[("RAM USAGE: ", headcol, None), (f"{ram.percent} %", bodycol, None)],
	[("           ", headcol, None), (f"({(ram.used / (1024 ** 3)) : .1f} /{(ram.total / (1024 ** 3)) : .1f} GB )", bodycol, None)]
]

printvtb()
while True:
	oldcol = col
	oldlin = lin

	size = shutil.get_terminal_size()
	col = size.columns
	lin = size.lines

	oldinfo = copy.deepcopy(info)
	ram = psutil.virtual_memory()
	info = [
		[("CPU USAGE: ", "blue", None), (f"{psutil.cpu_percent(interval=0.4)} %", "white", None)],
		[("RAM USAGE: ", "blue", None), (f"{ram.percent} %", "white", None)],
		[("           ", "blue", None), (f"({(ram.used / (1024 ** 3)) : .1f} /{(ram.total / (1024 ** 3)) : .1f} GB )", "white", None)]
	]

	clearvtb()
	for i, j in zip_longest(logo.logo, info, fillvalue=[(" "*logo.padding, "white", None)]):
		newline()

		for k in i:
			buffer(k[0], k[1], k[2])

		for k in j:
			buffer(k[0], k[1], k[2])

	if oldcol != col or oldlin != lin or info != oldinfo:
		printvtb()

