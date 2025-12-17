import maya.cmds as cmd
import random


base = cmd.joint()
mid = cmd.joint()
end = cmd.joint()


randomTranslate = random.choice([random.uniform(-30.0, -20.0), random.uniform(20.0, 30.0)])
randomAxis = random.randint(0,2)
print('randomTranslates = ' + str(randomTranslate))
print('randomAxis = ' + str(randomAxis))

translates = [0, 0, 0]
translates[randomAxis] = randomTranslate
print('translates = ' + str(translates))

cmd.select(base, r = 1)
cmd.move(random.uniform(100.0, 300.0), -26, 0)
cmd.select(mid, end, r = 1)
cmd.move(translates[0], translates[1], translates[2], r = 1, os = 1, wd = 1)



randomOrient = random.choice([random.uniform(-17.0, -2.0), random.uniform(2.0, 17.0)])
angleIDs = [0, 1, 2]
angleIDs.remove(randomAxis)
print('randomOrient = ' + str(randomOrient))
print('angleIDs = ' + str(angleIDs))

orients = [0, 0, 0]
orientsAxis = random.choice(angleIDs)
orients[orientsAxis] = randomOrient
print('orientsAxis = ' + str(orientsAxis))
print('orients = ' + str(orients))

cmd.select(mid, r = 1)
cmd.rotate(orients[0], orients[1], orients[2])



cmd.select(d = 1)