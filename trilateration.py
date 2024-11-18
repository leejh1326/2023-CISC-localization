import numpy as np
import matplotlib.pyplot as plt
import time

# AP 좌표와 반지름 설정
AP1 = (5, 5)
AP1_radius = 6
AP2 = (5, 15)
AP2_radius = 6
AP3 = (13, 10)
AP3_radius = 7

# 그림 그렸음
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
plt.plot(*AP1, 'bo')
plt.plot(*AP2, 'bo')
plt.plot(*AP3, 'bo')

num_trials = 5000  # 시뮬레이션 반복 횟수
total_error = 0  # 총 오차
num_success = 0  # 위치 추정이 성공한 횟수

start_time = time.time()  # 코드 실행 시작 시간 기록
for i in range(num_trials):
    # 무작위로 사용자 위치 생성
    user_loc = np.random.uniform(-5, 25, size=2)

    # 각 AP에서 사용자 위치까지의 거리 계산
    d1 = np.linalg.norm(user_loc - np.array(AP1))
    d2 = np.linalg.norm(user_loc - np.array(AP2))
    d3 = np.linalg.norm(user_loc - np.array(AP3))


    # 위치 추정
    A = np.array([[2 * (AP1[0] - AP3[0]), 2 * (AP1[1] - AP3[1])],
                  [2 * (AP2[0] - AP3[0]), 2 * (AP2[1] - AP3[1])]])
    b = np.array([d3**2 - d1**2 - AP3[0]**2 - AP3[1]**2 + AP1[0]**2 + AP1[1]**2,
                  d3**2 - d2**2 - AP3[0]**2 - AP3[1]**2 + AP2[0]**2 + AP2[1]**2])

    if d1 > AP1_radius and d2 > AP2_radius and d3 > AP3_radius:   #전파 닿지 않는부분은 제거해야해서!! 추가함.
        user_loc_est = None
    else:
      user_loc_est = np.linalg.solve(A, b)



    # 추정된 위치가 정확한지 검증
    if user_loc_est is not None:
        error = np.linalg.norm(user_loc - user_loc_est)
        #rx가 안찍혀서 문젠가 했는데, 거의 동일하게 찍혀서 그런가보네.
        #print(user_loc, " - ", user_loc_est, " = ", user_loc - user_loc_est)
        total_error += error

        plt.plot(*user_loc, 'ro')
        plt.plot(*user_loc_est, 'gx')

        if error <= 0.5:  # 오차가 0.5 이내면 위치 추정 성공으로 간주
            num_success += 1

end_time = time.time()  # 코드 실행 종료 시간 기록
elapsed_time = end_time - start_time  # 실행 시간 계산
print(num_trials, "번 반복시 Elapsed time: ", elapsed_time,"  seconds")

print(f"MAE: {total_error / num_trials:.2f}")
print("MAE: ",total_error / num_trials)