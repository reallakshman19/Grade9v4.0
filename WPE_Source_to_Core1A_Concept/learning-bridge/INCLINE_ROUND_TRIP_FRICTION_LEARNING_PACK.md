# WPE-E07 · Friction acts on the way up and the way down

**Role:** authored Core1A/Core1B practice for the unmapped **EX-N39** SYNTHESIZE/D3 reader theme; **NOT_ADMITTED**. The published 30° / half-speed values and exact original key are deliberately not reused. The child must recognize friction's work on both legs, even though gravity's total work cancels on the closed round trip.

**Learner-owned inference W:** use energy and/or acceleration for *ascent*, use a different signed force balance for *descent*, then coordinate the two legs by the same stopping distance; gravity's uphill loss is recovered downhill but friction removes energy twice.

## Core1A — guided model with known downhill forces

A **1 kg** block travels uphill at **4 m/s** on a rough straight incline. Gravity's component along the slope is **6 N downhill**, kinetic friction is **2 N against motion** on either leg. The surface is long enough for the block to return and friction stays the same.

1. **Set uphill positive for the first phase:** both gravity and friction point downhill, so uphill retarding force is 6+2=**8 N**.
2. **Find stopping distance:** starting K=½×1×4²=**8 J**. The 8 N resistance removes 8 J over **1 m**.
3. **Reverse the direction:** during descent gravity's 6 N acts along travel while friction's 2 N points **uphill**, so net downhill force magnitude is 6−2=**4 N**.
4. **Find returned speed:** descent over the same 1 m creates 4 J of kinetic energy, so v_return=√8≈**2.828 m/s**.
5. **Check closed-route work:** gravity contributes −6 J on ascent and +6 J on descent, net zero. Friction contributes −2 J EACH way =−4 J total. K_return−K_initial=4−8=**−4 J**.

**Wrong path:** treating friction as downhill on both legs, or subtracting friction only once. Friction always opposes the direction of motion.

## Core1B — fresh ratio task with a different slope

A block launches uphill on a **45° incline** with initial speed v₀. Kinetic friction coefficient μ is constant. It reaches a stop and slides back to its launch point with speed **(2/3)v₀**. Use sin45°=cos45° and ignore air drag. Find μ without inventing the mass, launch speed or path length.

### 01 Predict
Which force reverses its along-slope sign between ascent and descent: gravity or friction? Must the return speed be smaller than the launch speed if kinetic friction is positive?

### 02 Attempt
Write ascent retarding acceleration g(sinθ+μcosθ), downhill acceleration g(sinθ−μcosθ), and use the **same stopping distance** to relate speed squares. Show your model and μ.

### 03 Reconstruct
Compare the ascent and descent signs, derive the ratio v_return²/v₀²=(sinθ−μcosθ)/(sinθ+μcosθ), then test physical bounds.

### 04 Diagnose
Did you apply friction in the same direction on both legs, forget the square of 2/3, assume gravity loses energy on the closed route, or miss the descent-distance equality?

### 05 Repair
Rebuild both force arrows and the common distance, then recalculate μ separately from the original attempt.

### 06 Boundary test
Keep the same 45° rough incline but the block returns at **(3/4)v₀**. What coefficient μ is implied? Why is it lower than before?

## Author-only solution — reveal after first answer

- Up retarding component is mg(sinθ+μcosθ), so d=v₀²/[2g(sinθ+μcosθ)].
- Down acceleration is g(sinθ−μcosθ); returning from rest over d gives v_return²=2gd(sinθ−μcosθ).
- With sin45°=cos45°, ratio squared r²=(1−μ)/(1+μ). For r=2/3, r²=4/9 and **μ=(1−4/9)/(1+4/9)=5/13≈0.3846**.
- If r=3/4, r²=9/16, **μ=(1−9/16)/(1+9/16)=7/25=0.28**.
- Gravity contributes equal and opposite work across the round trip; friction contributes negative work in **both** directions.
- Check μ≥0 and μ<tan45°=1 so the block actually descends; the slower return speed follows from dissipated energy.

**Conditions and custody:** straight incline, constant normal force, Coulomb kinetic friction, genuine sliding in both directions, same starting/ending positions, no drag. Original EX-N39 has no admitted official key and a different angle/speed ratio; this is an authored bridge, not an exact-task QRT determination.
