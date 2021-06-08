from pdfminer.layout import LAParams, LTTextBox,LTTextLine
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

fp = open('./reports/thryocare.pdf', 'rb')
rsrcmgr = PDFResourceManager()
laparams = LAParams(line_margin=0.1)
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
pages = PDFPage.get_pages(fp)
pages = list(pages)
fig = plt.figure()
colors = ['r','b','g','k', 'c', 'm', 'y','teal', 'navy', 'gold', 'fuchsia']
ax = fig.add_subplot(111, aspect="equal")
x_max = 0
y_max = 0
for page in pages:
    print('Processing next page...')
    interpreter.process_page(page)
    layout = device.get_result()
    for t in layout:
        if isinstance(t,LTTextBox) :
            print(t.y0)
            r = patches.Rectangle((t.x0, t.y0), t.x1 - t.x0, t.y1 - t.y0, color=random.choice(colors))
            ax.add_patch(r)
            x_max = max(x_max, t.x1)
            y_max = max(y_max, t.y1)
#         if isinstance(lobj, LTTextBox):
#             x, y, text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()
#             patches.Rectangle((t[0], t[1]), t[2] - t[0], t[3] - t[1])
#             _text.extend([(t.x0, t.y0, t.x1, t.y1) for t in self.horizontal_text])
#             _text.extend([(t.x0, t.y0, t.x1, t.y1) for t in self.vertical_text])


    break
ax.set_xlim(0, x_max)
ax.set_ylim(0, y_max)
fig.show()