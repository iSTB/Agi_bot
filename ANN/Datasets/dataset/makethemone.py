import numpy as np

import pickle

import matplotlib.pyplot as plt

f= open("behaviour_right.pickle","rb")
right = pickle.load(f)

f= open("behaviour_left.pickle","rb")
left = pickle.load(f)

f= open("behaviour_nothing.pickle","rb")
nothing = pickle.load(f)

f= open("behaviour.pickle","rb")
nothing.extend(pickle.load(f))

right = np.array(right).astype(float)
right /= 550.
right *= 2.
right -=1.
right = [val for val in right for _ in range(4)]
right = np.array(right)
turn_right = np.zeros(right.shape)-.9
turn_right[25:100,4] = .9
turn_right[40:100,0] = .9 
turn_right[100:,2] = .9
print turn_right.shape
#(25,100),(100,152)

left = np.array(left).astype(float)
left /= 550.
left *= 2.
left -=1.
left = [val for val in left for _ in range(4)]
left = np.array(left)
turn_left = np.zeros(left.shape)-.9
turn_left[30:70,5] = .9 
turn_left[35:70,1] = .9
turn_left[70:,2] = .9
print turn_left.shape
#30,70 70,112

nothing = np.array(nothing).astype(float)
nothing /=550.
nothing *= 2.
nothing -=1.
nothing = [val for val in nothing for _ in range(4)]
nothing = np.array(nothing)
do_nothing = np.zeros(nothing.shape)-.9
do_nothing[400:600,4] = .9
do_nothing[400:600,1] = .9
print do_nothing.shape
#400,600

all_tog = np.append(do_nothing, turn_left)
all_tog1 = np.append(do_nothing, turn_right)
al = np.append(all_tog,all_tog1)
al = np.append(al,do_nothing).reshape((22536/6,6))
output = al

train_idx =[(400,600),(1194,1234),(1234,1276),(1676,1876),(1901,1976),(2376,2576)]

idle_idx = [(0,400),(600,1194),(1234,1234),(1276,1676),(1876,1901),(1976,2376),(2576,3140)]

all_tog = np.append(nothing, left)
all_tog1 = np.append(nothing, right)
al = np.append(all_tog,all_tog1)
al = np.append(al,nothing).reshape((22536/6,6))
inputs = al

print al.shape
plt.figure()
plt.plot(inputs)

plt.figure()
plt.plot(output)

# plt.show()

# import pickle
# f= open("dataset.pickle","wb")
# pickle.dump([inputs,output],f)
# f.close()

# plt.figure()
# for i, v in enumerate(right.transpose()):
# 	plt.plot(v,label=str(i))
# plt.legend()	
# plt.plot(turn_right)

# plt.figure()
# plt.plot(left)
# plt.plot(turn_left)

# plt.figure()
# plt.plot(nothing)
# plt.plot(do_nothing)
