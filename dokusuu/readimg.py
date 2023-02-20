import cv2
import numpy as np
import pytesseract

def readimg(path):

    #画像を読み込む
    img = cv2.imread(path)

    #外枠を見つけ出す--------------------------------------------------------------------------------------
    #画像をグレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #canny法（輪郭を出す）
    edges = cv2.Canny(gray,100,200)

    #線をを太くして内枠と外枠をくっつける------
    #太さの設定
    kernel_d = np.ones((6,6),np.uint8)
    dilated = cv2.dilate(edges, kernel_d, iterations=1)

    #線を細くする
    # 収縮のためのカーネルを作成
    kernel_e = np.ones((4, 4), np.uint8)

    # 収縮を実行
    #iterationsは実行回数
    eroded = cv2.erode(dilated, kernel_e, iterations=1)

    #輪郭を検出する
    #第2引数は抽出する輪郭線の種類を指定する,第3引数は輪郭線の近似方法を指定する
    #findContours() 関数は、輪郭線のリストと階層構造のリストを返す。
    contours,hierarchy = cv2.findContours(eroded,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    #フィールドを見つけるための変数
    fild_contour = None
    max_area=0
    co=0
    #すべての輪郭から
    for cnt in contours:

        #各輪郭に対して、cv2.approxPolyDP()で多角形の近似を行う
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        #四角形かどうか判別する
        if len(approx) == 4:
            area = cv2.contourArea(approx)
            #一番大きいものを変数へ
            if area > max_area:
                max_area = area
                fild_contour = approx
                co+=1

    if fild_contour is None:
        print('not found')
        exit

    # 四角形の座標を取得する
    x, y, w, h = cv2.boundingRect(fild_contour)

    # 四角形を切り出す
    cut = img[y:y+h, x:x+w]

    #外枠の中から数字を取り出す処理------------------------------------------------------------------------------
    cut_g = cv2.cvtColor(cut, cv2.COLOR_BGR2GRAY)

    #canny法（輪郭を出す）ノイズ除去
    #画像,エッジ数最低値,エッジとして認識する数値
    cut_e = cv2.Canny(cut_g,100,200)

    #線をを太くして内枠と外枠をくっつける------
    #太さの設定
    c_k_d = np.ones((5,5),np.uint8)
    cut_d = cv2.dilate(cut_e, c_k_d, iterations=1)

    #線を細くする
    # 収縮のためのカーネルを作成
    c_k_e = np.ones((4, 4), np.uint8)
    cut_ero = cv2.erode(cut_d,c_k_e , iterations=1)

    #二値化
    cut_t = cv2.threshold(cut_ero, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    conts,hichy = cv2.findContours(cut_t,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # 輪郭の面積を計算し、小さいものは削除
    min_area = 2000
    conts = [cnt for cnt in conts if cv2.contourArea(cnt) > min_area]

    co=0
    list=[]

    for cn in conts:

        #各輪郭に対して、cv2.approxPolyDP()で多角形の近似を行う
        approx = cv2.approxPolyDP(cn,0.01*cv2.arcLength(cn,True),True)

        if len(approx)==4:
            # 四角形の座標を取得する
            x, y, w, h = cv2.boundingRect(cn)

            # 四角形を切り出す
            c_c = cut_t[y:y+h, x:x+w]

            # 切り出した画像内の文字を読み取ります
            text = pytesseract.image_to_string(c_c, config='--psm 10 --oem 3 -c tessedit_char_whitelist=123456789')

            #空白の所に0を入れる
            if text == '':
                text='0'
            text=text.strip()

            list.append([x,y,int(text)])

            co+=1

    data = []

    if co == 81:
        print('ok')
        list.sort(key=lambda x:x[0])
        list.sort(key=lambda y:y[1])
        # for a in list:
        #     print(a)

        numpre=[a[2] for a in list]
        for i in range(0,len(numpre),9):
            data.append(numpre[i:i+9])
    else:
        print('not found')
        return None
    
    return data
    

