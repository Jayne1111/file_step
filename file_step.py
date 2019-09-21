#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sys, time
class ShowProcess():
  """
  显示处理进度的类
  调用该类相关函数即可实现处理进度的显示
  """
  f = 0 # 当前的处理进度
  max_nums = 0 # 总共需要处理的次数
  max_lenth = 50 #进度条的长度
  # 初始化函数，需要知道总共的处理次数
  def __init__(self, max_nums):
    self.max_nums = max_nums
    self.f = 0
  # 显示函数，根据当前的处理进度i显示进度
  # 效果为[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]100.00%
  def show_process(self, f=None):
    if f is not None:
      self.f = f
    else:
      self.f += 1
    num_arrow = int(self.f * self.max_lenth / self.max_nums) #计算显示多少个'>'
    num_line = self.max_lenth - num_arrow #计算显示多少个'-'
    percent = self.f * 100.0 / self.max_nums #计算完成进度，格式为xx.xx%
    process_bar = '[' + '>' * num_arrow + '-' * num_line + ']'\
           + '%.2f' % percent + '%' + '\r' #带输出的字符串，'\r'表示不换行回到最左边
    sys.stdout.write(process_bar) #这两句打印字符到终端
    sys.stdout.flush()
  def close(self, words='done'):
    print('')
    print(words)
    self.f = 0
if __name__=='__main__':
  max_nums = 100
  process_bar = ShowProcess(max_nums)
  for f in range(max_nums + 1):
    process_bar.show_process()
    time.sleep(0.05)
  process_bar.close()

