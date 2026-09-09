#!/usr/bin/env python3
"""Build deterministic SVG figures from validated public evidence; standard library only."""
import base64
from html import escape
import json
from pathlib import Path
from validate import load
from validate_evidence import validate_evidence

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'evidence/study-0001-v1'
READER = CASE / 'reader'
INK, MUTED, BG, GRID = '#eef3fa', '#a6b5c8', '#121f30', '#30445c'
BLUE, ORANGE, ROSE, VIOLET, GRAY = '#8cbaff', '#efb45c', '#ee9da6', '#b9a0f6', '#788da8'


class Figure:
    def __init__(self, title, subtitle, height, mobile=False):
        self.w = 600 if mobile else 1000
        self.mobile = mobile
        font = base64.b64encode((READER/'vendor/roboto.woff2').read_bytes()).decode()
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{height}" viewBox="0 0 {self.w} {height}" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>',
                      f'<style>@font-face{{font-family:Roboto;src:url(data:font/woff2;base64,{font})}}text{{font-family:Roboto,Arial,sans-serif;font-variant-numeric:tabular-nums}}</style>',
                      f'<rect width="100%" height="100%" fill="{BG}"/>']
        self.text(32, 32, 'ASTRA FIELD STUDY', 14 if not mobile else 18, ORANGE, weight=700)
        self.text(32, 80, title, 32 if not mobile else 29, weight=500)
        self.text(32, 117, subtitle, 19 if not mobile else 21, MUTED)

    def text(self, x, y, value, size=24, color=INK, anchor='start', weight=400):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(value))}</text>')

    def rect(self, x, y, w, h, color, **attrs):
        extra = ' '.join(f'{k}="{v}"' for k, v in attrs.items())
        self.parts.append(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="{color}" {extra}/>')

    def line(self, x1, y1, x2, y2, color=GRID):
        self.parts.append(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="1"/>')

    def save(self, name):
        (READER/'figures'/f'{name}{"-mobile" if self.mobile else ""}.svg').write_text('\n'.join(self.parts)+ '\n</svg>\n')


def daily(e, mobile):
    vals = [r['responses'] for r in sorted(e['usage']['by_day'], key=lambda r:r['day'])]
    f = Figure('25,254 recorded responses', 'Six study days · Day 6 ends at the cutoff', 520, mobile)
    left, right, bottom, height = 70, f_end(mobile), 416, 235
    for n in [0, 5000, 10000]:
        y = bottom-n/11000*height
        f.line(left,y,right,y)
        f.text(left-10,y+6,f'{n//1000}k',19,MUTED,'end')
    step = (right-left)/6
    for i,v in enumerate(vals):
        x=left+step*(i+.5); h=v/11000*height
        f.rect(x-step*.29,bottom-h,step*.58,h,ORANGE if v==max(vals) else BLUE)
        f.text(x,bottom-h-15,f'{v:,}',23 if mobile else 25,anchor='middle',weight=500)
        f.text(x,bottom+36,str(i+1) if mobile else f'Day {i+1}',24,anchor='middle')
    f.text(32,494,'Study day',21,MUTED)
    f.save('responses-by-day')


def f_end(mobile):
    return 565 if mobile else 956


def composition(e,mobile):
    s=e['coded_observations']['summary']
    groups=[('Routine',s['routine'],GRAY),('Dissatisfaction only',s['D_only'],ROSE),('Correction only',s['C_only'],ORANGE),('Both',s['both'],VIOLET),('Ambiguous',s['ambiguous'], '#52647d')]
    f=Figure('538 reviewed contributions','Each square represents one contribution',960 if mobile else 590,mobile)
    colors=[col for _,n,col in groups for _ in range(n)]
    assert len(colors)==s['eligible']
    for i,col in enumerate(colors):
        f.rect(32+(i%26)*19,158+(i//26)*17,14,12,col)
    for i,(label,n,col) in enumerate(groups):
        x,y=(32+(i%2)*285,610+(i//2)*104) if mobile else (584,181+i*72)
        f.rect(x,y-18,12,12,col)
        f.text(x+24,y,label,23 if mobile else 21)
        f.text(x+24,y+31,f'{n}   {100*n/s["eligible"]:.1f}%',26,INK if col in (GRAY, "#52647d") else col,weight=500)
    f.text(32,925 if mobile else 558,'147 corrective = 56 correction only + 91 both',22,MUTED)
    f.save('steering-partition')


def token(e,mobile):
    t=e['usage']['summary']['tokens']; ratio=t['cached_input_tokens']/t['input_tokens']
    f=Figure('98.21% of input was cached','Input tokens reused from earlier context',620 if mobile else 420,mobile)
    width=f.w-64
    f.rect(32,155,width*ratio,44,BLUE)
    f.rect(32+width*ratio,155,width*(1-ratio),44,ORANGE)
    blocks=[('Cached input',f'{t["cached_input_tokens"]/1e9:.2f}B',BLUE),('Uncached input',f'{t["uncached_input_tokens"]/1e6:.2f}M',ORANGE),('Output',f'{t["output_tokens"]/1e6:.2f}M',VIOLET)]
    for i,(label,value,color) in enumerate(blocks):
        x,y=(32,257+i*110) if mobile else (32+i*322,260)
        f.text(x,y,label,23,MUTED)
        f.text(x,y+46,value,42,color,weight=500)
    if not mobile:f.text(32,377,'3.42B total tokens · Output includes reasoning',21,MUTED)
    f.save('token-composition')


def matrix(e,mobile):
    projects=sorted(x['project'] for x in e['usage']['by_project'])
    cells={}
    for x in e['usage']['by_day_project_observer']:
        k=(x['day'],x['project']);cells[k]=cells.get(k,0)+x['responses']
    maximum=max(cells.values())
    f=Figure('Response activity by project','Responses per day; darker cells have fewer',1050 if mobile else 1020,mobile)
    left,step,rowh=(100,76,43) if mobile else (175,128,41)
    for d in range(1,7):f.text(left+(d-1)*step+step/2,168,str(d) if mobile else f'Day {d}',24,anchor='middle')
    for i,p in enumerate(projects):
        y=187+i*rowh
        f.text(left-12,y+rowh*.62,p[-2:] if mobile else p,24,anchor='end')
        for d in range(1,7):
            n=cells.get((d,p),0);a=n/maximum
            rgb=tuple(round(lo+a*(hi-lo)) for lo,hi in zip((24,41,62),(140,186,255)))
            f.rect(left+(d-1)*step,y,step-5,rowh-5,'#'+''.join(f'{c:02x}' for c in rgb))
            f.text(left+(d-1)*step+(step-5)/2,y+rowh*.64,f'{n:,}',24 if mobile else 22,INK if a<.70 else '#0d1522','middle')
    f.text(32,1015 if mobile else 985,'Project names are withheld for privacy.',21,MUTED)
    f.save('day-project-matrix')


def repo(e,mobile):
    rows=sorted(e['repository_activity']['by_project'],key=lambda r:-r['events']['pr_merged_in_window'])
    maxv=max(x['events']['pr_merged_in_window'] for x in rows)
    f=Figure('410 PRs merged in the window','17 repositories · Includes all authors',930,mobile)
    left,right=(110,500) if mobile else (165,887)
    for i,r in enumerate(rows):
        y=179+i*39;n=r['events']['pr_merged_in_window'];x=left+n/maxv*(right-left)
        f.text(left-16,y+8,r['project'][-2:] if mobile else r['project'],24,anchor='end')
        f.line(left,y,right,y)
        f.line(left,y,x,y,BLUE)
        f.parts.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{ORANGE if i==0 else BLUE}"/>')
        f.text(x+15,y+8,str(n),24,weight=500)
    f.text(32,900,'Project names are withheld for privacy.',21,MUTED)
    f.save('repository-merges')


def outcomes(e,mobile):
    s=e['coded_observations']['summary']
    # Canonical outcome keys are mapped explicitly below.
    values=[('Confirmed resolved',s['outcomes']['confirmed_resolved'],BLUE),('Accepted with waiver',s['outcomes']['accepted_with_residual_or_waived'],VIOLET),('Fix reported',s['outcomes']['fix_reported_unverified'],ORANGE),('Claim withdrawn',s['outcomes']['claim_withdrawn_artifact_unverified'],ROSE),('No closure established',s['outcomes']['no_closure_established'],GRAY)]
    f=Figure('78 correction episodes','What the reviewed conversations show',770 if mobile else 610,mobile)
    assert sum(n for _,n,_ in values)==s['correction_episodes']
    for i,(label,n,color) in enumerate(values):
        if mobile:
            y=172+i*105;f.text(32,y,label,25);f.rect(32,y+18,(f.w-128)*n/45,20,color);f.text(552,y+35,str(n),27,anchor='end')
        else:
            y=179+i*73;f.text(32,y+22,label,25);f.rect(365,y,515*n/45,28,color);f.text(940,y+23,str(n),28,anchor='end')
    f.text(32,735 if mobile else 576,'Later outcomes were not reviewed.',21,MUTED)
    f.save('episode-outcomes')


def main():
    e=load(CASE/'evidence.json');validate_evidence(e)
    for mobile in (False,True):
        for render in (daily,composition,token,matrix,repo,outcomes):render(e,mobile)
    print('Built six SVG figures at desktop and mobile footprints from canonical evidence.')

if __name__=='__main__':main()
