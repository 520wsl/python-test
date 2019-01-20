fish_record = '鲫鱼5条、鲤鱼8条、鲢鱼7条、草鱼2条、黑鱼6条、乌龟1只'
i = 0
for var in fish_record:
    if var == '条':
        i = i + 1
        print(i)
