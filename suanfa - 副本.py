__author__ = 'yecc'
__date__ = '2019/3/28 9:35'


from collections import deque,OrderedDict
from urllib.parse import quote,urlencode,unquote
from functools import wraps
import re


def fr(x):
    # 兔子问题
    if x ==1 or x ==2:
        return 1
    else:
        return fr(x-1) + fr(x-2)


def shuishu(x):
    # 水仙花数
    i = int(x / 100)
    j = int((x % 100)/10)
    y = int(x % 10)
    if (i*i*i + j*j*j + y*y*y) == x:
        return True


def qsort(lists):
    # 快速排序
    if len(lists) < 2:
        return lists
    else:
        pov = lists[0]
        less = [i for i in lists[1:] if i <= pov]
        big = [i for i in lists[1:] if i > pov]
    return qsort(less) + [pov] + qsort(big)


def psort(lists):
    # 冒泡排序
    for i in range(len(lists)):
        for j in range(len(lists)-1):
            if lists[j] > lists[j+1]:
                lists[j], lists[j+1] = lists[j+1], lists[j]
    return lists


def seach_wide():
    gar = {}
    seach_queue = deque()
    seach_queue += gar['you']
    while seach_queue:
        person = seach_queue.popleft()
        if wanted_person(person):
            print('find it %s' % person)
            return True
        else:
            seach_queue += gar[person]
        return False


def sortd(data):
    s2 = sorted(data.items(), key=lambda s1: s1[0])
    for i,v in enumerate(s2):
        if type(v[1]) is list:
            if len(v[1])!=0:
                for j in range(len(v[1])):
                    if v[1][j] == '':
                        s2.pop(i)
                    elif type(v[1][j]) is dict:
                        s = sortd(v[1][j])
                        s2.pop(i)
                        s2.insert(i,(v[0],s))
            else:
                s2.pop(i)
    return s2


def sign_data(data):
    signs = ''
    for i, j in enumerate(sortd(data)):
        if type(j[1]) is not list:
            l = "{}={}&".format(j[0], j[1])
        elif type(j[1]) is list:
            for index, value in enumerate(j[1]):
                if type(value) is tuple:
                    if type(value[1]) is list:
                        for m,n in enumerate(value[1]):
                            l += "{}[{}][{}][{}]={}&".format(j[0], len(j) - 2, value[0], m,n)
                    else:
                        l += "{}[{}][{}]={}&".format(j[0], len(j) - 2, value[0], value[1])
                else:
                    l = "{}[{}]={}&".format(j[0], index, value)
        signs+=l
    return signs.rstrip('&')


s11 = {"cno": "1353210023779896", "shop_id": 1905736354, "cashier_id": "1180940478", "consume_amount": 300,
      "sub_balance": 100, "sub_credit": 2, "deno_coupon_ids": [], "gift_coupons_ids": ["8888","001"], "payment_amount": 0,
      "credit_amount": 0, "payment_mode": 1, "count_num": 2, "biz_id": 8036, "table_id": "A023", "tags": ["交易标签"],
      "products": [{"name": "辣子鸡丁", "no": 219824, "num": "1", "price": "100", "is_activity": 1, "coupons_ids": [],
                    "tags": ["测试菜品标签","yyy","aaa"]}]}


def isdict(lists):
    """
    # 判断lists中是否包含dict
    :param lists:
    :return: True/False
    """
    flag = False
    for i,v in enumerate(lists):
        if isinstance(v,dict):
            flag = True
    return flag


def sortdicts(dic):
    """
    字典按key升序排列，子数组递归排序
    :param dic: dict
    :return: dict
    """
    key_list = []
    dicts = OrderedDict()
    try:
        if isinstance(dic, dict):
            for key, value in dic.items():  # 循环字典，取出key,van
                key_list.append(key)
            for i, values in enumerate(sorted(key_list)):
                dicts[values] = dic[values]  # dicts获取值
        for dicts_key, dicts_value in dicts.items():
            if isinstance(dicts_value, list) and len(dicts_value) > 0:
                if isdict(dicts_value):
                    for k, v in enumerate(dicts[dicts_key]):
                        # if isinstance(v, dict):
                        m = sortdicts(v)   # 递归排序
                        dicts[dicts_key][k] = m
                else:
                    sort_list = sorted(dicts[dicts_key])
                    dicts[dicts_key] = sort_list  # 对列表排序后重新返回给字典
        for key1 in list(dicts.keys()):
            if isinstance(dicts[key1], list) and len(dicts[key1]) == 0:
                del dicts[key1]  # 删除为空的字段
        return dicts
    except Exception as ex:
        print(ex)


def list_to_string(key,vlist):
    ds = ''
    for i,v in enumerate(vlist):
        m = '{0}[{1}]={2}&'.format(key,i,v)
        ds+=m
    return ds


