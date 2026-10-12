import math
import random
import pygame

# COOKIE QUEST: DELUXE
# Move: WASD/arrows | Dash: SPACE | Pause: P | Restart: R | Quit: ESC
pygame.init()
W, H, FPS, ROUND = 900, 620, 60, 75
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Cookie Quest: Deluxe")
clock = pygame.time.Clock()
F = pygame.font.Font(None, 29)
S = pygame.font.Font(None, 21)
TITLE = pygame.font.Font(None, 72)
BIG = pygame.font.Font(None, 45)
INK=(43,35,68); CREAM=(255,247,231); PINK=(255,218,232); PINK2=(239,179,208)
WHITE=(255,255,255); BLUE=(100,175,255); BLUE2=(45,104,177)
BROWN=(153,91,48); CHOC=(83,47,35); RED=(242,83,106); ORANGE=(255,169,76)
GOLD=(255,211,81); PURPLE=(165,125,242); MINT=(112,220,180)
PR=18

def label(msg, font, color, pos, center=False):
    img=font.render(str(msg), True, color); r=img.get_rect()
    r.center=pos if center else r.topleft
    if not center: r.topleft=pos
    screen.blit(img,r)

def panel(rect, color=WHITE, border=PINK2):
    pygame.draw.rect(screen,(218,194,221),(rect.x,rect.y+5,rect.w,rect.h),border_radius=22)
    pygame.draw.rect(screen,color,rect,border_radius=22)
    if border: pygame.draw.rect(screen,border,rect,3,border_radius=22)

def pos_random(m=45):
    return pygame.Vector2(random.randint(m,W-m),random.randint(95,H-m))

def cookie(gold=False):
    return {"pos":pos_random(),"gold":gold,"born":pygame.time.get_ticks()}

def enemy(level):
    edge=random.choice(("top","left","right","bottom"))
    if edge=="top": p=pygame.Vector2(random.randint(20,W-20),70)
    elif edge=="bottom": p=pygame.Vector2(random.randint(20,W-20),H-20)
    elif edge=="left": p=pygame.Vector2(10,random.randint(80,H-20))
    else: p=pygame.Vector2(W-10,random.randint(80,H-20))
    return {"pos":p,"speed":random.uniform(1.1,1.7)+level*.16,
            "r":random.choice((15,17,19)),"phase":random.random()*6}

def burst(p,color,n=14):
    out=[]
    for _ in range(n):
        a=random.random()*math.tau; sp=random.uniform(1,4)
        out.append({"p":pygame.Vector2(p),"v":pygame.Vector2(math.cos(a),math.sin(a))*sp,
                    "life":random.randint(16,32),"c":color,"r":random.randint(2,5)})
    return out

def draw_cookie(p,gold=False):
    x,y=int(p.x),int(p.y); r=15 if gold else 13
    pygame.draw.circle(screen,(226,177,113),(x,y+3),r+1)
    pygame.draw.circle(screen,GOLD if gold else BROWN,(x,y),r)
    for dx,dy,rr in [(-4,-4,3),(5,2,3),(1,-7,2),(-2,6,2)]:
        pygame.draw.circle(screen,WHITE if gold else CHOC,(x+dx,y+dy),rr)

def draw_player(p, inv=False, shield=False):
    x,y=int(p.x),int(p.y)
    if shield: pygame.draw.circle(screen,MINT,(x,y),29,3)
    if inv and pygame.time.get_ticks()//80%2==0: return
    pygame.draw.ellipse(screen,(218,195,226),(x-20,y-12,40,39))
    pygame.draw.circle(screen,BLUE2,(x,y),PR+2); pygame.draw.circle(screen,BLUE,(x,y-2),PR)
    for dx in (-6,6):
        pygame.draw.circle(screen,WHITE,(x+dx,y-5),5)
        pygame.draw.circle(screen,INK,(x+dx+1,y-4),2)
    pygame.draw.arc(screen,INK,(x-7,y-1,14,11),0,math.pi,2)
    pygame.draw.circle(screen,(255,160,181),(x-11,y+3),3)
    pygame.draw.circle(screen,(255,160,181),(x+11,y+3),3)

def draw_enemy(e):
    x,y=int(e["pos"].x),int(e["pos"].y); r=e["r"]
    pygame.draw.circle(screen,(194,55,83),(x,y+3),r+1); pygame.draw.circle(screen,RED,(x,y),r)
    pygame.draw.circle(screen,ORANGE,(x-3,y-4),5); pygame.draw.circle(screen,WHITE,(x+5,y-4),4)
    pygame.draw.circle(screen,INK,(x+6,y-3),2)
    pygame.draw.arc(screen,INK,(x-5,y+1,10,7),math.pi,math.tau,2)

def powerup():
    return {"pos":pos_random(),"kind":random.choice(("shield","speed","magnet")),
            "born":pygame.time.get_ticks()}

