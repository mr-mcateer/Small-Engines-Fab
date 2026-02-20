#!/usr/bin/env python3
"""Generate clean labeled technical diagrams for quiz review presentation."""

from PIL import Image, ImageDraw, ImageFont
import os

IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
os.makedirs(IMG_DIR, exist_ok=True)

W, H = 1200, 800
BG = (255, 255, 255)
CHARCOAL = (51, 51, 51)
BLUE = (0, 122, 255)
LIGHT_GRAY = (200, 200, 200)
LIGHT_BLUE = (232, 240, 254)

def get_font(size=24):
    for name in ['/System/Library/Fonts/Helvetica.ttc',
                 '/System/Library/Fonts/HelveticaNeue.ttc',
                 '/Library/Fonts/Arial.ttf']:
        try:
            return ImageFont.truetype(name, size)
        except (IOError, OSError):
            continue
    return ImageFont.load_default()

def get_bold_font(size=24):
    for name in ['/System/Library/Fonts/Helvetica.ttc']:
        try:
            return ImageFont.truetype(name, size, index=1)
        except (IOError, OSError):
            continue
    return get_font(size)

def draw_text(d, xy, text, fill=CHARCOAL, font=None, anchor='lt'):
    """Draw text handling multiline by splitting into separate lines."""
    if font is None:
        font = get_font(18)
    x, y = xy
    lines = text.split('\n')
    if len(lines) == 1:
        d.text(xy, text, fill=fill, font=font, anchor=anchor)
    else:
        # For multiline, calculate starting position based on anchor
        line_h = font.size + 4 if hasattr(font, 'size') else 20
        try:
            bbox = d.textbbox((0, 0), 'Ay', font=font)
            line_h = bbox[3] - bbox[1] + 4
        except:
            pass
        total_h = line_h * len(lines)
        # Adjust y for vertical anchor
        if 'm' in anchor:
            y = y - total_h // 2
        elif 'b' in anchor:
            y = y - total_h
        for i, line in enumerate(lines):
            line_anchor = anchor[0] + 't'  # keep horizontal, force top
            d.text((x, y + i * line_h), line, fill=fill, font=font, anchor=line_anchor)



