"""Draw the 128px mark and render four English store assets with Chromium."""
from pathlib import Path
import base64
import json
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
COLORS = json.loads((ROOT / 'manifest.json').read_text('utf-8-sig'))['theme']['colors']
def color(key):
    return '#%02X%02X%02X' % tuple(COLORS[key])

LOGO = 'data:image/png;base64,' + base64.b64encode((ROOT/'logo/logo128.png').read_bytes()).decode()
css = '''
*{box-sizing:border-box}body{margin:0;font-family:Arial,sans-serif;color:var(--ink)}
:root{--paper:#F1F3F5;--lavender:#C1C1E6;--rose:#A9A4D0;--pink:#D6DBF5}
.browser{width:1280px;height:800px;background:var(--ntp);position:relative;overflow:hidden}
.tabs{height:44px;background:var(--frame);color:var(--inactive);display:flex;align-items:end;gap:8px;padding:7px 12px 0}
.tab{width:228px;height:37px;border-radius:12px 12px 0 0;padding:11px 16px;font-size:13px}
.tab.active{background:var(--toolbar);color:var(--ink)}.close{float:right}.newtab{padding:9px 12px;font-size:22px}
.window-controls{margin-left:auto;display:flex;gap:30px;padding:11px 12px;font-size:16px}
.tools{height:52px;background:var(--toolbar);display:flex;align-items:center;padding:0 18px;gap:23px;font-size:22px}
.omni{height:36px;flex:1;background:var(--omni);border-radius:24px;display:flex;align-items:center;gap:13px;font-size:13px;padding:0 16px}
.omni .star{margin-left:auto;font-size:21px}.tune{font-size:18px}.profile{width:27px;height:27px;background:var(--frame);color:white;border-radius:50%;font-size:13px;display:grid;place-items:center}
.bookmarks{height:33px;background:var(--toolbar);border-bottom:1px solid #49385018;padding:9px 22px;display:flex;gap:30px;font-size:12px}
.content{text-align:center;padding-top:128px}.google{font-size:82px;line-height:1.15;letter-spacing:-4px;color:var(--accent);font-weight:500;margin-bottom:34px}
.search{width:590px;height:52px;border-radius:30px;background:var(--omni);margin:auto;display:flex;align-items:center;gap:18px;padding:0 22px;box-shadow:0 2px 9px #49385018;color:#6D626F;font-size:15px}
.search svg{width:20px;height:20px;stroke:var(--ink);fill:none;stroke-width:2}.search .mic{margin-left:auto}
.shortcuts{display:flex;justify-content:center;gap:35px;margin-top:31px}.shortcut{width:84px;font-size:12px}.circle{margin:0 auto 11px;width:47px;height:47px;border-radius:50%;display:grid;place-items:center;background:var(--toolbar);font-size:21px;color:var(--accent)}
.customize{position:absolute;right:22px;bottom:20px;border-radius:20px;background:var(--toolbar);padding:10px 16px;font-size:12px}
.intro{width:1280px;height:800px;background:#252B3A;color:#F7FBFC;padding:55px 65px;position:relative}
.eyebrow{font-size:12px;letter-spacing:3px;color:var(--accent)}h1{font-family:Georgia,serif;font-weight:normal}
.intro h1{font-size:53px;margin:18px 0 12px}.intro .subtitle{font-size:21px;margin:0}.intro .logo{position:absolute;right:69px;top:44px;width:100px;height:100px}
.cards{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:40px}.card{grid-column:span 1;height:205px;padding:25px;border:1px solid #49385022;border-radius:18px;display:flex;flex-direction:column;justify-content:end}
.card:nth-child(n+4){grid-column:span 1}.card strong{font-size:23px}.card .hex{font-size:15px;margin-top:10px}.card .role{font-size:14px;margin-top:8px}.intro .eyebrow{color:#D6DBF5}.intro .foot{font-size:15px;margin-top:29px}
.promo{background:var(--paper);position:relative;overflow:hidden}.small{width:440px;height:280px;display:flex;align-items:center;justify-content:center;text-align:center}
.small .copy{display:flex;align-items:center;flex-direction:column;transform:translateY(-4px)}.small img{width:78px;height:78px;margin-top:-9px;margin-bottom:2px}.small h1{font-size:29px;margin:5px 0 12px}.small p{font-size:13px;margin:0 0 19px}.small .eyebrow{font-size:10px;letter-spacing:3px}
.wide{width:1400px;height:560px}.wide .copy{position:absolute;left:61px;top:72px;width:390px}.wide img{width:94px;height:94px;margin:-15px 0 -3px -6px}.wide h1{font-size:55px;line-height:1.04;margin:8px 0 21px}.wide p{font-size:20px;line-height:1.55;margin:0 0 26px}.wide .preview{position:absolute;left:510px;top:77px;transform:scale(.66);transform-origin:top left;border:1px solid #957DAD70;border-radius:15px;overflow:hidden;box-shadow:0 18px 45px #49385022}.wide .browser{height:614px}.wide .content{padding-top:68px}.wide .cloud{position:absolute;width:620px;height:240px;border-radius:55% 45% 0 0;background:var(--lavender);right:-60px;bottom:-98px}.wide .cloud:before{content:'';position:absolute;width:320px;height:170px;border-radius:50%;background:var(--pink);left:-160px;bottom:-20px}
'''
css += ':root{' + ';'.join('--'+a+':'+color(b) for a,b in [
    ('frame','frame'),('toolbar','toolbar'),('omni','omnibox_background'),
    ('ntp','ntp_background'),('ink','ntp_text'),('accent','ntp_link'),
    ('inactive','tab_background_text')]) + '}'

