import lvgl as lv
import wlsdk
import gc
import math
gc.collect()

swatch=card=lbl_hex=lbl_rgb=lbl_status=dot=None
status_timer=idle_timer=anim_t=0
anim_active=fp_held=False
cur_r=97
cur_g=47
cur_b=139
lum=sat=100

def clamp(v):
    return 0 if v<0 else 255 if v>255 else int(v)

def h2(n):
    x="0123456789ABCDEF"
    return x[n//16]+x[n%16]

def get_rgb():
    gray=(cur_r+cur_g+cur_b)//3
    sf=sat/100;lf=lum/100
    return clamp(int((gray+(cur_r-gray)*sf)*lf)),clamp(int((gray+(cur_g-gray)*sf)*lf)),clamp(int((gray+(cur_b-gray)*sf)*lf))

def refresh():
    r,g,b=get_rgb()
    swatch.set_style_bg_color(lv.color_make(r,g,b),0)
    lbl_hex.set_text("#"+h2(r)+h2(g)+h2(b))
    lbl_rgb.set_text(str(r)+","+str(g)+","+str(b))

def reset_anim():
    global idle_timer,anim_active,anim_t
    idle_timer=anim_t=0
    anim_active=False
    swatch.set_style_bg_grad_dir(lv.GRAD_DIR.NONE,0)

def show_status(msg):
    global status_timer
    lbl_status.set_text(msg)
    status_timer=30

def build_ui():
    global swatch,card,lbl_hex,lbl_rgb,lbl_status,dot
    root=wlsdk.ui.get_root()
    root.set_style_bg_color(lv.color_hex(0x000000),0)
    root.set_style_pad_all(0,0)
    lbl_status=lv.label(root)
    lbl_status.set_text("")
    lbl_status.set_style_text_color(lv.color_hex(0xFFFFFF),0)
    lbl_status.set_style_text_font(wlsdk.ui.FONT.SMALL,0)
    lbl_status.align(lv.ALIGN.TOP_MID,0,6)
    swatch=lv.obj(root)
    swatch.set_size(156,306)
    swatch.set_style_bg_color(lv.color_make(0,0,0),0)
    swatch.set_style_border_width(0,0)
    swatch.set_style_radius(20,0)
    swatch.set_style_pad_all(0,0)
    swatch.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
    swatch.align(lv.ALIGN.CENTER,0,0)
    dot=lv.obj(swatch)
    dot.set_size(10,10)
    dot.set_style_bg_opa(0,0)
    dot.set_style_bg_color(lv.color_hex(0x000000),0)
    dot.set_style_radius(6,0)
    dot.set_style_border_width(0,0)
    dot.set_style_pad_all(0,0)
    dot.align(lv.ALIGN.TOP_LEFT,14,14)
    card=lv.obj(swatch)
    card.set_size(142,60)
    card.set_style_bg_color(lv.color_hex(0x000000),0)
    card.set_style_bg_opa(150,0)
    card.set_style_radius(15,0)
    card.set_style_border_width(0,0)
    card.set_style_pad_all(8,0)
    card.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
    card.align(lv.ALIGN.BOTTOM_MID,0,-7)
    lbl_hex=lv.label(card)
    lbl_hex.set_text("#000000")
    lbl_hex.set_style_text_color(lv.color_hex(0xFFFFFF),0)
    lbl_hex.set_style_text_font(wlsdk.ui.FONT.MEDIUM,0)
    lbl_hex.set_style_text_align(lv.TEXT_ALIGN.CENTER,0)
    lbl_hex.align(lv.ALIGN.TOP_MID,0,2)
    lbl_rgb=lv.label(card)
    lbl_rgb.set_text("0,0,0")
    lbl_rgb.set_style_text_color(lv.color_hex(0xAAAAAA),0)
    lbl_rgb.set_style_text_font(wlsdk.ui.FONT.SMALL,0)
    lbl_rgb.set_style_text_align(lv.TEXT_ALIGN.CENTER,0)
    lbl_rgb.align(lv.ALIGN.TOP_MID,0,26)

def on_color_received(ctx,params):
    global cur_r,cur_g,cur_b,lum,sat
    if params:
        cur_r=params["r"];cur_g=params["g"];cur_b=params["b"]
        lum=sat=100
        gc.collect()
        reset_anim()
        refresh()
    wlsdk.rpc.send_response(ctx,None)

wlsdk.rpc.register("color.data",on_color_received)

def start():
    wlsdk.ui.set_stay_on_screen(True)
    wlsdk.ui.set_grab_input(True)
    build_ui()
    refresh()

def update():
    global status_timer,idle_timer,anim_active,anim_t
    if status_timer>0:
        status_timer-=1
        if status_timer==0:lbl_status.set_text("")
    if not anim_active:
        idle_timer+=1
        if idle_timer>100:anim_active=True
        return
    anim_t=(anim_t+0.07)%6.28
    r,g,b=get_rgb()
    t=(math.sin(anim_t)+1)/2
    r1=clamp(r+(255-r)*t*0.6)
    g1=clamp(g+(255-g)*t*0.4)
    b1=clamp(b+(255-b)*t*0.4)
    t2=(math.sin(anim_t+1.5)+1)/2
    boost=1.0+t2*1.2
    gray=(r+g+b)//3
    r2=clamp(gray+(r-gray)*boost)
    g2=clamp(gray+(g-gray)*boost)
    b2=clamp(gray+(b-gray)*boost)
    swatch.set_style_bg_color(lv.color_make(r1,g1,b1),0)
    swatch.set_style_bg_grad_color(lv.color_make(r2,g2,b2),0)
    swatch.set_style_bg_grad_dir(lv.GRAD_DIR.VER,0)

def on_event(event_type,event_index,event_value):
    global lum,sat,fp_held,cur_r,cur_g,cur_b
    if event_type==wlsdk.EVENT.BUTTON:
        if event_index==5:
            if event_value==wlsdk.EVENT.BUTTON_DOWN:
                fp_held=not fp_held
                dot.set_style_bg_opa(255 if fp_held else 0,0)
            return
        if event_value!=wlsdk.EVENT.BUTTON_DOWN:return
        if event_index<1 or event_index>4:return
        reset_anim();refresh()
        if event_index==2:
            if fp_held:
                wlsdk.rpc.send_notify("color.capture","")
        elif event_index==1:
              if fp_held:
                r,g,b=get_rgb()
                wlsdk.rpc.send_notify("color.copy_hex",str(r)+","+str(g)+","+str(b))
    elif event_type==wlsdk.EVENT.ENCODER:
        if not fp_held:return
        reset_anim()
        d=5 if event_value==wlsdk.EVENT.ENCODER_RIGHT else -5
        if event_index==0:
            sat=sat+d
            if sat<0:sat=0
            if sat>200:sat=200
        elif event_index==1:
            cur_r=clamp(cur_r+d*3)
            cur_g=clamp(cur_g-d)
            cur_b=clamp(cur_b-d*2)
        refresh()

def end():
    wlsdk.ui.set_grab_input(False)
    wlsdk.ui.set_stay_on_screen(False)
