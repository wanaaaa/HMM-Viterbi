def printEmitBox(box):
    for key in box.keys():
        print(key, "->", box[key])

stateTran = {'s0': {'s1':0.6, 's2':0.2, 's3':0.2},
                's1': {'s1':0.8, 's2':0.1, 's3':0.1},
                's2': {'s1':0.2, 's2':0.7, 's3':0.1},
                's3': {'s1':0.1, 's2': 0.3, 's3':0.6}}
emissionProb = {'s1':{'eA':0.7, 'eB':0, 'eC':0.3},
                's2':{'eA':0.1, 'eB':0.9, 'eC':0},
                's3':{'eA':0, 'eB':0.2, 'eC':0.8}}

observedEmi = ['eA', 'eC', 'eA', 'eC', 'eC', 'eB']
emiStage = ['e1', 'e2', 'e3', 'e4', 'e5', 'e6']
emitBox = {ele:{} for ele in  emiStage}
backTrackBox = {}

preEnum = -777
for iNum, emitNum in enumerate(emiStage):
    # print("---->", iNum, emitNum)
    obsEmi = observedEmi[iNum]
    if iNum == 0:
        for stateKey in emissionProb.keys():
            initPro = stateTran['s0'][stateKey]
            emitBox[emitNum][stateKey] = initPro * emissionProb[stateKey][obsEmi]
        continue

    preEnum = emiStage[iNum - 1]
    backTrackBox[preEnum] = {}
    for stateKey in emissionProb.keys():
        temMax = -777
        for preStateKey in emissionProb.keys():
            preEmi = emitBox[preEnum][preStateKey]
            transi = stateTran[preStateKey][stateKey]
            tempPro = preEmi*transi
            if tempPro > temMax:
                temMax = tempPro
                maxKey = preStateKey

        emiPro = emissionProb[stateKey][obsEmi]
        emitBox[emitNum][stateKey] = temMax*emiPro
        backTrackBox[preEnum][stateKey] = maxKey

optimalPath = {}
preEmi = "xxx"
for currentEmi in sorted(emiStage, reverse=True):
    if currentEmi == 'e6':
        maxPro = -777
        maxKey = "xxx"
        for currentState in emitBox['e6'].keys():
            if maxPro < emitBox['e6'][currentState]:
                maxPro = emitBox['e6'][currentState]
                maxKey = currentState
        optimalPath[currentEmi] = maxKey
        preEmi = currentEmi
        continue

    optimalPath[currentEmi] = backTrackBox[currentEmi][optimalPath[preEmi]]
    preEmi = currentEmi

print("emitBox =====================================================")
printEmitBox(emitBox)
print("backTrackBox =====================================================")
printEmitBox(backTrackBox)
print("optimalPath =====================================================")

for key in emiStage:
    print(key, "->", optimalPath[key])
