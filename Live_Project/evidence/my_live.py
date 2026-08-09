import time
import random
L_M=["satheesh","Dhinesh","Pratheesh","Bharath"]
L_F=["Dhiya","Saraswathi"]

O_F=["Vantive","Baxter","Philips","GE"]
O_M=["Airtel","HDFC"]
D_M={}
D_F={}
for L in L_F:
    f=random.choice(O_M)
    D_F[L]=f
    O_M.remove(f)
print(D_F)
for L in L_M:
    f=random.choice(O_F)
    D_M[L]=f
    O_F.remove(f)
print(D_M)