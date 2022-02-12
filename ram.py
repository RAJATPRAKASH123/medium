from collections import defaultdict
# 1

def returnIPCount():
    first_octet = 132
    numIPAddressReq = 50
    ipClass = {"A": ["0.0.0.0", "127.255.255.255"], "B": ["128.0.0.0", "191.255.255.255" ], "C":["192.0.0.0", "223.255.255.255"] , "D": ["224.0.0.0", "239.255.255.255"], "E": ["240.0.0.0", "255.255.255.255"]}
    rangeIP = [[1, 126], [128, 191], [192, 223], [224, 239], [240, 255]]

    for low_high, curClass in zip(rangeIP, ipClass):
        minm, maxm = low_high[0], low_high[1]
        if minm <= first_octet <= maxm:
            ipAddressList = []
            
            start = ipClass[curClass][0]
            end = ipClass[curClass][1]

            print("All IP addresses between:", start, "to", end)

            # for firstBeg, secBeg, thirdBeg, fourthBeg in map(int, start.split(".")):
            for i in range(int(start.split(".")[0]), int(end.split(".")[0]) ):
                for j in range(int(start.split(".")[1]), int(end.split(".")[1]) ):
                    for k in range(int(start.split(".")[2]), int(end.split(".")[2]) ):
                        for l in range(int(start.split(".")[3]), int(end.split(".")[3]) ):
                            ipAddressList.append(str(i) + "." + str(j) + "." + str(k) + "." + str(l))
                            numIPAddressReq -= 1
                            if numIPAddressReq == 0:
                                print(ipAddressList)
                                return
            print(ipAddressList)
returnIPCount()
# 2

da = ['d1','d2','d3','d4']
db = ['1.1.1.1','2.2.2.2','3.3.3.3','4.4.4.4']

for first in range(len(da)):
    for sec in range(len(db)):
        if first != sec:
            print(da[first].strip("''") + " --- '" + db[sec] + "'")

# 3

s1 = "sky is blue in color"
s2 = "Amar likes sky blue color"

s2_freq = defaultdict(int)
for word in s2.split(" "):
    s2_freq[word] = 1
intersectingWords = set()

for word in s1.split():
    if s2_freq[word] == 1:
        intersectingWords.add(word)
print(s2_freq)

print(list(intersectingWords))

# increment and decrement using a function

def inc(num):
    return num + 1
num = 6
print(inc(num))
print(inc(num - 2))
