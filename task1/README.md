# Компьютерные технологии в математическое моделировании

1. Реализовать систему классов для системы частиц: частица( координаты x,y; скорость u, v; масса m; цвет; время жизни),
Эмиттер, который будет генерировать частицы ( расположение эмиттера x,y; вектор, по которому он "выкидывает" частицы u,v )

2. Реализовать GUI, позволяющий конфигурировать и визуализировать систему частиц: кнопка генерации частицы, средства для настройки величины массы (слайдер), вектора скорости частицы, средства для изменения положения эмиттера. Реализовать возможность анимации движения частиц ( по кнопке или в цикле программы с бесконечным расчетным временем ). 
Внешний вид частиц (радиус) должен зависеть от массы.
Реализовать ниспадающее меню для выбор способа решения задачи N тел из п.3.

Рекомендованное средство отрисовки: matplotlib, (seaborn, Bokeh)
Рекомендованные средства для создания GUI: pyQt, (kivy, tkinter, wxWidgets, gtk)

3.
    1. Реализовать решение задачи N тел:
        - с помощью odeint из scipy
        - методом Верле
        - методом Верле, распараллелив вычисления с помощью threading 
        - методом Верле, распараллелив вычисления с помощью multiprocessing
        - методом Верле, реализованным на Cython
        - методом Верле, реализованным на OpenCL или CUDA.

    2. Написать тест, проверяющий, что все решатели из п.1 выдают адекватный результат на примере моделирования движения планет Солнечной системы и расчета методом odeint.

    3. Привести графики 
    - времени работы методов из п.1 (всех, кроме odeint) 
    - ускорения по сравнению с последовательной версией метода Верле
    для N (N=100, 200, 500, 1000) сгенерированных случайным образом частиц. 
    N частиц генерируется один раз, после этого расчет проводится для всех методов, за временной результат берется среднее по 5 запускам время работы.


