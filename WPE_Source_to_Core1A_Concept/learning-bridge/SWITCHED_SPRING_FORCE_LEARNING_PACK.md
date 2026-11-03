# WPE-E08 · A sudden force switch changes the spring's effective potential

**Role:** original Core1A/Core1B author practice mapped as a proposed topic to **WEP07-01** (reader MODEL/D3; key/SL2/QRT and source status unresolved); not academic admission. The example intentionally does not repeat the original's force reversal-and-doubling numerical situation.

**Learner-owned inference W:** after a sudden constant-force switch, use the **new applied force** for the entire subsequent motion and conserve the **post-switch effective potential** plus kinetic energy; the new second turning point is symmetric about the **new equilibrium**, not about natural spring length or old equilibrium.

## Core1A — guided model: stretch, then a stronger same-direction pull

An ideal horizontal spring has stiffness **k=100 N/m**. Its extension coordinate x is positive RIGHT from natural length x=0. The block is initially motionless at x=+0.10 m under a holding force +10 N, balancing spring force −10 N. At t=0, the holding force is suddenly replaced by **constant +20 N**. Assume frictionless subsequent motion and zero speed at switching.

1. **Keep the coordinate:** x_i=+0.10 m; spring force is −kx. The new applied force is +20 N.
2. **Find NEW equilibrium:** kx_eq=20 N, hence **x_eq=+0.20 m**, not the old +0.10 m.
3. **Write effective potential after the switch:** U_eff(x)=½kx²−F_new x = 50x²−20x J (x in metres).
4. **Conserve only after switching:** at the initial rest position the post-switch energy is U_eff(0.10)=0.5−2=**−1.5 J**.
5. **Find other turning point:** the quadratic U_eff is symmetric about x_eq. The two rest points are x_i=0.10 m and x_other=2x_eq−x_i=**0.30 m**. Check U_eff(0.30)=4.5−6=−1.5 J.

**Wrong path:** conserving *spring energy alone* during the new constant external force, or treating the OLD force as still applied. The constant force does work; including −F_new x in effective potential accounts for it.

## Core1B — independent fresh task: compression to extension after a force switch

A different ideal horizontal spring has stiffness **50 N/m**. With x positive right from natural length, the block is initially held at rest **compressed x_i=−0.20 m** by an external holding force **−10 N**. At time zero the force is suddenly replaced by a constant **+15 N**, and the block is released from rest. Assume no friction. Find the NEW equilibrium, the far positive turning point and an effective-energy check. Explain why spring elastic energy alone is not conserved.

### 01 Predict
Will the block's far positive turning point be symmetric about x=0, about the old compressed position, or about the new equilibrium? Why?

### 02 Attempt
Draw right-positive x, spring force −kx and switched force +15 N. Use U_eff=½kx²−15x after switching; identify x_eq and the second K=0 turning point. Save your first model.

### 03 Reconstruct
Compare the energy calculated at x_i=−0.20 m with the other turning point, making the new-force work explicit.

### 04 Diagnose
Did you forget the minus sign for initial compression, conserve spring energy only, use the old external force after switching or choose symmetry about natural length instead of the new equilibrium?

### 05 Repair
Correct the initial sign or new effective potential, show both turning positions and explain the new equilibrium.

### 06 Boundary test
Keep the initial position x_i=−0.20 m and k=50 N/m, but switch instead to a constant force **+5 N**. Find the new equilibrium and far positive turning point using the post-switch energy.

## Author-only reference — unlock after first attempt

- Initial old force −10 N balances −kx_i = +10 N at x_i=−0.20 m.
- After new +15 N force, x_eq=F_new/k=15/50=**+0.30 m**.
- U_eff=½(50)x²−15x. At x_i=−0.20, U_eff=1+3=**4 J**.
- The second turning position is x_other=2x_eq−x_i=0.60−(−0.20)=**+0.80 m**; there U_eff=½(50)(0.80²)−15(0.80)=16−12=**4 J**. The equilibrium at x=0.30 lies between both turning points.
- **Boundary +5 N:** x_eq=5/50=**0.10 m**, other turning=2(0.10)−(−0.20)=**+0.40 m**. Effective potential at x_i is 1+1=**2 J** and at x_other is 4−2=2 J.
- The initial instantaneous force switch may supply impulse/work in a real actuator; the idealization specifies a force jump at fixed position and zero initial speed. Conserve *post-switch* effective mechanical energy after t=0, not across a finite actuator-motion process.

**Conditions and custody:** ideal Hookean spring, block attached, horizontal frictionless path, constant post-switch force, x measured from natural length, initial equilibrium/rest, fixed-position ideal switch. WEP07-01 is a separate examination candidate with unqualified original key and different force change; no native qualification inferred.
