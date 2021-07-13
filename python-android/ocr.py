from PIL import Image
import pytesseract

def OCR(self):
    print("[OCR] Starting OCR...")
    ocrResult=pytesseract.image_to_string(self)
    if not ocrResult:
        print("[OCR] OCR cannot find any Text in this element.")
        return ocrResult
    # elif len(ocrResult)>40:
    #     ocrResult=ocrResult[:40]+"..."
    #     print("[OCR] Trimming Text...")        
    proc_ocr_text=ocrResult.replace('\r', ' ').replace('\n', ' ').replace('\"', '\'').replace('<', '').replace('>','')
    if len(proc_ocr_text)>50:
        proc_ocr_text=proc_ocr_text[:50]+"..."
        print("[OCR] Trimming Text...")   
    print("[OCR] The ocr result is: \n"+ ocrResult+"\n")
    return proc_ocr_text

if __name__=="__main__":
    print("Test OCR...")
    OCR('pngs/cnn_463.0_124.36363636363636_617.0_192.0.png')