import sys

def putlog(str):
    STDOUT = sys.stdout
    fp = open("log.txt","a")
    sys.stdout =  fp
    print(str)
    fp.close()
    sys.stdout = STDOUT

def kugiri():
    print("########################################################")

def truetatuscode(statuscode,truestatucode):
    if statuscode != truestatucode:
        #print("エラーが発生しました.パソコンがインターネットにつながっていないか，回線が混み合っています．")
        #putlog(f"エラー,statuscode:{statuscode}")
        raise Exception(f"正しいstatuscodeではありません.\n statuscode:{statuscode}.\nしばらくしてから起動してください.")
