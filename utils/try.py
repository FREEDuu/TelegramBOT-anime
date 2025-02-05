def split_into_chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Example usage
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9,10]
chunks = list(split_into_chunks(my_list, 3))