def browser():
    return '''<div class="browser"><div class="tabs"><div class="tab">Reading list <span class="close">×</span></div><div class="tab">Inspiration <span class="close">×</span></div><div class="tab">Extensions <span class="close">×</span></div><div class="tab active">◉ &nbsp; New Tab <span class="close">×</span></div><div class="newtab">+</div><div class="window-controls"><span>−</span><span>□</span><span>×</span></div></div>
    <div class="tools"><span class="disabled">←</span><span class="disabled">→</span><span>↻</span><span>⌂</span><div class="omni"><span class="g-icon">G</span><span class="address-ai">✧ AI Mode</span><span>⌕</span></div><span>♧</span><div class="profile">P</div><span>⋮</span></div>
    <div class="bookmarks"><span>▦</span><span>▱ Tools</span><span>▱ AI</span><span>▱ UI</span><span>▱ Navigation</span><span>▱ API</span><span>▱ Dev</span></div>
    <div class="ntp-top">Images &nbsp;&nbsp;&nbsp; ▦</div>
    <div class="content"><div class="google">Google</div><div class="search"><span class="plus">+</span><span class="prompt">Ask Google</span><svg class="mic" viewBox="0 0 24 24"><rect x="9" y="2" width="6" height="12" rx="3" fill="#202124" stroke="none"/><path d="M5 10v2a7 7 0 0 0 14 0v-2M12 19v4"/></svg><svg viewBox="0 0 24 24"><path d="M8 4H5v4M16 4h3v4M5 16v3h3M19 16v3h-3"/><circle cx="12" cy="11" r="3"/><circle cx="17" cy="17" r="1" fill="#202124"/></svg><span class="ai-mode">✧ AI Mode</span></div>
    <div class="ai-cards"><div><span class="card-icon">✧</span><section><b>Try AI Mode</b><small>Create, summarize, plan</small></section></div><div><span class="card-icon">✦</span><section><b>Create images</b><small>Imagine, edit, draw</small></section></div></div>
    <div class="shortcuts"><div class="shortcut"><div class="circle"><span class="youtube">▶</span></div>YouTube</div><div class="shortcut"><div class="circle"><span class="store-icon">▣</span></div>Chrome Web Store</div><div class="shortcut"><div class="circle">+</div>Add shortcut</div></div></div><div class="customize">✎ &nbsp; Customize Chrome</div></div>'''

