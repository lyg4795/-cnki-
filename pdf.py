from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open


def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content


def saveTxt(txt):
    with open("istxt.txt", "w") as f:
        f.write(txt)


txt = readPDF(open('C:/Users/hp/Desktop/文献、/有用/离子液体介质中尿素醇解法合成碳酸二甲酯的工艺优化_卢翠英.pdf', 'rb'))
saveTxt(txt)