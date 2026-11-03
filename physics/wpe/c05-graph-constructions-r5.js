/* R5 C05 graph reasoning candidate signatures; NOT verified original exam plots.
 * Reuses merged gap-six-stage-engine.js, writes separate A/B attempt records,
 * leaves selected bank, source hashes, classifications, and all gateways alone.
 */
(() => {
"use strict";
const pick=(id,label,expected,wrong,mistake,kind="MODEL_CHOICE")=>({id,label,type:"select",choices:["Choose an idea",expected,...wrong,"I'm not sure yet"],expected,mistake,errorKind:kind});
const num=(id,label,expected,tol,mistake,kind="CALCULATION_OR_UNITS")=>({id,label,type:"number",expected,tol,mistake,errorKind:kind});
const reason=(label="Explain your physical law, axes, sign, units and the assumption that makes the operation valid")=>({id:"reason",label,type:"textarea"});
const why=(label="Explain the changed-condition model before reading its worked check")=>({id:"why",label,type:"textarea"});
const task=o=>({prediction:o.prediction,challenge:o.challenge,
 fields:[o.model,o.assumption,...o.numbers,reason(o.reason)],
 hints:o.hints,worked:o.worked,boundary:o.boundary,
 boundaryFields:[o.boundaryModel,...(o.boundaryNumbers||[]),why(o.boundaryWhy)],
 boundaryCheck:o.boundaryCheck});
const frame=(x,lo,hi,a,b)=>a+(x-lo)*(b-a)/(hi-lo);
const round=x=>Math.round(x*1000)/1000;

const G5U={
 source:"EX-M11",title:"A potential-energy curve is a force-sign and steepness map",short:"U(x) segments → signed force and |slope|",
 question:"Do the signs of potential-energy slopes change the RANKING of force magnitudes?",
 sourceCaution:"The available EX-M11 SVG is a smooth curve labeled stable/unstable, not a verified reproduction of the source's A–E four straight-segment plot. Its coaching slope coordinates (and option A) cannot be authenticated from this SVG. All R5 graphs here are deliberately NEW and explicitly labeled examples, never reconstructions of the original exam graph.",
 prerequisites:"For a 1D conservative force, F_x=−dU/dx; with U in J and x in m the slope has J/m=N. On a straight segment between two measured vertices the slope is ΔU/Δx; force has the opposite SIGN, while magnitude |F| uses ABSOLUTE slope. At a sharp corner a single derivative is undefined without a physical smoothing model.",
 core:"Choose axes before computing: U(x) graph means NEGATIVE SLOPE is force, whereas F(x) graph means SIGNED AREA is work. For piecewise-linear U, calculate every interior segment separately, convert units, then rank ABSOLUTE slopes. A horizontal U segment gives F=0, not the greatest force. An x axis in millimetres rather than metres changes conversion to newtons.",
 guide:"GUIDED EXAMPLE (not an original exam graph): a linear magnetic-trap potential has invented vertices (x m,U J) A(0,0), B(1,6), C(3,2), D(5,2), E(7,8). Its signed slopes are +6, −2, 0, +3 J/m. Thus forces are −6, +2, 0, −3 N and magnitude ranking AB>DE>BC>CD.",
 guideSteps:[
  ["Confirm which axes are displayed","Horizontal x (m), vertical potential U (J). The line SLOPE is J/m, not energy or work."],
  ["Read adjacent vertices; do not average across corners","AB ΔU/Δx=+6, BC=(2−6)/(3−1)=−2, CD=0, DE=(8−2)/(7−5)=+3 J/m."],
  ["Recover force DIRECTION","F=−dU/dx, so AB −6N, BC +2N, CD 0N, DE −3N. An increasing U pulls toward decreasing x."],
  ["Rank magnitude, not signed force","Take |F| for each interior segment: 6,2,0,3 N. Therefore AB>DE>BC>CD."],
  ["Ask where the rule is valid","At A/B/C/D/E corners the ideal piecewise graph has left/right slope disagreement; no unique instantaneous force at the corner is asserted."]
 ],
 wrong:"Wrong operator: using the signed slope itself as force, or ranking negative force values rather than absolute magnitudes; using area below U(x) would have units J·m, not N.",
 conditions:"1D position-dependent conservative field and an explicitly piecewise-linear potential; segment interiors have defined constant slopes. The provided guide graph is synthetic and uses SI x metres and U joules.",
 academic:{decision:"First check vertical U versus horizontal x. Negative slope gives SIGNED F; absolute slope gives force magnitude; never take area under U(x) as work.",
 observe:"Select a segment in the new guide's piecewise U(x) graph. The colored segment and its signed slope show that a large negative slope means large positive force, not weak force.",
 validity:"Conservative position field, known x and U units, interior of straight segments. At corners the derivative can be discontinuous or undefined.",
 limit:"A flat U interval gives zero force; a negative slope gives positive F; if the horizontal units shrink from m to 0.1m per tick, force magnitudes grow 10 times.",
 sourceBoundary:"Original EX-M11 author SVG and written step vertices disagree. No original exam force ranking or official answer is asserted from the available picture."},
 slider:{label:"Synthetic U(x): selected straight segment A–B, B–C, C–D, D–E",min:0,max:3,step:1,value:1},
 ...task({
  prediction:"If U rises with increasing x, which direction is the conservative force? Can the most negative signed force still have the LARGEST magnitude?",
  challenge:"TASK A · An ion trap has a NEW explicit piecewise potential (x in METRES, U in JOULES): A(0,0), B(2,10), C(5,4), D(7,4), E(8,7). On each open straight segment, rank |F| from greatest to least. Give signed F along BC and DE. These invented points are NOT the EX-M11 source graph.",
  model:pick("model","Which operation ranks force MAGNITUDES on U(x)?","Rank absolute values of each segment's negative slope",["Rank potential heights at the vertices","Take the signed area underneath U(x)"],"Conservative force is the negative derivative. Take |F| only after computing its sign."),
  assumption:pick("assumption","Where is each force value defined in this ideal graph?","Inside a linear segment, excluding unspecified sharp corners",["At every sharp corner a unique two-sided derivative is automatic","Force magnitudes depend only on vertical heights without Δx"],"Left and right slopes differ at corners; force there requires additional smoothness or a one-sided definition.","INVALID_ASSUMPTION"),
  numbers:[
   num("bc","SIGNED force on BC (N)",2,.08,"BC slope=(4−10)/(5−2)=−2 J/m, hence F=+2N.","SLOPE_SIGN"),
   num("de","SIGNED force on DE (N)",-3,.08,"DE slope=(7−4)/(8−7)=+3 J/m; force is −3N.","SLOPE_SIGN"),
  ],
  reason:"State the force magnitude rank AB>DE>BC>CD and why positive and negative force signs do not alone determine magnitude.",
  hints:["Label the axes: U in J, x in m. Compute ΔU/Δx for EACH open segment.","AB:+5, BC:−2, CD:0, DE:+3 J/m. F is the NEGATIVE slope, not the slope.","Take magnitudes 5,2,0,3 N for ranking: AB>DE>BC>CD."],
  worked:[
   ["Compute actual segment slopes","AB 10/2=+5, BC (4−10)/(5−2)=−2, CD 0, DE (7−4)/(8−7)=+3 J/m."],
   ["Invert signs to get forces","Signed F values are AB −5N; BC +2N; CD 0N; DE −3N."],
   ["Rank absolute values","Magnitudes are 5,2,0,3 N, so AB>DE>BC>CD. This is not a ranking of signed F or U."],
   ["Flag mathematical corners and units","Force is defined here on segment INTERIORS. At a sharp graph vertex the two-sided slope is not automatically defined."]
  ],
  boundary:"CHANGE THE HORIZONTAL SCALE: the same numbered A–E x tick values now denote units of 0.1 METRE per tick (U in J unchanged). What is signed F on DE in NEWTONS, and does the magnitude order change?",
  boundaryModel:pick("model","What happens to the slope when each x unit is 0.1m?", "Every force magnitude grows 10-fold; ordering stays the same",
       ["Forces unchanged because vertical energies unchanged","Only the graph's signed area changes"],"The physical Δx is 10 times smaller for each numeric tick step, so J/m slopes grow 10 times."),
  boundaryNumbers:[num("de","New signed F_DE (N)",-30,.5,"ΔU=3J across physical Δx=0.1m, so F=−30N.")],
  boundaryCheck:"DE has ΔU=+3 J and physical Δx=0.1m, so slope=+30J/m and F_DE=−30N. All slopes scale by 10, so |F| rank stays AB>DE>BC>CD. Reinterpreting axis units changes force, even when the plotted shape looks unchanged."
 }),
 transfer:task({
  label:"Task B · Optical microtrap graph measured in millijoules per millimetre",
  prediction:"Does an upward potential line always mean a force to the right? What unit does mJ/mm represent?",
  challenge:"UNFAMILIAR SETTING: optical-microtrap calibration records NEW vertices (x mm,U mJ): A(0,4), B(1,1), C(3,5), D(5,5). Each consecutive interval is straight. The bead experiences a 1D conservative force. Find signed F_AB, signed F_BC and rank their magnitudes against F_CD. Convert units carefully.",
  model:pick("model","Which graph rule and conversion are required?","F=−ΔU/Δx and 1 mJ/mm equals 1 N",["F=+ΔU/Δx and 1 mJ/mm is 0.001N","Area under U versus x is force"],"Both U and x units scale by 10⁻³, so mJ/mm = N; conservative force has a MINUS sign."),
  assumption:pick("assumption","Which graph observations are enough for each segment?","Straight measured intervals with conservative position force",["Any smooth-looking graph has constant slope everywhere","Potential energy can define dry friction force without limits"],"The segment-specific slope is meaningful for a conservative force on the stated interval.","INVALID_ASSUMPTION"),
  numbers:[
   num("ab","Signed force AB (N)",3,.07,"U decreases 3 mJ across +1 mm, slope −3mJ/mm, F=+3N.","AXIS_UNITS_AND_SIGN"),
   num("bc","Signed force BC (N)",-2,.07,"U increases 4mJ across 2mm; slope +2mJ/mm and F=−2N.","AXIS_UNITS_AND_SIGN"),
  ],
  reason:"Explain why AB force has magnitude 3N, BC 2N, CD 0, and why mJ/mm equals newtons.",
  hints:["Keep the factor 10⁻³ in BOTH potential and displacement; they cancel.","Find each straight segment's ΔU/Δx, then reverse its SIGN to obtain F.","AB slope −3, BC +2, CD zero mJ/mm. Thus F_AB +3N, F_BC −2N and magnitudes AB>BC>CD."],
  worked:[
   ["Inspect the graph's UNITS","U in millijoules and x in millimetres: 1mJ/mm=(10⁻³J)/(10⁻³m)=1N."],
   ["Calculate signed slopes","AB (1−4)/(1−0)=−3mJ/mm; BC (5−1)/(3−1)=+2mJ/mm; CD=(5−5)/(5−3)=0."],
   ["Obtain signed forces","F_AB=+3N, F_BC=−2N, F_CD=0N. Increasing U means force points LEFT."],
   ["Rank only magnitudes","|F_AB|=3>|F_BC|=2>|F_CD|=0N, irrespective of the opposite signs."]
  ],
  boundary:"REVERSE the coordinate definition x′=−x while describing the SAME physical microtrap force field. What is the signed F_AB with respect to x′, and does the physical force MAGNITUDE change?",
  boundaryModel:pick("model","What changes under reversal of the x coordinate?","Signed component reverses; physical magnitude stays unchanged",
    ["Both sign and magnitude reverse","Potential must change by a sign to remain conservative"],"Coordinate reversal flips the signed x-component but does not change the vector's length."),
  boundaryNumbers:[num("ab","Signed F_AB component in x′ (N)",-3,.07,"Originally F_x=+3N; under x′=−x, F_x′=−3N.")],
  boundaryCheck:"The same vector is +3N in the original +x direction, but in x′=−x coordinates its component is −3N. Magnitude remains 3N. Changing coordinates changes signs, not physical force size."
 })
};
const G5E={
 source:"EX-M61",title:"A potential-energy landscape filters allowed kinetic energy",short:"U(x) and total E → K(x), turning and forbidden regions",
 question:"Where can a particle with fixed total energy exist, move, stop or be unable to reach?",
 sourceCaution:"EX-M61's source-author SVG has a proposed E=8J line and potential plateaus, but exact ordinate values and source-equivalent figure are unverified. The coaching choice B is explicitly UNVERIFIED. This lesson uses a different invented graph; it DOES NOT certify an original 'incorrect statement' option.",
 prerequisites:"In 1D with time-independent conservative forces and no losses, total mechanical E=K+U is constant. Thus K(x)=E−U(x)≥0 at physically accessible positions, and v²=2(E−U)/m. If U>E, that part is classically forbidden. A local U≤E point may be disconnected from the current trajectory by an intervening U>E barrier.",
 core:"A potential graph gives kinetic energy from VERTICAL difference E−U at each position, not force from its height. Minimum U among points in the accessible region means maximum K and speed. If a plateau has U=E, K=0 throughout it; a particle cannot 'move slowly' across it without an additional force or energy. A turning point can occur where K=0, but not every K=0 point guarantees movement onward.",
 guide:"GUIDED NEW PROFILE: a 1kg cart in a conservative magnetic channel has synthetic points (x m,U J) (0,12),(1,12),(2,4),(3,16),(4,8) connected linearly. E=12J. At x=2 kinetic energy 8J and speed 4m/s; x=3 is forbidden (U=16>E). The high barrier prevents motion from x=2 to x=4 even though U(4)<E.",
 guideSteps:[
  ["Draw E as a horizontal level","Compare the graph's U(x) height with E=12J. Vertical gap down to U is K, not the graph's slope."],
  ["Calculate locally allowed K","At x2, U=4 so K=8J, v=√(2K/m)=4m/s. At x3, U=16 so K=−4J, physically forbidden."],
  ["Separate local allowance from connectivity","x4 has U=8, K=4J locally, but to reach it from x2 the particle would have to cross the U=16>E barrier."],
  ["Handle U=E exactly","On x0–1, U=E and K=0. A resting particle on a FLAT plateau has zero force and will not traverse the plateau spontaneously."],
  ["Check for source claims","No original potential-point heights are inferred from the unverified EX-M61 SVG. Model-specific x values and slopes are guide-only."]
 ],
 wrong:"Wrong: fastest motion where potential is greatest; K=E−U has the opposite relationship. Also wrong: every point with U<E can be reached from any starting point, despite barriers; K=0 is not a moving finite speed.",
 conditions:"Conservative 1D time-independent potential; specified fixed E, known m, no losses or hidden work; x paths constrained to the drawn continuous branch. If E changes or a motor acts, update the entire energy level.",
 academic:{decision:"For U(x) and a stated E, compare E with U and the whole connecting profile. Do not take an area under U(x) to find K.",
 observe:"Move the guide's horizontal E-level line: the allowed/forbidden status at x=2 and x=3 changes, while the U curve itself does not.",
 validity:"K=E−U applies to a fixed mechanical-energy ledger, with no friction, motor or explicit time dependence.",
 limit:"At U=E, speed=0; on a flat U=E plateau there is no tangential conservative force to initiate motion. If the energy lies below a barrier, a lower-U region beyond it can be locally allowed but inaccessible from a given side.",
 sourceBoundary:"Unverified figure and coaching option B remain HOLD; no invented original ordinate or motion region is certified."},
 slider:{label:"Synthetic U(x): total mechanical energy E (J)",min:6,max:18,step:1,value:12},
 ...task({
  prediction:"Is a location with U<E always reachable from a specific start? What happens where U=E or U>E?",
  challenge:"TASK A · A 2kg marble moves in a conservative ONE-DIMENSIONAL potential with synthetic connected vertices: A(x0,U3J), B(x1,U9J), C(x2,U12J), D(x3,U1J), all straight between. Total E=9J; it begins at A moving right. Find K at A and locally at D, determine if C is classically allowed and whether D is reachable without added energy.",
  model:pick("model","Which mathematical and physical tests are needed?","K=E−U for local allowance AND barrier connectivity from A",["Force is the area under U(x)","A low potential at D guarantees travel there irrespective of barriers"],"A point can be locally energy-allowed but disconnected from the starting motion by a higher U>E interval."),
  assumption:pick("assumption","What makes E a valid fixed reference?","No friction or extra work, fixed conservative U(x), continuous 1D path",["A motor provides unspecified energy but E remains 9J","Any negative K is physically permitted"],"Classical K must be nonnegative and conserved E only holds without hidden transfers.","INVALID_ASSUMPTION"),
  numbers:[num("ka","Kinetic energy at A (J)",6,.15,"E−U_A=9−3=6 J."),
           num("kd","LOCAL algebraic kinetic energy at D (J)",8,.15,"E−U_D=9−1=8J, but being locally allowed does not imply reachable.")],
  reason:"Explain that C is forbidden (U=12>E9) and D is inaccessible from A over the barrier despite its local 8J kinetic allowance.",
  hints:["Draw the horizontal E=9J line and mark U values above it.","At A K=9−3=6; at D local K=9−1=8; at C K would be −3J.","Trace the entire segment B→C→D: it rises above E. Motion from A cannot pass that barrier in classical energy-conserving mechanics."],
  worked:[
   ["Use energy as a vertical gap","At A K=9−3=6 J; D has a locally allowable K=9−1=8 J."],
   ["Detect forbidden region","At C, U=12J>E=9J, making K=−3J, impossible for an ordinary classical particle."],
   ["Check connectivity rather than isolated points","The straight-line profile crosses U=9 at B before rising to 12 at C; a bead moving from A cannot cross the forbidden B–C section."],
   ["State the two different conclusions","D is algebraically locally allowed, but the bead starting at A cannot reach D without added energy or another path."]
  ],
  boundary:"ADD 4J of external mechanical energy to the SAME marble before it reaches the barrier, so E becomes 13J and no further work/loss occurs. What is K at C? Can the marble cross C and reach D under the specified profile?",
  boundaryModel:pick("model","What does adding energy BEFORE the barrier change?","All points on the stated profile become energy-allowed when E=13J",["The previous forbidden interval remains forbidden regardless of E","K at C remains negative because its potential is large"],"Maximum U of the profile is 12J, below the new E=13J."),
  boundaryNumbers:[num("kc","New K at C (J)",1,.08,"K_C=13−12=+1J.")],
  boundaryCheck:"With E=13J, the full synthetic profile has U≤12J, so no part of this given segment is energy-forbidden. K_C=13−12=+1J, and D is reachable from A along the model path, unlike in the original 9J ledger."
 }),
 transfer:task({
  label:"Task B · Roller coaster gravitational-height map and an intervening hill",
  prediction:"If a roller coaster has enough total energy for a low valley beyond a hill, is it guaranteed to pass the hill?",
  challenge:"UNFAMILIAR SETTING: a 2kg carriage rolls without friction along a one-way vertical-profile track whose continuous height-versus-distance graph passes through (x m,h m): A(0,0.5), B(1,1.5), C(2,2.5), D(3,0.8), with straight connections. Take g10 and total mechanical E=40J with potential U=0 at h=0. Find K at B and locally at D. Can it move from A through C to D on this track?",
  model:pick("model","What representation gives energy and reachability?","Convert h(x) to U=mgh, then require E≥U along the ENTIRE path",["Take the area under h(x) to find kinetic energy","The final low point D alone proves it can cross the hill"],"Height is converted to gravitational U; an intervening U>E barrier blocks classical transit."),
  assumption:pick("assumption","Which track model permits using constant E?","Smooth stationary track, no braking/motor and constant g",["Unknown motor work throughout the hill","A moving guide adds unknown mechanical energy"],"The stated E applies only to the lossless fixed-track model.","INVALID_ASSUMPTION"),
  numbers:[num("kb","Kinetic energy at B (J)",10,.16,"U_B=2×10×1.5=30J; K=40−30=10J."),
           num("kd","LOCAL K at D (J)",24,.18,"U_D=2×10×0.8=16J; K=24J, though that does not prove arrival.")],
  reason:"Explain that at C, U=50J exceeds E=40J and the carriage cannot cross from A to D despite local K_D>0.",
  hints:["Vertical graph measures h (m), NOT energy. Multiply h by mg to obtain U.","E=40; at B U=30 K=10; at C U=50 > E; D has U=16 K=24 locally.","Passing through a hill with U>E would require negative K. A locally allowed valley beyond it does not provide a route."],
  worked:[
   ["Convert the axes to physical potential","U=mgh with m2, g10: at B U=30J; at C U=50J; at D U=16J."],
   ["Compute independent local values","K_B=40−30=10J and K_D(local)=40−16=24J."],
   ["Check the entire path","The hill at C requires 50J, but E is only 40J. The carriage turns before C and cannot reach D from A."],
   ["Name the missing inference","A force or speed at a separated endpoint does not prove that the path between endpoints is dynamically accessible."]
  ],
  boundary:"A MOTOR adds 15 J to the carriage's mechanical energy just after A and then switches OFF. E=55J for the remainder. What is K at the top of hill C, and can it cross now?",
  boundaryModel:pick("model","What changes after a stated finite motor work increment?","New constant E=55J exceeds the entire height barrier",["Motor energy never affects kinetic energy","The old E=40J remains conserved after a motor adds 15J"],"External motor work changes E, which is constant again only after the motor stops."),
  boundaryNumbers:[num("kc","Kinetic energy at C (J)",5,.11,"U_C=50J; K_C=55−50=5J.")],
  boundaryCheck:"After the +15J input, E=55J. The maximum profile potential is U_C=50J, so K_C=5J>0 and the carriage may pass C in the ideal no-loss model. Without the motor it was forbidden."
 })
};
const G5P={
 source:"EX-M69",title:"Constant POWER decides speed and displacement-time curvature",short:"Constant P → v(t), s(t) curvature, not a graph guess",
 question:"What does an s-versus-t curve look like when mechanical POWER is constant instead of FORCE?",
 sourceCaution:"EX-M69 has FOUR source options consisting only of missing [FIG-options-*] images, with no accessible authentic figures. None of A/B/C/D can be matched to a curve from the present evidence. The source steps implicitly assume a start from rest; finite nonzero constant power at exactly v=0 needs an idealized singular initial acceleration, so the t→0 solution is a limiting model, not a realistic finite-force launch.",
 prerequisites:"Power P=dK/dt = F·v. For a 1D constant-mass system driven by constant positive MECHANICAL power with no losses, K=½mv², so d(v²)/dt=2P/m. Therefore v(t)=√(u²+2Pt/m), and s(t)−s(0)=∫v(t)dt = [m/(3P)]{(u²+2Pt/m)^(3/2)−u³}, P>0. The slope ds/dt is speed, and the second derivative d²s/dt²=P/(mv)>0 for v>0.",
 core:"Starting formally from rest gives v∝√t and s∝t^(3/2), with increasing slope and decreasing positive curvature magnitude; NONZERO u instead gives s=[m/(3P)]{(u²+2Pt/m)^(3/2)−u³}, not a pure power law. Constant power differs from constant force (v∝t, s∝t² starting at rest); using an area under s(t) has no standard work meaning.",
 guide:"GUIDED (ideal post-start model, not the source graph): m=4kg, positive mechanical P=18W, u=0 at ideal t=0. For t>0, v=3√t m/s, s=2t^(3/2) metres; at t=4s, v=6m/s and s=16m. At the exact rest instant P=Fv would require unbounded F to keep P finite, so real drives start by a transition with finite force.",
 guideSteps:[
  ["Read the s–time axes","Displacement vertical (m), time horizontal (s). Slope is velocity (m/s); positive CURVATURE means increasing speed."],
  ["Start with a power ledger","P=d(½mv²)/dt, not P=constant force. Integrate over time: v²=u²+2Pt/m."],
  ["Derive a curve instead of picking its appearance","With ideal u0, m4, P18, v=3√t and s=∫3√t dt=2t^(3/2)."],
  ["Check concrete times and tangent slope","At t4, s=16m, v=6m/s. The curve increases and has positive curvature for t>0."],
  ["Mark the startup and figure limits","Finite positive power at exactly zero speed is an unphysical infinite-force limit. No missing EX-M69 option graph is recreated or selected."]
 ],
 wrong:"Wrong: constant power implies constant acceleration or a straight displacement-time line. Also wrong: claim a source option letter from unavailable figure images. Slope of s(t) is velocity; its area has units m·s, not kinetic-energy work.",
 conditions:"One-dimensional forward translation, constant positive MECHANICAL power transferred to kinetic energy, mass fixed, no losses or resistance, t>0 for formal rest start. With u>0 the initial acceleration stays finite; graph options absent remain unverified.",
 academic:{decision:"Derive d(v²)/dt from power before judging the DISPLACEMENT versus TIME curve; do not assume constant F.",
 observe:"Move time on an explicitly NEW s=2t^(3/2) graph. Its s grows faster than linearly, tangent slope v rises as √t, and acceleration falls for t>0.",
 validity:"Constant mechanical input P, fixed mass, no losses; actual startup from exactly zero speed needs a finite-force phase outside the ideal t>0 model.",
 limit:"At P→0 for nonzero u, s→ut and the s(t) graph becomes a straight line. For u=0 and t>0, s∝t^(3/2); at t=0 the ideal acceleration singularity must be disclosed.",
 sourceBoundary:"EX-M69 four option pictures are missing. No source option, curve identity, or official key is certified."},
 slider:{label:"Ideal guide: time t (seconds), P18W, m4kg, u0 limit",min:.25,max:4,step:.25,value:2},
 ...task({
  prediction:"Does constant motor power imply constant force? If an object already moves, must s(t) follow exactly t^(3/2)?",
  challenge:"TASK A · An automated towing winch supplies constant net MECHANICAL power P=50W to a 4kg frictionless cart already moving at u=5m/s at t0. Find its speed after 3s and displacement during those 3s. State whether the displacement-time curve is convex or linear, and why pure t^(3/2) is not exact here.",
  model:pick("model","Which dynamics law correctly determines displacement?", "Integrate v(t)=√(u²+2Pt/m) after a kinetic-energy rate equation",
    ["Use constant acceleration a=P/m","Use a straight line s(t)=ut because power is constant"],"Power is energy/time; F=P/v changes with speed, so acceleration is not constant."),
  assumption:pick("assumption","Which start and energy conditions are actually specified?", "Nonzero starting speed, fixed mass and all net power going into kinetic energy",
    ["Cart starts at rest with unbounded startup force assumed physically real","Unknown friction loss but all 50W still increases kinetic energy"],"The given nonzero u avoids the exact-rest singularity; losses would alter the net power.","INVALID_ASSUMPTION"),
  numbers:[num("speed","Speed at t=3s (m/s)",10,.12,"v²=25+(2×50/4)×3=100."),
           num("distance","Displacement over 3s (m)",70/3,.22,"∫_0³√(25+25t)dt = 2/(3×25)[1000−125]=70/3m.")],
  reason:"Explain that acceleration decreases with speed while s(t) has positive curvature, and why nonzero u changes the pure rest-start scaling.",
  hints:["Integrate P=d(½mv²)/dt to find v²=u²+(2P/m)t.","At t=3, v²=100, giving 10m/s. Displacement is the AREA under v(t), not under s(t).","Use ∫√(25+25t)dt = (2/(75))(25+25t)^(3/2) and evaluate 0..3."],
  worked:[
   ["Start with exact energy rate","2P/m=(2×50)/4=25 m²/s³, so v²(t)=25+25t and v(3)=√100=10m/s."],
   ["Integrate speed for distance","s(3)−s(0)=∫₀³√(25+25t)dt = [2(25+25t)^(3/2)/75]₀³."],
   ["Evaluate the endpoint powers","(100)^(3/2)=1000; (25)^(3/2)=125. Distance=(2/75)(875)=70/3≈23.333m."],
   ["Check curve type","Velocity rises and a=P/(mv)>0, so s(t) curves upward, but starting u=5 means it is not proportional only to t^(3/2)."]
  ],
  boundary:"AFTER t=3s the winch switches OFF and no resistive forces act for another 2 seconds. What ADDITIONAL distance is covered during the motor-OFF interval, and what graph shape applies?",
  boundaryModel:pick("model","What does zero net power and no force imply after shutdown?","Speed stays 10m/s; s(t) is linear during the extra 2s",
     ["It instantly stops when P becomes zero","It continues increasing as t^(3/2) with P off"],"With no net force or work, velocity is constant at the switch-off value."),
  boundaryNumbers:[num("distance","Extra motor-OFF displacement (m)",20,.18,"10m/s times 2s=20m.")],
  boundaryCheck:"At switch-off speed is 10m/s. With P_net=0 and no other tangential force, speed stays 10m/s. Extra distance over 2s is 20m; the new s(t) segment is straight."
 }),
 transfer:task({
  label:"Task B · Airport baggage trolley with constant useful power",
  prediction:"Why does a moving electric trolley speed up more slowly as it gets faster if its useful mechanical watts are fixed?",
  challenge:"UNFAMILIAR SETTING: a baggage trolley of mass 2kg rolls horizontally with negligible resistance. Its motor supplies useful constant MECHANICAL power 8W, starting speed 3m/s. Compute speed and distance after 2s. Show why force cannot be treated as constant.",
  model:pick("model","Which feature of a constant-power drive changes as speed rises?","F=P/v falls while v² grows linearly in time",
       ["F stays constant at P/m","Acceleration stays constant because mechanical power is constant"],"A fixed power source does decreasing force at higher v: F=P/v."),
  assumption:pick("assumption","Which output is included in the 8W value?", "Useful mechanical power after losses, with negligible resistance",
    ["8W is electrical input while motor efficiency is unknown","Unknown drag absorbs a variable part of 8W"],"Without an efficiency or loss model, electrical input watts cannot all be assigned to kinetic energy.","INVALID_ASSUMPTION"),
  numbers:[num("speed","Trolley speed at t=2s (m/s)",5,.08,"v²=9+(2×8/2)×2=25."),
           num("distance","Distance traveled in 2s (m)",49/6,.14,"∫₀²√(9+8t)dt = 2/(3×8)[125−27]=49/6m.")],
  reason:"Explain in words why useful constant watts raise kinetic energy linearly while acceleration decreases with speed.",
  hints:["Mechanical P=d(½mv²)/dt gives v²=9+8t.","After 2s, v²=25. For distance integrate speed √(9+8t), not its square.","s=(2/(3×8))[(9+8t)^(3/2)−27]; at t2 gives 49/6m."],
  worked:[
   ["Energy rate in seconds","2P/m=(2×8)/2=8, giving v²(t)=9+8t."],
   ["Speed at requested time","v²(2)=25 ⇒ v(2)=5m/s."],
   ["Integrate the velocity shape","s(2)=∫₀²√(9+8t)dt = 2/(24)(125−27)=98/12=49/6≈8.167m."],
   ["Inspect the physical driver","Since F=P/v, the motor force decreases as speed rises. Distance-time curvature is positive, but not quadratic as for constant acceleration."]
  ],
  boundary:"Motor input remains 8W ELECTRICAL, but the MECHANICAL efficiency drops to 50% throughout an independent 2s run at the same initial 3m/s; resistance is negligible. Find new final speed and displacement.",
  boundaryModel:pick("model","What energy rate now accelerates the trolley?", "Useful mechanical power is 4W, not the 8W electrical input",
     ["All electrical power remains 8W useful to kinetic energy","An unspecified motor efficiency does not affect kinetic-energy rate"],"Only ηP_electric is mechanical power when efficiency is specified."),
  boundaryNumbers:[num("speed","New speed after 2s (m/s)",Math.sqrt(17),.09,"v²=9+(2×4/2)×2=17."),
                   num("distance","New displacement (m)",(17*Math.sqrt(17)-27)/6,.14,"Integrate √(9+4t), result [2/(3×4)](17^(3/2)−27).")],
  boundaryCheck:"Useful power=0.5×8=4W. v²=9+4t, so v(2)=√17≈4.123m/s. Distance=(2/(3×4))[(17)^(3/2)−27]=(17√17−27)/6≈7.18m. Mechanical efficiency, not a guessed graph option, selects the curve."
 })
};