def dict_to_strings(key,lists):
    """
    dict拼接字符串,xx=111&yyy=2222
    :param key: key值
    :param lists:
    :return: xx=111&yyy=2222
    """
    ts = ''
    for ii, ss in enumerate(lists):
        for ks, vs in ss.items():
            if isinstance(vs,list):
                mm = list_to_string(ks, vs)
                tt = mm.replace('tags', "{0}[{1}][{2}]".format(key,ii,ks))
            else:
                tt = "{0}[{1}][{2}]={3}&".format(key,ii,ks,vs)
            ts += tt

    return ts


def signdatas(dicts):
    ss = ''
    for key,value in dicts.items():
        if isinstance(value,list):  # 判断是否为list
            if isdict(value):  # 判断是否包含dict
                for i, v in enumerate(value):
                    strs = dict_to_strings(key,value)
            else:
                strs = list_to_string(key,value)
        else:
            strs = "{}={}&".format(key, value)  # 拼接字符
        ss += strs
    return ss.rstrip("&")

def foobo(n):
    # 斐波那契数列，输入整数n,返回第n个位置的数
    relst = [0, 1]
    if n < 2:
        return relst[n]
    first = 1  # 前一个数
    second = 2  # 后一个数
    temps = 0  # 临时变量
    for i in range(1,n):
        temps = second  # 将后一个数保存为一个变量
        second = second + first  # 后一个数等于前2个相加
        first = temps  # 将后一个赋值给前一个
    return second

def removeDulpicates(num_lists):
    l = []
    if len(num_lists) == 0:
        return 0
    fast = 0
    slow = 0
    length = len(num_lists)
    # while slow < length:
    #     if num_lists[slow] == num_lists[fast]:
    #         fast += 1
    #     else:
    #         slow += 1
    #         #num_lists[slow] = num_lists[fast]
    #         fast += 1
    # return slow + 1
    for i in range(length):
        if num_lists[i] != num_lists[slow]:
            slow += 1
            num_lists[slow] = num_lists[i]
    return slow + 1



def removeDu(nlist):
    """
    一个排序数组，删除重复的数字,
    使得每个元素只出现一次，并且返回新的数组的长度
    :param nlist: 排序数组
    :return: 新的数组的长度
    """
    if len(nlist) == 0:
        return 0
    i = 0
    while i < len(nlist) - 1:
        if nlist[i] == nlist[i]:
            nlist.remove(nlist[i])
        else:
            i += 1
    return len(nlist)


def removeDu1(nlist):
    """
    一个排序数组，删除重复的数字,
    允许出现两次重复，并且返回新的数组的长度
    :param nlist: 排序数组
    :return: 新的数组的长度
    """
    if len(nlist) == 0:
        return 0
    i = 0
    while i < len(nlist) - 2:
        if nlist[i] == nlist[i+2]:
            nlist.remove(nlist[i+2])
        else:
            i += 1
    return len(nlist)

def oneNum(num):
    """
    一个整数，二进制表示有多少个1
    :param num:
    :return: 数量
    """
    count = 0
    while num > 0:
        count += 1
        num = num & (num-1)
    return count

def twoSum(lists,target):
    """

    :param lists:
    :param target:
    :return:
    """
    l = []
    for i in range(len(lists)):
        j = i + 1
        for j in range(j,len(lists)):
            if (lists[i] + lists[j]) == target:
                l = [i,j]
                break
    return l

def twoSum1(lists,target):
    l = []
    dicts = {}
    for j in range(len(lists)):
        otherword = target - lists[j]
        if otherword not in dicts:
            dicts[lists[j]] = j
            print(dicts)
        else:
            l = [dicts[otherword],j]
    return l

def trailingZeroes(n):
    if n == 0:
        return 1
    count = 0
    while n > 1:
        n = n / 5
        count += n
    return int(count)


def twoSum2(numbers, target):
    # 排序好的，求和
    left = 0
    right = len(numbers) - 1
    for i in numbers[1:]:
        if numbers[left] + numbers[right] == target:
            return [left+1, right+1]
        elif numbers[left] + numbers[right] < target:
            left += 1
        else:
            right -= 1


def singleNumber(nums):
    index = nums[0]
    for i in range(1,len(nums)):
        index = index ^ nums[i]
    return index

def singleNumber1(nums):
    index = 0
    for i in nums:
        index ^= i
    return index

def maxProfit(prices):
    """"""
    if len(prices)<0:
        return 0
    buy = -prices[0]
    sell = 0
    for i in range(1,len(prices)):
        buy = max(buy, -prices[i])
        sell = max(sell, buy + prices[i])
    return sell


def emmo(fn):
    cache = {}
    miss = object()

    @wraps(fn)
    def wrapper(*args):
        relsult = cache.get(args, miss)
        if relsult is miss:
            relsult = fn(*args)
            cache[args] = relsult
        return relsult
    return wrapper


@emmo
def fn(n):
    if n < 2:
        return n
    return fn(n-1) + fn(n-2)


