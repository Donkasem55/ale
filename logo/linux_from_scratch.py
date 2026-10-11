padding = 16
space = ("  ", "white", None)
space2 = ("    ", "white", None)

color = "yellow"
color_empty = "white"

logo_col = ("yellow", "black", "white")

logo = [
	[(r"  ▐█▌            ", logo_col[0], None), space],
	[(r"  ▐█▌   ", logo_col[0], None), (r"         ", logo_col[1], None), space],
	[(r"  ▐█▌   ", logo_col[0], None), (r"▐████████", logo_col[1], None), space],
	[(r"  ▐█▌   ", logo_col[0], None), (r"▐█▌      ", logo_col[1], None), space],
	[(r"  ▐█████", logo_col[0], None), (r"▐████", logo_col[1], f"on_{logo_col[0]}"), space2, space],
	[(r"        ", logo_col[2], None), (r"▐█▌", logo_col[1], None), (r"      ", logo_col[2], None), space],
	[(r"     ▐██", logo_col[2], None), (r"▐█▌", logo_col[1], f"on_{logo_col[2]}"), (r"███   ", logo_col[2], None), space],
	[(r"     ▐█▌", logo_col[2], None), (r"▐█▌", logo_col[1], None), (r"      ", logo_col[2], None), space],
	[(r"     ▐██████▌    ", logo_col[2], None), space],
	[(r"          ▐█▌    ", logo_col[2], None), space],
	[(r"  ▐█████████▌    ", logo_col[2], None), space],
	[(r"                 ", logo_col[2], None), space],
]

