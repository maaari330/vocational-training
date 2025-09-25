import threading
import time


# スレッド処理関数
def thread1():
    for n in range(10):
        print("thread1:", n)
        time.sleep(1)


# スレッド処理関数
def thread2():
    for n in range(10):
        print("    thread2:", n)
        time.sleep(0.5)


# スレッドオブジェクト生成
th1 = threading.Thread(target=thread1)
th2 = threading.Thread(target=thread2)

# スレッド開始
th1.start()
th2.start()

# スレッド終了待ち
th1.join()
th2.join()
