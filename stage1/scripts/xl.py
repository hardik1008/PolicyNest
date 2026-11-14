import zipfile, sys, re, csv, os
import xml.etree.ElementTree as ET
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def col(ref):
    s=re.match(r'[A-Z]+',ref).group(); n=0
    for ch in s: n=n*26+ord(ch)-64
    return n-1
def read(path):
    z=zipfile.ZipFile(path)
    ss=[]
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',NS):
            ss.append(''.join(t.text or '' for t in si.iter('{%s}t'%NS['m'])))
    wb=ET.fromstring(z.read('xl/workbook.xml'))
    rels=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
    rmap={r.get('Id'):r.get('Target') for r in rels}
    out={}
    for sh in wb.find('m:sheets',NS):
        rid=sh.get('{%s}id'%NS['r']); t=rmap[rid]
        t=t.lstrip('/'); t=t if t.startswith('xl/') else 'xl/'+t
        rows=[]
        for row in ET.fromstring(z.read(t)).find('m:sheetData',NS):
            r=[]
            for c in row:
                i=col(c.get('r'))
                while len(r)<=i: r.append('')
                ty=c.get('t'); v=c.find('m:v',NS)
                if ty=='s': val=ss[int(v.text)]
                elif ty=='inlineStr': val=''.join(x.text or '' for x in c.iter('{%s}t'%NS['m']))
                else: val=v.text if v is not None else ''
                r[i]=val
            rows.append(r)
        out[sh.get('name')]=rows
    return out
if __name__=='__main__':
    path,outdir=sys.argv[1],sys.argv[2]
    os.makedirs(outdir,exist_ok=True)
    for name,rows in read(path).items():
        with open(os.path.join(outdir,name+'.csv'),'w',newline='',encoding='utf-8') as f:
            csv.writer(f).writerows(rows)
        print(name,len(rows),rows[0] if rows else '')