def draw_engine_full():
    """Full engine overview diagram."""
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    f = get_font(20)
    fb = get_bold_font(28)
    fs = get_font(16)

    draw_text(d, (W//2, 30), "Predator 212 — Major Components", fill=CHARCOAL, font=fb, anchor='mt')

    # Engine body (simplified cross-section)
    # Crankcase
    d.rounded_rectangle([300, 400, 900, 700], radius=15, outline=CHARCOAL, width=3)
    draw_text(d, (600, 550), "CRANKCASE", fill=CHARCOAL, font=f, anchor='mm')
    d.text((600, 580), "(crankshaft, camshaft, con rod)", fill=LIGHT_GRAY[:1]*3, font=fs, anchor='mm')

    # Cylinder
    d.rectangle([450, 180, 750, 400], outline=CHARCOAL, width=3)
    draw_text(d, (600, 290), "CYLINDER", fill=CHARCOAL, font=f, anchor='mm')
    d.text((600, 320), "(piston moves here)", fill=(150,150,150), font=fs, anchor='mm')

    # Cylinder head
    d.rounded_rectangle([430, 100, 770, 180], radius=8, outline=BLUE, width=3, fill=LIGHT_BLUE)
    draw_text(d, (600, 140), "CYLINDER HEAD", fill=BLUE, font=f, anchor='mm')

    # Valve cover
    d.rounded_rectangle([450, 60, 750, 100], radius=5, outline=CHARCOAL, width=2)
    draw_text(d, (600, 80), "Valve Cover", fill=CHARCOAL, font=fs, anchor='mm')

    # Labels with lines — external components
    # Shroud (top)
    d.text((600, 15), "SHROUD (covers top, directs cooling air)", fill=BLUE, font=fs, anchor='mt')

    # Air filter (left)
    d.rounded_rectangle([50, 200, 250, 300], radius=10, outline=CHARCOAL, width=2)
    draw_text(d, (150, 250), "Air Filter", fill=CHARCOAL, font=f, anchor='mm')
    d.line([250, 250, 310, 250], fill=CHARCOAL, width=1)

    # Carburetor
    d.rounded_rectangle([310, 220, 450, 320], radius=5, outline=CHARCOAL, width=2)
    draw_text(d, (380, 270), "Carb", fill=CHARCOAL, font=f, anchor='mm')
    d.line([380, 320, 380, 400], fill=CHARCOAL, width=1)

    # Muffler (right)
    d.rounded_rectangle([800, 200, 1050, 320], radius=15, outline=CHARCOAL, width=2)
    draw_text(d, (925, 260), "Muffler", fill=CHARCOAL, font=f, anchor='mm')
    d.line([750, 300, 800, 300], fill=CHARCOAL, width=1)

    # Spark plug
    d.ellipse([760, 120, 790, 160], outline=BLUE, width=2)
    draw_text(d, (820, 140), "Spark Plug", fill=BLUE, font=fs, anchor='lm')

    # Recoil starter (top left)
    d.rounded_rectangle([50, 50, 250, 130], radius=10, outline=CHARCOAL, width=2)
    draw_text(d, (150, 90), "Recoil Starter", fill=CHARCOAL, font=f, anchor='mm')

    # Flywheel
    d.ellipse([100, 400, 280, 580], outline=CHARCOAL, width=2)
    draw_text(d, (190, 490), "Flywheel", fill=CHARCOAL, font=f, anchor='mm')

    # PTO side
    d.line([900, 550, 1050, 550], fill=CHARCOAL, width=3)
    draw_text(d, (1080, 550), "PTO\n(output shaft)", fill=BLUE, font=fs, anchor='lm')

    # Fuel tank
    d.rounded_rectangle([950, 400, 1150, 530], radius=10, outline=CHARCOAL, width=2)
    draw_text(d, (1050, 465), "Fuel Tank", fill=CHARCOAL, font=f, anchor='mm')

    # Governor
    draw_text(d, (450, 650), "Governor", fill=CHARCOAL, font=fs, anchor='mm')
    draw_text(d, (750, 650), "Oil Slinger", fill=CHARCOAL, font=fs, anchor='mm')

    img.save(os.path.join(IMG_DIR, 'engine_full.png'))
    print("  [+] engine_full.png")


def draw_four_stroke():
    """Four-stroke cycle diagram — 4 panels."""
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    f = get_font(18)
    fb = get_bold_font(24)
    fs = get_font(14)

    draw_text(d, (W//2, 20), "The Four-Stroke Cycle", fill=CHARCOAL, font=fb, anchor='mt')
    draw_text(d, (W//2, 50), "Suck · Squeeze · Bang · Blow", fill=BLUE, font=f, anchor='mt')

    strokes = [
        ("1. INTAKE", "(Suck)", "Piston moves DOWN\nIntake valve OPEN\nAir-fuel drawn in", "↓"),
        ("2. COMPRESSION", "(Squeeze)", "Piston moves UP\nBoth valves CLOSED\nMixture compressed", "↑"),
        ("3. POWER", "(Bang)", "Spark fires!\nPiston pushed DOWN\nBoth valves closed", "↓ ⚡"),
        ("4. EXHAUST", "(Blow)", "Piston moves UP\nExhaust valve OPEN\nBurnt gases pushed out", "↑"),
    ]

    panel_w = 260
    gap = 25
    start_x = (W - (4 * panel_w + 3 * gap)) // 2

    for i, (title, nickname, desc, arrow) in enumerate(strokes):
        x = start_x + i * (panel_w + gap)
        y = 100

        # Panel background
        d.rounded_rectangle([x, y, x + panel_w, y + 600], radius=12, outline=LIGHT_GRAY, width=2, fill=(250, 250, 252))

        # Title
        draw_text(d, (x + panel_w//2, y + 25), title, fill=BLUE, font=fb, anchor='mt')
        d.text((x + panel_w//2, y + 55), nickname, fill=(150, 150, 150), font=f, anchor='mt')

        # Cylinder visualization
        cy_x = x + 50
        cy_y = y + 100
        cy_w = panel_w - 100
        cy_h = 250

        # Cylinder walls
        d.rectangle([cy_x, cy_y, cy_x + cy_w, cy_y + cy_h], outline=CHARCOAL, width=2)

        # Piston position
        if arrow.startswith("↓"):
            piston_y = cy_y + cy_h - 60  # bottom
        else:
            piston_y = cy_y + 30  # top

        # Piston
        d.rectangle([cy_x + 5, piston_y, cy_x + cy_w - 5, piston_y + 40], fill=(180, 180, 180), outline=CHARCOAL, width=2)
        draw_text(d, (cy_x + cy_w//2, piston_y + 20), "PISTON", fill=CHARCOAL, font=get_font(11), anchor='mm')

        # Valves at top
        # Intake valve (left)
        iv_color = (0, 180, 0) if i == 0 else (150, 150, 150)  # green if open
        d.rectangle([cy_x + 15, cy_y - 5, cy_x + 45, cy_y + 10], fill=iv_color, outline=CHARCOAL, width=1)
        draw_text(d, (cy_x + 30, cy_y - 15), "IN", fill=iv_color, font=get_font(10), anchor='mm')

        # Exhaust valve (right)
        ev_color = (0, 180, 0) if i == 3 else (150, 150, 150)
        d.rectangle([cy_x + cy_w - 45, cy_y - 5, cy_x + cy_w - 15, cy_y + 10], fill=ev_color, outline=CHARCOAL, width=1)
        draw_text(d, (cy_x + cy_w - 30, cy_y - 15), "EX", fill=ev_color, font=get_font(10), anchor='mm')

        # Spark plug (center top) — highlighted on power stroke
        sp_color = (255, 200, 0) if i == 2 else (150, 150, 150)
        d.ellipse([cy_x + cy_w//2 - 6, cy_y - 8, cy_x + cy_w//2 + 6, cy_y + 8], fill=sp_color, outline=CHARCOAL, width=1)

        # Arrow showing piston direction
        arrow_x = cy_x + cy_w + 20
        if arrow.startswith("↓"):
            d.line([arrow_x, cy_y + 50, arrow_x, cy_y + cy_h - 30], fill=BLUE, width=3)
            d.polygon([(arrow_x - 8, cy_y + cy_h - 40), (arrow_x + 8, cy_y + cy_h - 40), (arrow_x, cy_y + cy_h - 20)], fill=BLUE)
        else:
            d.line([arrow_x, cy_y + cy_h - 50, arrow_x, cy_y + 30], fill=BLUE, width=3)
            d.polygon([(arrow_x - 8, cy_y + 40), (arrow_x + 8, cy_y + 40), (arrow_x, cy_y + 20)], fill=BLUE)

        # Description text
        lines = desc.split('\n')
        for j, line in enumerate(lines):
            draw_text(d, (x + panel_w//2, y + 420 + j * 28), line, fill=CHARCOAL, font=f, anchor='mt')

    img.save(os.path.join(IMG_DIR, 'four_stroke_cycle.png'))
    print("  [+] four_stroke_cycle.png")


def draw_valvetrain():
    """Valvetrain diagram showing rocker arms, springs, valves, pushrods."""
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    f = get_font(18)
    fb = get_bold_font(24)
    fs = get_font(14)

    draw_text(d, (W//2, 20), "OHV Valvetrain — How Valves Are Controlled", fill=CHARCOAL, font=fb, anchor='mt')

    # Cylinder head area
    d.rounded_rectangle([200, 100, 1000, 350], radius=10, outline=BLUE, width=2, fill=LIGHT_BLUE)
    draw_text(d, (600, 115), "CYLINDER HEAD", fill=BLUE, font=f, anchor='mt')

    # Valve cover
    d.rounded_rectangle([250, 65, 950, 100], radius=5, outline=CHARCOAL, width=2, fill=(230, 230, 230))
    draw_text(d, (600, 82), "VALVE COVER", fill=CHARCOAL, font=fs, anchor='mm')

    # Intake valve (left side)
    # Rocker arm
    d.line([350, 160, 500, 160], fill=CHARCOAL, width=4)
    d.ellipse([415, 150, 435, 170], fill=(200, 200, 200), outline=CHARCOAL, width=2)  # pivot
    draw_text(d, (425, 140), "Rocker Arm", fill=CHARCOAL, font=fs, anchor='mb')

    # Valve spring
    for y in range(200, 310, 15):
        d.line([470, y, 500, y + 8], fill=(100, 100, 100), width=2)
        d.line([500, y + 8, 470, y + 15], fill=(100, 100, 100), width=2)
    draw_text(d, (530, 255), "Valve Spring", fill=CHARCOAL, font=fs, anchor='lm')

    # Valve stem
    d.rectangle([480, 160, 490, 340], fill=(150, 150, 150), outline=CHARCOAL, width=1)
    d.text((440, 345), "INTAKE VALVE", fill=(0, 150, 0), font=f, anchor='mt')

    # Pushrod (from rocker arm down to crankcase)
    d.line([350, 160, 350, 600], fill=CHARCOAL, width=3)
    draw_text(d, (310, 400), "Pushrod", fill=CHARCOAL, font=fs, anchor='rm')

    # Exhaust valve (right side)
    d.line([700, 160, 850, 160], fill=CHARCOAL, width=4)
    d.ellipse([765, 150, 785, 170], fill=(200, 200, 200), outline=CHARCOAL, width=2)
    draw_text(d, (775, 140), "Rocker Arm", fill=CHARCOAL, font=fs, anchor='mb')

    for y in range(200, 310, 15):
        d.line([710, y, 740, y + 8], fill=(100, 100, 100), width=2)
        d.line([740, y + 8, 710, y + 15], fill=(100, 100, 100), width=2)

    d.rectangle([720, 160, 730, 340], fill=(150, 150, 150), outline=CHARCOAL, width=1)
    d.text((760, 345), "EXHAUST VALVE", fill=(200, 0, 0), font=f, anchor='mt')

    d.line([850, 160, 850, 600], fill=CHARCOAL, width=3)
    draw_text(d, (890, 400), "Pushrod", fill=CHARCOAL, font=fs, anchor='lm')

    # Crankcase area
    d.rounded_rectangle([200, 500, 1000, 750], radius=10, outline=CHARCOAL, width=2)
    draw_text(d, (600, 520), "CRANKCASE (ENGINE BLOCK)", fill=CHARCOAL, font=fs, anchor='mt')

    # Tappets
    d.rectangle([340, 560, 360, 600], fill=(180, 180, 180), outline=CHARCOAL, width=1)
    draw_text(d, (350, 555), "Tappet", fill=CHARCOAL, font=get_font(12), anchor='mb')
    d.rectangle([840, 560, 860, 600], fill=(180, 180, 180), outline=CHARCOAL, width=1)
    draw_text(d, (850, 555), "Tappet", fill=CHARCOAL, font=get_font(12), anchor='mb')

    # Camshaft
    d.line([250, 650, 950, 650], fill=CHARCOAL, width=4)
    draw_text(d, (600, 670), "CAMSHAFT", fill=BLUE, font=fb, anchor='mt')

    # Cam lobes
    d.ellipse([330, 620, 380, 660], fill=(200, 200, 200), outline=CHARCOAL, width=2)
    draw_text(d, (355, 610), "Lobe", fill=CHARCOAL, font=get_font(12), anchor='mb')
    d.ellipse([830, 620, 880, 660], fill=(200, 200, 200), outline=CHARCOAL, width=2)
    draw_text(d, (855, 610), "Lobe", fill=CHARCOAL, font=get_font(12), anchor='mb')

    # Timing gear label
    d.text((600, 720), "Timing gears connect camshaft to crankshaft (timing marks align them)", fill=(150,150,150), font=fs, anchor='mt')

    # Motion arrows
    draw_text(d, (100, 400), "Motion chain:\nCam lobe →\nTappet →\nPushrod →\nRocker arm →\nValve opens →\nSpring closes", fill=BLUE, font=fs, anchor='lm')

    img.save(os.path.join(IMG_DIR, 'valvetrain.png'))
    print("  [+] valvetrain.png")


def draw_cylinder_piston():
    """Cylinder and piston assembly diagram."""
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    f = get_font(18)
    fb = get_bold_font(24)
    fs = get_font(14)

    draw_text(d, (W//2, 20), "Cylinder & Piston Assembly", fill=CHARCOAL, font=fb, anchor='mt')

    # Cylinder wall
    d.rectangle([400, 100, 800, 550], outline=CHARCOAL, width=3)
    draw_text(d, (600, 80), "CYLINDER (Bore)", fill=CHARCOAL, font=f, anchor='mb')

    # Cooling fins on outside
    for y in range(120, 540, 30):
        d.line([370, y, 400, y], fill=LIGHT_GRAY, width=2)
        d.line([800, y, 830, y], fill=LIGHT_GRAY, width=2)
    draw_text(d, (850, 300), "Cooling\nFins", fill=(150, 150, 150), font=fs, anchor='lm')

    # Head gasket
    d.rectangle([390, 95, 810, 110], fill=LIGHT_BLUE, outline=BLUE, width=2)
    draw_text(d, (900, 102), "HEAD GASKET", fill=BLUE, font=f, anchor='lm')

    # Bore condition label
    draw_text(d, (350, 300), "Bore\nCondition\n(wall surface)", fill=BLUE, font=fs, anchor='rm')
    d.line([360, 300, 400, 300], fill=BLUE, width=1)

    # Piston
    d.rectangle([415, 280, 785, 360], fill=(200, 200, 200), outline=CHARCOAL, width=3)
    draw_text(d, (600, 320), "PISTON", fill=CHARCOAL, font=fb, anchor='mm')

    # Piston rings (3 rings)
    ring_labels = ["Compression Ring 1", "Compression Ring 2", "Oil Ring"]
    for i, (ry, label) in enumerate(zip([285, 305, 340], ring_labels)):
        d.line([415, ry, 785, ry], fill=CHARCOAL, width=2)
        side = 'rm' if i % 2 == 0 else 'lm'
        x_pos = 395 if side == 'rm' else 805
        draw_text(d, (x_pos, ry), label, fill=CHARCOAL, font=get_font(11), anchor=side)

    d.text((600, 375), "Piston rings seal the gap", fill=(150, 150, 150), font=fs, anchor='mt')

    # Wrist pin
    d.ellipse([575, 385, 625, 405], fill=(180, 180, 180), outline=CHARCOAL, width=2)
    draw_text(d, (650, 395), "Wrist Pin (Piston Pin)", fill=CHARCOAL, font=f, anchor='lm')

    # Connecting rod
    d.polygon([(580, 405), (620, 405), (640, 620), (560, 620)], fill=(190, 190, 190), outline=CHARCOAL, width=2)
    draw_text(d, (500, 520), "CONNECTING\nROD", fill=CHARCOAL, font=f, anchor='rm')

    # Crankshaft journal
    d.ellipse([540, 610, 660, 700], fill=(180, 180, 180), outline=CHARCOAL, width=3)
    draw_text(d, (600, 655), "CRANKSHAFT\nJOURNAL", fill=CHARCOAL, font=fs, anchor='mm')

    # Crankshaft
    d.line([300, 655, 540, 655], fill=CHARCOAL, width=4)
    d.line([660, 655, 900, 655], fill=CHARCOAL, width=4)
    draw_text(d, (600, 720), "CRANKSHAFT", fill=BLUE, font=fb, anchor='mt')

    # Motion labels
    draw_text(d, (200, 200), "Combustion pushes\npiston DOWN", fill=BLUE, font=f, anchor='lm')
    d.line([200, 250, 200, 350], fill=BLUE, width=2)
    d.polygon([(192, 340), (208, 340), (200, 360)], fill=BLUE)

    draw_text(d, (200, 600), "Con rod converts to\nROTATION", fill=BLUE, font=f, anchor='lm')

    img.save(os.path.join(IMG_DIR, 'cylinder_piston.png'))
    print("  [+] cylinder_piston.png")


def draw_flywheel():
    """Flywheel and ignition system diagram."""
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    f = get_font(18)
    fb = get_bold_font(24)
    fs = get_font(14)

    draw_text(d, (W//2, 20), "Flywheel & Ignition System", fill=CHARCOAL, font=fb, anchor='mt')

    # Flywheel (large circle)
    cx, cy = 500, 400
    r = 200
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(230, 230, 230), outline=CHARCOAL, width=3)
    d.ellipse([cx-30, cy-30, cx+30, cy+30], fill=(180, 180, 180), outline=CHARCOAL, width=2)
    draw_text(d, (cx, cy), "FLYWHEEL", fill=CHARCOAL, font=fb, anchor='mm')

    # Magnets on flywheel
    d.rounded_rectangle([cx-r+10, cy-30, cx-r+50, cy+30], radius=5, fill=(100, 100, 200), outline=CHARCOAL, width=2)
    draw_text(d, (cx-r+30, cy), "N", fill=BG, font=f, anchor='mm')
    d.rounded_rectangle([cx+r-50, cy-30, cx+r-10, cy+30], radius=5, fill=(200, 100, 100), outline=CHARCOAL, width=2)
    draw_text(d, (cx+r-30, cy), "S", fill=BG, font=f, anchor='mm')

    draw_text(d, (cx, cy+70), "Permanent magnets\nembedded in rim", fill=(150, 150, 150), font=fs, anchor='mt')

    # Ignition coil (outside flywheel)
    d.rounded_rectangle([750, 350, 950, 450], radius=8, outline=CHARCOAL, width=2)
    draw_text(d, (850, 400), "Ignition Coil", fill=CHARCOAL, font=f, anchor='mm')
    d.line([700, 400, 750, 400], fill=CHARCOAL, width=2)

    # Spark plug wire
    d.line([950, 400, 1050, 300], fill=CHARCOAL, width=2)
    d.ellipse([1040, 280, 1080, 320], fill=(255, 220, 0), outline=CHARCOAL, width=2)
    draw_text(d, (1060, 270), "Spark Plug", fill=CHARCOAL, font=fs, anchor='mb')

    # Crankshaft through center
    d.line([cx-30, cy, 100, cy], fill=CHARCOAL, width=4)
    draw_text(d, (80, cy), "Crankshaft", fill=CHARCOAL, font=fs, anchor='rm')

    # Functions box
    box_y = 550
    d.rounded_rectangle([100, box_y, 1100, box_y+180], radius=10, outline=BLUE, width=2, fill=LIGHT_BLUE)
    draw_text(d, (600, box_y+15), "Flywheel Functions:", fill=BLUE, font=fb, anchor='mt')
    draw_text(d, (150, box_y+55), "1. Stores rotational energy — keeps crankshaft spinning through non-power strokes", fill=CHARCOAL, font=f, anchor='lt')
    draw_text(d, (150, box_y+85), "2. Generates magnetic field — magnets spin past ignition coil to create spark", fill=CHARCOAL, font=f, anchor='lt')
    draw_text(d, (150, box_y+115), "3. Provides mounting for recoil starter cup", fill=CHARCOAL, font=f, anchor='lt')
    draw_text(d, (150, box_y+145), "4. Fan blades on flywheel push air through shroud for cooling", fill=CHARCOAL, font=f, anchor='lt')

    # Rotation arrow
    d.arc([cx-r-20, cy-r-20, cx+r+20, cy+r+20], start=200, end=340, fill=BLUE, width=3)

    img.save(os.path.join(IMG_DIR, 'flywheel.png'))
    print("  [+] flywheel.png")


def draw_recoil_starter():
    """External components overview."""
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    f = get_font(18)
    fb = get_bold_font(24)
    fs = get_font(14)

    draw_text(d, (W//2, 20), "External Components — What You See Outside", fill=CHARCOAL, font=fb, anchor='mt')

    components = [
        ("Recoil Starter", "Pull cord mechanism\nSpins flywheel to crank engine", 150, 150),
        ("Shroud", "Covers top of engine\nDirects cooling air over fins", 500, 150),
        ("Fuel Tank", "Stores gasoline\nGravity-feeds to carburetor", 850, 150),
        ("Air Filter", "Filters incoming air\nProtects carburetor from debris", 150, 450),
        ("Spark Plug", "Ignites air-fuel mixture\nEnd of ignition circuit", 500, 450),
        ("Muffler", "Reduces exhaust noise\nDirects gases away from operator", 850, 450),
    ]

    for name, desc, x, y in components:
        d.rounded_rectangle([x-120, y, x+120, y+180], radius=12, outline=CHARCOAL, width=2, fill=(250, 250, 252))
        draw_text(d, (x, y+20), name, fill=BLUE, font=f, anchor='mt')
        d.line([x-80, y+45, x+80, y+45], fill=LIGHT_GRAY, width=1)
        lines = desc.split('\n')
        for i, line in enumerate(lines):
            draw_text(d, (x, y+65+i*25), line, fill=CHARCOAL, font=fs, anchor='mt')

    img.save(os.path.join(IMG_DIR, 'recoil_starter.png'))
    print("  [+] recoil_starter.png")


def draw_air_filter_carb():
    """Air filter and carburetor diagram."""
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    f = get_font(18)
    fb = get_bold_font(24)
    fs = get_font(14)

    draw_text(d, (W//2, 20), "Fuel & Air System — Carburetor", fill=CHARCOAL, font=fb, anchor='mt')

    # Air path visualization
    draw_text(d, (W//2, 60), "Air-Fuel Path: Outside Air → Air Filter → Carburetor → Intake Valve → Cylinder", fill=BLUE, font=f, anchor='mt')

    # Air filter
    d.rounded_rectangle([80, 250, 280, 500], radius=15, outline=CHARCOAL, width=3)
    draw_text(d, (180, 280), "AIR FILTER", fill=BLUE, font=fb, anchor='mt')
    draw_text(d, (180, 380), "Traps dirt\nand debris\nbefore air\nenters carb", fill=CHARCOAL, font=fs, anchor='mm')

    # Arrow
    d.line([280, 375, 380, 375], fill=BLUE, width=3)
    d.polygon([(370, 365), (370, 385), (390, 375)], fill=BLUE)
    draw_text(d, (335, 355), "Clean air", fill=BLUE, font=fs, anchor='mb')

    # Carburetor
    d.rounded_rectangle([390, 200, 700, 550], radius=10, outline=CHARCOAL, width=3)
    draw_text(d, (545, 220), "CARBURETOR", fill=BLUE, font=fb, anchor='mt')

    # Venturi inside carb
    draw_text(d, (545, 270), "Venturi Effect:", fill=CHARCOAL, font=f, anchor='mt')
    draw_text(d, (545, 300), "Air speeds up through\nnarrow passage →", fill=CHARCOAL, font=fs, anchor='mt')
    draw_text(d, (545, 350), "Low pressure pulls\nfuel up through jets →", fill=CHARCOAL, font=fs, anchor='mt')
    draw_text(d, (545, 410), "Creates fine mist of\nair + fuel (~14.7:1)", fill=CHARCOAL, font=fs, anchor='mt')

    # Fuel line from below
    d.line([545, 550, 545, 650], fill=CHARCOAL, width=2)
    draw_text(d, (545, 670), "Fuel from tank", fill=CHARCOAL, font=fs, anchor='mt')

    # Arrow to intake
    d.line([700, 375, 800, 375], fill=BLUE, width=3)
    d.polygon([(790, 365), (790, 385), (810, 375)], fill=BLUE)
    draw_text(d, (755, 355), "Air-fuel\nmix", fill=BLUE, font=fs, anchor='mb')

    # Intake valve
    d.rounded_rectangle([820, 300, 1020, 450], radius=10, outline=CHARCOAL, width=2)
    draw_text(d, (920, 330), "INTAKE", fill=CHARCOAL, font=f, anchor='mt')
    draw_text(d, (920, 360), "VALVE", fill=CHARCOAL, font=f, anchor='mt')
    d.text((920, 400), "→ Cylinder", fill=(150, 150, 150), font=fs, anchor='mt')

    # Throttle note
    d.rounded_rectangle([390, 600, 700, 700], radius=8, outline=BLUE, width=1, fill=LIGHT_BLUE)
    draw_text(d, (545, 620), "Throttle plate controls how much", fill=CHARCOAL, font=fs, anchor='mt')
    draw_text(d, (545, 645), "air-fuel mixture enters the engine", fill=CHARCOAL, font=fs, anchor='mt')
    draw_text(d, (545, 670), "Governor adjusts throttle automatically", fill=BLUE, font=fs, anchor='mt')

    img.save(os.path.join(IMG_DIR, 'air_filter_carb.png'))
    print("  [+] air_filter_carb.png")


def draw_spark_plug():
    """Spark plug diagram."""
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    f = get_font(18)
    fb = get_bold_font(24)
    fs = get_font(14)

    draw_text(d, (W//2, 20), "Spark Plug — The Ignition Source", fill=CHARCOAL, font=fb, anchor='mt')

    # Large spark plug drawing
    cx = 450

    # Terminal
    d.rectangle([cx-15, 100, cx+15, 160], fill=(180, 180, 180), outline=CHARCOAL, width=2)
    draw_text(d, (cx+80, 130), "Terminal ←\n(wire connects here)", fill=CHARCOAL, font=fs, anchor='lm')

    # Insulator (ceramic)
    d.rectangle([cx-25, 160, cx+25, 350], fill=(240, 240, 240), outline=CHARCOAL, width=2)
    draw_text(d, (cx+80, 255), "Ceramic Insulator ←\n(insulates electrode)", fill=CHARCOAL, font=fs, anchor='lm')

    # Hex nut
    d.polygon([(cx-35, 350), (cx+35, 350), (cx+35, 390), (cx-35, 390)], fill=(200, 200, 200), outline=CHARCOAL, width=2)
    draw_text(d, (cx+80, 370), "Hex Nut ←\n(wrench fits here)", fill=CHARCOAL, font=fs, anchor='lm')

    # Thread
    d.rectangle([cx-20, 390, cx+20, 500], fill=(190, 190, 190), outline=CHARCOAL, width=2)
    for y in range(395, 500, 10):
        d.line([cx-20, y, cx+20, y], fill=(160, 160, 160), width=1)
    draw_text(d, (cx+80, 445), "Threads ←\n(screws into head)", fill=CHARCOAL, font=fs, anchor='lm')

    # Ground electrode
    d.rectangle([cx-5, 500, cx+5, 550], fill=(180, 180, 180), outline=CHARCOAL, width=2)
    d.line([cx, 550, cx+25, 550], fill=CHARCOAL, width=3)
    d.line([cx+25, 550, cx+25, 530], fill=CHARCOAL, width=3)

    # Spark gap
    draw_text(d, (cx+80, 540), "SPARK GAP ←\n(spark jumps here!)", fill=BLUE, font=f, anchor='lm')

    # Spark visual
    d.line([cx, 520, cx+10, 510], fill=(255, 200, 0), width=3)
    d.line([cx+10, 510, cx+5, 525], fill=(255, 200, 0), width=3)
    d.line([cx+5, 525, cx+20, 515], fill=(255, 200, 0), width=3)

    # Ignition circuit box
    d.rounded_rectangle([100, 620, 1100, 750], radius=10, outline=BLUE, width=2, fill=LIGHT_BLUE)
    draw_text(d, (600, 640), "Ignition Circuit:", fill=BLUE, font=fb, anchor='mt')
    draw_text(d, (600, 680), "Flywheel magnets spin past ignition coil → High voltage pulse →", fill=CHARCOAL, font=f, anchor='mt')
    draw_text(d, (600, 710), "Spark plug wire → Spark jumps the gap → Ignites air-fuel mixture", fill=CHARCOAL, font=f, anchor='mt')

    img.save(os.path.join(IMG_DIR, 'spark_plug.png'))
    print("  [+] spark_plug.png")


def draw_ohv_crosssection():
    """OHV engine cross-section showing the complete system."""
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    f = get_font(18)
    fb = get_bold_font(24)
    fs = get_font(14)

    d.text((W//2, 15), "Predator 212 — Single-Cylinder, Four-Stroke, Air-Cooled, OHV", fill=BLUE, font=fb, anchor='mt')

    # Engine classification box
    classifications = [
        ("Single-Cylinder", "One cylinder, one piston"),
        ("Four-Stroke", "Intake → Compression → Power → Exhaust"),
        ("Air-Cooled", "Fins + shroud (no radiator/coolant)"),
        ("OHV", "Valves in head, camshaft in block"),
    ]

    for i, (term, desc) in enumerate(classifications):
        x = 100 + i * 280
        y = 60
        d.rounded_rectangle([x, y, x+260, y+90], radius=8, outline=BLUE, width=2, fill=LIGHT_BLUE)
        draw_text(d, (x+130, y+20), term, fill=BLUE, font=f, anchor='mt')
        draw_text(d, (x+130, y+55), desc, fill=CHARCOAL, font=fs, anchor='mt')

    # OHV diagram — simplified cross-section
    # Engine block
    d.rectangle([350, 200, 850, 700], outline=CHARCOAL, width=2)

    # Cylinder head
    d.rectangle([400, 200, 800, 300], outline=BLUE, width=2, fill=LIGHT_BLUE)
    draw_text(d, (600, 210), "CYLINDER HEAD", fill=BLUE, font=f, anchor='mt')
    draw_text(d, (600, 240), "Valves located HERE (Overhead)", fill=BLUE, font=fs, anchor='mt')
    d.text((600, 260), "Rocker arms + springs + valve stems", fill=(100, 100, 100), font=fs, anchor='mt')

    # Cylinder bore
    d.rectangle([450, 300, 750, 520], outline=CHARCOAL, width=2)
    draw_text(d, (600, 400), "CYLINDER", fill=CHARCOAL, font=f, anchor='mm')

    # Piston
    d.rectangle([460, 380, 740, 430], fill=(200, 200, 200), outline=CHARCOAL, width=2)
    draw_text(d, (600, 405), "Piston + Rings", fill=CHARCOAL, font=fs, anchor='mm')

    # Connecting rod
    d.polygon([(590, 430), (610, 430), (625, 560), (575, 560)], fill=(190, 190, 190), outline=CHARCOAL, width=2)
    draw_text(d, (520, 500), "Con Rod", fill=CHARCOAL, font=fs, anchor='rm')

    # Crankcase area
    draw_text(d, (600, 530), "CRANKCASE", fill=CHARCOAL, font=f, anchor='mt')

    # Crankshaft
    d.ellipse([560, 555, 640, 610], fill=(180, 180, 180), outline=CHARCOAL, width=2)
    d.line([350, 582, 560, 582], fill=CHARCOAL, width=4)
    d.line([640, 582, 850, 582], fill=CHARCOAL, width=4)
    draw_text(d, (600, 620), "Crankshaft", fill=CHARCOAL, font=fs, anchor='mt')

    # Camshaft (in block, below crankshaft)
    d.line([400, 660, 800, 660], fill=CHARCOAL, width=3)
    d.ellipse([440, 645, 480, 675], fill=(200,200,200), outline=CHARCOAL, width=1)
    d.ellipse([700, 645, 740, 675], fill=(200,200,200), outline=CHARCOAL, width=1)
    d.text((600, 680), "Camshaft (in block, connected by timing gears)", fill=CHARCOAL, font=fs, anchor='mt')

    # Pushrods
    d.line([460, 660, 430, 280], fill=(150, 0, 0), width=2)
    d.line([740, 660, 770, 280], fill=(150, 0, 0), width=2)
    d.text((380, 480), "Pushrods", fill=(150, 0, 0), font=fs, anchor='rm')

    # OHV explanation
    d.rounded_rectangle([870, 350, 1180, 550], radius=8, outline=BLUE, width=2, fill=LIGHT_BLUE)
    draw_text(d, (1025, 370), "OHV Design:", fill=BLUE, font=f, anchor='mt')
    draw_text(d, (1025, 400), "Cam in block →", fill=CHARCOAL, font=fs, anchor='mt')
    draw_text(d, (1025, 420), "Tappet →", fill=CHARCOAL, font=fs, anchor='mt')
    draw_text(d, (1025, 440), "Pushrod (goes up) →", fill=CHARCOAL, font=fs, anchor='mt')
    draw_text(d, (1025, 460), "Rocker arm →", fill=CHARCOAL, font=fs, anchor='mt')
    draw_text(d, (1025, 480), "Valve opens", fill=CHARCOAL, font=fs, anchor='mt')
    draw_text(d, (1025, 510), "Spring closes valve", fill=CHARCOAL, font=fs, anchor='mt')

    # Oil sump
    d.text((600, 700), "Oil Sump (oil slinger splashes oil onto components)", fill=(150,150,150), font=fs, anchor='mt')

    img.save(os.path.join(IMG_DIR, 'ohv_crosssection.png'))
    print("  [+] ohv_crosssection.png")


if __name__ == '__main__':
    print("Generating presentation images...")
    draw_engine_full()
    draw_recoil_starter()
    draw_air_filter_carb()
    draw_spark_plug()
    draw_valvetrain()
    draw_cylinder_piston()
    draw_flywheel()
    draw_four_stroke()
    draw_ohv_crosssection()
    print(f"\nAll images saved to {IMG_DIR}")
