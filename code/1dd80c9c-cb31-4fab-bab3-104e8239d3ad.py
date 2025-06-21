def find_largest(arr):
    if not arr:
        return "Array is empty"
    return max(arr)

# Example 1
arr1 = [2, 5, 1, 3, 0]
print(find_largest(arr1))  # Output: 5

# Example 2
arr2 = [8, 10, 5, 7, 9]
print( find_largest(arr2))  # Output: 10