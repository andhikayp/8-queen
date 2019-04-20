import os
import time

papan = [ [ '_', '_', '_' ], 
    [ '_', '_', '_' ], 
    [ '_', '_', '_' ]]

pemain='o'
ai='x'
kosong='_'
MIN = -1000
MAX = 1000

def lihat():
    for i in range(0,3):
        for j in range(0,3):
            print(papan[i][j], end =" ")
        print()

def other(pion:chr) -> chr:
    if(pion==pemain) : 
        return ai
    else : 
        return pemain


def masihbermain() -> bool:
    for i in range(0,3):
        for j in range(0,3):
            if(papan[i][j]==kosong):
                return True

    return False


def score_eval() -> int:
    for i in range(0,3):
        if(papan[i][0]==papan[i][1] and papan[i][1]==papan[i][2] and papan[i][0]==pemain):
            return -10
        elif(papan[0][i]==papan[1][i] and papan[1][i]==papan[2][i] and papan[0][i]==pemain):
            return -10
        elif(papan[i][0]==papan[i][1] and papan[i][1]==papan[i][2] and papan[i][0]==ai):
            return 10
        elif(papan[0][i]==papan[1][i] and papan[1][i]==papan[2][i] and papan[0][i]==ai):
            return 10
    if(papan[0][0]==papan[1][1] and papan[1][1]==papan[2][2] and papan[0][0]==pemain):
        return -10
    elif(papan[0][2]==papan[1][1] and papan[1][1]==papan[2][0] and papan[0][2]==pemain):
        return -10
    elif(papan[0][0]==papan[1][1] and papan[1][1]==papan[2][2] and papan[0][0]==ai):
        return 10
    elif(papan[0][2]==papan[1][1] and papan[1][1]==papan[2][0] and papan[0][2]==ai):
        return 10
    return 0

def minimax(pion:chr,alpha:int,beta:int) -> int:
    skor = score_eval()
    flag = 0
    if(skor!=0):
        return skor
    if(not masihbermain()):
        return 0
    hasil = MIN
    if(pion==ai):
        hasil = MIN
        for i in range(0,3):
            if(beta<=alpha):
                flag=1
                break
            for j in range(0,3):
                if(papan[i][j]==kosong):
                    papan[i][j] = pion
                    hasil = max(hasil,minimax(other(pion),alpha,beta))
                    papan[i][j]=kosong
                    if(alpha<hasil):
                        alpha = hasil
                    if(beta<=alpha):
                        flag=1
                        break
            if(flag == 1):
                break
    else:
        hasil = MAX
        for i in range(0,3):
            if(beta<=alpha):
                flag=1
                break
            for j in range(0,3):
                if(papan[i][j]==kosong):
                    papan[i][j] = pion
                    hasil = min(hasil,minimax(other(pion),alpha,beta))
                    papan[i][j]=kosong
                    if(beta>hasil):
                        beta = hasil
                    if(beta<=alpha):
                        flag=1
                        break
            if(flag == 1):
                break

    return hasil

def ambilpath():
    hasil = MIN
    x=-1
    y=-1
    for i in range(0,3):
        for j in range(0,3):
            if(papan[i][j]==kosong):
                papan[i][j]=ai
                sementara = minimax(pemain,MIN,MAX)
                if(sementara>hasil):
                    hasil = sementara
                    x = i
                    y = j   
                papan[i][j]=kosong
    papan[x][y] = ai
    return

def play():
    os.system("cls")
    print("Mari bermain tic tac toe:\nAnda: O, Computer: X")
    print("Tekan sembarang tombol untuk lanjut")
    input()
    score = MIN
    for i in range(0,9):
        if(not masihbermain()):
            break
        os.system("cls")
        score = score_eval()
        if(score!=0):
            break
        if(i%2 == 0):
            print("Giliran anda:")
            lihat()
            print("Baris:")
            x = input()
            print("Kolom:")
            y = input()
            x = int(x)
            y = int(y)
            x = x-1
            y = y-1
            while(x>2 or y>2 or papan[x][y]!=kosong):
                os.system("cls")
                print("Giliran anda:")
                lihat()                
                print("Tempat tersebut telah diisi")
                print("Baris:")
                x = input()
                print("Kolom:")
                y = input()
                x = int(x)
                y = int(y)
                x = x - 1
                y = y - 1
            papan[x][y]=pemain
            os.system("cls")
            print("Giliran anda:")
            lihat()            
            time.sleep(1)
        else:
            os.system("cls")
            print("Giliran komputer:")
            lihat()
            print("Komputer sedang berfikir")
            time.sleep(1)
            ambilpath()
            os.system("cls")
            print("Giliran komputer:")
            lihat()
            time.sleep(1)

    os.system("cls")
    print("Hasilnya adalah:")
    lihat()
    if(score == 10):
        print("Komputer menang!")
    if(score == -10):
        print("Anda menang!")
    if(score == 0):
        print("SERI!")


if __name__ == '__main__':
    play()