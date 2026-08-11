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
if osname == "nt":
	import ctypes
	import ctypes.wintypes
	stdouthandle = ctypes.windll.kernel32.GetStdHandle(-11)
	mode = ctypes.wintypes.DWORD()
	ctypes.windll.kernel32.GetConsoleMode(stdouthandle, sys.modules["ctypes"].byref(mode))
	ctypes.windll.kernel32.SetConsoleMode(stdouthandle, mode.value | 0x0004)

def clear():
	sys.stdout.write("\x1b[2J\x1b[3J\x1b[1;1H")
	sys.stdout.flush()

osname2 = platform.system()
if osname2 == "Linux":
	distroname = platform.freedesktop_os_release()
	logo = __import__(f"logo.{str(distroname).lower().replace(" ", "_")}", fromlist=[None])
else:
	logo = __import__(f"logo.{str(osname2).lower()}", fromlist=[None])

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

def printvtb(end="^C  Exit     "):
	global vtb, col, lin, tl, top, tr, bl, br, side
	buf = "1b[2J\x1b[3J\x1b[1;1H"
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

	buf += side + "  " + colored(end, color="green", on_color=None) + " "*(col-4-len(end)) + side + "\n"
	buf += bl + (col-2)*top + br
	sys.stdout.write(buf)
	sys.stdout.flush()

coreuse = psutil.cpu_percent(interval=0.4)

def resetinfo(mode = "main"):
	global cpuuse, col
	if mode == "main":
		coreuse = psutil.cpu_percent(interval=None, percpu=True)
		cpuuse = psutil.cpu_percent(interval=0.4)
		battery = psutil.sensors_battery()
		ram = psutil.virtual_memory()
		threadcount = psutil.cpu_count(logical=True)
		info = [
			[("CPU: ", headcol, None), (f"{platform.processor()}", bodycol, None)],
			[("Physical Cores: ", headcol, None), (f"{psutil.cpu_count(logical=False)}", bodycol, None)],
			[("Logical Cores: ", headcol, None), (f"{threadcount}", bodycol, None)],
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

		info2 = [
			[("", "white", None)],
			[("Logical Processor Usages: ", headcol, None)],
			[("", "white", None)],
			[("", "white", None)]
		]

		for i, coreusage in enumerate(coreuse):
			if col >= 124:
				info2[-1] += [
					("| ", bodycol, None),
					("\u2589"*int(coreusage//5), headcol, None), 
					("\u2589"*int(20-(coreusage//5)), bodycol, None), 
					(f" {" " if coreusage < 10 else ""}{coreusage}% ", bodycol, None)
				]
				if i%4 == 3:
					info2[-1] += [
						("|", bodycol, None)
					]
					info2.append([("", "white", None)])
					info2.append([("", "white", None)])

			else:
				info2[-1] += [
					("| ", bodycol, None),
					(f"{" " if coreusage < 10 else ""}{coreusage}% ", bodycol, None)
				]
				if i%9 == 8:
					info2[-1] += [
						("|", bodycol, None)
					]
					info2.append([("", "white", None)])
					info2.append([("", "white", None)])


		return info, info2

info, info2 = resetinfo()

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
		info, info2 = resetinfo()

		clearvtb()
		for i, j in zip_longest(logo.logo, info, fillvalue=[(" "*logo.padding, "white", None)]):
			newline()

			for k in i:
				buffer(k[0], k[1], k[2])

			for k in j:
				buffer(k[0], k[1], k[2])

		for i in info2:
			newline()
			for j in i:
				buffer(j[0], j[1], j[2])

		if oldcol != col or oldlin != lin or info != oldinfo:
			printvtb()

except KeyboardInterrupt:
	clear()
	sys.exit(0)
