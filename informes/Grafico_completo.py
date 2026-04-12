import matplotlib.pyplot as plt

meses = [1,2,3,4]
ventas = [100,120,90,140]

plt.plot(meses, ventas)
plt.title("Ventas mensuales")
plt.xlabel("Mes")
plt.ylabel("Ventas")
plt.show()