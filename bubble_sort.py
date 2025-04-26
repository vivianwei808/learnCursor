def bubble_sort(arr):
    """
    冒泡排序算法实现
    :param arr: 待排序的列表
    :return: 排序后的列表
    """
    n = len(arr)
    # 遍历所有数组元素
    for i in range(n):
        # 最后 i 个元素已经在正确的位置上
        for j in range(0, n-i-1):
            # 如果当前元素大于下一个元素，则交换它们
            if arr[j] > arr[j+1]:
                # 交换相邻元素的位置
                arr[j], arr[j+1] = arr[j+1], arr[j]
    # 返回排序后的数组
    return arr

# 测试代码
if __name__ == "__main__":
    # 测试用例
    test_array = [10, 20, 33, 21, 3, 5, 11, 55]  # 创建一个包含多个整数的测试数组
    print("原始数组:", test_array)  # 打印原始数组
    sorted_array = bubble_sort(test_array)  # 调用冒泡排序函数对数组进行排序
    print("排序后数组:", sorted_array)  # 打印排序后的数组