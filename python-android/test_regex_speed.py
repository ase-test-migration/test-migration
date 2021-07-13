# import re
# import timeit
#
# def matchRegex(ins):
#     pattern=re.compile(r"\[(?P<x1>[\d]+),(?P<y1>[\d]+)\]\[(?P<x2>[\d]+),(?P<y2>[\d]+)\]")
#     match = pattern.match(ins)
#     if match:
#         x = int(match.group('x1'))
#         y = int(match.group('y1'))
#         x2 = int(match.group('x2'))
#         y2 = int(match.group('y2'))
#         width = x2-x
#         height = y2-y
#         # print(x,y,width,height)
#         return x,y,width,height
# def stupid2(ins):
#     # temp = re.findall(r'\d+', ins)
#     # arr = list(map(int, temp))
#
#     ins=ins[1:-1]
#     ins=ins.replace('][',',')
#     arr=ins.split(",")
#     arr=list(map(int, arr))
#     # print(arr[0],arr[1],arr[2],arr[3])
#     # return res[]
#     return arr
#
# def stupid(ins):
#     ins=ins[1:-1]
#     result_list = []
#     start = 0
#     for index, char in enumerate(ins):
#         if not char.isnumeric():
#             if start!=index:
#                 result_list.append(ins[start:index])
#             start = index + 1
#     if start == 0:
#         return [ins]
#     result_list.append(ins[start:index + 1])
#     return result_list
#
# def f_test():
#     ins="[1234342,321214][24224,5456]"
#     stupid(ins)
# def f_test2():
#     ins="[1234342,321214][24224,5456]"
#     stupid2(ins)
# def f_test3():
#     ins="[122,34][244,56]"
#     matchRegex(ins)
#
# print(timeit.timeit("f_test()", setup="from __main__ import f_test"))
# print(timeit.timeit("f_test2()", setup="from __main__ import f_test2"))
# print(timeit.timeit("f_test3()", setup="from __main__ import f_test3"))

# list1 = [1,2,3,4]
# list2 = [1,2,3]
# remove_list = []
# for element in list1:
#     if element in list2:
#         remove_list.append(element)
#
# list1 = [x for x in list1 if x not in list2]
#
# print(list1)

import os.path
#from os import path

#path.exists("guru99.txt")

