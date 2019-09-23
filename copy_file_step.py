import string
import os
import threading
import time
import queue
from progressbar import *

mp3_file_list = queue.Queue()
copy_dest_path = r"C:\Users\lx\Desktop\music"


# 负责遍历文件系统的线程
def fs_traverse():
    disk_list = []    # 存放磁盘分区列表

    for c in string.ascii_uppercase:
        disk = c + ":\\"
        if os.path.isdir(disk):
            disk_list.append(disk)

    print(disk_list)

    disk_list[0] = r"C:\Users\Public\Music\示例音乐"

    for disk in disk_list:
        for root,dirs,files in os.walk("D:\\"):
            if root == copy_dest_path:
                continue

            for f in files:
                if f[-4:].lower() == ".mp3":
                    dest_file_path = os.path.join(root,f)
                    print(dest_file_path)
                    mp3_file_list.put(dest_file_path)
    
    mp3_file_list.put(False)
    print("遍历文件系统的线程已经执行完毕！")


total = 1000
def dosomework():
  time.sleep(0.01)
  '''
  widgets参数含义：
  'Progress:' ：设置进度条前显示的文字
   Percentage() ：显示百分比
   Bar('#') ： 设置进度条形状
   ETA() ： 显示预计剩余时间
   Timer() ：显示已用时间
  '''
widgets = ['Progress: ',Percentage(), ' ', Bar('#'),' ', Timer(),
      ' ', ETA(), ' ', FileTransferSpeed()]
pbar = ProgressBar(widgets=widgets, maxval=10*total).start()
for i in range(total):
  # do something
  pbar.update(10 * i + 1)
  dosomework()
pbar.finish()


# 负责拷贝文件的线程
def copy_file():
    while True:
        copy_src_file = mp3_file_list.get()

        if copy_src_file == False:
            break

        file_name = copy_src_file.split("\\")[-1]
        des_file_path = os.path.join(copy_dest_path,file_name)

        # 文件拷贝操作
        src_file = open(copy_src_file,'rb')
        des_file = open(des_file_path,'wb')
        des_file.write(src_file.read())
        src_file.close()
        des_file.close()

        print("拷贝完",copy_src_file)

    print("拷贝线程已经执行完毕！")


# 主线程负责管理Worker线程
def main():
    t_start = time.time()

    fs_traverse_thread = threading.Thread(target=fs_traverse)
    copy_file_thread = threading.Thread(target=copy_file)

    fs_traverse_thread.start()
    copy_file_thread.start()

    t_end = time.time()

    t = t_end - t_start

    print("耗时%s毫秒！" % int((t) * 1000))





if __name__ == "__main__":
    main()


# **Semaphore(共享对象访问)** 同步锁 
# Semaphore管理一个内置的计数器， 
# 每当调用acquire()时内置计数器-1；
# 调用release() 时内置计数器+1；  
# 计数器不能小于0；当计数器为0时，acquire()将阻塞线程直到其他线程调用release()。 
# `semaphore ``=` `threading.Semaphore(``3``)` 
# 同时有3个线程可以用这个锁 


## 线程优先级队列（ Queue）
# Python的Queue模块中提供了同步的、线程安全的队列类，包括FIFO（先入先出)队列Queue，LIFO（后入先出）队列LifoQueue，和优先级队列PriorityQueue。这些队列都实现了锁原语，能够在多线程中直接使用。可以使用队列来实现线程间的同步。
# Queue模块中的常用方法:
# - Queue.qsize() 返回队列的大小
# - Queue.empty() 如果队列为空，返回True,反之False
# - Queue.full() 如果队列满了，返回True,反之False
# - Queue.full 与 maxsize 大小对应
# - Queue.get([block[, timeout]])获取队列，timeout等待时间
# - Queue.get_nowait() 相当Queue.get(False)
# - Queue.put(item) 写入队列，timeout等待时间
# - Queue.put_nowait(item) 相当Queue.put(item, False)
# - Queue.task_done() 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号
# - Queue.join() 实际上意味着等到队列为空，再执行别的操作
