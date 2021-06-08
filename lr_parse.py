from pdfminer.layout import LAParams, LTTextBox,LTTextLine, LTLine, LTCurve
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
import numpy as np

#TODO - detect report type - urine or blood or covid report

def parse_report(rpath):
    try:
        fp = open(rpath, 'rb')
    except:
        print('EXCEPTION')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams(line_margin=0.1)
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp)
    pages = list(pages)
    page_results = []
    for page in pages:
        all_tb = []
        all_sps = []
        interpreter.process_page(page)
        layout = device.get_result()
        for t in layout:
            if isinstance(t, LTCurve):
                print(t)
            if isinstance(t,LTTextBox):
                all_tb.append(t)
            #TODO seperator can be image as well - just check if bboth line and image >80% of page width
            if isinstance(t,LTLine):
                if np.isclose(t.pts[0][1], t.pts[1][1], atol=2):
                    all_sps.append(t)
        all_tb.sort(key=lambda t:-t.y0)
        r_ts = break_in_rows(all_tb)
        print('r_ts',len(r_ts),'all_tb',len(all_tb))
        page_results.append(merge_r_s(r_ts, all_sps))
    return page_results
    

def merge_r_s(r_ts,all_sps):
    i,j = 0,0
    final = []
    while i < len(r_ts) and j < len(all_sps):
        if r_ts[i][1] > all_sps[j].pts[0][1]:
            final.append(r_ts[i])
            i = i + 1
        elif r_ts[i][1] < all_sps[j].pts[0][1]:
            final.append(('sp', all_sps[j].pts[0][1]))
            j = j + 1
    if j== len(all_sps):
        final.extend(r_ts[i:])
    else:
        final.extend([ ('sp', sp.pts[0][1]) for sp in all_sps[j:]])
    return final

def break_in_rows(tbs):
    row_y = 0
    rows = []
    temp = []

    for t in tbs:
        if t.get_text().strip():
            if not np.isclose(row_y, t.y0, atol=3):
                rows.append(sorted(temp, key=lambda t: t.x0))
                temp = []
                row_y = t.y0
            temp.append(t)

    rows.append(sorted(temp, key=lambda t: t.x0))
    if len(rows) > 1:
        __ = rows.pop(0)  # TODO: hacky
    r_ts = []
    for r in rows:
        r_t = ''
        r_t_y = 0
        for t in r:
            r_t =  r_t + '\t' +  t.get_text().strip()
            r_t_y = t.y0
        r_ts.append((r_t.strip(),r_t_y))
    return r_ts

def normalize_text(t):
    #removing superscript
    t = t.strip()
    t = t.replace('⁰','^0').replace('¹', '^1').replace('²', '^2').replace('³','^3').replace('⁴','^4').replace('⁵','^5').replace('⁶','^6').replace('⁷','^7').replace('⁸','^8').replace('⁹','^9')
    