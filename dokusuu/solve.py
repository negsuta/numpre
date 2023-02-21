import time
import readimg

def set_number(data):
    for i in range(9):
        for j in range(9):
            if data[i][j] == 0:
                for num in range(1,10):
                    if check(data,i,j,num):
                        data[i][j]=num
                        if set_number(data):
                            return True
                        data[i][j] = 0
                return False
    return True

def check(data,x,y,num):
    #縦に同じ数字があるかどうか
    for i in range(9):
        if data[x][i] == num and i != y:
            return False
    #横に同じ数字があるかどうか
    for i in range(9):
        if data[i][y] == num and i !=x:
            return False
    #3x3のボックス内に同じ数字があるかどうか
    #3で割って切り捨て属している3x3の位置を見る
    box_x = (x//3)*3
    box_y = (y//3)*3
    for i in range(3):
        for j in range(3):
            #ボックス内に同じ数字があるかどうか
            if data[box_x+i][box_y+j] == num and box_x+i != x and box_y+j != y:
                return False
    return True

if __name__ == '__main__':

    path = '画像のpath'
    
    print('画像読み込み中')
    data = readimg.readimg(path)

    if len(data)==9:
        for i in range(9):
            if len(data[i]) != 9:
                print('not found')
                exit
    else:
        print('not found')
        exit

    print('read ok')
    #問題
    adata = data
    print('read field')
    for i in data:
        print(i)

    if set_number(adata):
        print('answer')
        for i in adata:
            print(i)
    else:
        print('can\'t solve')
