# arr= [5,4,3,9,6,7]
# target=8
# indexMap={}
# for i in range(len(arr)):
#     complement=target-arr[i]
#     if complement in indexMap:
#         print(indexMap[complement],i)
#     indexMap[arr[i]]=i

# input='A man a plan a canal Panama'
# input=input.replace(' ','').lower()
# # print(input==input[::-1])
# i=0
# l=len(input)-1
# while i<l:
#     if input[i]!=input[l]:
#          print(False)
#     i+=1
#     l+=2
# print(True)


select d.dept_name from department d 
join employee e on e.dept_id=d.dept_id 
group by d.dept_name having avg(e.salary)>10000

