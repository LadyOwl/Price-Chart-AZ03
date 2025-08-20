import numpy as np
import matplotlib.pyplot as plt

# Генерация двух наборов случайных данных по 5 элементов
random_array_x = np.random.rand(5)  # массив из 5 случайных чисел
random_array_y = np.random.rand(5)  # второй массив из 5 случайных чисел

# Вывод массивов (как в примере)
print("X данные:", random_array_x)
print("Y данные:", random_array_y)

# Построение диаграммы рассеяния
plt.figure(figsize=(8, 6))
plt.scatter(random_array_x, random_array_y, color='purple', edgecolors='k', s=60)
plt.title('Диаграмма рассеяния: два набора по 5 случайных чисел')
plt.xlabel('X (np.random.rand)')
plt.ylabel('Y (np.random.rand)')
plt.grid(True, alpha=0.3)
plt.show()