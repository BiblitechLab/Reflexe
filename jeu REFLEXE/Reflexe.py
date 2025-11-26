# Python 3.9+ / pygame 2.x
# -*- coding: utf-8 -*-


import pygame as pg
import random, math, sys, time
import os, json, hashlib, base64

pg.init()
pg.mixer.init()

# chemin du dossier ou se trouve le script
base_path = os.path.dirname(os.path.abspath(__file__))
music_path = os.path.join(base_path, "az.mp3")
TITLE_FONT_PATH = os.path.join(base_path, "playful_boxes.otf")
TITLE_FONT_FALLBACK = os.path.join(base_path, "playful_boxes.ttf")
BEST_SCORE_PATH = os.path.join(base_path, "best_score.txt")
SFX_NEAR_PATH = os.path.join(base_path, "sfx_near.wav")
SFX_NEAR_FALLBACK = os.path.join(base_path, "sfx_near.mp3")
SFX_DEATH_PATH = os.path.join(base_path, "sfx_death.wav")
SFX_DEATH_FALLBACK = os.path.join(base_path, "sfx_death.mp3")
GITHUB_URL = "https://github.com/BiblitechLab"
MUSIC_DIR = os.path.join(base_path, "musi")
MUSIC_END_EVENT = pg.USEREVENT + 1

try:
    if os.path.exists(music_path):
        pg.mixer.music.load(music_path)
        pg.mixer.music.set_volume(0.6)
        pg.mixer.music.play(-1, fade_ms=1500)
    else:
        print("Musique introuvable (az.mp3) - son coupe.")
except Exception as e:
    print("Erreur chargement musique:", e)


# ---------- Config ----------
W, H = 1280, 720
FPS = 60

BG = (10, 10, 10)
BG_TOP = (12, 16, 26)
BG_BOT = (14, 10, 24)
FG = (240, 240, 240)
UI_DIM = (130, 130, 130)
SPIKE_COL = (220, 50, 50)
TP_COL = (70, 150, 255)
LINE_COL = (130, 150, 180)
LASER_COL = (120, 210, 255)
ACCENT = (120, 200, 255)
ACCENT_ALT = (255, 160, 190)
BTN_BG = (24, 26, 36)
BTN_BG_HOVER = (40, 44, 60)
BTN_BORDER = (230, 230, 230)
BTN_SHADOW = (0, 0, 0, 70)
THEME_LIGHT = False
BG_TOP_LIGHT = (220, 224, 236)
BG_BOT_LIGHT = (200, 206, 222)
BG_LIGHT = (235, 238, 245)
BG_THEMES = [
    {
        "name": "Neo Blue",
        "top": (12, 16, 26),
        "bot": (14, 10, 24),
        "halos": [
            (0.28, 0.32, 260, (90, 180, 255, 36)),
            (0.72, 0.64, 320, (255, 120, 160, 32)),
        ],
    },
    {
        "name": "Sunset Pulse",
        "top": (48, 18, 30),
        "bot": (18, 8, 24),
        "halos": [
            (0.25, 0.30, 240, (255, 110, 90, 32)),
            (0.70, 0.66, 320, (255, 210, 120, 28)),
        ],
    },
    {
        "name": "Cyber Lime",
        "top": (18, 28, 22),
        "bot": (6, 12, 14),
        "halos": [
            (0.30, 0.34, 260, (140, 255, 170, 28)),
            (0.76, 0.60, 300, (90, 200, 255, 28)),
        ],
    },
]

PLAYER_R = 10
GAP = PLAYER_R * 2
LINE_THICK = 1
MARGIN_TOP = 60
MARGIN_BOT = 60

PLAYER_X = int(W * 0.28)
BG_BASE_SURF = pg.Surface((W, H))
BG_GLOW_SURF = pg.Surface((W, H), pg.SRCALPHA)

# Difficulte (progressive)
SCROLL_BASE = 470
SCROLL_GROWTH = 0.020
SPAWN_BASE = 290
SPAWN_MIN = 220
DENSITY_GROWTH = 0.004
DIFF_CAP = 3.0
RELIEF_DIST = 2200
RELIEF_TIME = 2.4
RELIEF_SCROLL_FAC = 0.66
RELIEF_SPAWN_FAC = 1.35
RELIEF_MAX = 3
RELIEF_SCORE_STEP = 500
AI_STEPS = 14
AI_CELL_X_MIN = 60
AI_CELL_X_MAX = 110
AI_CELL_SCROLL_FAC = 0.18
AI_COLL_COST = 1200
AI_NEAR_COST = 110
AI_DIST_COST = 0.10
AI_LANE_CHANGE_COST = 6
AI_CLOSE_WEIGHT = 1.35
AI_SAFE_LANE_BONUS = 8
AI_DEAD_END_PENALTY = 280
AI_DASH_LOOK_STEPS = 4
AI_EMERGENCY_THRESHOLD = 360

# --- Comfort Mode ---
COMFORT_MODE = True
FOCUS_BAND = GAP * 1.6
LINE_ALPHA_NEAR = 180
LINE_ALPHA_FAR  = 40
LINE_THICK_PLAY = 1

# Scanlines du menu
MENU_SCAN_SPACING = 6
MENU_SCAN_ALPHA = 10   # un peu plus doux

# Triangles
TRI_W = PLAYER_R * 2
TRI_H = PLAYER_R * 2

MAX_LINES_PER_COLUMN = 3
NEAR_T = 6
NEAR_DECAY_S = 1.0
NEAR_STEP = 0.2
NEAR_CAP = 3.0

# Lasers / Clapets
LASER_LEN = 110
LASER_DEPTH = PLAYER_R
LASER_TELE = 0.5
LASER_ACTIVE = 0.35
LASER_COOLDOWN = 0.9

CLAP_ACTIVE = 0.7
CLAP_REST = 1.2
CLAP_DEPTH = GAP

# Drones / Mines
DRONE_R = 8
MINE_R = 10
MINE_REVEAL_DIST = 300
MINE_ARM_TIME = 0.30

# Lame pivot
BLADE_ARM = 26
BLADE_SPEED = 2.2  # rad/s

# Lasers diag
DIAG_LEN = 70
DIAG_THICK = 6
DIAG_ACTIVE = 0.22
DIAG_COOL = 1.2

# Turrets / projectiles
TURRET_R = 10
TURRET_FIRE_MIN = 1.0
TURRET_FIRE_MAX = 2.2
PROJECTILE_SPEED = 420
PROJECTILE_R = 6
PROJECTILE_WARN = 0.3

# Pulse walls
PULSE_THICK = 18
PULSE_TELE = 0.5
PULSE_ACTIVE = 0.35
PULSE_COOL = 1.0

# TP
TP_R = 24
TP_CD = 0.35

DEFAULT_SEED = 1337

# ---------- Levels & Editor ----------
DIFF_LABELS = ["Facile", "Moyen", "Dur", "Extra", "Mega", "Insane", "Extreme", "AUTO"]
SIZE_LABELS = ["Petit", "Moyen", "Grand", "XL", "XXL"]
LEVEL_DB_PATH = os.path.join(os.path.dirname(base_path), ".projectx_data", "levels_db.json")
ACCOUNT_PATH = os.path.join(os.path.dirname(base_path), ".projectx_data", "account.json")

# ---------- SKINS ----------
SKINS = [
    {"name":"Classique", "req":0, "col":(240,240,240), "style":"classic"},
    {"name":"Neon Bleu", "req":200, "col":(90,180,255), "style":"glow"},
    {"name":"Crimson", "req":400, "col":(255,80,110), "style":"classic"},
    {"name":"Void Ring", "req":600, "col":(190,160,255), "style":"ring"},
    {"name":"Spectre", "req":900, "col":(160,255,200), "style":"ghost"},
    {"name":"Orbite", "req":1200, "col":(255,220,120), "style":"crown"},
]

PATCH_NOTES = [
    {
        "ver": "1.5.0",
        "date": "2025-11-26",
        "items": [
            "Editeur refondu : panneaux lisibles, halo couleur par type, grille precision et apercu en direct",
            "Placement precis : mode precision (F), nudges A/D/W/S, ENTER pour poser, palette couleur pour les piques",
            "Import express : Ctrl+V dans le menu Niveaux pour coller un code base64, export toujours en un clic",
            "Aide enrichie pour l'editeur et la creation de niveaux custom"
        ],
    },
    {
        "ver": "1.4.6",
        "date": "2024-07-09",
        "items": [
            "Arriere-plans multiples (Neo Blue / Sunset Pulse / Cyber Lime) choisis aleatoirement",
            "Playlist auto depuis /app/musi ou /app (mp3/ogg/wav/flac) avec enchainement des pistes",
            "Ecran Aide recentre sur commandes/modes/options (recap patchs retire)",
            "Code coop supprime: experience solo propre et stable"
        ],
    },
    {
        "ver": "1.4.5",
        "date": "2024-07-08",
        "items": [
            "Cosmetiques & QoL: unlocks de skins via succes, skins prestige, particules custom et trails dynamiques",
            "Options avancees en jeu: FPS lock, theme clair/sombre, toggle vignette/scanlines, confort affine",
            "Modes bonus actifs: Zen (pas de mort), Chaos (vitesse random + obstacles modules), Mirror, IA Only",
            "Ecran Aide plein ecran avec recap commandes/modes/options"
        ],
    },
    {
        "ver": "1.4.4",
        "date": "2024-07-07",
        "items": [
            "Parametres plein ecran avec bouton Retour et grille options (FPS/theme/scanlines/vignette/trails/modes)",
            "Modes bonus actifs: Zen, Chaos, Mirror, IA Only + toggles mirroir/IA/chaos/zen",
            "Options avancees: FPS lock, theme clair/sombre, vignette/scanlines switchables, trails dynamiques",
            "Cosmetiques a venir: skins prestige, particules custom et unlocks par succes"
        ],
    },
    {
        "ver": "1.4.3",
        "date": "2024-07-07",
        "items": [
            "Panneau Parametres aligne aux boutons (fps/theme/vignette/scanlines/trails/modes)",
            "Nouveaux modes bonus: Zen, Chaos, Mirror, IA Only",
            "Options avancées: FPS lock, theme clair/sombre, toggle vignette/scanlines",
            "Cosmetiques: trails dynamiques et prochaines skins prestige"
        ],
    },
    {
        "ver": "1.4.2",
        "date": "2024-07-06",
        "items": [
            "Refonte boutons menu: nouvelles icones (engrenage, carnet, etoile) et croix alignee",
            "Layout menu resserre au centre avec marge sup/inf plus aeree",
            "Hover plus lisible (glow) et texte/padding ajustes pour les labels longs",
            "Notes plein ecran: clipping/scroll et sections release/snapshot/roadmap"
        ],
    },
    {
        "ver": "1.4.1",
        "date": "2024-07-05",
        "items": [
            "Boutons du menu recalés (plus de débordement bas)",
            "Notes plein écran: clipping corrigé et barre de scroll alignée"
        ],
    },
    {
        "ver": "1.4.0",
        "date": "2024-07-01",
        "items": [
            "Nouveau mode Notes plein écran avec défilement",
            "Bouton Paramètres pour régler musique/SFX",
            "Interface menu retouchée (navigation claire)"
        ],
    },
    {
        "ver": "1.3.0",
        "date": "2024-06-25",
        "items": [
            "IA plus forte : grille dynamique, anticipation lasers/clapets, dash d'urgence",
            "Nouveau panneau Notes dans le menu principal",
            "Support direct pour playful_boxes.otf"
        ],
    },
    {
        "ver": "1.2.0",
        "date": "2024-06-10",
        "items": [
            "Ajout des tourelles et projectiles avertis",
            "Equilibrage des murs pulsés et des lasers diagonaux",
            "Visuels du menu retouchés (scanlines plus doux)"
        ],
    },
    {
        "ver": "1.1.0",
        "date": "2024-05-20",
        "items": [
            "Mode confort activé par défaut",
            "Nouvelles particules de traînée pour le joueur",
            "Optimisations des collisions et du spawn"
        ],
    },
]

RELEASE_NOTES = [
    {
        "ver": "Release 1.4",
        "date": "2024-07-01",
        "items": [
            "Build stable recentree sur la lisibilite du menu",
            "Reequilibrage global apres les nouvelles tourelles",
        ],
    },
    {
        "ver": "Release 1.3",
        "date": "2024-06-25",
        "items": [
            "Stabilisation IA + seeds fixes pour le mode classement",
            "Compatibilite police playful_boxes sur plus de machines",
        ],
    },
]

SNAPSHOT_NOTES = [
    {
        "ver": "Snapshot r4207",
        "date": "2024-07-04",
        "items": [
            "Test du dash IA plus agressif",
            "Ajustement de la densite drone/mine",
            "Premieres couleurs pour le mode plein ecran Notes",
        ],
    },
    {
        "ver": "Snapshot r4188",
        "date": "2024-07-02",
        "items": [
            "Laser diagonaux: telegraphies plus lisibles",
            "Scanlines menus alloupees pour moins de flicker",
        ],
    },
]

UPCOMING_NOTES = [
    {
        "ver": "Multijoueur",
        "date": "Bientot",
        "items": [
            "Matchmaking rapide et lobby amis en preparation",
            "Sync des seeds et obstacles partagee pour runs duo",
            "Alpha fermee tres bientot: reste connecte !",
        ],
    },
]

# ---------- Utils ----------
_FONT_CACHE = {}
def get_font(size, bold=True):
    key = (size, bold)
    f = _FONT_CACHE.get(key)
    if f is None:
        f = pg.font.SysFont("consolas", size, bold=bold)
        _FONT_CACHE[key] = f
    return f

def ob_x(o):
    if hasattr(o, "xc"): return o.xc
    if hasattr(o, "x"): return o.x
    if hasattr(o, "inp"): return o.inp[0]
    return 0.0

def draw_text(surf, txt, size, x, y, align="topleft", col=FG, bold=True, shadow=False, stroke=False):
    font = get_font(size, bold=bold)
    img = font.render(txt, True, col)
    r = img.get_rect()
    setattr(r, align, (x, y))
    if shadow:
        sh = font.render(txt, True, (0,0,0))
        sr = sh.get_rect(); setattr(sr, align, (x+2, y+2))
        surf.blit(sh, sr)
    if stroke:
        for ox,oy in ((-1,0),(1,0),(0,-1),(0,1)):
            st = font.render(txt, True, (0,0,0))
            sr = st.get_rect(); setattr(sr, align, (x+ox, y+oy)); surf.blit(st, sr)
    surf.blit(img, r)

def circle_mask(r):
    s = pg.Surface((r*2, r*2), pg.SRCALPHA)
    pg.draw.circle(s, FG, (r, r), r)
    return s, pg.mask.from_surface(s)

