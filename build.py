import csv,json,re,pathlib,sys
ROOT=pathlib.Path(__file__).parent
sys.path.insert(0,str(ROOT/'src'))
from readings import READINGS
from pairs import PAIRS

def rows(name):return list(csv.reader((ROOT/'src'/name).open(),delimiter='\t'))
vocab=[]
for row in rows('vocabulary.tsv'):
 assert len(row)==9,row
 id,level,w,r,c,t,usage,ja,uk=row
 vocab.append(dict(id=id,kind='v',level=level,w=w,r=r,c=c,t=t,usage=usage,ja=ja,uk=uk))
grammar=[]
for row in rows('grammar.tsv'):
 assert len(row)==9,row
 id,level,w,c,t,rule,usage,ja,uk=row
 grammar.append(dict(id=id,kind='g',level=level,w=w,c=c,t=t,rule=rule,usage=usage,ja=ja,uk=uk))
questions=[]
for row in rows('questions.tsv'):
 assert len(row)==9,row
 id,target,type,prompt,*other=row
 questions.append(dict(id=id,target=target,type=type,prompt=prompt,choices=other[:4],answer=0,explain=other[4]))
pairs=[dict(zip(['id','a','b','type','note','jaA','ukA','jaB','ukB'],p)) for p in PAIRS]
data=dict(vocab=vocab,grammar=grammar,questions=questions,pairs=pairs,readings=READINGS)
serialized=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
html=(ROOT/'src/app.html').read_text().replace('__DATA__',serialized)
(ROOT/'JLPT_N5_N4_ukrainian_v1.html').write_text(html)
(ROOT/'src/course.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print({k:len(v) for k,v in data.items()})
