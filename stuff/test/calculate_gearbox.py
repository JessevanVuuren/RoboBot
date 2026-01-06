# R1(Teeth ring stage1)  = 36
# P1 (Teeth planet stage1) = 12
# S1 (teeth sun stage1) = 12

# R2(teeth ring stage2) = 39
# P2 (teeth planet stage 2) = 12

# final Ratio = 1 / (((R2 - ((R1 / P1)  P2)) / R2)  (S1 / (R1 + S1)))
# final Ratio = 52, not 40

# weird person on internet
# ring = sun + 2 * planets = 52
# ring = sun + 2 * planets 
# ring = 3 * planets 

# R1 = 52
# P1 = 20
# S1 = 12

# R2 = 48
# P2 = 16 



R1 = 39
P1 = 13
S1 = 12

P2 = 10
R2 = 36


# R1 = 40
# P1 = 14
# S1 = 12

# P2 = 11
# R2 = 37


planets = 4
sunRing2 = 37 - (P2 * 2)

amount1 = (S1 + R1) / planets 
amount2 = (sunRing2 + R2) / planets

print(amount1, amount2)


# https://mevirtuoso.com/planetary-gear-simulator/
# https://www.thecatalystis.com/gears/
# https://www.etotheipiplusone.net/?p=1882

final_Ratio = 1 / (((R2 - ((R1 / P1) * P2)) / R2) * (S1 / (R1 + S1)))
print(final_Ratio)