def draw_powerup(o):
    x,y=int(o["pos"].x),int(o["pos"].y)
    color={"shield":MINT,"speed":ORANGE,"magnet":PURPLE}[o["kind"]]
    pygame.draw.circle(screen,WHITE,(x,y),19); pygame.draw.circle(screen,color,(x,y),15)
    symbol={"shield":"S","speed":">","magnet":"M"}[o["kind"]]
    label(symbol,F,WHITE,(x,y),True)

def background():
    screen.fill(CREAM)
    for x in range(18,W,42):
        for y in range(80,H,42): pygame.draw.circle(screen,(247,228,236),(x,y),2)

def new_game():
    now=pygame.time.get_ticks()
    return {"player":pygame.Vector2(W/2,H/2),"cookies":[cookie()],
            "gold":None,"enemies":[enemy(1)],"powerups":[],"particles":[],
            "score":0,"lives":3,"level":1,"start":now,"enemy_at":now,
            "gold_at":now,"power_at":now,"inv":0,"shield":0,"speed":0,
            "magnet":0,"dash_at":0,"state":"playing"}

mode="menu"; g=None; best=0; running=True
while running:
    clock.tick(FPS); now=pygame.time.get_ticks()
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT: running=False
        if ev.type==pygame.KEYDOWN:
            if ev.key==pygame.K_ESCAPE: running=False
            elif mode=="menu" and ev.key in (pygame.K_RETURN,pygame.K_SPACE):
                g=new_game(); mode="playing"
            elif mode in ("over","win") and ev.key==pygame.K_r:
                g=new_game(); mode="playing"
            elif mode=="playing" and ev.key==pygame.K_p: mode="paused"
            elif mode=="paused" and ev.key==pygame.K_p: mode="playing"
            elif mode=="playing" and ev.key==pygame.K_SPACE and now>=g["dash_at"]:
                k=pygame.key.get_pressed(); d=pygame.Vector2(0,0)
                if k[pygame.K_LEFT] or k[pygame.K_a]: d.x-=1
                if k[pygame.K_RIGHT] or k[pygame.K_d]: d.x+=1
                if k[pygame.K_UP] or k[pygame.K_w]: d.y-=1
                if k[pygame.K_DOWN] or k[pygame.K_s]: d.y+=1
                if d.length_squared()==0: d.x=1
                g["player"]+=d.normalize()*100
                g["player"].x=max(PR,min(W-PR,g["player"].x))
                g["player"].y=max(84+PR,min(H-PR,g["player"].y))
                g["inv"]=now+400; g["dash_at"]=now+1900
                g["particles"]+=burst(g["player"],BLUE,18)

    background()
    if mode=="menu":
        panel(pygame.Rect(125,100,650,420))
        draw_cookie(pygame.Vector2(210,170),True); draw_cookie(pygame.Vector2(690,450))
        label("COOKIE QUEST",TITLE,INK,(W//2,185),True)
        label("DELUXE EDITION",BIG,PURPLE,(W//2,235),True)
        label("Collect cookies. Dodge grumpy blobs. Grab power-ups.",S,INK,(W//2,285),True)
        panel(pygame.Rect(280,320,340,58),PINK)
        label("PRESS ENTER TO PLAY",F,INK,(W//2,349),True)
        label("MOVE WASD/ARROWS   DASH SPACE   PAUSE P",S,INK,(W//2,405),True)
        label("Golden cookies = 5 points!",S,PURPLE,(W//2,445),True)
    else:
        if mode=="playing":
            k=pygame.key.get_pressed(); d=pygame.Vector2(0,0)
            if k[pygame.K_LEFT] or k[pygame.K_a]: d.x-=1
            if k[pygame.K_RIGHT] or k[pygame.K_d]: d.x+=1
            if k[pygame.K_UP] or k[pygame.K_w]: d.y-=1
            if k[pygame.K_DOWN] or k[pygame.K_s]: d.y+=1
            speed=4.5*(1.55 if now<g["speed"] else 1)
            if d.length_squared(): g["player"]+=d.normalize()*speed
            g["player"].x=max(PR,min(W-PR,g["player"].x))
            g["player"].y=max(84+PR,min(H-PR,g["player"].y))
            g["level"]=1+g["score"]//8
            if now-g["enemy_at"]>max(420,1400-g["level"]*100):
                g["enemies"].append(enemy(g["level"])); g["enemy_at"]=now
            if g["gold"] is None and now-g["gold_at"]>9000:
                g["gold"]=cookie(True); g["gold_at"]=now
            if now-g["power_at"]>11500 and not g["powerups"]:
                g["powerups"].append(powerup()); g["power_at"]=now
            for e in g["enemies"]:
                d=g["player"]-e["pos"]
                if d.length_squared():
                    d=d.normalize()
                    wob=pygame.Vector2(math.sin(now/230+e["phase"]),math.cos(now/280+e["phase"]))*.3
                    e["pos"]+=(d+wob)*e["speed"]
            if now<g["magnet"]:
                for c in g["cookies"]:
                    d=g["player"]-c["pos"]
                    if d.length_squared(): c["pos"]+=d.normalize()*2
            for c in g["cookies"][:]:
                if g["player"].distance_to(c["pos"])<PR+13:
                    g["cookies"].remove(c); g["score"]+=1
                    g["particles"]+=burst(c["pos"],BROWN)
                    g["cookies"].append(cookie())
            if g["gold"] and g["player"].distance_to(g["gold"]["pos"])<PR+16:
                g["score"]+=5; g["particles"]+=burst(g["gold"]["pos"],GOLD,26)
                g["gold"]=None; g["gold_at"]=now
            if g["gold"] and now-g["gold"]["born"]>6500: g["gold"]=None
            for o in g["powerups"][:]:
                if now-o["born"]>8500: g["powerups"].remove(o)
                elif g["player"].distance_to(o["pos"])<PR+16:
                    g["powerups"].remove(o); g["particles"]+=burst(o["pos"],PURPLE,18)
                    g[o["kind"]]=now+6500
            if now>=g["inv"] and now>=g["shield"]:
                for e in g["enemies"]:
                    if g["player"].distance_to(e["pos"])<PR+e["r"]:
                        g["lives"]-=1; g["inv"]=now+1600
                        g["particles"]+=burst(g["player"],RED,22)
                        for enemy_obj in g["enemies"]:
                            away=enemy_obj["pos"]-g["player"]
                            if away.length_squared(): enemy_obj["pos"]+=away.normalize()*60
                        break
            for p in g["particles"]:
                p["p"]+=p["v"]; p["v"]*=.94; p["life"]-=1
            g["particles"]=[p for p in g["particles"] if p["life"]>0]
            best=max(best,g["score"])
            if g["lives"]<=0: mode="over"
            elif now-g["start"]>=ROUND*1000: mode="win"

        # HUD
        pygame.draw.rect(screen,WHITE,(0,0,W,66)); pygame.draw.line(screen,PINK2,(0,65),(W,65),3)
        label("COOKIE QUEST",F,INK,(18,20)); label(f"🍪 {g['score']}",F,INK,(245,20))
        label(f"LEVEL {g['level']}",F,PURPLE,(350,20))
        label(f"TIME {max(0,math.ceil((ROUND*1000-(now-g['start']))/1000)):02d}",F,INK,(W-145,20))
        label("LIVES",S,INK,(W-285,23))
        for i in range(g["lives"]):
            x=W-220+i*24
            pygame.draw.circle(screen,RED,(x-4,27),6); pygame.draw.circle(screen,RED,(x+4,27),6)
            pygame.draw.polygon(screen,RED,[(x-10,29),(x+10,29),(x,40)])
        for c in g["cookies"]: draw_cookie(c["pos"])
        if g["gold"]: draw_cookie(g["gold"]["pos"],True)
        for o in g["powerups"]: draw_powerup(o)
        for e in g["enemies"]: draw_enemy(e)
        for p in g["particles"]:
            pygame.draw.circle(screen,p["c"],(int(p["p"].x),int(p["p"].y)),max(1,int(p["r"]*p["life"]/28)))
        draw_player(g["player"],now<g["inv"],now<g["shield"])
        if now<g["speed"]: label("SPEED BOOST!",S,ORANGE,(15,H-28))
        if now<g["magnet"]: label("COOKIE MAGNET!",S,PURPLE,(150,H-28))
        if now<g["shield"]: label("SHIELD ACTIVE!",S,(45,130,177),(310,H-28))
        label("SPACE: DASH",S,INK,(W-135,H-28))
        if mode=="paused":
            shade=pygame.Surface((W,H),pygame.SRCALPHA); shade.fill((43,35,68,150)); screen.blit(shade,(0,0))
            panel(pygame.Rect(245,225,410,150))
            label("PAUSED",TITLE,INK,(W//2,270),True); label("Press P to resume",F,INK,(W//2,325),True)
        elif mode in ("over","win"):
            shade=pygame.Surface((W,H),pygame.SRCALPHA); shade.fill((255,247,231,210)); screen.blit(shade,(0,0))
            panel(pygame.Rect(205,150,490,320))
            label("COOKIE CHAMPION!" if mode=="win" else "GAME OVER",BIG,PURPLE if mode=="win" else RED,(W//2,210),True)
            label(f"Cookies collected: {g['score']}",F,INK,(W//2,270),True)
            label(f"Level reached: {g['level']}",F,INK,(W//2,310),True)
            label(f"Best score this session: {best}",S,PURPLE,(W//2,350),True)
            panel(pygame.Rect(325,390,250,48),PINK)
            label("PRESS R TO RESTART",S,INK,(W//2,414),True)
    pygame.display.flip()
pygame.quit()
