#!/usr/bin/env python3
"""Render the reader's documented Markdown subset; no third-party dependencies.

Supports headings, paragraphs, simple lists, tables, links, bold and inline code.
Figure comments refer to the explicit public figure catalog below. All other
HTML is escaped. This is a small renderer for these authored files, not a
replacement for a general Markdown engine.
"""
from html import escape
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
READER=ROOT/'evidence/brad-groux-six-days-v1/reader'
FIGURES={
 'responses-by-day': ('Recorded responses by relative study day', '25,254 responses across six relative days. Day 6 ends at the common cutoff. Source: recorded usage in evidence.json.'),
 'steering-partition': ('Exclusive categories among 538 substantive contributions', 'Each square represents one contribution. The five categories are exclusive: 310 routine, 63 dissatisfaction only, 56 correction only, 91 both, and 18 ambiguous. Source: contextual review, protocol 1.1.'),
 'token-composition': ('Cached and uncached input tokens, with output shown separately', 'The strip divides input tokens into cached and uncached input. Output is shown separately and includes reasoning. Source: recorded usage in evidence.json.'),
 'day-project-matrix': ('Recorded response counts for six days and eighteen generic projects', 'Each cell reports an exact response count. The color scale is linear and fixed across all cells. Project numbers are generic labels. Source: recorded usage in evidence.json.'),
 'episode-outcomes': ('Recorded outcomes for 78 correction episodes', 'Fourteen episodes were confirmed resolved in the reviewed context. Forty-five had no established closure; their later status is unknown. Source: contextual review, protocol 1.1.'),
 'repository-merges': ('PR merges by generic project over the full study window', '410 in-window PR merges across 17 identifiable repositories. Counts include all authors and are not allocated to individual study days. Source: repository activity in evidence.json.'),
}