# Native UI colors sampled from the user's installed Chrome screenshot.
# These browser-controlled colors are distinct from manifest link/header colors.
css += '''
.tabs{height:38px;padding-top:5px;gap:5px}.tab{width:185px;height:33px;padding:9px 14px}.tools{height:44px;gap:19px;font-size:20px}.disabled{opacity:.42}
.omni{height:35px;border:2px solid #6C7E9C;padding:0 8px;gap:10px}.g-icon{background:white;color:#4285F4;font-size:21px;font-weight:bold;width:27px;height:27px;border-radius:50%;display:grid;place-items:center}.address-ai{margin-left:auto;background:var(--toolbar);padding:4px 10px;border-radius:20px;color:#202124}
.bookmarks{height:32px;padding:8px 13px;gap:23px;color:#685B70;border-bottom-color:#D5BEC9}
.ntp-top{position:absolute;right:22px;top:136px;font-size:13px;color:#303134}
.content{padding-top:106px}.google{color:#628BF1;font-size:80px;letter-spacing:-4px;margin-bottom:40px}
.search{width:630px;height:48px;background:#FFFFFF;color:#202124;border:1px solid #E5E5E5;padding:0 17px;gap:16px}.search svg{width:17px;height:19px;stroke:#202124}.plus{font-size:26px}.prompt{color:#B2B2B2;font-size:16px}.ai-mode{background:#F3F5F6;border-radius:22px;padding:8px 10px;font-size:12px;white-space:nowrap}
.ai-cards{display:flex;justify-content:center;gap:12px;margin-top:14px;text-align:left}.ai-cards>div{width:203px;height:48px;border-radius:15px;background:#3C4043;color:#E8F0FE;display:flex;align-items:center;gap:11px;padding:10px 14px}.card-icon{font-size:23px}.ai-cards b{font-weight:normal;font-size:13px;display:block}.ai-cards small{font-size:11px;display:block;margin-top:4px}
.shortcuts{margin-top:49px;gap:20px}.shortcut{width:76px;color:#685B70;font-size:11px;white-space:nowrap}.circle{width:41px;height:41px;margin-bottom:16px;background:#8FACF5;color:#202124;font-size:26px}.youtube{background:#FF0033;color:white;font-size:13px;border-radius:5px;padding:2px 6px}.store-icon{color:#4285F4;background:#FAF7F9;font-size:24px;line-height:25px}
.customize{right:12px;bottom:10px;background:#202124;color:#A8C7FA;box-shadow:0 2px 6px #0003;padding:8px 14px}
.wide .content{padding-top:65px}.wide .google{margin-bottom:25px}.wide .shortcuts{margin-top:34px}
'''

palette = [
    ('Mist Lavender', '#A9A4D0', 'Window frame', '#373449'),
    ('Soft Periwinkle', '#C1C1E6', 'Logo breeze accents', '#373449'),
    ('Pale Periwinkle', '#D6DBF5', 'Toolbar & active tab', '#373449'),
    ('Icy Blue', '#E8EEFD', 'New tab background', '#373449'),
]
cards=''.join(f'<div class="card" style="background:{c};color:{fg}"><strong>{n}</strong><span class="hex">{c}</span><span class="role">{role}</span></div>' for n,c,role,fg in palette)
intro=f'<div class="intro"><img class="logo" src="{LOGO}" alt="Cloud and sunset mark"><div class="eyebrow">A QUIETER SHADE OF WINTER</div><h1>Winter Whisper Theme</h1><p class="subtitle">A quiet winter moment in every tab.</p><div class="cards">{cards}</div><p class="foot">Solid colors · Cool pastel palette · Minimal design · No permissions required</p></div>'
small=f'<div class="promo small"><div class="copy"><img src="{LOGO}"><h1>Winter Whisper</h1><p>A quiet winter moment in every tab.</p><div class="eyebrow">CHROME THEME</div></div></div>'
wide=f'<div class="promo wide"><div class="cloud"></div><div class="copy"><img src="{LOGO}"><h1>Winter<br>Whisper</h1><p>Soft lavender. Winter blue.<br>A calmer space for everyday browsing.</p><div class="eyebrow">CHROME THEME</div></div><div class="preview">{browser()}</div></div>'
css += '.wide .cloud{background:transparent}.wide .cloud:before{background:transparent}.wide .cloud:after{content:"✧";position:absolute;left:380px;top:20px;font-size:110px;color:#C1C1E6;opacity:.4}'
jobs=[('screenshot-1-browser',1280,800,browser(),'screenshots/en/screenshot-1-browser.png'),('screenshot-2-introduction',1280,800,intro,'screenshots/en/screenshot-2-introduction.png'),('promo-440x280',440,280,small,'promo/440x280.png'),('promo-1400x560',1400,560,wide,'promo/1400x560.png')]
with sync_playwright() as p:
    engine=p.chromium.launch(headless=True)
    page=engine.new_page(device_scale_factor=1)
    for name,w,h,body,destination in jobs:
        html='<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Winter Whisper Theme</title><style>'+css+'</style></head><body>'+body+'</body></html>'
        reference=ROOT/'store-assets/references'/f'{name}.html'
        reference.parent.mkdir(parents=True,exist_ok=True)
        reference.write_text(html,'utf-8')
        page.set_viewport_size({'width':w,'height':h})
        page.set_content(html)
        page.evaluate('document.fonts.ready')
        png=reference.with_suffix('.png')
        page.screenshot(path=str(png))
        target=ROOT/'store-assets'/destination
        target.parent.mkdir(parents=True,exist_ok=True)
        with Image.open(png) as img:
            assert img.size == (w,h)
            img.convert('RGB').save(target)
        print(f'Rendered {destination}: {w}x{h}')
    engine.close()
print('Logo validated: logo/logo128.png, 128x128 RGBA')



