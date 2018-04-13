# encoding:utf-8
'''
@author:lk

@time:2017/10/30 

@desc:

'''
import time

def primes(n):
    #质数列表P
    P = []
    #n以内的列表f,元素0代表质数,1代表非质数
    f = []
    for i in range(n + 1):
        # 如果当前数字能被2整除就表示非质数,将f列表添加1的元素,否则f列表添加0的元素
        if i > 2 and i % 2 == 0:
            f.append(1)
        else:
            f.append(0)
    i = 3
    # 从i的平方中开始查找筛选
    while i * i <= n:
        # 如果从f列表中取出来的元素等于0(不能被2整除的数)
        if f[i] == 0:
            # 所以该数的平方则表示非质数
            j = i * i
            while j <= n:
                # 将该数的平方及以上的倍数设置为不是质数,i*i,i*(i+1),i*(i+2),i*(i+3)...
                f[j] = 1
                # 所有奇数的平方一定是奇数
                # 奇数如果加上一个i(奇数)一定就是偶数,而偶数能被2整除
                j += 2 * i
        # i如果加上1变偶数,偶数能被2整除所以不是质数,所以此处加2变奇数
        i += 2
    # 先将2添加到质数列表中
    P.append(2)
    # 取出列表f中等于0的数就是质数并添加到质数列表p中
    for i in range(3, n, 2):
        if f[i] == 0:
            P.append(i)
    return P


if __name__ == '__main__':
    start = time.clock()
    n = 10000000
    P = primes(n)
    index = 522048
    print("从%d以内的数中查找质数一共所花时间: %f 秒" % (n, (time.clock() - start)))
    if index < len(P):
        print("第 %d 质数是: %d" % (index, P[index - 1]))
    else:
        print("%d以内的数中只包含%d个质数" % (n, len(P)))
