import shutil, os, psutil, copy, sys, subprocess, platform, math
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

def printvtb(end="^C  Exit     ^M  Main Menu     ^G  GPU Monitor "):
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
		for i in range(lin - 3 - lins):
			buf += side + (col-2)*" " + side + "\n"

	buf += side + "  " + colored(end, "green", None) + " "*(col-4-len(end)) + side + "\n"
	buf += bl + (col-2)*top + br
	clear()
	sys.stdout.write(buf)
	sys.stdout.flush()

ram = psutil.virtual_memory()

def resetinfo(mode = "main"):
	if mode == "main":
		cpuuse = psutil.cpu_percent(interval=0.4)
		battery = psutil.sensors_battery()
		info = [
			[("CPU: ", headcol, None), (f"{platform.processor()}", bodycol, None)],
			[("Physical Cores: ", headcol, None), (f"{psutil.cpu_count(logical=False)}", bodycol, None)],
			[("Logical Cores: ", headcol, None), (f"{psutil.cpu_count(logical=True)}", bodycol, None)],
			[("Total CPU Usage: ", headcol, None)],
			[("\u2589"*int(cpuuse//5), headcol, None), 
			 ("\u2589"*int(20-(cpuuse//5)), bodycol, None), 
			 (f"  {" " if cpuuse < 10 else ""}{cpuuse}%", bodycol, None)],

			[("", headcol, None)],

			[("Total Memory Usage: ", headcol, None), (f"{(ram.used / (1024 ** 2)) : .1f} MiB", bodycol, None)],
			[("Total Available Memory: ", headcol, None), (f"{(ram.total / (1024 ** 2)) : .1f} MiB", bodycol, None)],
			[("\u2589"*int(ram.percent//5), headcol, None), 
			 ("\u2589"*int(20-(ram.percent//5)), bodycol, None), 
			 (f"  {" " if ram.percent < 10 else ""}{ram.percent}%", bodycol, None)],

			[("", headcol, None)],

			[("Battery Percentage: ", headcol, None)],
			[("\u2589"*int(battery.percent//5), headcol, None), 
			 ("\u2589"*int(20-(battery.percent//5)), bodycol, None), 
			 (f"  {" " if battery.percent < 10 else ""}{battery.percent}%", bodycol, None)],
		]
		return info

info = resetinfo()

info2 = []

printvtb()
try:
	while True:
		oldcol = col
		oldlin = lin

		size = shutil.get_terminal_size()
		col = size.columns
		lin = size.lines

		oldinfo = copy.deepcopy(info)
		ram = psutil.virtual_memory()
		info = resetinfo()

		clearvtb()
		for i, j in zip_longest(logo.logo, info, fillvalue=[(" "*logo.padding, "white", None)]):
			newline()

			for k in i:
				buffer(k[0], k[1], k[2])

			for k in j:
				buffer(k[0], k[1], k[2])

		if oldcol != col or oldlin != lin or info != oldinfo:
			printvtb()

except KeyboardInterrupt:
	clear()
	sys.exit(0)
