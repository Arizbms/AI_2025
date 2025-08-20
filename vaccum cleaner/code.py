pos=[[0,0],[0,1],[1,1],[1,0]]
clean=[[0,1],[1,0]]


for i in pos:
    row=i[0]
    col=i[1]
    if(clean[row][col]):
        print(f"Room {i} already clean")
    else:
        print(f"Room {i} was dirty,cleaned now")
        clean[row][col]=1
print("All rooms cleaned")
