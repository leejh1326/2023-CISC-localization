#coarse한 측위
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import time
import math


# AP 좌표와 반지름 설정
AP1 = (5, 5)
AP1_radius = 6
AP2 = (5, 15)
AP2_radius = 6
AP3 = (13, 10)
AP3_radius = 7

# 그림 그렸음
AP1_AP2_dist = distance.euclidean(AP1, AP2)
AP1_AP3_dist = distance.euclidean(AP1, AP3)
AP2_AP3_dist = distance.euclidean(AP2, AP3)
circle1 = plt.Circle(AP1, AP1_radius, fill=False, linestyle='--')
circle2 = plt.Circle(AP2, AP2_radius, fill=False, linestyle='--')
circle3 = plt.Circle(AP3, AP3_radius, fill=False, linestyle='--')
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')
ax.set_xlim((-5, 25))
ax.set_ylim((-5, 25))
ax.add_artist(circle1)
ax.add_artist(circle2)
ax.add_artist(circle3)

# add circle centers - AP 중심 좌표 -> 파란색으로 찍음.
plt.plot(*AP1, 'y', marker='o', markersize=10)   # 진한 노랑으로 변경
plt.plot(*AP2, 'y', marker='o', markersize=10)
plt.plot(*AP3, 'y', marker='o', markersize=10)
# plt.plot(*AP1, 'yo')   #bo파랑말고 노랑으로 변경
# plt.plot(*AP2, 'yo')
# plt.plot(*AP3, 'yo')

################################## TODO: 1단계 구역 미리 정하기##################################
#  AP1, 2, 3의 신호가 도달하는지 안하는지에 따라, 총 8개의 구역으로 나뉜다.
#  삼변측위에 비해 정확하진 않지만 어느 지역쯤에 있는지 위치를 추정하는 코드 작성해야함

#estimated_pos_XXX는 None이라 따로 적지 않겠음.
estimated_pos_OXX = AP1
estimated_pos_XOX = AP2
estimated_pos_XXO = AP3
estimated_pos_OOX = (AP1[0]+AP2[0])/2, (AP1[1]+AP2[1])/2  # (AP12의 x 좌표평균, AP12의 y 좌표평균)로 설정
estimated_pos_OXO = (AP1[0]+AP3[0])/2, (AP1[1]+AP3[1])/2
estimated_pos=XOO = (AP2[0]+AP3[0])/2, (AP2[1]+AP3[1])/2
estimated_pos_OOO = estimated_pos = ((AP1[0] + AP2[0] + AP3[0] ) / 3, (AP1[1] + AP2[1] + AP3[1] ) / 3)

#2. 통신횟수 (삼변측위는 6번, 제안방식은 구역따라 달라지는데 4,5,6번)
cnt_4 = 0
cnt_5 = 0
cnt_6 = 0
cnt_0 = 0   #신호가 잡히지 않는 구역 -> 총 5000개 맞나 확인하려고

num_trials = 500  # 시뮬레이션 반복 횟수
total_error = 0  # 총 오차
num_success = 0  # 위치 추정이 성공한 횟수

start_time = time.time()  # 코드 실행 시작 시간 기록
for i in range(num_trials):
    # 실제 위치를 무작위로 선택 - 난수 최소값~ 난수 최대값
    actual_pos = np.random.uniform(-1, 21, size=2)

    ################################## TODO: 2단계 8개 구역 할당 ##################################
    #세 개의 점(AP1, AP2, AP3)과 실제 위치(actual_pos) 사이의 유클리디안 거리를 계산
    AP1_dist = distance.euclidean(actual_pos, AP1)
    AP2_dist = distance.euclidean(actual_pos, AP2)
    AP3_dist = distance.euclidean(actual_pos, AP3)


    # 8개 구역 중에서 가장 가능성이 높은 구역을 찾아냄 ->  'dist<radius'면 반지름보다 좁은 곳에 위치 = 신호 수신O

    if AP1_dist > AP1_radius and AP2_dist > AP2_radius and AP3_dist > AP3_radius:        #3개의 신호가 닿지X
        estimated_pos = None
        cnt_0+=1
    elif AP1_dist < AP1_radius:
        if AP2_dist >= AP2_radius:
            if AP3_dist >= AP3_radius:         #1(O) 2(X) 3(X)
                estimated_pos = estimated_pos_OXX
                cnt_4+=1
            else:                              #elif AP3_dist < AP3_radius:   #1(O) 2(X) 3(O)
                estimated_pos = estimated_pos_OXO
                cnt_5+=1
        else:                                  #elif AP2_dist < AP2_radius:
            if AP3_dist >= AP3_radius:         #1(O) 2(O) 3(X)
                estimated_pos =      estimated_pos_OOX
                cnt_5+=1
            else:                              #elif AP3_dist < AP3_radius:    #1(O) 2(O) 3(O)
                estimated_pos = estimated_pos_OOO
                cnt_6+=1
    else:                                      #elif AP1_dist >= AP1_radius
        if AP2_dist < AP2_radius:
            if AP3_dist >= AP3_radius:         #1(X) 2(O) 3(X)
                estimated_pos = estimated_pos_XOX
                cnt_4+=1
            else:                              #elif AP3_dist < AP3_radius:   #1(X) 2(O) 3(O)
                estimated_pos = estimated_pos=XOO
                cnt_5+=1
        else:                                  #elif AP3_dist < AP3_radius:  #1(X) 2(X) 3(O)
            estimated_pos = estimated_pos_XXO
            cnt_4+=1


    # 위치 추정이 성공하면, 위치 오차 계산 및 통계량 업데이트
    if estimated_pos is not None:
        error = distance.euclidean(actual_pos, estimated_pos)
        total_error += error
        num_success += 1
        plt.plot(*actual_pos, 'o', color='gray')        # plt.plot(*actual_pos, 'ro')  #ro대신 회색으로 변경 light
        plt.plot(*estimated_pos, 'rx')  #gx대신 rx로 변경


end_time = time.time()  # 코드 실행 종료 시간 기록
elapsed_time = end_time - start_time  # 실행 시간 계산

print(num_trials, "번 반복시 Elapsed time: ", elapsed_time,"  seconds")

final_accuracy = total_error / num_success
print("MAE :", final_accuracy, "\n")   #, "=", total_error, "(total error)/(num_success인)", num_success

print(cnt_4, cnt_5, cnt_6, cnt_0, cnt_4+cnt_5+cnt_6+cnt_0)