def inline(s):
    tokens=[]
    def link(m):
        label,url=m.groups()
        if not (url.startswith(('https://','http://','#','../','./')) or re.fullmatch(r'[\w./#-]+',url)):
            raise ValueError('Unsupported link target')
        tokens.append(f'<a href="{escape(url,quote=True)}">{escape(label)}</a>')
        return f'\x00{len(tokens)-1}\x00'
    s=re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)',link,s)
    s=escape(s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    return re.sub(r'\x00(\d+)\x00',lambda m:tokens[int(m[1])],s)

def slug(text):
    return re.sub(r'[^a-z0-9]+','-',text.lower()).strip('-')

def figure(key):
    alt,caption=FIGURES[key]
    desktop=ET.parse(READER/'figures'/f'{key}.svg').getroot().attrib
    mobile=ET.parse(READER/'figures'/f'{key}-mobile.svg').getroot().attrib
    return f'<figure id="figure-{key}"><picture><source width="{mobile['width']}" height="{mobile['height']}" media="(max-width:760px)" srcset="figures/{key}-mobile.svg"><img width="{desktop['width']}" height="{desktop['height']}" src="figures/{key}.svg" alt="{escape(alt)}" loading="lazy"></picture><figcaption>{escape(caption)}<span class="figure-links"><a href="figures/{key}.svg" download>Download SVG</a><a href="figures/{key}.png" download>Download PNG</a><a href="../evidence.json">Source data</a></span></figcaption></figure>'

def render(source):
    blocks=re.split(r'\n\s*\n',source.strip())
    out=[]
    for block in blocks:
        if block.startswith('> Editorial draft'):continue
        match=re.fullmatch(r'<!-- figure: ([\w-]+) -->',block)
        if match:
            out.append(figure(match[1]));continue
        if block.startswith('#'):
            m=re.fullmatch(r'(#{1,3}) (.+)',block)
            if not m:raise ValueError('Unsupported heading')
            n=len(m[1]);out.append(f'<h{n} id="{slug(m[2])}">{inline(m[2])}</h{n}>');continue
        if block.startswith('|'):
            rows=[[c.strip() for c in line.strip().strip('|').split('|')] for line in block.splitlines()]
            if len(rows)<2 or not all(re.fullmatch(r':?-+:?',c) for c in rows[1]):raise ValueError('Invalid table')
            n=len(rows[0])
            if any(len(r)!=n for r in rows):raise ValueError('Inconsistent table columns')
            head='<thead><tr>'+''.join('<th scope="col">'+inline(c)+'</th>' for c in rows[0])+'</tr></thead>'
            body='<tbody>'+''.join('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in r)+'</tr>' for r in rows[2:])+'</tbody>'
            out.append('<p class="table-scroll-hint">Scroll the table horizontally for all columns.</p><div class="table-wrap" tabindex="0" role="region" aria-label="Scrollable study table"><table>'+head+body+'</table></div>');continue
        if block.startswith('- '):
            out.append('<ul>'+''.join('<li>'+inline(line[2:])+'</li>' for line in block.splitlines())+'</ul>');continue
        if block.startswith(('```','<!--','> ')):raise ValueError('Unsupported block')
        out.append('<p>'+inline(' '.join(block.splitlines()))+'</p>')
    return '\n'.join(out)


def page(title,body,kind='Research draft'):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><title>{escape(title)} | Digital Meld</title><link rel="preload" href="vendor/roboto.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="editorial.css"></head>
<body><a class="skip" href="#main">Skip to article</a><header class="mast"><a href="blog.html">DIGITAL MELD / RESEARCH</a><nav aria-label="Main"><a href="blog.html">Blog</a><a href="study.html">Study</a><a href="explorer.html">Explore the data</a><a href="social.html">Social drafts</a></nav></header>
<main class="article" id="main"><div class="eyebrow">ASTRA FIELD STUDY / {escape(kind.upper())}</div><p class="meta">Brad Groux · Six study days · Draft for review</p>{body}
<footer><div class="article-footer-links"><a href="explorer.html">Explore the data</a><a href="../methodology.md">Detailed methods</a><a href="https://github.com/BradGroux/astra-field-study">Contribute to the study</a></div><p>Reviewed aggregate evidence is available in the repository. Article and social drafts remain subject to author review.</p></footer></main></body></html>\n'''


def main():
    for name in ('blog','study'):
        source=(READER/f'{name}.md').read_text()
        title=re.search(r'^# (.+)$',source,re.M)[1]
        (READER/f'{name}.html').write_text(page(title,render(source),'Blog draft' if name=='blog' else 'Study draft'))
    twitter=render((READER/'twitter-article.md').read_text()).replace('<h1 ','<h2 ').replace('</h1>','</h2>')
    linkedin=(READER/'linkedin.txt').read_text()
    body='<h1>Social drafts</h1><nav class="preview-nav" aria-label="Draft formats"><a href="#twitter">Twitter Article</a><a href="#linkedin">LinkedIn</a><a href="twitter-article.md">Twitter Markdown</a><a href="linkedin.txt">LinkedIn text</a></nav>'
    body+='<section id="twitter">'+twitter+'</section><section id="linkedin"><h2>LinkedIn</h2><p class="note">'+str(len(linkedin))+' characters, including spaces, links and trailing newline.</p><div class="share-draft">'+escape(linkedin)+'</div></section>'
    (READER/'social.html').write_text(page('Social drafts',body,'Social drafts'))
    manifest=json.loads((READER/'manifest.json').read_text());manifest['linkedin_characters']=len(linkedin)
    if 'social.html' not in manifest['articles']:manifest['articles'].append('social.html')
    manifest['figures']=[f'figures/{k}{suffix}' for k in FIGURES for suffix in ('.svg','-mobile.svg','.png')]
    manifest['font_license']='vendor/Roboto-OFL.txt';manifest['font_notice']='vendor/Roboto-NOTICE.md'
    if 'vendor/roboto.woff2' not in manifest['runtime_assets']:manifest['runtime_assets'].append('vendor/roboto.woff2')
    (READER/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (READER/'figure-captions.md').write_text('# Figures and source notes\n\n'+'\n\n'.join(f'## {name}\n\nAlt text: {alt}\n\n{cap}\n\n[SVG](figures/{name}.svg) · [PNG](figures/{name}.png) · [Mobile SVG](figures/{name}-mobile.svg)' for name,(alt,cap) in FIGURES.items())+'\n')
    assert len(linkedin)<4000
    print(f'Built blog, study and social HTML; LinkedIn {len(linkedin)} characters.')

if __name__=='__main__':main()
