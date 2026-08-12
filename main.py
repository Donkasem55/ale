import shutil, os, psutil, copy, sys, subprocess, platform, math
from termcolor import colored
from itertools import zip_longest
from pynput import keyboard

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

def printvtb(end="^C  Exit     ^M  Main Menu     ^D  Disk Menu"):
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

		if col >= 124:
			enu = (col - 7) // 29
		else:
			enu = (col - 7) // 8

		for i, coreusage in enumerate(coreuse):
			if col >= 124:
				info2[-1] += [
					("| ", bodycol, None),
					("\u2589"*int(coreusage//5), headcol, None), 
					("\u2589"*int(20-(coreusage//5)), bodycol, None), 
					(f" {" " if coreusage < 10 else ""}{coreusage}% ", bodycol, None)
				]
				if i%enu == enu-1:
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
				if i%enu == enu-1:
					info2[-1] += [
						("|", bodycol, None)
					]
					info2.append([("", "white", None)])
					info2.append([("", "white", None)])

		return info, info2


	elif mode == "disk":
		info = [
			 [("Connected Drives: ", headcol, None)],
			 [("", "white", None)]
		]
		info2 = [
			 [("", "white", None)],
			 [("", "white", None)],
			 [("-"*(16+16+57+4), "white", None)],
			 [("|" + "Partition".center(16) + "|" + "Mountpoint".center(16) + "|" + "Capacity".center(57) + "|", "white", None)]
		]
		parts = psutil.disk_partitions(all=False)
		for i in parts:
			try:
				info.append([(f"{i.device} ", headcol, None), (f"{i.mountpoint}", bodycol, None), (f" ({i.fstype})", headcol, None)])
			except:
				pass

		for j in range(len(parts)):
			try:
				i = parts[j]
				usage = psutil.disk_usage(i.mountpoint)
				info2.append([
			 			("|", "white", None),
						(f"{str(i.device).center(16)}", headcol, None),
			 			("|", "white", None),
						(f"{str(i.mountpoint).center(16)}", headcol, None),
			 			("| ", "white", None),
						("\u2589"*int(usage.percent//5), headcol, None), 
						("\u2589"*int(20-(usage.percent//5)), bodycol, None), 
						(f"{usage.used / (1024**3):.2f} / {usage.total / (1024**3):.2f} GB ({" " if usage.percent < 10 else ""}{usage.percent}%)".rjust(35), headcol, None),
			 			(" |", "white", None)
					])

			except:
				pass

		info2.append([("-"*(16+16+57+4), "white", None)])

		return info, info2


mode = "main"
info, info2 = resetinfo(mode)

def tomain():
	global mode
	mode = "main"

def todisk():
	global mode
	mode = "disk"

h = keyboard.GlobalHotKeys({
		'<ctrl>+m': tomain,
		'<ctrl>+d': todisk
	})
h.start()

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
		info, info2 = resetinfo(mode)

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