def lengthOfLongestSubstring(s: str):
    """
    给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度
    采用滑动窗口
    :param self:
    :param s:
    :return:
    """
    # h = len(s)
    # if h < 0: return 0
    # look = set()
    # left = 0
    # max_len = 0
    # cur_len = 0
    # for i in range(h):
    #     cur_len += 1
    #     while s[i] in look:
    #         look.remove(s[left])
    #         left += 1
    #         cur_len -= 1
    #     if cur_len > max_len:
    #         max_len = cur_len
    #     look.add(s[i])
    # return max_len
    if len(s) == 0:
        return 0

    # 非空字符串的最小长度定义为1
    longestlen = 1
    temp_str = ""
    for item in s:
        # 对其进行迭代,如果item不在s中,那么就把item写入暂时的temp_str
        if item not in temp_str:
            temp_str += item
        else:
            # 如果item在s中,则对temp_str长度进行判断,如果长度大于定义的最小长度,进行赋值
            if len(temp_str) > longestlen:
                longestlen = len(temp_str)
            # 长度小于暂定,那么就写入temp_str
            temp_str += item
            temp_str = temp_str[temp_str.index(item) + 1:]
    if len(temp_str) > longestlen:
        longestlen = len(temp_str)

    return longestlen


def reverse(x):
    if x == 0:
        return 0
    string_x = str(x)
    # if string_x.endswith('0') and x > 0:
    #     pass
    if x < 0:
        del_x = string_x.replace('-','')
        last = int('-' + del_x[::-1])
        if last < -(2**31 - 1):
            return 0
        else:
            return last
    else:
        last = int(string_x[::-1])
        if last > 2**31 - 1:
            return 0
        else:
            return last

def myAtoi(s):
    # if len(s) == 0:return 0
    # if str(s).isspace():return 0
    # ss = ''
    # for i in str(s):
    #     if i.isspace():
    #         continue
    #     elif i == '+' or i == '-':
    #         continue
    #     elif not i.isdigit():
    #         return 0
    #         break
    #     elif i.isdigit():
    #         ss+=i
    # return ss
    return max(min(int(*re.findall('^[\+\-]?\d+', s.lstrip())), 2 ** 31 - 1), -2 ** 31)


def searchRange(nums,target):

    # 通过二分法找到第一个等于 target 的值, 然后以该值向左向右查找边界
    lens = len(nums)
    if lens == 0:
        return [-1, -1]
    left = 0
    right = lens - 1
    while left <= right:
        mid = left + (-left+right) // 2
        if nums[mid] == target:
            left = mid
            right = mid
            # 找到向左判断
            while left >= 1 and nums[left-1] == target:
                left -= 1
            # 向右判断
            while right < lens - 1 and nums[right+1] == target:
                right += 1
            return [left, right]
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return [-1, -1]

def searchInsert(nums,target):
    # LeetCode 第 35 题：搜索插入位置
    """
    给定一个排序数组和一个目标值，在数组中找到目标值，并返回其索引。
    如果目标值不存在于数组中，返回它将会被按顺序插入的位置。
    你可以假设数组中无重复元素。

    示例 1:
    输入: [1,3,5,6], 5
     输出: 2
    :param nums:
    :param target:
    :return:
    """
    lens = len(nums)
    if lens == 0:
        return 0
    left = 0
    # right = lens - 1
    # while left <= right:
    #     mid = (left + right) // 2
    #     if nums[mid] == target:
    #         return mid
    #     elif nums[mid] < target:
    #         left = mid + 1
    #     else:
    #         right = mid - 1
    # return left
    right = lens
    while left < right:
        mid = left + (right-left)//2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left





if __name__ == "__main__":
    # ss = {"cno":"1353210023779896","shop_id":1905736354,"cashier_id":"1180940478","consume_amount":10000,"sub_balance":0,"sub_credit":2,"deno_coupon_ids":[""],"gift_coupons_ids":[""],"payment_amount":0,"credit_amount":0,"payment_mode":1,"count_num":1,"biz_id":8036,"table_id":"A023","tags":["tt"],"products":[{"name":"辣子鸡丁","no":219830,"num": "1","price":"2000","is_activity":1,"product_use_coupon":["1633055871722665982"],"coupons_ids":[],"tags":["测试cl"]},{"name":"吗豆腐","no":219830,"num": "1","price":"2000","is_activity":1,"product_use_coupon":["1633055871722665982"],"coupons_ids":[],"tags":["测试cl"]}]}
    #
    # import json
    #
    # json_data = '{"errno":0,"msg":"","result":{"2018-06-02":{"tool":16760,"adapter":16772},"2018-06-03":{"tool":16746,"adapter":16733},"2018-06-05":{"tool":18959,"adapter":18956},"2018-06-01":{"tool":18208,"adapter":18210},"2018-06-06":{"tool":17816,"adapter":17827},"2018-06-04":{"tool":19929,"adapter":19908},"2018-06-07":{"tool":17790,"adapter":17774}}}'
    # d1 = json.loads(json_data)
    # d = d1["result"]
    #
    # # 对字典的key值进行排序
    # d_list = sorted(ss.items(), key=lambda item: item[0])
    # print(d_list)
    # # 转换为字典
    # d_new = {}
    # for i in d_list:
    #     d_new[i[0]] = i[1]
    # print(d_new)
    l = [2,5,7]
    s = '42'
    print(5//5)
    print(searchInsert(l,3))