def triangle_surface(w, h, orientation="up"):
    surf = pg.Surface((w, h), pg.SRCALPHA)
    if orientation == "up":
        pts = [(0, h), (w, h), (w//2, 0)]
    else:
        pts = [(0, 0), (w, 0), (w//2, h)]
    pg.draw.polygon(surf, FG, pts)
    return surf, pg.mask.from_surface(surf)

def rect_from_cxcywh(cx, cy, w, h):
    return pg.Rect(int(cx - w/2), int(cy - h/2), int(w), int(h))

def clamp(v, a, b):
    return a if v < a else b if v > b else v

def circle_rect_collide(cx, cy, cr, rect: pg.Rect):
    px = clamp(cx, rect.left, rect.right)
    py = clamp(cy, rect.top, rect.bottom)
    dx, dy = cx - px, cy - py
    return (dx*dx + dy*dy) <= cr*cr

def compute_lines():
    usable = H - MARGIN_TOP - MARGIN_BOT
    n_gaps = max(1, usable // GAP)
    total_gap = n_gaps * GAP
    top = (H - total_gap) // 2
    ys = [top + i*GAP for i in range(int(n_gaps)+1)]
    return ys

# Comfort-mode lines drawing
def draw_lines_comfort(surf, lines, player_y, color=FG, thick=2):
    if not COMFORT_MODE:
        for y in lines:
            pg.draw.line(surf, color, (0, int(y)), (W, int(y)), thick)
        return
    layer = pg.Surface((W, surf.get_height()), pg.SRCALPHA)
    for y in lines:
        d = abs(y - player_y)
        t = min(1.0, d / FOCUS_BAND)
        alpha = int(LINE_ALPHA_NEAR * (1.0 - t) + LINE_ALPHA_FAR * t)
        pg.draw.line(layer, (*color, alpha), (0, int(y)), (W, int(y)), thick)
    surf.blit(layer, (0, 0))

# ---------- Level storage ----------
class LevelManager:
    def __init__(self, path=LEVEL_DB_PATH):
        self.path = path
        self.data = {"levels": [], "profiles": {}}
        self._ensure_dir()
        self._load()

    def _ensure_dir(self):
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
        except Exception:
            pass

    def _load(self):
        try:
            if os.path.exists(self.path):
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
        except Exception:
            self.data = {"levels": [], "profiles": {}}

    def _save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=True, indent=2)
        except Exception:
            pass

    def _hash(self, pseudo, pwd):
        h = hashlib.sha1()
        h.update(f"{pseudo}:{pwd}".encode("utf-8"))
        return h.hexdigest()

    def _new_id(self):
        return f"lvl_{int(time.time()*1000)}_{random.randint(1000,9999)}"

    def upsert_level(self, level_dict):
        if not level_dict.get("id"):
            level_dict["id"] = self._new_id()
            self.data["levels"].append(level_dict)
        else:
            found = False
            for i, lv in enumerate(self.data["levels"]):
                if lv.get("id") == level_dict["id"]:
                    self.data["levels"][i] = level_dict
                    found = True
                    break
            if not found:
                self.data["levels"].append(level_dict)
        pseudo = level_dict.get("author", {}).get("pseudo", "")
        pwd_hash = level_dict.get("author", {}).get("password_hash", "")
        if pseudo and pwd_hash:
            self.data["profiles"][pseudo] = pwd_hash
        self._save()
        return level_dict["id"]

    def list_levels(self):
        return list(self.data.get("levels", []))

    def get_level(self, lvl_id):
        for lv in self.data.get("levels", []):
            if lv.get("id") == lvl_id:
                return lv
        return None

    def vote_difficulty(self, lvl_id, label):
        lv = self.get_level(lvl_id)
        if not lv or label not in DIFF_LABELS:
            return False
        votes = lv.setdefault("difficulty_votes", {k:0 for k in DIFF_LABELS})
        votes[label] = votes.get(label, 0) + 1
        lv["updated_at"] = time.time()
        self._save()
        return True

    def current_difficulty(self, lv):
        votes = lv.get("difficulty_votes", {})
        if not votes:
            return "AUTO"
        best = max(DIFF_LABELS, key=lambda k: votes.get(k, 0))
        if votes.get(best, 0) == 0:
            return "AUTO"
        return best

    def export_code(self, lvl):
        try:
            payload = json.dumps(lvl)
            b = base64.urlsafe_b64encode(payload.encode("utf-8")).decode("ascii")
            return b
        except Exception:
            return ""

    def import_code(self, code):
        try:
            raw = base64.urlsafe_b64decode(code.encode("ascii")).decode("utf-8")
            lv = json.loads(raw)
            return lv
        except Exception:
            return None

    def build_author(self, pseudo, pwd):
        return {"pseudo": pseudo, "password_hash": self._hash(pseudo, pwd or "")}

# ---------- Account ----------
class AccountManager:
    def __init__(self, path=ACCOUNT_PATH):
        self.path = path
        self._ensure_dir()
        self.profile = self._load()

    def _ensure_dir(self):
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
        except Exception:
            pass

    def _load(self):
        try:
            if os.path.exists(self.path):
                with open(self.path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        # default pseudo random pour eviter les doublons evidents
        pseudo = f"Player{random.randint(1000,9999)}"
        return {"pseudo": pseudo, "password_hash": ""}

    def save(self, profile):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(profile, f, ensure_ascii=True, indent=2)
            self.profile = profile
        except Exception:
            pass

    def delete(self):
        try:
            if os.path.exists(self.path):
                os.remove(self.path)
        except Exception:
            pass
        # reset to a fresh random profile
        self.profile = {"pseudo": f"Player{random.randint(1000,9999)}", "password_hash": ""}

# ---------- Level Editor (menu) ----------
class LevelEditor:
    TYPES = [
        ("tri", "Triangles"),
        ("laser", "Laser"),
        ("clap", "Clapet"),
        ("drone", "Drone"),
        ("mine", "Mine"),
        ("turret", "Tourelle"),
        ("tp", "Portail"),
        ("pulse", "Mur pulse"),
    ]

    def __init__(self, game):
        self.game = game
        self.lines = compute_lines()
        self.corr = [(self.lines[i] + self.lines[i+1]) / 2 for i in range(len(self.lines)-1)]
        self.reset()

    def reset(self):
        self.objects = []
        self.selected_idx = 0
        self.level_length = 2800
        self.cam_x = 0
        self.size_idx = 0
        self.level_name = "Mon niveau"
        self.author = ""
        self.password = ""
        self.info = "Clic sur la grille pour poser des obstacles"
        self.active_field = None
        self.last_saved_id = None
        self.pending_tp = None
        self.status = ""
        self.precision_mode = False
        self.preview_x = 0
        self.preview_lane = 0
        self.preview_y = 0.0
        self.current_level_loaded = None
        self.login_mode = False
        self.login_field = "pseudo"
        self.login_pseudo = ""
        self.login_pwd = ""
        self.require_login = True

    def _canvas_rect(self):
        pad = 80
        w = W - pad*2
        h = int(H*0.55)
        x = pad
        y = int(H*0.26)
        return pg.Rect(x, y, w, h)

    def _screen_to_dist(self, mx):
        rect = self._canvas_rect()
        return clamp(self.cam_x + (mx - rect.left), 0, self.level_length)

    def _closest_lane(self, my):
        best = 0; best_d = 1e9
        for i, y in enumerate(self.lines):
            d = abs(my - y)
            if d < best_d:
                best_d = d; best = i
        return best

    def _obj_color(self, typ):
        return {
            "tri": (255, 140, 120),
            "laser": (120, 210, 255),
            "clap": (220, 220, 120),
            "drone": (140, 255, 160),
            "mine": (220, 120, 200),
            "turret": (255, 210, 120),
            "tp": (70, 150, 255),
            "pulse": (200, 120, 255),
        }.get(typ, FG)

    def _place_at(self, dist, lane):
        typ = self.TYPES[self.selected_idx][0]
        line_count = len(self.lines)
        ori = "down" if lane == 0 else "up" if lane == line_count-1 else "up"
        if typ == "tp":
            if self.pending_tp is None:
                self.pending_tp = {"x": dist, "lane": lane}
                self.status = "Portail entree place - clic/Entrer pour sortie"
                return
            entry = self.pending_tp
            obj = {"type": "tp", "x": entry["x"], "lane": entry["lane"], "dest_lane": lane, "dx": 260}
            self.objects.append(obj)
            self.pending_tp = None
            self.status = "Portail cree"
            return
        obj = {"type": typ, "x": dist, "lane": lane, "ori": ori, "custom_y": self.preview_y}
        self.objects.append(obj)
        self.status = f"{typ} ajoute (lane {lane}, x {int(dist)})"

    def _add_object(self, pos):
        rect = self._canvas_rect()
        if not rect.collidepoint(pos):
            return
        dist = self._screen_to_dist(pos[0])
        lane = self._closest_lane(pos[1])
        self.preview_x = dist
        self.preview_lane = lane
        self._place_at(dist, lane)

    def _place_preview(self):
        self._place_at(self.preview_x, self.preview_lane)

    def _handle_text_input(self, e):
        if self.active_field is None:
            return
        target = {"name": "level_name", "author": "author", "password": "password"}.get(self.active_field)
        if target is None:
            return
        cur = getattr(self, target)
        if e.key == pg.K_BACKSPACE:
            setattr(self, target, cur[:-1])
        elif e.key == pg.K_RETURN:
            self.active_field = None
        else:
            ch = e.unicode
            if ch and 32 <= ord(ch) <= 126 and len(cur) < 24:
                setattr(self, target, cur + ch)

    def _update_preview(self):
        mx, my = pg.mouse.get_pos()
        rect = self._canvas_rect()
        if rect.collidepoint((mx, my)):
            self.preview_x = self._screen_to_dist(mx)
            self.preview_lane = self._closest_lane(my)
            self.preview_y = my
        else:
            self.preview_x = clamp(self.preview_x, self.cam_x, self.cam_x + rect.width)
            self.preview_lane = clamp(self.preview_lane, 0, len(self.lines)-1)
            self.preview_y = clamp(self.preview_y, rect.top, rect.bottom)

    def _remove_nearest(self, pos):
        if not self.objects:
            return
        rect = self._canvas_rect()
        if not rect.collidepoint(pos):
            return
        distx = self._screen_to_dist(pos[0])
        lane = self._closest_lane(pos[1])
        best_i = None; best_d = 1e9
        for i, obj in enumerate(self.objects):
            dx = abs(obj.get("x", 0) - distx)
            dy = abs(obj.get("custom_y", self.lines[obj.get("lane", 0)]) - pos[1])
            d = dx + dy*0.25 + abs(obj.get("lane", 0) - lane)*5
            if d < best_d:
                best_d = d; best_i = i
        if best_i is not None:
            removed = self.objects.pop(best_i)
            self.status = f"Objet supprime ({removed.get('type','?')})"

    def _build_level_dict(self):
        diff_votes = {k:0 for k in DIFF_LABELS}
        active_pseudo = self.game.user_profile.get("pseudo", "") if self.game.user_profile else ""
        active_pwdhash = self.game.user_profile.get("password_hash", "") if self.game.user_profile else ""
        author = {"pseudo": active_pseudo, "password_hash": active_pwdhash}
        length = max(self.level_length, max([o["x"] for o in self.objects], default=0) + 600)
        return {
            "id": self.last_saved_id,
            "name": self.level_name or "Niveau",
            "author": author,
            "size": SIZE_LABELS[self.size_idx],
            "objects": self.objects,
            "length": length,
            "difficulty_votes": diff_votes,
            "created_at": time.time(),
            "updated_at": time.time(),
        }

    def save_level(self):
        if self.require_login and not (self.game.user_profile and self.game.user_profile.get("pseudo")):
            self.status = "Connexion requise pour sauvegarder"
            return
        lvl = self._build_level_dict()
        lvl_id = self.game.level_manager.upsert_level(lvl)
        self.last_saved_id = lvl_id
        self.status = f"Niveau enregistre ({lvl_id})"

    def playtest(self):
        if self.require_login and not (self.game.user_profile and self.game.user_profile.get("pseudo")):
            self.status = "Connexion requise pour tester"
            return
        lvl = self._build_level_dict()
        self.game.start_custom_level(lvl)

    def load_level(self, lv):
        self.reset()
        self.last_saved_id = lv.get("id")
        self.level_name = lv.get("name", "Niveau")
        self.size_idx = SIZE_LABELS.index(lv.get("size", SIZE_LABELS[0])) if lv.get("size") in SIZE_LABELS else 0
        self.level_length = int(lv.get("length", 2800))
        self.author = lv.get("author", {}).get("pseudo", self.author)
        self.password = ""
        self.objects = lv.get("objects", [])
        if self.objects:
            self.preview_x = self.objects[-1].get("x", 0)
            self.preview_lane = self.objects[-1].get("lane", 0)
            self.preview_y = self.objects[-1].get("custom_y", self.corr[self.preview_lane] if self.preview_lane < len(self.corr) else self.corr[0])
        self.current_level_loaded = lv.get("id")
        self.status = "Edition du niveau charge"

    def handle_event(self, e):
        if e.type == pg.KEYDOWN and self.active_field:
            self._handle_text_input(e); return
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                self.game.state = "menu"
            elif e.key == pg.K_TAB:
                order = ["name", "author", "password"]
                if self.active_field is None:
                    self.active_field = "name"
                else:
                    idx = order.index(self.active_field)
                    self.active_field = order[(idx+1)%len(order)]
            elif e.key == pg.K_n:
                self.active_field = "name"
            elif e.key == pg.K_a:
                self.active_field = "author"
            elif e.key == pg.K_p:
                self.active_field = "password"
            elif e.key == pg.K_t:
                self.size_idx = (self.size_idx + 1) % len(SIZE_LABELS)
            elif e.key == pg.K_s:
                self.save_level()
            elif e.key == pg.K_f:
                self.precision_mode = not self.precision_mode
                self.status = "Precision ON" if self.precision_mode else "Precision OFF"
            elif e.key == pg.K_BACKSPACE:
                if self.objects:
                    self.objects.pop()
                    self.status = "Dernier objet supprime"
            elif e.key == pg.K_DELETE:
                self.objects = []; self.status = "Grille vide"
            elif e.key == pg.K_RETURN:
                if self.precision_mode:
                    self._place_preview()
                else:
                    self.playtest()
            elif e.key in (pg.K_LEFT, pg.K_q) and (not self.precision_mode):
                self.cam_x = clamp(self.cam_x - 180, 0, max(0, self.level_length - self._canvas_rect().width))
            elif e.key in (pg.K_RIGHT, pg.K_d) and (not self.precision_mode):
                self.cam_x = clamp(self.cam_x + 180, 0, max(0, self.level_length - self._canvas_rect().width))
            elif e.key in (pg.K_LEFTBRACKET,):
                self.level_length = max(800, self.level_length - 200)
            elif e.key in (pg.K_RIGHTBRACKET,):
                self.level_length = min(6000, self.level_length + 200)
            elif self.precision_mode and e.key in (pg.K_a, pg.K_d, pg.K_w, pg.K_s):
                step = 10 if e.key in (pg.K_a, pg.K_d) else 1
                if e.key == pg.K_a:
                    self.preview_x = max(0, self.preview_x - step)
                elif e.key == pg.K_d:
                    self.preview_x = min(self.level_length, self.preview_x + step)
                elif e.key == pg.K_w:
                    self.preview_y = max(self._canvas_rect().top, self.preview_y - 4)
                    self.preview_lane = self._closest_lane(self.preview_y)
                elif e.key == pg.K_s:
                    self.preview_y = min(self._canvas_rect().bottom, self.preview_y + 4)
                    self.preview_lane = self._closest_lane(self.preview_y)
            else:
                for i in range(len(self.TYPES)):
                    if e.key == getattr(pg, f"K_{i+1}", None):
                        self.selected_idx = i
                        self.pending_tp = None
                        self.status = f"Type: {self.TYPES[i][1]}"
                        break
        if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
            self._add_object(e.pos)
        elif e.type == pg.MOUSEBUTTONDOWN and e.button == 3:
            self._remove_nearest(e.pos)

    def draw(self, surf):
        t = pg.time.get_ticks()/1000.0
        self._update_preview()
        draw_background(surf, t, theme_idx=1)

        # Overlay halos
        for ox, oy, rad, col in [(W*0.22, H*0.18, 220, (80, 200, 255, 60)), (W*0.78, H*0.24, 200, (255, 160, 210, 50)), (W*0.55, H*0.70, 280, (120, 90, 255, 40))]:
            pg.draw.circle(surf, col, (int(ox), int(oy)), rad)

        panel = make_panel(int(W*0.94), int(H*0.88), alpha=230)
        pr = panel.get_rect(center=(W//2, H//2 + 6))
        surf.blit(panel, pr.topleft)

        header_y = pr.top + 10
        draw_text(surf, "Editeur de niveaux", 46, pr.centerx, header_y, "midtop", shadow=True, stroke=True)

        # Metadata cards (pseudo auto)
        meta_y = header_y + 54
        meta_x = pr.left + 20
        meta_band = pg.Rect(meta_x - 10, meta_y - 6, pr.width * 0.50, 96)
        pg.draw.rect(surf, (10, 14, 24, 230), meta_band, border_radius=10)
        line_h = 22
        user_pseudo = self.game.user_profile.get("pseudo", "") if self.game.user_profile else ""
        meta = [
            f"Nom (N/Tab) : {self.level_name}",
            f"Compte : {user_pseudo or 'non connecte'}",
            f"Taille (T) : {SIZE_LABELS[self.size_idx]}",
            f"Longueur [{int(self.level_length)}]  <[ / ]> pour ajuster",
        ]
        for i, txt in enumerate(meta):
            col = FG if i == 0 else UI_DIM
            draw_text(surf, txt, 18, meta_x, meta_y + i*line_h, "topleft", col=col, bold=(i==0))

        rect = self._canvas_rect()
        rect.y = meta_band.bottom + 16
        pg.draw.rect(surf, (8, 10, 16), rect, border_radius=14)
        pg.draw.rect(surf, BTN_BORDER, rect, width=2, border_radius=14)

        # canvas clip pour la grille/objets
        canvas = pg.Surface((rect.width, rect.height), pg.SRCALPHA)

        # timeline and grid teinte par la couleur du type selectionne
        tint = self._obj_color(self.TYPES[self.selected_idx][0])
        tint_dim = (tint[0]//2 + 20, tint[1]//2 + 20, tint[2]//2 + 20)
        for x in range(0, int(self.level_length)+1, 200):
            # work in local space
            sx = (x - self.cam_x)
            if 0 <= sx <= rect.width:
                pg.draw.line(canvas, (*tint_dim, 140), (int(sx), 8), (int(sx), rect.height-8), 1)
                draw_text(canvas, str(x), 12, int(sx), 8, "midtop", col=(220,220,220), bold=False)
        for y in self.lines:
            ly = int(y - rect.top)
            if 0 <= ly <= rect.height:
                pg.draw.line(canvas, (*tint_dim, 120), (0, ly), (rect.width, ly), 1)

        # objects and preview on clipped canvas
        for obj in self.objects:
            sx = (obj["x"] - self.cam_x)
            if sx < -60 or sx > rect.width+60:
                continue
            ly_abs = obj.get("custom_y")
            if ly_abs is None:
                ly_abs = self.lines[obj["lane"]] if obj["type"] in ("tri","laser") else self.corr[obj["lane"]] if obj["type"] in ("clap","drone","mine","turret","tp","pulse") else self.lines[obj["lane"]]
            ly = ly_abs - rect.top
            col = self._obj_color(obj["type"])
            if obj["type"] == "tri":
                pg.draw.polygon(canvas, col, [(sx-8, ly), (sx+8, ly), (sx, ly - 14 if obj.get("ori","up")=="up" else ly + 14)])
            elif obj["type"] == "laser":
                pg.draw.line(canvas, col, (sx-18, ly), (sx+18, ly), 3)
            elif obj["type"] == "clap":
                pg.draw.rect(canvas, col, (sx-14, ly-10, 28, 20), border_radius=6)
            elif obj["type"] == "drone":
                pg.draw.circle(canvas, col, (int(sx), int(ly)), 8, 2)
            elif obj["type"] == "mine":
                pg.draw.circle(canvas, col, (int(sx), int(ly)), 10, 1)
            elif obj["type"] == "turret":
                pg.draw.rect(canvas, col, (sx-10, ly-10, 20, 20), border_radius=4)
            elif obj["type"] == "tp":
                pg.draw.circle(canvas, TP_COL, (int(sx), int(ly)), 12, 2)
                dest_lane = obj.get("dest_lane", obj["lane"])
                dy = self.corr[dest_lane] - rect.top
                pg.draw.circle(canvas, (90, 180, 255), (int(sx + obj.get("dx", 240)), int(dy)), 10, 1)
                pg.draw.line(canvas, (90,180,255), (int(sx), int(ly)), (int(sx + obj.get("dx", 240)), int(dy)), 1)
            elif obj["type"] == "pulse":
                pg.draw.rect(canvas, col, (sx-10, 12, 20, rect.height-24), 2, border_radius=6)

        # preview ghost
        ghost_x = (self.preview_x - self.cam_x)
        ghost_lane_y = (self.preview_y if self.precision_mode else (self.lines[self.preview_lane] if self.preview_lane < len(self.lines) else self.lines[-1])) - rect.top
        ghost_col = self._obj_color(self.TYPES[self.selected_idx][0])
        if -20 <= ghost_x <= rect.width+20:
            pg.draw.line(canvas, (*ghost_col, 120), (ghost_x, 0), (ghost_x, rect.height), 1)
            pg.draw.line(canvas, (*ghost_col, 120), (0, ghost_lane_y), (rect.width, ghost_lane_y), 1)
            pg.draw.circle(canvas, (*ghost_col, 160), (int(ghost_x), int(ghost_lane_y)), 6, 2)

        # blit clipped canvas
        surf.blit(canvas, rect.topleft)

        # Palette bar (draw after grid, anchored top-right of rect)
        palette_w, palette_h = 320, 110
        palette_rect = pg.Rect(rect.right - palette_w - 10, rect.top - palette_h - 10, palette_w, palette_h)
        palette_rect.y = max(int(pr.top + 60), palette_rect.y)
        pg.draw.rect(surf, (14, 16, 28, 250), palette_rect, border_radius=10)
        pg.draw.rect(surf, BTN_BORDER, palette_rect, 1, border_radius=10)
        draw_text(surf, "Palette (1-8)", 18, palette_rect.left + 10, palette_rect.top + 8, "topleft")
        px = palette_rect.left + 10; py = palette_rect.top + 34
        for i, (typ, label) in enumerate(self.TYPES):
            col = self._obj_color(typ)
            slot = pg.Rect(px + (i%4)*78, py + (i//4)*36, 70, 28)
            active = (i == self.selected_idx)
            pg.draw.rect(surf, (*col, 60), slot, border_radius=6)
            pg.draw.rect(surf, col, slot, 2 if active else 1, border_radius=6)
            draw_text(surf, f"{i+1}:{label}", 14, slot.centerx, slot.centery-2, "midtop", col=FG if active else UI_DIM, bold=active)

        info_y = rect.bottom + 12
        info_band = pg.Rect(pr.left + 8, info_y - 6, pr.width - 16, 46)
        pg.draw.rect(surf, (10, 12, 18, 220), info_band, border_radius=10)
        precision_txt = "Precision ON (A/D/W/S + ENTREE)" if self.precision_mode else "Precision OFF (F)"
        draw_text(surf, f"{precision_txt} | Type actif: {self.TYPES[self.selected_idx][1]} (1-8) | Clic/Entree pour poser | S: sauvegarder | Echap: menu", 16, info_band.left + 10, info_band.top + 6, "topleft", col=UI_DIM, bold=False)
        draw_text(surf, self.status or self.info, 18, info_band.left + 10, info_band.top + 24, "topleft", col=ACCENT, bold=False)
        if self.current_level_loaded:
            draw_text(surf, f"Edition: {self.current_level_loaded}", 14, pr.left + 12, info_y + 44, "topleft", col=UI_DIM, bold=False)

        if self.active_field:
            y_map = {"name": meta_y, "author": meta_y+line_h, "password": meta_y+2*line_h}
            y = y_map.get(self.active_field)
            if y:
                pg.draw.line(surf, ACCENT, (meta_x-2, y+18), (meta_x+240, y+18), 2)


# ---------- UI helpers ----------
def make_panel(w, h, alpha=210):
    s = pg.Surface((w, h), pg.SRCALPHA)
    base_col = (18, 20, 26, alpha)
    top_glow = (60, 80, 120, max(0, alpha - 100))
    pg.draw.rect(s, base_col, (0, 0, w, h), border_radius=14)
    pg.draw.rect(s, top_glow, (0, 0, w, h // 3), border_radius=14)
    pg.draw.rect(s, BTN_BORDER, (0, 0, w, h), width=2, border_radius=14)
    return s

def make_vignette(w, h):
    v = pg.Surface((w, h), pg.SRCALPHA)
    step = 8
    for i in range(0, min(w, h)//2, step):
        a = int(6 + 240 * (i / (min(w, h)//2))**2 * 0.08)
        pg.draw.rect(v, (0, 0, 0, a), (i, i, w - 2*i, h - 2*i), width=step)
    return v

def draw_scanlines(surf, spacing=4, alpha=28, clip_rect=None):
    sl = pg.Surface((surf.get_width(), surf.get_height()), pg.SRCALPHA)
    for y in range(0, surf.get_height(), spacing*2):
        pg.draw.line(sl, (255, 255, 255, alpha), (0, y), (surf.get_width(), y))
    if clip_rect:
        # on "efface" autour de la zone pour ne pas gener la lisibilite
        mask = pg.Surface((surf.get_width(), surf.get_height()), pg.SRCALPHA)
        mask.blit(sl, (0,0))
        pg.draw.rect(mask, (0,0,0,0), clip_rect)
        surf.blit(mask, (0,0))
    else:
        surf.blit(sl, (0, 0))


def draw_background(surf, t, theme_idx=0):
    theme = BG_THEMES[theme_idx % len(BG_THEMES)]
    top_base, bot_base = (BG_TOP_LIGHT, BG_BOT_LIGHT) if THEME_LIGHT else (theme["top"], theme["bot"])
    grad = pg.Surface((1, 2))
    top = tuple(clamp(top_base[i] + int(12*math.sin(t*0.18 + i)), 0, 255) for i in range(3))
    bot = tuple(clamp(bot_base[i] + int(18*math.sin(t*0.12 + i*0.7)), 0, 255) for i in range(3))
    grad.set_at((0, 0), top); grad.set_at((0, 1), bot)
    pg.transform.smoothscale(grad, (W, H), BG_BASE_SURF)
    surf.blit(BG_BASE_SURF, (0, 0))
    BG_GLOW_SURF.fill((0, 0, 0, 0))
    halos = theme.get("halos", [])
    for x, y, r, col in halos:
        px = W * x + math.sin(t*0.5 + x) * 40
        py = H * y + math.cos(t*0.3 + y) * 30
        pg.draw.circle(BG_GLOW_SURF, col, (int(px), int(py)), int(r))
    surf.blit(BG_GLOW_SURF, (0, 0), special_flags=pg.BLEND_ADD)


class Button:
    def __init__(self, rect, text, on_click, icon="none"):
        self.rect = pg.Rect(rect)
        self.text = text
        self.on_click = on_click
        self.hover = False
        self._font = pg.font.SysFont("consolas", 26, bold=True)
        self.icon = icon  # "play","dice","quit","skin","left","right","select","back"

    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def handle_event(self, e):
        if e.type == pg.MOUSEBUTTONDOWN and e.button == 1 and self.hover:
            self.on_click()

    def _draw_icon(self, surf, area):
        cx, cy = area.center
        main_col = ACCENT if self.hover else FG
        dim_col = UI_DIM
        if self.icon == "play":
            w,h = 18,20
            pts = [(cx - w//2, cy - h//2), (cx - w//2, cy + h//2), (cx + w//2, cy)]
            pg.draw.polygon(surf, main_col, pts)
            pg.draw.circle(surf, (*main_col, 60), (cx - 8, cy), 9, 2)
        elif self.icon == "dice":
            r = pg.Rect(0,0,26,26); r.center = (cx,cy)
            pg.draw.rect(surf, main_col, r, 2, border_radius=6)
            for dx,dy in [(-6,-6),(6,-6),(-6,6),(6,6),(0,0)]:
                pg.draw.circle(surf, main_col, (r.centerx+dx, r.centery+dy), 3)
        elif self.icon == "quit":
            size = 14
            pg.draw.circle(surf, (*ACCENT_ALT, 80), (cx, cy), size+2, 2)
            pg.draw.line(surf, main_col, (cx-size, cy-size), (cx+size, cy+size), 3)
            pg.draw.line(surf, main_col, (cx+size, cy-size), (cx-size, cy+size), 3)
        elif self.icon == "skin":
            w,h = 28,20
            pg.draw.polygon(surf, main_col, [(cx-w//2,cy-h//2),(cx-w//6,cy-h//2),(cx,cy-h//3),
                                             (cx+w//6,cy-h//2),(cx+w//2,cy-h//2),
                                             (cx+w//3,cy+h//2),(cx-w//3,cy+h//2)], 2)
            pg.draw.circle(surf, main_col, (cx, cy+2), 3)
        elif self.icon == "left":
            pg.draw.polygon(surf, main_col, [(cx+8,cy-12),(cx-8,cy),(cx+8,cy+12)])
        elif self.icon == "right":
            pg.draw.polygon(surf, main_col, [(cx-8,cy-12),(cx+8,cy),(cx-8,cy+12)])
        elif self.icon == "gear":
            r = 12
            for i in range(6):
                ang = math.tau * i / 6
                ox = math.cos(ang) * (r + 2)
                oy = math.sin(ang) * (r + 2)
                pg.draw.rect(surf, main_col, (cx + ox - 3, cy + oy - 3, 6, 6))
            pg.draw.circle(surf, main_col, (cx, cy), r, 2)
            pg.draw.circle(surf, ACCENT, (cx, cy), 5, 0)
        elif self.icon == "note":
            w,h = 22,26
            rect = pg.Rect(0,0,w,h); rect.center = (cx,cy)
            pg.draw.rect(surf, main_col, rect, 2, border_radius=4)
            pg.draw.line(surf, main_col, (rect.left+4, rect.top+8), (rect.right-4, rect.top+8), 2)
            pg.draw.line(surf, main_col, (rect.left+4, rect.centery), (rect.right-4, rect.centery), 2)
            pg.draw.circle(surf, ACCENT, (rect.right-6, rect.top+6), 3)
        elif self.icon == "star":
            pts = []
            for i in range(5):
                ang = math.tau * i / 5 - math.pi/2
                r1 = 11; r2 = 5
                pts.append((cx + math.cos(ang)*r1, cy + math.sin(ang)*r1))
                ang += math.tau / 10
                pts.append((cx + math.cos(ang)*r2, cy + math.sin(ang)*r2))
            pg.draw.polygon(surf, main_col, pts)
            pg.draw.circle(surf, (*ACCENT_ALT, 100), (cx, cy), 14, 2)
        elif self.icon == "help":
            pg.draw.circle(surf, main_col, (cx, cy), 12, 2)
            pg.draw.circle(surf, (*ACCENT, 80), (cx, cy), 14, 1)
            font = pg.font.SysFont("consolas", 18, bold=True)
            img = font.render("?", True, main_col)
            r = img.get_rect(center=(cx, cy))
            surf.blit(img, r)
        elif self.icon == "select":
            pg.draw.circle(surf, main_col, (cx,cy), 10, 2)
            pg.draw.circle(surf, ACCENT, (cx,cy), 4)
        elif self.icon == "back":
            pg.draw.polygon(surf, main_col, [(cx+10,cy-10),(cx-6,cy),(cx+10,cy+10)], 0)
            pg.draw.circle(surf, (*dim_col, 80), (cx+6, cy), 10, 1)

    def draw(self, surf):
        layer = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        pg.draw.rect(layer, BTN_SHADOW, (4, 6, self.rect.width, self.rect.height), border_radius=14)
        pg.draw.rect(layer, BTN_BG_HOVER if self.hover else BTN_BG, (0, 0, self.rect.width, self.rect.height), border_radius=14)
        accent_col = ACCENT if self.hover else (80, 120, 200)
        pg.draw.rect(layer, accent_col, (8, 8, 6, self.rect.height-16), border_radius=6)
        pg.draw.rect(layer, BTN_BORDER, (0, 0, self.rect.width, self.rect.height), width=2, border_radius=14)
        if self.hover:
            glow = pg.Rect(0, 0, self.rect.width, self.rect.height); glow.inflate_ip(8, 8)
            pg.draw.rect(layer, (*ACCENT, 80), glow, width=2, border_radius=18)
        cy = self.rect.height // 2
        icon_rect = pg.Rect(16, cy-14, 28, 28)
        self._draw_icon(layer, icon_rect)
        img = self._font.render(self.text, True, FG)
        r = img.get_rect(midleft=(icon_rect.right + 12, cy))
        layer.blit(img, r)
        surf.blit(layer, self.rect.topleft)

# ---------- Base obstacle ----------
class Ob:
    def update(self, dt, scroll): ...
    def draw(self, surf, t): ...
    def alive(self): return True
    def collide(self, player): return False
    def near(self, player, near_mask): return False

# ---------- Triangles ----------
class SpikeTri(Ob):
    def __init__(self, x, line_y, line_idx, orientation):
        self.cx = float(x); self.y_line = float(line_y); self.line_idx = line_idx
        self.ori = orientation
        self.r = PLAYER_R
        self.w = self.h = self.r * 2
        self.surf = pg.Surface((self.w, self.h), pg.SRCALPHA)
        pg.draw.circle(self.surf, SPIKE_COL, (self.r, self.r), self.r)
        self.mask = pg.mask.from_surface(self.surf)
        self.cy = self.y_line - self.r if self.ori == "up" else self.y_line + self.r
        self.bltx = self.cx - self.r
        self.blty = self.cy - self.r
    def update(self, dt, scroll):
        self.cx -= scroll*dt
        self.bltx = self.cx - self.r
        self.blty = self.cy - self.r
    def alive(self): return self.cx + self.r > -80
    def draw(self, surf, t):
        surf.blit(self.surf, (int(self.bltx), int(self.blty)))
    def _overlap_mask(self, player_mask, player_rect):
        offx = int(player_rect.left - self.bltx); offy = int(player_rect.top - self.blty)
        return self.mask.overlap(player_mask, (offx, offy)) is not None
    def collide(self, player): return self._overlap_mask(player.circle_mask, player.rect())
    def near(self, player, near_mask):
        if self.collide(player): return False
        return self._overlap_mask(near_mask, player.near_rect())

class SlidingSpike(SpikeTri):
    def __init__(self, x, line_y, line_idx, orientation, amp=20, speed=1.4, phase=0.0):
        super().__init__(x, line_y, line_idx, orientation)
        self.amp = amp; self.speed = speed; self.phase = phase
        self.base_x = self.cx
    def update(self, dt, scroll):
        self.base_x -= scroll*dt
        self.phase += self.speed*dt
        loc = math.sin(self.phase) * self.amp
        self.cx = self.base_x + loc
        self.bltx = self.cx - self.r
        self.blty = self.cy - self.r

# ---------- Double triangles helper ----------
def spawn_double_triangles(world, xbase, lines):
    if len(lines) < 3: return []
    li = random.randint(1, len(lines)-2)
    objs = []
    objs.append(SpikeTri(xbase, lines[li], li, "up"))
    objs.append(SpikeTri(xbase + random.randint(40, 80), lines[li-1], li-1, "down"))
    return objs

# ---------- Blade pivot ----------
class BladePivot(Ob):
    def __init__(self, x, line_y, line_idx, phase=0.0):
        self.cx = float(x); self.cy = float(line_y); self.line_idx = line_idx; self.phase = phase
        self.w = TRI_W; self.h = TRI_H
        self.base_surf, self.base_mask = triangle_surface(self.w, self.h, "up")
        side = int(max(self.w, self.h)*1.6)
        self.canvas = pg.Surface((side, side), pg.SRCALPHA)
        self.canvas.blit(self.base_surf, ((side-self.w)//2, (side-self.h)//2))
        self.canvas_mask = pg.mask.from_surface(self.canvas)
        self.angle = 0.0; self.end_pos = (self.cx, self.cy)
        self._rot_surf = self.canvas; self._rot_mask = self.canvas_mask
        self.rect_blit = self._rot_surf.get_rect(center=(int(self.cx), int(self.cy)))
    def update(self, dt, scroll):
        self.cx -= scroll*dt
        self.angle = math.sin(pg.time.get_ticks()*0.001*BLADE_SPEED + self.phase) * 70
        rad = math.radians(self.angle - 90)
        ex = self.cx + math.cos(rad)*BLADE_ARM
        ey = self.cy + math.sin(rad)*BLADE_ARM
        self.end_pos = (ex, ey)
        self._rot_surf = pg.transform.rotate(self.canvas, self.angle)
        self._rot_mask = pg.mask.from_surface(self._rot_surf)
        self.rect_blit = self._rot_surf.get_rect(center=(int(ex), int(ey)))
    def alive(self): return self.rect_blit.right > -80
    def draw(self, surf, t):
        pg.draw.line(surf, FG, (int(self.cx), int(self.cy)), (int(self.end_pos[0]), int(self.end_pos[1])), 2)
        surf.blit(self._rot_surf, self.rect_blit.topleft)
    def collide(self, player):
        off = (int(player.rect().left - self.rect_blit.left), int(player.rect().top - self.rect_blit.top))
        return self._rot_mask.overlap(player.circle_mask, off) is not None
    def near(self, player, near_mask):
        if self.collide(player): return False
        off = (int(player.near_rect().left - self.rect_blit.left), int(player.near_rect().top - self.rect_blit.top))
        return self._rot_mask.overlap(near_mask, off) is not None

# ---------- Lasers de ligne ----------
class LaserSegment(Ob):
    def __init__(self, xcenter, line_y, line_idx, orientation, length=LASER_LEN):
        self.xc = float(xcenter); self.y_line = float(line_y); self.line_idx = line_idx
        self.ori = orientation; self.len = length
        self.state = "tele"; self.timer = LASER_TELE
    def update(self, dt, scroll):
        self.xc -= scroll*dt
        self.timer -= dt
        if self.timer <= 0:
            if self.state == "tele": self.state = "active"; self.timer = LASER_ACTIVE
            elif self.state == "active": self.state = "cool"; self.timer = LASER_COOLDOWN
            else: self.state = "tele"; self.timer = LASER_TELE
    def alive(self): return self.xc + self.len/2 > -80
    def _rect(self):
        x1 = self.xc - self.len/2
        if self.ori == "up":
            rect = pg.Rect(int(x1), int(self.y_line - LASER_DEPTH), int(self.len), int(LASER_DEPTH))
        else:
            rect = pg.Rect(int(x1), int(self.y_line), int(self.len), int(LASER_DEPTH))
        return rect
    def draw(self, surf, t):
        x1 = int(self.xc - self.len/2); x2 = int(self.xc + self.len/2)
        pg.draw.line(surf, LASER_COL, (x1, int(self.y_line)), (x2, int(self.y_line)), 1)
        rect = self._rect()
        if self.state == "tele": pg.draw.rect(surf, LASER_COL, rect, 1)
        elif self.state == "active": pg.draw.rect(surf, LASER_COL, rect)
    def collide(self, player):
        if self.state != "active": return False
        return circle_rect_collide(player.x, player.y, player.r, self._rect())
    def near(self, player, near_mask):
        if self.state != "active": return False
        rect = self._rect()
        return (not self.collide(player)) and circle_rect_collide(player.x, player.y, player.r+NEAR_T, rect)

# ---------- Clapets ----------
class Clapet(Ob):
    def __init__(self, xcenter, lane_center, width=TRI_W*2):
        self.xc = float(xcenter); self.yc = float(lane_center)
        self.width = width; self.state = "rest"; self.timer = CLAP_REST
    def update(self, dt, scroll):
        self.xc -= scroll*dt; self.timer -= dt
        if self.timer <= 0:
            if self.state == "rest": self.state = "active"; self.timer = CLAP_ACTIVE
            else: self.state = "rest"; self.timer = CLAP_REST
    def alive(self): return self.xc + self.width/2 > -80
    def _rect(self): return rect_from_cxcywh(self.xc, self.yc, self.width, CLAP_DEPTH)
    def draw(self, surf, t):
        rect = self._rect()
        if self.state == "active": pg.draw.rect(surf, FG, rect)
        else: pg.draw.rect(surf, FG, rect, 1)
    def collide(self, player):
        if self.state != "active": return False
        return circle_rect_collide(player.x, player.y, player.r, self._rect())
    def near(self, player, near_mask):
        if self.state != "active": return False
        rect = self._rect()
        return (not self.collide(player)) and circle_rect_collide(player.x, player.y, player.r+NEAR_T, rect)

# ---------- Drones & Mines ----------
class Drone(Ob):
    def __init__(self, x, lane_center):
        self.x = float(x); self.y = float(lane_center); self.r = DRONE_R
        self.surf, self.mask = circle_mask(self.r)
    def update(self, dt, scroll): self.x -= scroll*dt
    def alive(self): return self.x + self.r > -80
    def draw(self, surf, t): surf.blit(self.surf, (int(self.x - self.r), int(self.y - self.r)), special_flags=0)
    def collide(self, player):
        offx = int(player.x - self.x); offy = int(player.y - self.y)
        return (offx*offx + offy*offy) <= (self.r + player.r)*(self.r + player.r)
    def near(self, player, near_mask):
        if self.collide(player): return False
        offx = int(player.x - self.x); offy = int(player.y - self.y)
        return (offx*offx + offy*offy) <= (self.r + player.r + NEAR_T)**2

class GhostMine(Drone):
    def __init__(self, x, lane_center):
        super().__init__(x, lane_center); self.state = "hidden"; self.timer = 0.0
    def draw(self, surf, t):
        if self.state == "hidden": return
        elif self.state == "reveal": pg.draw.circle(surf, FG, (int(self.x), int(self.y)), self.r, 1)
        else: pg.draw.circle(surf, FG, (int(self.x), int(self.y)), self.r)
    def update(self, dt, scroll):
        self.x -= scroll * dt
        if self.state == "hidden":
            if self.x - PLAYER_X <= MINE_REVEAL_DIST:
                self.state = "reveal"; self.timer = MINE_ARM_TIME
        elif self.state == "reveal":
            self.timer -= dt
            if self.timer <= 0: self.state = "armed"
    def collide(self, player):
        if self.state != "armed": return False
        return super().collide(player)
    def near(self, player, near_mask):
        if self.state != "armed": return False
        return super().near(player, near_mask)

# ---------- Laser diagonal ----------
class DiagLaser(Ob):
    def __init__(self, xcenter, lane_center, slope=1):
        self.xc = float(xcenter); self.yc = float(lane_center)
        self.slope = slope; self.state = "cool"; self.timer = DIAG_COOL
        self.base = pg.Surface((DIAG_LEN, DIAG_THICK), pg.SRCALPHA)
        pg.draw.rect(self.base, LASER_COL, self.base.get_rect())
        self.angle = 35 if slope>0 else -35
        self.rot = pg.transform.rotate(self.base, self.angle)
        self.mask = pg.mask.from_surface(self.rot)
        self.rect = self.rot.get_rect(center=(int(self.xc), int(self.yc)))
    def update(self, dt, scroll):
        self.xc -= scroll*dt; self.timer -= dt
        if self.timer <= 0:
            if self.state == "cool": self.state = "active"; self.timer = DIAG_ACTIVE
            else: self.state = "cool"; self.timer = DIAG_COOL
        self.rect = self.rot.get_rect(center=(int(self.xc), int(self.yc)))
    def alive(self): return self.rect.right > -80
    def draw(self, surf, t):
        if self.state == "active": surf.blit(self.rot, self.rect.topleft)
        else: pg.draw.rect(surf, LASER_COL, self.rect, 1)
    def collide(self, player):
        if self.state != "active": return False
        off = (int(player.rect().left - self.rect.left), int(player.rect().top - self.rect.top))
        return self.mask.overlap(player.circle_mask, off) is not None
    def near(self, player, near_mask):
        if self.state != "active": return False
        if self.collide(player): return False
        off = (int(player.near_rect().left - self.rect.left), int(player.near_rect().top - self.rect.top))
        return self.mask.overlap(near_mask, off) is not None

# ---------- Spirales sens unique ----------
class OneWayTP(Ob):
    def __init__(self, x_in, y_in, x_out, y_out):
        self.inp = [float(x_in), float(y_in)]; self.out = [float(x_out), float(y_out)]
    def update(self, dt, scroll):
        self.inp[0] -= scroll*dt; self.out[0] -= scroll*dt
    def alive(self): return self.out[0] > -120
    def draw(self, surf, t):
        self._draw_portal(surf, self.inp[0], self.inp[1], t, filled=False)
        self._draw_portal(surf, self.out[0], self.out[1], t, filled=True)
    def _draw_portal(self, surf, cx, cy, t, filled=False):
        pulse = 2 + math.sin(t*4) * 2
        glow_r = TP_R + int(pulse)
        core_r = TP_R - 4
        pg.draw.circle(surf, (*TP_COL, 90), (int(cx), int(cy)), glow_r)
        if filled:
            pg.draw.circle(surf, TP_COL, (int(cx), int(cy)), TP_R)
            pg.draw.circle(surf, (255, 255, 255), (int(cx), int(cy)), core_r, 2)
        else:
            pg.draw.circle(surf, TP_COL, (int(cx), int(cy)), TP_R, 2)
            pg.draw.circle(surf, TP_COL, (int(cx), int(cy)), core_r, 1)
            pg.draw.polygon(surf, TP_COL, [(int(cx+TP_R+8), int(cy)), (int(cx+TP_R-2), int(cy-6)), (int(cx+TP_R-2), int(cy+6))])
    def collide(self, player):
        dx = player.x - self.inp[0]; dy = player.y - self.inp[1]
        if dx*dx + dy*dy <= (TP_R + player.r)**2 and player.tp_cd <= 0 and not player.tp_lock:
            player.lock_to_portal(self)
        return False
    def near(self, player, near_mask): return False

# ---------- Turret / Projectiles ----------
class Projectile(Ob):
    def __init__(self, x, y):
        self.x = float(x); self.y = float(y); self.r = PROJECTILE_R
    def update(self, dt, scroll):
        self.x -= (scroll + PROJECTILE_SPEED) * dt
    def alive(self): return self.x + self.r > -80
    def draw(self, surf, t):
        pg.draw.circle(surf, LASER_COL, (int(self.x), int(self.y)), self.r)
    def collide(self, player):
        dx = player.x - self.x; dy = player.y - self.y
        return (dx*dx + dy*dy) <= (self.r + player.r)*(self.r + player.r)
    def near(self, player, near_mask):
        if self.collide(player): return False
        dx = player.x - self.x; dy = player.y - self.y
        return (dx*dx + dy*dy) <= (self.r + player.r + NEAR_T)**2

class Turret(Ob):
    def __init__(self, x, lane_center):
        self.x = float(x); self.y = float(lane_center); self.r = TURRET_R
        self.fire_cd = random.uniform(TURRET_FIRE_MIN, TURRET_FIRE_MAX)
        self.warn_t = 0.0
        self.shot_this_cycle = False
    def update(self, dt, scroll):
        self.x -= scroll * dt
        if self.warn_t > 0: self.warn_t -= dt
        self.fire_cd -= dt
        if self.fire_cd <= 0:
            self.warn_t = PROJECTILE_WARN
            self.fire_cd = random.uniform(TURRET_FIRE_MIN, TURRET_FIRE_MAX)
            self.shot_this_cycle = False
    def alive(self): return self.x + self.r > -80
    def draw(self, surf, t):
        pg.draw.circle(surf, LASER_COL, (int(self.x), int(self.y)), self.r, 2)
        if self.warn_t > 0:
            pg.draw.circle(surf, LASER_COL, (int(self.x), int(self.y)), self.r + 6, 1)
    def spawn_projectile(self):
        if self.warn_t <= 0.02 and not self.shot_this_cycle:
            self.shot_this_cycle = True
            return Projectile(self.x, self.y)
        return None
    def collide(self, player):
        dx = player.x - self.x; dy = player.y - self.y
        return (dx*dx + dy*dy) <= (self.r + player.r)*(self.r + player.r)
    def near(self, player, near_mask):
        if self.collide(player): return False
        dx = player.x - self.x; dy = player.y - self.y
        return (dx*dx + dy*dy) <= (self.r + player.r + NEAR_T)**2

# ---------- Pulse wall ----------
class PulseWall(Ob):
    def __init__(self, x):
        self.x = float(x)
        self.state = "tele"
        self.timer = PULSE_TELE
        self.width = PULSE_THICK
    def update(self, dt, scroll):
        self.x -= scroll * dt
        self.timer -= dt
        if self.timer <= 0:
            if self.state == "tele":
                self.state = "active"; self.timer = PULSE_ACTIVE
            elif self.state == "active":
                self.state = "cool"; self.timer = PULSE_COOL
            else:
                self.state = "tele"; self.timer = PULSE_TELE
    def alive(self): return self.x + self.width > -40
    def draw(self, surf, t):
        rect = pg.Rect(int(self.x - self.width/2), 0, int(self.width), H)
        if self.state == "tele":
            pg.draw.rect(surf, (80,80,80), rect, 1)
        elif self.state == "active":
            pg.draw.rect(surf, LASER_COL, rect)
    def collide(self, player):
        if self.state != "active": return False
        rect = pg.Rect(int(self.x - self.width/2), 0, int(self.width), H)
        return rect.colliderect(player.rect())
    def near(self, player, near_mask):
        if self.state != "active": return False
        rect = pg.Rect(int(self.x - self.width/2), 0, int(self.width), H)
        return rect.colliderect(player.near_rect())

# ---------- Joueur (avec skins) ----------
class Player:
    def __init__(self, corridor_centers, skin):
        self.x = PLAYER_X; self.centers = corridor_centers
        self.lane = len(corridor_centers)//2; self.y = float(self.centers[self.lane])
        self.r = PLAYER_R
        self.circle_surf, self.circle_mask = circle_mask(self.r)
        self.near_surf, self.near_mask = circle_mask(self.r + NEAR_T)
        self.alive = True; self.tp_cd = 0.0
        self.tp_lock = False; self.tp_lock_timer = 0.0; self.tp_portal = None; self.tp_target = (PLAYER_X, 0.0)
        self.mult = 1.0; self.last_near_t = 0.0; self.spark_t = 0.0
        self.near_sfx_cd = 0.0
        self.ai_mode = False; self.ai_dir = 0
        # dash
        self.dash_cd = 0.0; self.dash_timer = 0.0
        self.dash_cooldown = 1.5; self.dash_duration = 0.25
        # spin anim periodique
        self.spin_interval = 5.0; self.spin_duration = 0.6; self.spin_max = math.radians(22)
        self._spin_cd = self.spin_interval; self._spin_t = 0.0; self._angle = 0.0
        # skin
        self.skin = skin

    def rect(self):
        return pg.Rect(int(self.x - self.r), int(self.y - self.r), self.r*2, self.r*2)

    def near_rect(self):
        rr = self.r + NEAR_T
        return pg.Rect(int(self.x - rr), int(self.y - rr), rr*2, rr*2)

    def input_axis(self):
        if self.ai_mode:
            return self.ai_dir
        m = pg.mouse.get_pressed(3); keys = pg.key.get_pressed()
        up = m[0] or keys[pg.K_UP]; down = m[2] or keys[pg.K_DOWN]
        if getattr(self, "ia_only_mode", False):
            return 0
        if getattr(self, "mirror_input", False):
            up, down = down, up
        if up and not down: return -1
        if down and not up: return +1
        return 0

    def try_dash(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
            if self.dash_cd <= 0.0:
                self.dash_timer = self.dash_duration
                self.dash_cd = self.dash_cooldown

    def ai_dash(self):
        if self.dash_cd <= 0.0:
            self.dash_timer = self.dash_duration
            self.dash_cd = self.dash_cooldown

    def lock_to_portal(self, portal):
        self.tp_lock = True
        self.tp_lock_timer = TP_CD
        self.tp_portal = portal
        self.tp_target = (PLAYER_X, portal.out[1])
        self.x, self.y = PLAYER_X, portal.inp[1]

    def invulnerable(self):
        return self.dash_timer > 0.0

    def step_to(self, target_lane):
        if target_lane < self.lane: self.lane -= 1
        elif target_lane > self.lane: self.lane += 1
        self.lane = max(0, min(self.lane, len(self.centers)-1))
        self.y = float(self.centers[self.lane])

    def update(self, dt):
        if not self.alive: return
        # verrouillage dans un portail: on reste collé à l'entrée jusqu'au tp effectif
        if self.tp_lock:
            if self.tp_portal:
                # garder l'ancrage "X" fixe pour éviter le décalage caméra
                self.x, self.y = PLAYER_X, self.tp_portal.inp[1]
            self.tp_lock_timer -= dt
            if self.tp_lock_timer <= 0.0:
                self.x, self.y = self.tp_target
                self.tp_cd = TP_CD
                self.tp_lock = False
                self.tp_portal = None
                self.spark_t = 0.18
            return

        self.try_dash()
        mv = self.input_axis()
        if mv != 0: self.step_to(self.lane + (-1 if mv < 0 else 1))
        if self.tp_cd > 0: self.tp_cd -= dt
        if self.dash_cd > 0: self.dash_cd -= dt
        if self.dash_timer > 0: self.dash_timer -= dt
        self.last_near_t += dt
        if self.last_near_t > NEAR_DECAY_S: self.mult = max(1.0, self.mult - 0.5*dt)
        if self.spark_t > 0: self.spark_t -= dt
        if self.near_sfx_cd > 0: self.near_sfx_cd -= dt

        # spin
        self._spin_cd -= dt
        if self._spin_cd <= 0.0:
            self._spin_cd += self.spin_interval; self._spin_t = self.spin_duration
        if self._spin_t > 0.0:
            p = 1.0 - (self._spin_t / self.spin_duration)
            self._angle = self.spin_max * math.sin(math.pi * p); self._spin_t -= dt
        else:
            self._angle = 0.0

    def on_near(self):
        self.last_near_t = 0.0; self.mult = min(NEAR_CAP, self.mult + NEAR_STEP); self.spark_t = 0.15
        self.near_sfx_cd = 0.15

    def draw(self, surf, t):
        col = self.skin["col"]
        # anneau fin (pas de remplissage)
        pg.draw.circle(surf, col, (int(self.x), int(self.y)), self.r, 2)
        # croix tournante
        L = self.r + 6; c = math.cos(self._angle); s = math.sin(self._angle)
        x1, y1 = self.x - L*c, self.y - L*s; x2, y2 = self.x + L*c, self.y + L*s
        pg.draw.line(surf, col, (x1, y1), (x2, y2), 1)
        cp, sp = -s, c
        x3, y3 = self.x - L*cp, self.y - L*sp; x4, y4 = self.x + L*cp, self.y + L*sp
        pg.draw.line(surf, col, (x3, y3), (x4, y4), 1)
        if self.invulnerable():
            pg.draw.circle(surf, (*col, 90), (int(self.x), int(self.y)), self.r + 4, 2)

        st = self.skin["style"]
        if st == "glow":
            pg.draw.circle(surf, (*col, 60), (int(self.x), int(self.y)), self.r+8, 2)
        elif st == "ring":
            pg.draw.circle(surf, col, (int(self.x), int(self.y)), self.r-4, 1)
        elif st == "crown":
            # mini couronne
            y = int(self.y - self.r - 6)
            x = int(self.x)
            pts = [(x-10,y+8),(x-6,y),(x-2,y+8),(x+2,y),(x+6,y+8),(x+10,y)]
            pg.draw.lines(surf, col, False, pts, 2)
        elif st == "ghost":
            for i in range(6):
                ang = t*6 + i*math.tau/6
                pg.draw.circle(surf, (*col, 120), (int(self.x+math.cos(ang)*10), int(self.y+math.sin(ang)*10)), 1)

        if self.spark_t > 0:
            for i in range(6):
                ang = t*8 + i*math.tau/6
                x = self.x + math.cos(ang)*(self.r+6); y = self.y + math.sin(ang)*(self.r+6)
                pg.draw.line(surf, col, (self.x, self.y), (x, y), 1)

# ---------- Particules ----------
class TrailParticle:
    def __init__(self, x, y, col, boosted=False):
        self.x = x + random.uniform(-3, 3)
        self.y = y + random.uniform(-4, 4)
        self.vx = random.uniform(-90, -60) * (1.25 if boosted else 1.0)
        self.vy = random.uniform(-28, 28)
        self.life = random.uniform(0.35, 0.55)
        self.age = 0.0
        self.col = col
        self.scale = random.uniform(0.7, 1.1) * (1.15 if boosted else 1.0)

    def update(self, dt):
        self.age += dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy *= 0.97

    def alive(self):
        return self.age < self.life

    def draw(self, surf):
        if not self.alive(): return
        p = 1.0 - (self.age / self.life)
        a = clamp(int(140 * p), 0, 180)
        r = max(1, int(self.scale * 3 * p))
        pg.draw.circle(surf, (*self.col, a), (int(self.x), int(self.y)), r)


class ParticleTrail:
    def __init__(self):
        self.parts = []
        self.spawn_accum = 0.0
        self.max_parts = 220

    def clear(self):
        self.parts.clear()
        self.spawn_accum = 0.0

    def emit(self, dt, x, y, col, boosted=False):
        rate = 32 if boosted else 18
        self.spawn_accum += rate * dt
        while self.spawn_accum >= 1.0:
            self.spawn_accum -= 1.0
            if len(self.parts) < self.max_parts:
                self.parts.append(TrailParticle(x, y, col, boosted))

    def update(self, dt):
        for p in self.parts:
            p.update(dt)
        self.parts = [p for p in self.parts if p.alive()]

    def draw(self, surf):
        for p in self.parts:
            p.draw(surf)

# ---------- Monde ----------
class World:
    def __init__(self, seed=DEFAULT_SEED):
        random.seed(seed); self.seed = seed
        self.lines = compute_lines()
        self.corr_centers = [(self.lines[i] + self.lines[i+1]) / 2 for i in range(len(self.lines)-1)]
        self.scroll = SCROLL_BASE; self.world_x = 0.0
        self.generated_until = 0.0; self.spawn_gap = SPAWN_BASE
        self.relief_timer = 0.0
        self.relief_used = 0
        self.relief_next_score = RELIEF_SCORE_STEP
        self.obs = []
        self.custom_mode = False
        self.custom_length = 0.0
        self.custom_level_id = None
    def diff(self):
        # difficulté plafonnée pour éviter l'effet "mur"
        base = 1.0 + self.world_x / 6000.0
        return min(base, 1.0 + DIFF_CAP)
    def update_params(self):
        if self.custom_mode:
            self.scroll = SCROLL_BASE
            self.spawn_gap = SPAWN_BASE
            return
        self.scroll = SCROLL_BASE + SCROLL_GROWTH * self.world_x
        self.spawn_gap = max(SPAWN_MIN, SPAWN_BASE - DENSITY_GROWTH * self.world_x)
        if self.relief_timer > 0.0:
            self.scroll *= RELIEF_SCROLL_FAC
            self.spawn_gap *= RELIEF_SPAWN_FAC
    def spawn_column(self):
        d = self.diff(); total_lines = len(self.lines)
        max_this_col = min(MAX_LINES_PER_COLUMN, 1 + int(min(3, d)))
        choice_count = random.randint(1, min(max_this_col, total_lines))
        family = random.choices(
            population=["tri", "slide", "double", "laser", "clap", "drone", "mine", "diag", "tp1", "turret", "pulse"],
            weights=[32, 16, 10, 8, 7, 7, 5, 4, 3, 4, 4], k=1
        )[0]
        xbase = W + self.generated_until + random.randint(-12, 12)
        if family == "tri":
            idxs = random.sample(range(total_lines), choice_count)
            for li in idxs:
                ori = "down" if li==0 else "up" if li==total_lines-1 else random.choice(["up","down"])
                self.obs.append(SpikeTri(xbase, self.lines[li], li, ori))
        elif family == "slide":
            idxs = random.sample(range(total_lines), choice_count)
            for li in idxs:
                ori = "down" if li==0 else "up" if li==total_lines-1 else random.choice(["up","down"])
                amp = random.randint(16, 30); speed = random.uniform(1.2, 2.2); phase = random.random()*math.tau
                self.obs.append(SlidingSpike(xbase, self.lines[li], li, ori, amp, speed, phase))
        elif family == "double":
            self.obs += spawn_double_triangles(self, xbase, self.lines)
        elif family == "laser":
            li = random.randint(0, total_lines-1)
            ori = "down" if li==0 else "up" if li==total_lines-1 else random.choice(["up","down"])
            self.obs.append(LaserSegment(xbase, self.lines[li], li, ori, length=LASER_LEN))
        elif family == "clap":
            lane = random.randint(0, len(self.corr_centers)-1)
            self.obs.append(Clapet(xbase, self.corr_centers[lane], width=TRI_W*2))
        elif family == "drone":
            lane = random.randint(0, len(self.corr_centers)-1)
            self.obs.append(Drone(xbase, self.corr_centers[lane]))
        elif family == "mine":
            lane = random.randint(0, len(self.corr_centers)-1)
            self.obs.append(GhostMine(xbase, self.corr_centers[lane]))
        elif family == "diag":
            lane = random.randint(0, len(self.corr_centers)-1)
            slope = random.choice([1,-1])
            self.obs.append(DiagLaser(xbase, self.corr_centers[lane], slope))
        elif family == "tp1":
            if len(self.corr_centers) >= 2:
                c1 = random.randint(0, len(self.corr_centers)-1)
                c2 = random.randint(0, len(self.corr_centers)-1)
                while c2 == c1: c2 = random.randint(0, len(self.corr_centers)-1)
                x1 = xbase + 80; x2 = x1 + random.randint(180, 360)
                self.obs.append(OneWayTP(x1, self.corr_centers[c1], x2, self.corr_centers[c2]))
        elif family == "turret":
            lane = random.randint(0, len(self.corr_centers)-1)
            self.obs.append(Turret(xbase, self.corr_centers[lane]))
        elif family == "pulse":
            self.obs.append(PulseWall(xbase))
        if random.random() < 0.10:
            li = random.randint(1, total_lines-2) if total_lines>2 else 0
            self.obs.append(BladePivot(xbase+random.randint(40,120), self.lines[li], li, phase=random.random()*math.tau))
        if random.random() < 0.15:
            self.generated_until += random.randint(10, 30)
    def generate_until(self):
        if self.custom_mode:
            return
        while self.generated_until < self.world_x + W*2:
            self.spawn_column(); self.generated_until += self.spawn_gap
    def update(self, dt):
        self.world_x += self.scroll*dt
        if self.relief_timer > 0.0:
            self.relief_timer -= dt
        self.update_params(); self.generate_until()
        for o in self.obs: o.update(dt, self.scroll)
        self.obs = [o for o in self.obs if o.alive()]
    def draw(self, surf, t, player_y=None):
        center_y = player_y if player_y is not None else H // 2
        draw_lines_comfort(surf, self.lines, center_y, color=LINE_COL, thick=LINE_THICK_PLAY)
        for o in self.obs:
            o.draw(surf, t)

    # ---------- Custom levels ----------
    def _build_obj(self, data):
        typ = data.get("type")
        lane = int(clamp(data.get("lane", 0), 0, len(self.lines)-1))
        dist = float(data.get("x", 0.0))
        x = PLAYER_X + dist
        cy_custom = data.get("custom_y", None)
        if typ == "tri":
            ori = data.get("ori") or ("down" if lane == 0 else "up" if lane == len(self.lines)-1 else "up")
            y_line = cy_custom if cy_custom is not None else self.lines[lane]
            return SpikeTri(x, y_line, lane, ori)
        if typ == "laser":
            ori = data.get("ori") or ("down" if lane == 0 else "up" if lane == len(self.lines)-1 else "up")
            length = data.get("len", LASER_LEN)
            y_line = cy_custom if cy_custom is not None else self.lines[lane]
            return LaserSegment(x, y_line, lane, ori, length=length)
        if typ == "clap":
            width = data.get("w", TRI_W*2)
            y_c = cy_custom if cy_custom is not None else self.corr_centers[lane]
            return Clapet(x, y_c, width=width)
        if typ == "drone":
            y_c = cy_custom if cy_custom is not None else self.corr_centers[lane]
            return Drone(x, y_c)
        if typ == "mine":
            y_c = cy_custom if cy_custom is not None else self.corr_centers[lane]
            return GhostMine(x, y_c)
        if typ == "turret":
            y_c = cy_custom if cy_custom is not None else self.corr_centers[lane]
            return Turret(x, y_c)
        if typ == "tp":
            dest_lane = int(clamp(data.get("dest_lane", lane), 0, len(self.corr_centers)-1))
            dx = data.get("dx", 240)
            y_from = cy_custom if cy_custom is not None else self.corr_centers[lane]
            return OneWayTP(x, y_from, x + dx, self.corr_centers[dest_lane])
        if typ == "pulse":
            return PulseWall(x)
        return None

    def load_custom_level(self, level_data):
        self.custom_mode = True
        self.custom_length = float(level_data.get("length", 2400.0))
        self.custom_level_id = level_data.get("id")
        self.world_x = 0.0
        self.generated_until = 0.0
        self.relief_timer = 0.0
        self.obs = []
        for data in level_data.get("objects", []):
            o = self._build_obj(data)
            if o:
                self.obs.append(o)

# ---------- Jeu ----------
class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("REFLEXE - Reloaded (Endless Mecha + GOD + Comfort)")
        self.screen = pg.display.set_mode((W, H))
        self.clock = pg.time.Clock()
        self.fps_cap = FPS
        self.theme_light = False
        self.enable_vignette = True
        self.enable_scanlines = True
        self.mode_cycle = ["Normal", "Zen", "Chaos", "Mirror", "IA Only"]
        self.mode_idx = 0
        self.dynamic_trails = True
        self.unlock_skins = True
        self.level_manager = LevelManager()
        self.account_manager = AccountManager()
        self.user_profile = self.account_manager.profile
        self.level_editor = LevelEditor(self)
        self.levels_cursor = 0
        self.levels_scroll = 0
        self.level_import_buffer = ""
        self.import_mode = False
        self.last_played_level = None
        self.custom_running = False
        self.custom_finished_success = False
        self.current_custom_level = None
        self.levels_status = ""
        self.show_auth_modal = False
        self.auth_mode = "login"
        self.auth_pseudo = ""
        self.auth_pwd = ""
        self.auth_field = "pseudo"

        self.state = "menu"
        self.seed = DEFAULT_SEED
        self.world = World(self.seed)
        self.show_credits = False
        self.show_notes = False
        self.show_settings = False
        self.show_help = False
        self.show_skins_panel = False
        self.notes_scroll = 0.0
        self.help_scroll = 0.0
        self.settings_hitboxes = {}
        self.music_vol = 0.6
        self.sfx_vol = 1.0
        self.mirror_input = False
        self.chaos_mode = False
        self.zen_mode = False
        self.ia_only_mode = False

        # skins
        self.best_score = self._load_best()
        self.score = 0.0
        self.skin_idx = 0
        self.player = Player(self.world.corr_centers, SKINS[self.skin_idx])
        self.player.mirror_input = self.mirror_input
        self.player.ia_only_mode = self.ia_only_mode
        self.trail = ParticleTrail()
        self.bg_theme_idx = random.randint(0, len(BG_THEMES)-1)

        # GOD mode
        self.god = False
        self.ai_enabled = False
        self.ia_only_mode = False

        # sfx
        self.sfx_near = self._load_sfx(SFX_NEAR_PATH, fallback=SFX_NEAR_FALLBACK, volume=0.8)
        self.sfx_death = self._load_sfx(SFX_DEATH_PATH, fallback=SFX_DEATH_FALLBACK, volume=1.0)
        self._apply_audio_settings()
        self.music_tracks = []
        self.music_idx = 0
        self._start_music_playlist()

        # UI
        self.vignette = make_vignette(W, H)
        self.play_vignette = make_vignette(W, H)
        self.left_panel = make_panel(int(W*0.46), int(H*0.82))
        self.small_panel = make_panel(int(W*0.46), 120)
        if os.path.exists(TITLE_FONT_PATH):
            self.font_title = pg.font.Font(TITLE_FONT_PATH, 84)
        elif os.path.exists(TITLE_FONT_FALLBACK):
            self.font_title = pg.font.Font(TITLE_FONT_FALLBACK, 84)
        else:
            self.font_title = pg.font.SysFont("consolas", 84, bold=True)
        self.font_sub = pg.font.SysFont("consolas", 24, bold=True)
        self.font_small = pg.font.SysFont("consolas", 18, bold=False)

        # Buttons
        col_x = int(W*0.08); col_y = int(H*0.22)
        bw, bh, gap = 360, 54, 10
        self.btn_play = Button((col_x, col_y, bw, bh), "Jouer (endless)", self.reset, icon="play")
        self.btn_custom_levels = Button((col_x, col_y + (bh+gap), bw, bh), "Niveaux custom", self.open_levels_menu, icon="select")
        self.btn_editor = Button((col_x, col_y + 2*(bh+gap), bw, bh), "Editeur de niveaux", self.open_editor, icon="gear")
        self.btn_seed = Button((col_x, col_y + 3*(bh+gap), bw, bh), "Nouveau seed (menu)", self.new_seed_menu, icon="dice")
        self.btn_skins = Button((col_x, col_y + 4*(bh+gap), bw, bh), "Skins", self.toggle_skins_panel, icon="skin")
        self.btn_settings = Button((col_x, col_y + 5*(bh+gap), bw, bh), "Paramètres", self.toggle_settings, icon="gear")
        self.btn_notes = Button((col_x, col_y + 6*(bh+gap), bw, bh), "Notes", self.toggle_notes, icon="note")
        self.btn_help = Button((col_x, col_y + 7*(bh+gap), bw, bh), "Aide", self.toggle_help, icon="help")
        self.btn_credits = Button((col_x, col_y + 8*(bh+gap), bw, bh), "Credits", self.toggle_credits, icon="star")
        self.btn_quit = Button((col_x, col_y + 9*(bh+gap), bw, bh), "Quitter", self.quit_game, icon="quit")
        self.btn_notes_back = Button((int(W*0.06), int(H*0.12), 220, 52), "Retour menu", self.toggle_notes, icon="back")
        self.btn_settings_back = Button((int(W*0.06), int(H*0.12), 220, 52), "Retour menu", self.toggle_settings, icon="back")
        self.btn_help_back = Button((int(W*0.06), int(H*0.12), 220, 52), "Retour menu", self.toggle_help, icon="back")
        self.buttons = [self.btn_play, self.btn_custom_levels, self.btn_editor, self.btn_seed, self.btn_skins, self.btn_settings, self.btn_notes, self.btn_help, self.btn_credits, self.btn_quit]
        self.copy_btn_rect = None
        self.copy_feedback_t = 0.0

        # clipboard init (best effort)
        try:
            if not pg.scrap.get_init():
                pg.scrap.init()
        except Exception:
            pass

    # ---------- Flow ----------
    def _load_best(self):
        try:
            if os.path.exists(BEST_SCORE_PATH):
                with open(BEST_SCORE_PATH, "r", encoding="utf-8") as f:
                    return float(f.read().strip() or 0.0)
        except Exception:
            pass
        return 0.0

    def _save_best(self):
        try:
            with open(BEST_SCORE_PATH, "w", encoding="utf-8") as f:
                f.write(str(self.best_score))
        except Exception:
            pass

    def _load_sfx(self, path, fallback=None, volume=1.0):
        try:
            p = path if os.path.exists(path) else fallback
            if p and os.path.exists(p):
                s = pg.mixer.Sound(p)
                s.set_volume(min(1.0, max(0.0, volume)))
                return s
        except Exception:
            pass
        return None

    def _apply_audio_settings(self):
        self.music_vol = clamp(self.music_vol, 0.0, 1.0)
        self.sfx_vol = clamp(self.sfx_vol, 0.0, 1.0)
        try:
            pg.mixer.music.set_volume(self.music_vol)
        except Exception:
            pass
        for s in (self.sfx_near, self.sfx_death):
            try:
                if s:
                    s.set_volume(self.sfx_vol)
            except Exception:
                pass
        globals()['THEME_LIGHT'] = self.theme_light

    def _load_music_library(self):
        tracks = []
        seen = set()
        def add_folder(folder):
            if not os.path.isdir(folder):
                return
            for name in os.listdir(folder):
                if name.lower().endswith((".mp3", ".ogg", ".wav", ".flac")):
                    full = os.path.join(folder, name)
                    if full not in seen:
                        seen.add(full); tracks.append(full)
        add_folder(MUSIC_DIR)
        add_folder(base_path)
        return tracks

    def _play_track(self, idx):
        if not self.music_tracks:
            return
        path = self.music_tracks[idx % len(self.music_tracks)]
        try:
            pg.mixer.music.stop()
            pg.mixer.music.load(path)
            pg.mixer.music.set_volume(self.music_vol)
            pg.mixer.music.play(0, fade_ms=800)
            pg.mixer.music.set_endevent(MUSIC_END_EVENT)
        except Exception as e:
            print("Erreur lecture musique:", e)

    def _start_music_playlist(self):
        self.music_tracks = self._load_music_library()
        if not self.music_tracks:
            return
        self.music_idx = self.music_idx % len(self.music_tracks)
        self._play_track(self.music_idx)

    def _next_track(self):
        if not self.music_tracks:
            return
        self.music_idx = (self.music_idx + 1) % len(self.music_tracks)
        self._play_track(self.music_idx)

    def _pause_music(self):
        try:
            pg.mixer.music.pause()
        except Exception:
            pass

    def _resume_music(self):
        try:
            pg.mixer.music.unpause()
        except Exception:
            pass

    def _copy_text(self, txt):
        try:
            if not pg.scrap.get_init():
                pg.scrap.init()
            pg.scrap.put(pg.SCRAP_TEXT, txt.encode("utf-8"))
            return True
        except Exception:
            return False

    def _paste_text(self):
        try:
            if not pg.scrap.get_init():
                pg.scrap.init()
            data = pg.scrap.get(pg.SCRAP_TEXT)
            if not data:
                return ""
            try:
                return data.decode("utf-8")
            except Exception:
                return data.decode("latin-1", errors="ignore")
        except Exception:
            return ""

    def _hash_pwd(self, pseudo, pwd):
        h = hashlib.sha1()
        h.update(f"{pseudo}:{pwd}".encode("utf-8"))
        return h.hexdigest()

    def _open_auth_modal(self, mode):
        self.show_auth_modal = True
        self.auth_mode = mode
        self.auth_field = "pseudo"
        self.auth_pseudo = self.user_profile.get("pseudo", "") if self.user_profile else ""
        self.auth_pwd = ""

    def _auth_confirm(self):
        pseudo = (self.auth_pseudo or "").strip()
        pwd = (self.auth_pwd or "")
        if not pseudo or not pwd:
            return
        prof = {"pseudo": pseudo, "password_hash": self._hash_pwd(pseudo, pwd)}
        self.user_profile = prof
        self.account_manager.save(prof)
        self.show_auth_modal = False

    def _prompt_signup(self):
        self._open_auth_modal("signup")

    def _prompt_login(self):
        self._open_auth_modal("login")

    def _logout_account(self):
        self.user_profile = {"pseudo": "", "password_hash": ""}
        self.account_manager.save(self.user_profile)

    def _delete_account(self):
        self.account_manager.delete()
        self.user_profile = self.account_manager.profile

    def _auth_handle_event(self, e):
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                self.show_auth_modal = False
                return
            if e.key == pg.K_TAB:
                self.auth_field = "pwd" if self.auth_field == "pseudo" else "pseudo"
                return
            if e.key == pg.K_RETURN:
                self._auth_confirm()
                return
            if self.auth_field == "pseudo":
                if e.key == pg.K_BACKSPACE:
                    self.auth_pseudo = self.auth_pseudo[:-1]
                else:
                    ch = e.unicode
                    if ch and 32 <= ord(ch) <= 126 and len(self.auth_pseudo) < 24:
                        self.auth_pseudo += ch
            else:
                if e.key == pg.K_BACKSPACE:
                    self.auth_pwd = self.auth_pwd[:-1]
                else:
                    ch = e.unicode
                    if ch and 32 <= ord(ch) <= 126 and len(self.auth_pwd) < 24:
                        self.auth_pwd += ch

    def _copy_github_link(self):
        if self._copy_text(GITHUB_URL):
            self.copy_feedback_t = 1.2
        else:
            self.copy_feedback_t = 0.6

    def quit_game(self):
        pg.quit(); sys.exit(0)

    def reset(self):
        self.custom_running = False
        self.custom_finished_success = False
        self.current_custom_level = None
        self.world = World(self.seed)
        self.player = Player(self.world.corr_centers, SKINS[self.skin_idx])
        self.player.mirror_input = self.mirror_input
        self.player.ia_only_mode = self.ia_only_mode
        self.trail.clear()
        self.score = 0.0
        self.state = "playing"
        self._resume_music()
        self.chaos_mode = (self.mode_cycle[self.mode_idx].lower() == "chaos")
        self.zen_mode = (self.mode_cycle[self.mode_idx].lower() == "zen")
        self.mirror_input = (self.mode_cycle[self.mode_idx].lower() == "mirror")
        self.ia_only_mode = (self.mode_cycle[self.mode_idx].lower() == "ia only")
        self.ai_enabled = self.ia_only_mode
        self.player.mirror_input = self.mirror_input
        self.player.ia_only_mode = self.ia_only_mode

    def new_seed(self):
        self.seed = int(time.time()) & 0x7fffffff
        self.reset()

    def new_seed_menu(self):
        self.seed = int(time.time()) & 0x7fffffff
        self.world = World(self.seed)
        self._resume_music()

    def start_custom_level(self, level_data):
        self.custom_running = True
        self.custom_finished_success = False
        self.current_custom_level = level_data
        if not level_data.get("id"):
            level_data["id"] = self.level_manager.upsert_level(level_data)
        else:
            self.level_manager.upsert_level(level_data)
        self.last_played_level = level_data.get("id")
        self.world = World(self.seed)
        self.world.load_custom_level(level_data)
        self.player = Player(self.world.corr_centers, SKINS[self.skin_idx])
        self.player.mirror_input = False
        self.player.ia_only_mode = False
        self.trail.clear()
        self.score = 0.0
        self.state = "playing"
        self._resume_music()
        # modes off for custom
        self.chaos_mode = False
        self.zen_mode = False
        self.mirror_input = False
        self.ia_only_mode = False
        self.ai_enabled = False

    def toggle_credits(self):
        self.show_credits = not self.show_credits

    def toggle_settings(self):
        self.show_settings = not self.show_settings
        if self.show_settings:
            self.show_notes = False
            self.show_credits = False
            self.show_help = False
            self.show_skins_panel = False

    def toggle_notes(self):
        self.show_notes = not self.show_notes
        self.notes_scroll = 0.0
        if self.show_notes:
            self.show_settings = False
            self.show_credits = False
            self.show_help = False
            self.show_skins_panel = False

    def toggle_help(self):
        self.show_help = not self.show_help
        self.help_scroll = 0.0
        if self.show_help:
            self.show_settings = False
            self.show_credits = False
            self.show_notes = False
            self.show_skins_panel = False

    def open_editor(self):
        self.show_settings = False
        self.show_credits = False
        self.show_notes = False
        self.show_help = False
        self.show_skins_panel = False
        self.level_editor.reset()
        self.state = "editor"

    def open_levels_menu(self):
        self.show_settings = False
        self.show_credits = False
        self.show_notes = False
        self.show_help = False
        self.show_skins_panel = False
        self.state = "levels_menu"
        self.levels_cursor = 0
        self.levels_scroll = 0
        self.level_import_buffer = ""
        self.import_mode = False
        self.levels_status = ""
        self.level_editor.login_mode = False

    def _handle_levels_event(self, e):
        levels = self.level_manager.list_levels()
        if e.type == pg.MOUSEWHEEL:
            self.levels_scroll += e.y * 30
            return
        if e.type != pg.KEYDOWN:
            return
        if self.import_mode:
            if e.key == pg.K_v and (e.mod & pg.KMOD_CTRL):
                pasted = self.game._paste_text()
                if pasted:
                    self.level_import_buffer = pasted.strip()
                return
            if e.key == pg.K_ESCAPE:
                self.import_mode = False
                return
            if e.key == pg.K_RETURN:
                lv = self.level_manager.import_code(self.level_import_buffer.strip())
                if lv:
                    self.level_manager.upsert_level(lv)
                    self.levels_status = "Niveau importe: %s" % lv.get("name", "?")
                else:
                    self.levels_status = "Code invalide"
                self.import_mode = False
                return
            if e.key == pg.K_BACKSPACE:
                self.level_import_buffer = self.level_import_buffer[:-1]
                return
            ch = e.unicode
            if ch and 32 <= ord(ch) <= 126:
                self.level_import_buffer += ch
            return
        if e.key == pg.K_ESCAPE:
            self.state = "menu"; return
        if e.key == pg.K_UP:
            self.levels_cursor = max(0, self.levels_cursor - 1)
        elif e.key == pg.K_DOWN:
            self.levels_cursor = min(max(0, len(levels)-1), self.levels_cursor + 1)
        elif e.key in (pg.K_RETURN, pg.K_SPACE):
            if levels:
                idx = min(self.levels_cursor, len(levels)-1)
                self.start_custom_level(levels[idx])
        elif e.key == pg.K_e and levels:
            idx = min(self.levels_cursor, len(levels)-1)
            code = self.level_manager.export_code(levels[idx])
            if code:
                copied = self._copy_text(code)
                self.levels_status = "Code copie" if copied else "Code: %s..." % code[:64]
            else:
                self.levels_status = "Export impossible"
        elif e.key == pg.K_i:
            self.import_mode = True
            self.level_import_buffer = ""
        elif e.key == pg.K_v and (e.mod & pg.KMOD_CTRL):
            pasted = self._paste_text()
            if pasted:
                lv = self.level_manager.import_code(pasted.strip())
                if lv:
                    self.level_manager.upsert_level(lv)
                    self.levels_status = "Niveau importe via presse-papier"
                else:
                    self.levels_status = "Code presse-papier invalide"
        elif e.key == pg.K_l and levels:
            idx = min(self.levels_cursor, len(levels)-1)
            self.level_editor.load_level(levels[idx])
            self.state = "editor"
        elif e.key == pg.K_o:
            self._open_auth_modal("login")

    def _handle_custom_complete_event(self, e):
        if e.type != pg.KEYDOWN:
            return
        if e.key in (pg.K_RETURN, pg.K_SPACE):
            if self.current_custom_level:
                self.start_custom_level(self.current_custom_level)
            return
        if e.key == pg.K_m:
            self.custom_running = False
            self.state = "menu"
            self._resume_music()
            return
        if pg.K_1 <= e.key <= pg.K_8:
            idx = e.key - pg.K_1
            if idx < len(DIFF_LABELS) and self.current_custom_level:
                if not self.current_custom_level.get("id"):
                    self.current_custom_level["id"] = self.level_manager.upsert_level(self.current_custom_level)
                label = DIFF_LABELS[idx]
                self.level_manager.vote_difficulty(self.current_custom_level["id"], label)
                self.levels_status = "Vote: %s" % label
            return

    def toggle_skins_panel(self):
        self.show_skins_panel = not self.show_skins_panel
        # remettre le skin sélectionné
        self.player.skin = SKINS[self.skin_idx]

    def next_skin(self):
        self.skin_idx = (self.skin_idx + 1) % len(SKINS)
        self.player.skin = SKINS[self.skin_idx]

    def prev_skin(self):
        self.skin_idx = (self.skin_idx - 1) % len(SKINS)
        self.player.skin = SKINS[self.skin_idx]

    # ---------- Events ----------
    def handle_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.quit_game()
            if e.type == MUSIC_END_EVENT:
                self._next_track()
                continue
            if self.state == "menu" and self.show_auth_modal:
                self._auth_handle_event(e)
                continue
            if self.state == "editor":
                self.level_editor.handle_event(e)
                continue
            if self.state == "levels_menu":
                self._handle_levels_event(e)
                continue
            if self.state == "custom_complete":
                self._handle_custom_complete_event(e)
                continue
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.quit_game()
                if e.key == pg.K_s:
                    if self.state == "menu": self.new_seed_menu()
                    elif self.state == "playing" and (not self.custom_running): self.new_seed()
                if e.key == pg.K_p and self.state == "playing":
                    self.state = "pause"
                elif e.key == pg.K_p and self.state == "pause":
                    self.state = "playing"
                if e.key == pg.K_i and self.state == "playing":
                    self.ai_enabled = not self.ai_enabled
                    self.player.ai_mode = self.ai_enabled
                if self.state == "pause" and e.key == pg.K_m:
                    self.state = "menu"; self._resume_music()
                if self.state == "menu" and self.show_skins_panel:
                    if e.key == pg.K_LEFT: self.prev_skin()
                    elif e.key == pg.K_RIGHT: self.next_skin()
                if self.state == "menu" and e.key in (pg.K_RETURN, pg.K_SPACE): self.reset()
                elif self.state == "dead" and e.key in (pg.K_r, pg.K_RETURN, pg.K_SPACE): self.reset()
                elif self.state == "dead" and e.key == pg.K_m:
                    self.state = "menu"; self._resume_music()
                elif self.state == "playing":
                    if e.key == pg.K_r: self.reset()
                    elif e.key == pg.K_g: self.god = not self.god
                    elif e.key == pg.K_c:
                        globals()['COMFORT_MODE'] = not globals()['COMFORT_MODE']
            # clics en menu
            if self.state == "menu":
                if self.show_notes:
                    if e.type == pg.MOUSEWHEEL:
                        self.notes_scroll += e.y * 22
                    if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                        self.btn_notes_back.handle_event(e)
                    continue
                if self.show_help:
                    if e.type == pg.MOUSEWHEEL:
                        self.help_scroll += e.y * 22
                    if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                        self.btn_help_back.handle_event(e)
                    continue
                if self.show_settings:
                    if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                        self._handle_settings_click(e.pos)
                        self.btn_settings_back.handle_event(e)
                    continue
                # boutons principaux
                for b in self.buttons:
                    b.handle_event(e)
                # copie github
                if self.show_credits and e.type == pg.MOUSEBUTTONDOWN and e.button == 1 and self.copy_btn_rect:
                    if self.copy_btn_rect.collidepoint(e.pos):
                        self._copy_github_link()

    # ---------- Update ----------
    def update(self, dt):
        if self.state != "playing": return
        if self.custom_running and self.world.custom_mode and self.world.world_x >= self.world.custom_length:
            self.custom_finished_success = True
            self.state = "custom_complete"
            self._pause_music()
            return
        if self.ai_enabled:
            self.player.ai_mode = True
            self.player.ai_dir = self.ai_decide()
            if self.ai_should_dash():
                self.player.ai_dash()
        else:
            self.player.ai_mode = False
        self.player.update(dt)
        boosted_trail = self.player.invulnerable() or self.player.spark_t > 0
        self.trail.emit(dt, self.player.x - self.player.r * 0.6, self.player.y, self.player.skin["col"], boosted_trail and self.dynamic_trails)
        self.trail.update(dt)
        if self.chaos_mode:
            base_scroll = self.world.scroll
            jitter = 1.0 + random.uniform(-0.18, 0.22)
            self.world.scroll = clamp(base_scroll * jitter, SCROLL_BASE * 0.5, SCROLL_BASE * 1.8)
            self.world.spawn_gap = clamp(self.world.spawn_gap * jitter, SPAWN_MIN, SPAWN_BASE * 1.2)
            self.world.update(dt)
            self.world.scroll = base_scroll
        else:
            self.world.update(dt)

        base = self.world.scroll * dt / 10.0
        self.score += base * self.player.mult
        # déclenche les respirations: max 3, tous les RELIEF_SCORE_STEP points
        if self.world.relief_used < RELIEF_MAX and self.score >= self.world.relief_next_score:
            self.world.relief_timer = RELIEF_TIME
            self.world.relief_used += 1
            self.world.relief_next_score += RELIEF_SCORE_STEP

        for o in self.world.obs:
            if isinstance(o, OneWayTP): o.collide(self.player)
            if isinstance(o, Turret):
                proj = o.spawn_projectile()
                if proj: self.world.obs.append(proj)

        if any(o.near(self.player, self.player.near_mask) for o in self.world.obs):
            prev_cd = self.player.near_sfx_cd
            self.player.on_near()
            if self.sfx_near and prev_cd <= 0:
                self.sfx_near.play()

        if self.zen_mode:
            self.player.alive = True
        if (not self.god) and self.player.alive and (not self.player.invulnerable()) and (not self.zen_mode):
            for o in self.world.obs:
                if not isinstance(o, OneWayTP) and o.collide(self.player):
                    self.player.alive = False
                    self._pause_music()
                    if self.sfx_death: self.sfx_death.play()
                    break

        if not self.player.alive:
            if self.custom_running:
                self.custom_finished_success = False
                self.state = "custom_complete"
            else:
                self.best_score = max(self.best_score, self.score)
                self._save_best()
                self.state = "dead"

    # ---------- Draw ----------
    def draw_hud(self):
        meters = int(self.world.world_x // 10)
        scr = int(self.score); best = int(self.best_score)
        draw_text(self.screen, f"Score: {scr}  (x{self.player.mult:.1f})", 28, 12, 10, "topleft")
        draw_text(self.screen, f"Record: {best}   Seed: {self.seed}", 18, 14, 44, "topleft", col=UI_DIM, bold=False)
        dash_txt = "Dash prêt" if self.player.dash_cd <= 0 else f"Dash: {self.player.dash_cd:.1f}s"
        draw_text(self.screen, dash_txt, 16, 14, 66, "topleft", col=UI_DIM, bold=False)
        draw_text(self.screen, f"Vitesse: {int(self.world.scroll)}  Densite: {int(self.world.spawn_gap)}  Dist(m): {meters}", 16, W-12, 12, "topright", col=UI_DIM, bold=False)
        if self.world.relief_timer > 0:
            draw_text(self.screen, "Respire...", 18, W-12, 34, "topright", col=LINE_COL, bold=False)
        if self.ai_enabled:
            draw_text(self.screen, "IA (I)", 18, W-12, 56, "topright", col=LINE_COL, bold=False)
        if self.god:
            draw_text(self.screen, "GOD MODE", 20, W//2, 12, "midtop")
            draw_text(self.screen, "G pour desactiver", 16, W//2, 36, "midtop", col=UI_DIM, bold=False)
        if COMFORT_MODE:
            draw_text(self.screen, "CONFORT ON (C)", 16, W//2, 58, "midtop", col=UI_DIM, bold=False)
        else:
            draw_text(self.screen, "CONFORT OFF (C)", 16, W//2, 58, "midtop", col=UI_DIM, bold=False)

    def _draw_title_block(self, lp_rect):
        # Titre + bande sombre pour lisibilite
        t = pg.time.get_ticks()/1000.0
        title_bob = int(math.sin(t*2.0) * 4)
        title_txt = "REFLEXE"
        # contour + ombre
        draw_text(self.screen, title_txt, 84, lp_rect.centerx, lp_rect.top + 12 + title_bob, "midtop", col=FG, shadow=True, stroke=True)
        # sous-titre optionnel (vide pour ne pas afficher)
        sub = ""
        if sub:
            band = pg.Rect(lp_rect.left+16, lp_rect.top+110, lp_rect.width-32, 30)
            pg.draw.rect(self.screen, (0,0,0,160), band, border_radius=6)
            sub_img = self.font_sub.render(sub, True, (230,230,230))
            self.screen.blit(sub_img, (band.left+10, band.top+4))

    def _draw_github_icon(self, surf, center, main_col=FG):
        cx, cy = center
        r = 11
        bg_col = (230, 235, 240)
        cat_col = main_col if len(main_col)==3 else main_col[:3]
        pg.draw.circle(surf, bg_col, (cx, cy), r+3)
        pg.draw.circle(surf, cat_col, (cx, cy+2), r)
        # decoupe pour le cou
        pg.draw.rect(surf, bg_col, pg.Rect(cx-6, cy+3, 12, 8))
        # oreilles
        pg.draw.polygon(surf, cat_col, [(cx-6, cy-2), (cx-8, cy-10), (cx-2, cy-4)])
        pg.draw.polygon(surf, cat_col, [(cx+6, cy-2), (cx+8, cy-10), (cx+2, cy-4)])
        # queue
        pg.draw.arc(surf, cat_col, pg.Rect(cx+4, cy+2, 10, 10), math.radians(30), math.radians(220), 3)

    def _draw_slider(self, label, rect, value, color):
        draw_text(self.screen, label, 16, rect.left, rect.top - 16, "topleft", col=UI_DIM, bold=False)
        pg.draw.rect(self.screen, (60, 60, 60), rect.inflate(4, 8), border_radius=10)
        pg.draw.rect(self.screen, (30, 30, 30), rect, border_radius=8)
        fill_w = int(rect.width * clamp(value, 0.0, 1.0))
        pg.draw.rect(self.screen, color, (rect.left, rect.top, fill_w, rect.height), border_radius=8)
        pct = int(value * 100)
        draw_text(self.screen, f"{pct}%", 14, rect.right - 4, rect.centery - 2, "midright", col=FG, bold=True)

    def _draw_settings_panel(self, popup_x=None, sr_override=None):
        if sr_override:
            sr = sr_override
        else:
            sr = pg.Rect(int(popup_x), int(H*0.12), int(W*0.36), 300)
        panel = make_panel(sr.width, sr.height)
        self.screen.blit(panel, sr.topleft)
        draw_text(self.screen, "Parametres", 26, sr.centerx, sr.top + 10, "midtop")

        music_rect = pg.Rect(sr.left + 18, sr.top + 60, sr.width - 36, 18)
        sfx_rect = pg.Rect(sr.left + 18, sr.top + 104, sr.width - 36, 18)
        self._draw_slider("Musique", music_rect, self.music_vol, (90, 180, 255))
        self._draw_slider("SFX", sfx_rect, self.sfx_vol, (255, 180, 120))

        comfort_rect = pg.Rect(sr.left + 18, sr.top + 144, 160, 32)
        pg.draw.rect(self.screen, (40, 40, 40), comfort_rect, border_radius=14)
        if COMFORT_MODE:
            pg.draw.rect(self.screen, (120, 200, 255), comfort_rect, 0, border_radius=14)
            draw_text(self.screen, "Confort ON", 16, comfort_rect.centerx, comfort_rect.centery-2, "center")
        else:
            pg.draw.rect(self.screen, (60, 60, 60), comfort_rect, 0, border_radius=14)
            draw_text(self.screen, "Confort OFF", 16, comfort_rect.centerx, comfort_rect.centery-2, "center", col=UI_DIM, bold=False)
        draw_text(self.screen, "Clique pour basculer", 12, comfort_rect.right + 6, comfort_rect.centery-2, "midleft", col=UI_DIM, bold=False)

        row_y = sr.top + 188
        btn_h = 30
        btn_w = 120
        # fps lock
        fps_rect = pg.Rect(sr.left + 18, row_y, btn_w, btn_h)
        pg.draw.rect(self.screen, (40, 40, 40), fps_rect, border_radius=10)
        pg.draw.rect(self.screen, BTN_BORDER, fps_rect, 1, border_radius=10)
        draw_text(self.screen, f"FPS: {self.fps_cap}", 14, fps_rect.centerx, fps_rect.centery-2, "center")

        theme_rect = pg.Rect(fps_rect.right + 12, row_y, btn_w, btn_h)
        pg.draw.rect(self.screen, (40, 40, 40), theme_rect, border_radius=10)
        pg.draw.rect(self.screen, BTN_BORDER, theme_rect, 1, border_radius=10)
        draw_text(self.screen, "Clair" if self.theme_light else "Sombre", 14, theme_rect.centerx, theme_rect.centery-2, "center")

        scan_rect = pg.Rect(theme_rect.right + 12, row_y, btn_w, btn_h)
        pg.draw.rect(self.screen, (40, 40, 40), scan_rect, border_radius=10)
        pg.draw.rect(self.screen, BTN_BORDER, scan_rect, 1, border_radius=10)
        draw_text(self.screen, "Scanlines ON" if self.enable_scanlines else "Scanlines OFF", 12, scan_rect.centerx, scan_rect.centery-2, "center")

        row2_y = row_y + btn_h + 10
        vignette_rect = pg.Rect(sr.left + 18, row2_y, btn_w + 20, btn_h)
        pg.draw.rect(self.screen, (40, 40, 40), vignette_rect, border_radius=10)
        pg.draw.rect(self.screen, BTN_BORDER, vignette_rect, 1, border_radius=10)
        draw_text(self.screen, "Vignette ON" if self.enable_vignette else "Vignette OFF", 12, vignette_rect.centerx, vignette_rect.centery-2, "center")

        trail_rect = pg.Rect(vignette_rect.right + 12, row2_y, btn_w + 20, btn_h)
        pg.draw.rect(self.screen, (40, 40, 40), trail_rect, border_radius=10)
        pg.draw.rect(self.screen, BTN_BORDER, trail_rect, 1, border_radius=10)
        draw_text(self.screen, "Trails dyn." if self.dynamic_trails else "Trails simples", 12, trail_rect.centerx, trail_rect.centery-2, "center")

        mode_rect = pg.Rect(sr.left + 18, row2_y + btn_h + 12, sr.width - 36, 32)
        pg.draw.rect(self.screen, (40, 40, 40), mode_rect, border_radius=12)
        pg.draw.rect(self.screen, BTN_BORDER, mode_rect, 1, border_radius=12)
        draw_text(self.screen, f"Mode: {self.mode_cycle[self.mode_idx]}", 14, mode_rect.centerx, mode_rect.centery-2, "center")
        hint = "Audio, confort, fps lock, theme, vignette/scanlines, trails dynamiques, modes bonus."
        draw_text(self.screen, hint, 12, sr.left + 18, sr.bottom - 18, "topleft", col=UI_DIM, bold=False)

        self.settings_hitboxes["music"] = music_rect
        self.settings_hitboxes["sfx"] = sfx_rect
        self.settings_hitboxes["comfort"] = comfort_rect
        self.settings_hitboxes["fps"] = fps_rect
        self.settings_hitboxes["theme"] = theme_rect
        self.settings_hitboxes["scan"] = scan_rect
        self.settings_hitboxes["vignette"] = vignette_rect
        self.settings_hitboxes["trail"] = trail_rect
        self.settings_hitboxes["mode"] = mode_rect

        # Auth card aside
        card = make_panel(int(sr.width * 0.9), 210)
        cr = card.get_rect(topright=(sr.right - 8, sr.top + 4))
        self.screen.blit(card, cr.topleft)
        draw_text(self.screen, "Compte", 22, cr.centerx, cr.top + 8, "midtop")
        pseudo = self.user_profile.get("pseudo", "") if self.user_profile else ""
        draw_text(self.screen, f"Connecte: {pseudo or 'aucun'}", 16, cr.left + 12, cr.top + 40, "topleft", col=UI_DIM, bold=False)

        btn_w, btn_h, pad = cr.width - 24, 34, 10
        btn_signup = pg.Rect(cr.left + 12, cr.top + 70, btn_w, btn_h)
        btn_login = pg.Rect(cr.left + 12, cr.top + 70 + btn_h + pad, btn_w, btn_h)
        btn_logout = pg.Rect(cr.left + 12, cr.top + 70 + 2*(btn_h + pad), btn_w, btn_h)
        btn_delete = pg.Rect(cr.left + 12, cr.top + 70 + 3*(btn_h + pad), btn_w, btn_h)
        for rect, txt in [(btn_signup, "Sign up"), (btn_login, "Login"), (btn_logout, "Logout"), (btn_delete, "Supprimer compte")]:
            pg.draw.rect(self.screen, BTN_BG, rect, border_radius=10)
            pg.draw.rect(self.screen, BTN_BORDER, rect, 2, border_radius=10)
            draw_text(self.screen, txt, 16, rect.centerx, rect.centery-8, "midtop")
        self.auth_buttons = {"signup": btn_signup, "login": btn_login, "logout": btn_logout, "delete": btn_delete}
        if self.show_auth_modal:
            modal_w, modal_h = 320, 240
            modal = make_panel(modal_w, modal_h, alpha=245)
            mr = modal.get_rect(center=(int(sr.left + sr.width*0.30), sr.centery))
            self.screen.blit(modal, mr.topleft)
            draw_text(self.screen, "Identification", 24, mr.centerx, mr.top + 12, "midtop")
            lab1 = "Pseudo"
            lab2 = "Mot de passe"
            draw_text(self.screen, lab1, 16, mr.left + 14, mr.top + 52, "topleft")
            draw_text(self.screen, lab2, 16, mr.left + 14, mr.top + 102, "topleft")
            inp1 = pg.Rect(mr.left + 12, mr.top + 70, modal_w - 24, 26)
            inp2 = pg.Rect(mr.left + 12, mr.top + 120, modal_w - 24, 26)
            for rect, active in [(inp1, self.auth_field=="pseudo"), (inp2, self.auth_field=="pwd")]:
                pg.draw.rect(self.screen, (20,20,20), rect, border_radius=6)
                pg.draw.rect(self.screen, ACCENT if active else BTN_BORDER, rect, 2, border_radius=6)
            draw_text(self.screen, self.auth_pseudo, 16, inp1.left + 8, inp1.centery-2, "midleft", col=FG)
            masked = "*"*len(self.auth_pwd)
            draw_text(self.screen, masked, 16, inp2.left + 8, inp2.centery-2, "midleft", col=FG)
            draw_text(self.screen, "Entree: valider / Echap: fermer / Tab: changer champ", 14, mr.centerx, mr.bottom - 18, "midtop", col=UI_DIM, bold=False)
        

    def _handle_settings_click(self, pos):
        if not self.settings_hitboxes:
            return
        music_rect = self.settings_hitboxes.get("music")
        sfx_rect = self.settings_hitboxes.get("sfx")
        comfort_rect = self.settings_hitboxes.get("comfort")
        fps_rect = self.settings_hitboxes.get("fps")
        theme_rect = self.settings_hitboxes.get("theme")
        scan_rect = self.settings_hitboxes.get("scan")
        vignette_rect = self.settings_hitboxes.get("vignette")
        trail_rect = self.settings_hitboxes.get("trail")
        mode_rect = self.settings_hitboxes.get("mode")
        if getattr(self, "auth_buttons", None):
            if self.auth_buttons["signup"].collidepoint(pos):
                self._prompt_signup()
                return
            if self.auth_buttons["login"].collidepoint(pos):
                self._prompt_login()
                return
            if self.auth_buttons["logout"].collidepoint(pos):
                self._logout_account()
                return
            if self.auth_buttons["delete"].collidepoint(pos):
                self._delete_account()
                return
        if music_rect and music_rect.collidepoint(pos):
            rel = (pos[0] - music_rect.left) / music_rect.width
            self.music_vol = clamp(rel, 0.0, 1.0)
            self._apply_audio_settings()
        elif sfx_rect and sfx_rect.collidepoint(pos):
            rel = (pos[0] - sfx_rect.left) / sfx_rect.width
            self.sfx_vol = clamp(rel, 0.0, 1.0)
            self._apply_audio_settings()
        elif comfort_rect and comfort_rect.collidepoint(pos):
            globals()['COMFORT_MODE'] = not globals()['COMFORT_MODE']
        elif fps_rect and fps_rect.collidepoint(pos):
            self.fps_cap = 120 if self.fps_cap == 60 else (0 if self.fps_cap == 120 else 60)
        elif theme_rect and theme_rect.collidepoint(pos):
            self.theme_light = not self.theme_light
            globals()['THEME_LIGHT'] = self.theme_light
        elif scan_rect and scan_rect.collidepoint(pos):
            self.enable_scanlines = not self.enable_scanlines
        elif vignette_rect and vignette_rect.collidepoint(pos):
            self.enable_vignette = not self.enable_vignette
        elif trail_rect and trail_rect.collidepoint(pos):
            self.dynamic_trails = not self.dynamic_trails
        elif mode_rect and mode_rect.collidepoint(pos):
            self.mode_idx = (self.mode_idx + 1) % len(self.mode_cycle)
            self.chaos_mode = (self.mode_cycle[self.mode_idx].lower() == "chaos")
            self.zen_mode = (self.mode_cycle[self.mode_idx].lower() == "zen")
            self.mirror_input = (self.mode_cycle[self.mode_idx].lower() == "mirror")
            self.ia_only_mode = (self.mode_cycle[self.mode_idx].lower() == "ia only")
            self.ai_enabled = self.ia_only_mode
            if self.player:
                self.player.mirror_input = self.mirror_input
                self.player.ia_only_mode = self.ia_only_mode

    def draw_notes_fullscreen(self):
        overlay = pg.Surface((W, H), pg.SRCALPHA)
        overlay.fill((2, 2, 6, 255))
        self.screen.blit(overlay, (0, 0))

        draw_text(self.screen, "Notes & Roadmap", 46, int(W*0.52), int(H*0.10), "midtop", shadow=True, stroke=True)
        draw_text(self.screen, "Releases, snapshots, patch notes et multijoueur", 20, int(W*0.52), int(H*0.17), "midtop", col=UI_DIM, bold=False)

        panel = make_panel(int(W*0.90), int(H*0.74))
        pr = panel.get_rect(center=(W//2, int(H*0.58)))
        self.screen.blit(panel, pr.topleft)

        content_clip = pr.inflate(-26, -30)
        prev_clip = self.screen.get_clip()
        self.screen.set_clip(content_clip)

        start_y = content_clip.top + 18
        y = start_y + self.notes_scroll
        sections = [
            ("Releases", RELEASE_NOTES, (90, 180, 255)),
            ("Snapshots", SNAPSHOT_NOTES, (160, 255, 200)),
            ("Patch notes", PATCH_NOTES, (255, 220, 120)),
            ("Roadmap", UPCOMING_NOTES, (255, 140, 160)),
        ]
        x = content_clip.left + 8
        for title, entries, col in sections:
            draw_text(self.screen, title, 22, x, y, "topleft", col=col)
            y += 24
            for entry in entries:
                draw_text(self.screen, f"{entry['ver']}  ({entry['date']})", 18, x + 10, y, "topleft")
                y += 18
                for it in entry["items"]:
                    draw_text(self.screen, f"- {it}", 16, x + 22, y, "topleft", col=UI_DIM, bold=False)
                    y += 18
                y += 6
            y += 12
        content_height = y - start_y - self.notes_scroll
        view_h = content_clip.height
        min_offset = min(0, view_h - content_height - 12)
        self.notes_scroll = clamp(self.notes_scroll, min_offset, 0)
        if content_height > view_h:
            scroll_range = (0 - min_offset) or 1
            bar_h = max(50, int(view_h * (view_h / content_height)))
            rel = abs(self.notes_scroll) / scroll_range
            bar_y = content_clip.top + int((view_h - bar_h) * rel)
            bar_x = pr.right - 12
            pg.draw.rect(self.screen, (80, 80, 80), (bar_x, bar_y, 4, bar_h), border_radius=4)

        self.screen.set_clip(prev_clip)

        self.btn_notes_back.update(pg.mouse.get_pos())
        self.btn_notes_back.draw(self.screen)

    def draw_settings_fullscreen(self):
        overlay = pg.Surface((W, H), pg.SRCALPHA)
        overlay.fill((2, 2, 6, 245))
        self.screen.blit(overlay, (0, 0))
        draw_text(self.screen, "Parametres", 46, int(W*0.52), int(H*0.10), "midtop", shadow=True, stroke=True)
        sr = pg.Rect(int(W*0.08), int(H*0.16), int(W*0.84), int(H*0.68))
        self._draw_settings_panel(sr_override=sr)

        self.btn_settings_back.update(pg.mouse.get_pos())
        self.btn_settings_back.draw(self.screen)

    def draw_help_fullscreen(self):
        overlay = pg.Surface((W, H), pg.SRCALPHA)
        overlay.fill((2, 2, 6, 245))
        self.screen.blit(overlay, (0, 0))
        draw_text(self.screen, "Aide & Infos", 46, int(W*0.52), int(H*0.10), "midtop", shadow=True, stroke=True)
        panel = make_panel(int(W*0.90), int(H*0.74))
        pr = panel.get_rect(center=(W//2, int(H*0.58)))
        self.screen.blit(panel, pr.topleft)

        content_clip = pr.inflate(-26, -30)
        prev_clip = self.screen.get_clip()
        self.screen.set_clip(content_clip)

        y = content_clip.top + 12 + self.help_scroll
        x = content_clip.left + 8
        sections = [
            ("Commandes", [
                "Souris/Haut/Bas : deplacement",
                "P : pause   /   M : menu",
                "C : Confort ON/OFF   /   G : GOD mode",
                "I : IA on/off (mode IA Only force l'IA)",
                "S : nouveau seed (menu ou en jeu)",
                "Entree / Espace : lancer une partie",
            ]),
            ("Editeur de niveaux", [
                "1-8 : choisir type (Tri, Laser, Clap, Drone, Mine, Tourelle, TP, Pulse)",
                "Clic: poser  /  F : mode precision (ghost couleur)",
                "Precision: A/D nudge X, W/S change de ligne, Entree pose au curseur",
                "[ ] : longueur niveau, T : taille (Petit->XXL), S : sauvegarder, Entree : tester",
                "Couleurs: piques rouge, lasers cyan, clap or, drone vert, mine rose, tourelle or, TP bleu, pulse violet",
            ]),
            ("Niveaux custom", [
                "Menu Niveaux: Haut/Bas pour choisir, Entree pour jouer",
                "E : exporter (copie code base64)  /  I ou Ctrl+V : importer un code colle",
                "Votes difficulte apres partie : 1-8 = Facile..AUTO (majorite)",
            ]),
            ("Modes bonus", [
                "Zen : pas de mort (entrainement tranquille)",
                "Chaos : vitesse et spawn fluctuent",
                "Mirror : commandes inversees",
                "IA Only : l'IA joue a votre place",
            ]),
            ("Audio & Musique", [
                "Volume musique/SFX ajustables (Parametres)",
                "Playlist auto : tous les .mp3/.ogg/.wav/.flac dans /app/musi ou /app",
                "Passage auto au morceau suivant en fin de piste",
            ]),
            ("Cosmetiques & QoL", [
                "Skins via succes + skins prestige (a venir)",
                "Particules personnalisees, trails dynamiques",
                "Theme clair/sombre, FPS lock, scanlines/vignette toggles",
            ]),
            ("Astuce", [
                "Gauche/Droite : changer de skin dans le menu",
                "Dash : Shift (si dispo) ; TP: auto sur portail quand tp_cd <= 0",
                "IA: active avec I ou via mode IA Only",
            ]),
        ]
        for title, items in sections:
            draw_text(self.screen, title, 22, x, y, "topleft", col=ACCENT)
            y += 22
            for it in items:
                draw_text(self.screen, f"- {it}", 16, x + 12, y, "topleft", col=UI_DIM, bold=False)
                y += 18
            y += 8
        content_height = y - (content_clip.top + 12) - self.help_scroll
        view_h = content_clip.height
        min_offset = min(0, view_h - content_height - 8)
        self.help_scroll = clamp(self.help_scroll, min_offset, 0)
        if content_height > view_h:
            scroll_range = (0 - min_offset) or 1
            bar_h = max(40, int(view_h * (view_h / content_height)))
            rel = abs(self.help_scroll) / scroll_range
            bar_y = content_clip.top + int((view_h - bar_h) * rel)
            bar_x = pr.right - 12
            pg.draw.rect(self.screen, (80, 80, 80), (bar_x, bar_y, 4, bar_h), border_radius=4)

        self.screen.set_clip(prev_clip)
        self.btn_help_back.update(pg.mouse.get_pos())
        self.btn_help_back.draw(self.screen)

    def draw_levels_menu(self):
        t = pg.time.get_ticks()/1000.0
        draw_background(self.screen, t, self.bg_theme_idx)
        panel = make_panel(int(W*0.92), int(H*0.84))
        pr = panel.get_rect(center=(W//2, H//2))
        self.screen.blit(panel, pr.topleft)
        draw_text(self.screen, "Niveaux custom", 42, pr.centerx, pr.top + 12, "midtop", shadow=True, stroke=True)
        draw_text(self.screen, "Entrer: jouer  |  Haut/Bas: selection  |  E: code partage  |  I / Ctrl+V: importer  |  Esc: menu", 16, pr.centerx, pr.top + 52, "midtop", col=UI_DIM, bold=False)

        list_rect = pg.Rect(pr.left + 18, pr.top + 80, pr.width - 36, pr.height - 170)
        levels = self.level_manager.list_levels()
        content_h = len(levels) * 56
        min_offset = min(0, list_rect.height - content_h - 10)
        self.levels_scroll = clamp(self.levels_scroll, min_offset, 0)

        start_y = list_rect.top + self.levels_scroll
        for idx, lv in enumerate(levels):
            y = start_y + idx * 56
            item_rect = pg.Rect(list_rect.left, int(y), list_rect.width, 50)
            if item_rect.bottom < list_rect.top or item_rect.top > list_rect.bottom:
                continue
            active = (idx == self.levels_cursor)
            pg.draw.rect(self.screen, (30, 34, 46) if active else (18, 20, 26), item_rect, border_radius=8)
            pg.draw.rect(self.screen, BTN_BORDER, item_rect, width=1, border_radius=8)
            diff = self.level_manager.current_difficulty(lv)
            name = lv.get("name", "Sans nom")
            author = lv.get("author", {}).get("pseudo", "??")
            size = lv.get("size", "Moyen")
            votes = lv.get("difficulty_votes", {})
            total_votes = sum(votes.values()) if votes else 0
            draw_text(self.screen, f"{name}", 22, item_rect.left + 12, item_rect.top + 6, "topleft", col=FG)
            draw_text(self.screen, f"Auteur: {author}   Taille: {size}   Difficulte: {diff} ({total_votes} votes)", 16, item_rect.left + 12, item_rect.top + 28, "topleft", col=UI_DIM, bold=False)
            draw_text(self.screen, f"{len(lv.get('objects', []))} objets", 16, item_rect.right - 12, item_rect.centery, "topright", col=LINE_COL, bold=False)

        if content_h > list_rect.height:
            bar_h = max(40, int(list_rect.height * (list_rect.height / max(1, content_h))))
            scroll_range = (0 - min_offset) or 1
            rel = abs(self.levels_scroll) / scroll_range
            bar_y = list_rect.top + int((list_rect.height - bar_h) * rel)
            bar_x = list_rect.right - 8
            pg.draw.rect(self.screen, (80,80,80), (bar_x, bar_y, 4, bar_h), border_radius=4)

        info_y = list_rect.bottom + 12
        status = self.levels_status or "Importer un code base64 (I ou Ctrl+V) ou exporter (E)."
        if self.import_mode:
            status = "Import code (Entrer pour valider, Echap pour annuler, Ctrl+V pour coller) : " + self.level_import_buffer
        draw_text(self.screen, status, 16, pr.left + 16, info_y, "topleft", col=ACCENT, bold=False)

    def draw_custom_complete(self):
        self.screen.fill(BG)
        lvl_name = self.current_custom_level.get("name", "Niveau custom") if self.current_custom_level else "Niveau custom"
        draw_text(self.screen, lvl_name, 48, W//2, 120, "midtop", shadow=True, stroke=True)
        res = "TERMINE" if self.custom_finished_success else "ECHEC"
        draw_text(self.screen, res, 36, W//2, 176, "midtop", col=ACCENT if self.custom_finished_success else ACCENT_ALT, shadow=True)
        draw_text(self.screen, f"Score: {int(self.score)}   Longueur: {int(self.world.custom_length)}", 22, W//2, 230, "midtop")
        draw_text(self.screen, "Vote difficulte (1-8) : Facile / Moyen / Dur / Extra / Mega / Insane / Extreme / AUTO", 18, W//2, 280, "midtop", col=UI_DIM, bold=False)
        draw_text(self.screen, "Entrer pour rejouer   |   M pour menu", 18, W//2, 310, "midtop", col=UI_DIM, bold=False)

    def draw_menu(self, dt):
        t = pg.time.get_ticks() / 1000.0
        draw_background(self.screen, t, self.bg_theme_idx)
        self.world.update(1/180.0)
        self.world.draw(self.screen, t, player_y=None)

        if self.enable_vignette:
            self.screen.blit(self.vignette, (0, 0))
        lp = self.left_panel
        lp_rect = lp.get_rect(topleft=(int(W*0.06), int(H*0.18)))
        self.screen.blit(lp, lp_rect.topleft)

        # scanlines en dehors du panneau pour laisser le texte clean
        if self.enable_scanlines:
            draw_scanlines(self.screen, spacing=MENU_SCAN_SPACING, alpha=MENU_SCAN_ALPHA,
                           clip_rect=lp_rect.inflate(20,20))

        self._draw_title_block(lp_rect)
        self.settings_hitboxes = {}

        mouse = pg.mouse.get_pos()
        for b in self.buttons:
            b.update(mouse); b.draw(self.screen)

        sp = self.small_panel
        sp_rect = sp.get_rect(topleft=(int(W*0.06), lp_rect.bottom + 20))
        self.screen.blit(sp, sp_rect.topleft)
        tip = "Entree/Espace: Jouer - S: Seed - Echap: Quitter - G: GOD - C: Confort - Fleches G/D: Skin"
        tip_img = self.font_small.render(tip, True, UI_DIM)
        self.screen.blit(tip_img, (sp_rect.left + 12, sp_rect.top + 12))
        self.screen.blit(self.font_sub.render(f"Skin: {SKINS[self.skin_idx]['name']}", True, FG), (sp_rect.left + 12, sp_rect.top + 38))
        self.screen.blit(self.font_sub.render(f"Seed actuel: {self.seed}", True, FG), (sp_rect.left + 12, sp_rect.top + 62))

        # popups alignes a droite, bien espaces
        popup_x = int(W * 0.62)

        if self.show_credits:
            cred = make_panel(int(W*0.34), 180)
            cr_rect = cred.get_rect(topleft=(popup_x, int(H*0.14)))
            self.screen.blit(cred, cr_rect.topleft)
            draw_text(self.screen, "Credits", 28, cr_rect.centerx, cr_rect.top + 12, "midtop")
            draw_text(self.screen, "Jeu par BiblitechLab", 20, cr_rect.centerx, cr_rect.top + 42, "midtop", col=UI_DIM, bold=False)
            draw_text(self.screen, "Plus d'info via le lien ci-dessous", 16, cr_rect.centerx, cr_rect.top + 68, "midtop", col=UI_DIM, bold=False)
            url_y = cr_rect.top + 94
            self._draw_github_icon(self.screen, (cr_rect.left + 26, url_y + 8), main_col=LINE_COL)
            draw_text(self.screen, GITHUB_URL, 16, cr_rect.left + 44, url_y, "topleft", col=LINE_COL, bold=False)
            # bouton copier
            btn_w, btn_h = 180, 30
            btn_rect = pg.Rect(0, 0, btn_w, btn_h)
            btn_rect.center = (cr_rect.centerx, cr_rect.top + 130)
            self.copy_btn_rect = btn_rect
            pg.draw.rect(self.screen, (40, 40, 40), btn_rect, border_radius=8)
            pg.draw.rect(self.screen, FG, btn_rect, width=2, border_radius=8)
            draw_text(self.screen, "Copier le lien", 16, btn_rect.centerx, btn_rect.centery-10, "midtop")
            if self.copy_feedback_t > 0:
                draw_text(self.screen, "Copié !", 14, btn_rect.centerx, btn_rect.bottom + 6, "midtop", col=LINE_COL, bold=False)
        else:
            self.copy_btn_rect = None
        if self.copy_feedback_t > 0:
            self.copy_feedback_t -= dt

        if self.show_skins_panel:
            panel = make_panel(int(W*0.30), 130)
            pr = panel.get_rect(topleft=(popup_x, int(H*0.34)))
            self.screen.blit(panel, pr.topleft)
            draw_text(self.screen, "Skins", 26, pr.centerx, pr.top + 12, "midtop")
            sk = SKINS[self.skin_idx]
            draw_text(self.screen, f"Actif: {sk['name']}", 18, pr.centerx, pr.top + 44, "midtop", col=UI_DIM, bold=False)
            draw_text(self.screen, f"Style: {sk['style']}", 16, pr.centerx, pr.top + 66, "midtop", col=UI_DIM, bold=False)
            draw_text(self.screen, "Fleches G/D pour changer", 14, pr.centerx, pr.top + 90, "midtop", col=UI_DIM, bold=False)

        # ghost player a droite
        bob_lane = int((math.sin(t*1.6) + 1.0) * 0.5 * (len(self.world.corr_centers)-1))
        ghost_y = self.world.corr_centers[bob_lane]
        pg.draw.circle(self.screen, FG, (int(W*0.78), int(ghost_y)), PLAYER_R, 2)
        pg.draw.line(self.screen, FG, (W*0.78 - PLAYER_R - 6, ghost_y), (W*0.78 + PLAYER_R + 6, ghost_y), 1)
        pg.draw.line(self.screen, FG, (W*0.78, ghost_y - PLAYER_R - 6), (W*0.78, ghost_y + PLAYER_R + 6), 1)

        if self.show_notes:
            self.draw_notes_fullscreen()
        if self.show_settings:
            self.draw_settings_fullscreen()
        if self.show_help:
            self.draw_help_fullscreen()

    def draw_dead(self):
        self.screen.fill(BG)
        scr = int(self.score); best = int(self.best_score)
        draw_text(self.screen, "Game Over !", 58, W//2, 210, "midtop", shadow=True, stroke=True)
        draw_text(self.screen, f"Score: {scr}    Record: {best}    Seed: {self.seed}", 26, W//2, 270, "midtop")
        draw_text(self.screen, "R / Entree / Espace / Clic : Recommencer    -    S : seed aleatoire", 20, W//2, 320, "midtop")
        draw_text(self.screen, "M : Retour menu", 18, W//2, 360, "midtop", col=UI_DIM, bold=False)

    def draw_play(self):
        t = pg.time.get_ticks()/1000.0
        draw_background(self.screen, t, self.bg_theme_idx)
        self.world.draw(self.screen, t, player_y=self.player.y)
        self.trail.draw(self.screen)
        if self.god:
            pg.draw.circle(self.screen, FG, (int(self.player.x), int(self.player.y)), self.player.r + 6, 1)
        self.player.draw(self.screen, t)
        if self.enable_vignette:
            self.screen.blit(self.play_vignette, (0, 0))
        self.draw_hud()

    def draw_pause(self):
        # on réutilise l'état courant sans update
        self.draw_play()
        overlay = pg.Surface((W, H), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))
        draw_text(self.screen, "Pause", 42, W//2, H//2 - 40, "midtop")
        draw_text(self.screen, "P : Reprendre   /   M : Menu", 20, W//2, H//2 + 6, "midtop", col=UI_DIM, bold=False)
    def run(self):
        while True:
            cap = self.fps_cap if self.fps_cap else 240
            dt = self.clock.tick(cap)/1000.0
            self.handle_events()
            if self.state == "menu":
                self.draw_menu(dt)
            elif self.state == "playing":
                self.update(dt); self.draw_play()
            elif self.state == "pause":
                self.draw_pause()
            elif self.state == "dead":
                self.draw_dead()
            elif self.state == "editor":
                self.level_editor.draw(self.screen)
            elif self.state == "levels_menu":
                self.draw_levels_menu()
            elif self.state == "custom_complete":
                self.draw_custom_complete()
            pg.display.flip()

    # ---------- IA ----------
    def _ai_cell_size(self):
        speed = max(140.0, getattr(self.world, "scroll", SCROLL_BASE))
        base = speed * AI_CELL_SCROLL_FAC
        return clamp(base, AI_CELL_X_MIN, AI_CELL_X_MAX)

    def _ai_time_penalty(self, obj, time_to_reach):
        if time_to_reach <= 0:
            return 0.0
        if isinstance(obj, LaserSegment):
            state = obj.state
            timer = obj.timer
            t = time_to_reach
            while t > timer:
                t -= timer
                if state == "tele":
                    state = "active"; timer = LASER_ACTIVE
                elif state == "active":
                    state = "cool"; timer = LASER_COOLDOWN
                else:
                    state = "tele"; timer = LASER_TELE
            if state == "active" or (state == "tele" and t < 0.12):
                return AI_NEAR_COST * 2
        if isinstance(obj, Clapet):
            state = obj.state
            timer = obj.timer
            t = time_to_reach
            while t > timer:
                t -= timer
                if state == "rest":
                    state = "active"; timer = CLAP_ACTIVE
                else:
                    state = "rest"; timer = CLAP_REST
            if state == "active":
                return AI_NEAR_COST * 1.4
        return 0.0

    def _ai_risk_matrix(self, lanes, steps, cell_x):
        p = self.player
        risk = [[0.0 for _ in lanes] for _ in range(steps)]
        safe_run = [0 for _ in lanes]
        backup_y, backup_lane = p.y, p.lane
        max_dist = cell_x * steps + 80
        for o in self.world.obs:
            ox = ob_x(o)
            dx = ox - PLAYER_X
            if dx < -80 or dx > max_dist:
                continue
            step = max(0, min(steps-1, int(dx // cell_x)))
            time_to_reach = dx / max(1.0, self.world.scroll)
            close_weight = 1.0 + ((steps - step) / steps) * (AI_CLOSE_WEIGHT - 1.0)
            for li in lanes:
                p.y = self.world.corr_centers[li]
                p.lane = li
                if o.collide(p):
                    lane_risk = AI_COLL_COST
                elif o.near(p, p.near_mask):
                    lane_risk = AI_NEAR_COST
                else:
                    lane_risk = max(0.0, (cell_x * (step+1) - dx)) * AI_DIST_COST
                lane_risk += self._ai_time_penalty(o, time_to_reach)
                risk[step][li] += lane_risk * close_weight
        p.y, p.lane = backup_y, backup_lane

        for li in lanes:
            streak = 0; best = 0
            for s in range(steps):
                if risk[s][li] < AI_NEAR_COST * 0.6:
                    streak += 1
                else:
                    best = max(best, streak); streak = 0
            safe_run[li] = max(best, streak)
        return risk, safe_run, cell_x

    def ai_decide(self):
        p = self.player
        lanes = list(range(len(self.world.corr_centers)))
        cur_lane = p.lane
        if len(lanes) <= 1:
            return 0
        cell_x = self._ai_cell_size()
        risk, safe_run, _ = self._ai_risk_matrix(lanes, AI_STEPS, cell_x)

        dp = [[1e9 for _ in lanes] for _ in range(AI_STEPS)]
        prev = [[None for _ in lanes] for _ in range(AI_STEPS)]
        for li in lanes:
            dp[0][li] = risk[0][li] + (abs(li - cur_lane) * AI_LANE_CHANGE_COST) - (safe_run[li] * AI_SAFE_LANE_BONUS)
        for s in range(1, AI_STEPS):
            for li in lanes:
                for lj in lanes:
                    cost = dp[s-1][lj] + risk[s][li]
                    if li != lj:
                        cost += AI_LANE_CHANGE_COST * abs(li - lj)
                    else:
                        cost -= AI_SAFE_LANE_BONUS * 0.5
                    if risk[s][li] >= AI_COLL_COST:
                        cost += AI_DEAD_END_PENALTY
                    if cost < dp[s][li]:
                        dp[s][li] = cost
                        prev[s][li] = lj

        end_lane = min(range(len(lanes)), key=lambda l: dp[AI_STEPS-1][l])
        if end_lane < cur_lane: return -1
        if end_lane > cur_lane: return 1
        return 0

    def ai_should_dash(self):
        p = self.player
        if p.invulnerable() or p.dash_cd > 0:
            return False

        lanes = list(range(len(self.world.corr_centers)))
        if not lanes:
            return False

        cell_x = self._ai_cell_size()
        steps = min(AI_DASH_LOOK_STEPS, AI_STEPS)
        risk, _, _ = self._ai_risk_matrix(lanes, steps, cell_x)

        if all(risk[0][li] >= AI_NEAR_COST for li in lanes):
            return True

        lane_totals = [sum(risk[s][li] for s in range(steps)) for li in lanes]
        if min(lane_totals) >= AI_EMERGENCY_THRESHOLD:
            return True

        for s in range(steps):
            collisions = [risk[s][li] >= AI_COLL_COST for li in lanes]
            if all(collisions):
                return True
        return False


if __name__ == "__main__":
    Game().run()

