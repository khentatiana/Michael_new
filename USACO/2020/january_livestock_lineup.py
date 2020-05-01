import sys

sys.stdin("txt.in")
sys.stdout("txt.out")

n = int(input())

cows = ["Beatrice", "Belinda", "Bella", "Bessie", "Betsy", "Blue", "Buttercup", "Sue"]

cowDict = {
    cows[0]: 0,
    cows[1]: 1,
    cows[2]: 2,
    cows[3]: 3,
    cows[4]: 4,
    cows[5]: 5,
    cows[6]: 6,
    cows[7]: 7,
}

constraints = []
for i in range(n):
    constraint = input().split()
    name1, name2 = constraint[0], constraint[5]
    name1, name2 = cowDict[name1], cowDict[name2]

    constraints.append([name1, name2])

newCows = ["Beatrice", "Belinda", "Bella", "Bessie", "Betsy", "Blue", "Buttercup", "Sue"]
cowDictKeys = list(cowDict.keys())
cowDictVals = list(cowDict.values())

for i in range(n):
    name1, name2 = constraints[i]

    if name1 > name2:
        newCows.insert(name2 + 1, cowDictKeys[name1])
    else:
        newCows.insert(name2 - 1, cowDictKeys[name1])

for i in range(8):
    print(newCows[i])
