import json,pathlib,re,hashlib
R=pathlib.Path(__file__).resolve().parents[1];d=json.loads((R/'src/course.json').read_text());res=[]
def check(n,f):
 try:f();res.append(dict(name=n,passed=True))
 except Exception as e:res.append(dict(name=n,passed=False,error=str(e)))
def eq(a,b):assert a==b,(a,b)
def plain(s):return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]',r'\1',s)
items=d['vocab']+d['grammar'];ids={x['id'] for x in items}
check('80 words,24 grammar,12 texts,40 card questions',lambda:eq([len(d[k]) for k in ['vocab','grammar','readings','questions']],[80,24,12,40]))
check('Unique stable IDs',lambda:eq(len(ids),len(items)))
def content():
 for x in items:
  assert x['level'] in ['N5','N4']
  assert all(x.get(k) for k in ['w','c','t','usage','ja','uk'])
  assert re.search('[А-Яа-яІіЇїЄєҐґ]',x['t']+x['uk'])
  assert not re.search(r'\[\[|\]\]',plain(x['ja'])),x['id']
 for q in d['questions']:
  assert q['target'] in ids and len(set(q['choices']))==4 and 0<=q['answer']<4
 for r in d['readings']:
  for target,quote in r['targets']:assert target in ids and quote in plain(r['ja']),(r['id'],target,quote)
  for q in r['questions']:
   assert len(set(q['choices']))==4 and q['evidence'] in plain(r['ja']),(r['id'],q['evidence'])
check('All fields, choices, evidence and exact coverage quotations',content)
def pairs():
 seen=set()
 for p in d['pairs']:
  assert p['a'] in ids and p['b'] in ids and p['a']!=p['b']
  k=tuple(sorted([p['a'],p['b']]))
  assert k not in seen;seen.add(k)
check('All17 pairs unique and refer to existing cards',pairs)
html=(R/'JLPT_N5_N4_ukrainian_v1.html').read_text()
check('Standalone HTML, no external script or stylesheet',lambda:eq(bool(re.search(r'<script[^>]+src=|<link[^>]+stylesheet',html)),False))
(R/'reports/content-results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2));print(res);assert all(x['passed'] for x in res)
