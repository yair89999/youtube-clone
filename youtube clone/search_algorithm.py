def search(to_search,in_dict): # in_dict is list/dict
    print("\n")
    on_list = sorted(list(in_dict))
    using_list = on_list.copy()
    iterations = 0
    while True:
        print(using_list)
        middle_index = len(using_list)//2-1
        middle = using_list[middle_index]
        if middle == to_search:
            break
        if to_search not in using_list[len(using_list)//4] and to_search not in using_list[len(using_list)//4*3]:
            if middle < to_search: # del left
                using_list = using_list[middle_index:]
                print("del left",using_list)
            elif middle > to_search: # del right
                using_list = using_list[:middle_index+1]
                print("del right",using_list)
        else:
            break
        iterations += 1
        
        if iterations >= 20 or len(using_list) < 20:
            break
    
    return_list = []
    return_ids = []
    index = 0
    for search_word in using_list:
        if to_search in search_word:
            return_list.append(search_word)
            return_ids.append(in_dict[search_word])
        index += 1
    print("\n")
    return return_list, return_ids