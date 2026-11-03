/* WPE E01-E08: distinct authored extensions, not original exam questions.
 * Core1A follows the existing WPE extension learning packs. The fresh
 * reconstruction is revealed only after a locally saved first attempt.
 * Browser storage is practice convenience, not secure assessment.
 */
(() => {
  "use strict";
  const lessons = {
    E01: {
      title:"Potential wells: possible versus reachable",
      question:"Can two low valleys be separated by a hill you cannot cross?",
      prereq:"A moving object's total energy E is potential U plus kinetic K. Because K = ½mv², K cannot be negative. At K = 0 it can momentarily turn.",
      core:"A place is energetically allowed when U(x) ≤ E. A journey is possible only if EVERY intermediate place along a continuous route is allowed.",
      guide:"A 2 kg bead slides on a smooth one-dimensional track with U(x) = (x − 2)² joules when x is in metres. Total energy is 4 J. The bowl has its lowest point at x = 2 m.",
      steps:[
        ["Read the potential map","At x = 0, 1, 2, 3, 4 m, the potential energies are 4, 1, 0, 1, 4 J. Draw a horizontal E = 4 J line."],
        ["Make a kinetic-energy budget","Subtract each U from 4 J: K = 0, 3, 4, 3, 0 J. Anything with U greater than 4 J would demand negative K and is forbidden."],
        ["Locate the turning positions","At x = 0 and 4 m, K = 0, so the bead may momentarily stop and reverse. The entire interval from 0 to 4 m is connected and accessible."],
        ["Locate the greatest speed","Smallest U means largest K. At x = 2 m, K = 4 J and v = √(2K/m) = √(8/2) = 2 m/s."],
        ["Change one condition","At E = 1 J, the line meets the bowl at x = 1 and 3 m, so the allowed interval becomes [1, 3] m. Moving the energy line changes what is possible."]
      ],
      contrast:"An isolated low destination is not automatically reachable: if a higher hill lies between it and the start, compare the entire route with E. The lowest point also need not be where the bead starts.",
      misconception:"K = 0 is allowed at a turning position; K less than 0 is not. Speed is fastest at LOWEST potential, not at the highest hill. Exactly at a stable minimum with E = Umin, the bead can remain at rest.",
      assumptions:"One-dimensional conservative motion, no friction, fixed total E, and a smooth track. At a barrier top where E exactly equals a local maximum, crossing requires special dynamical care. The fresh crossing check uses E greater than the barrier.",
      challenge:"A different 2 kg bead moves on a frictionless x-axis. Put q = x/(1 m), so q is dimensionless. Its potential energy is U(q) = (q² − 4)² J. It has E = 9 J, starts at x = +2 m moving LEFT, and can only travel along this axis. Can it get into the valley near −2 m? Find the allowed x intervals, the turning positions in its starting valley and its maximum possible speed.",
      fields:[
        {id:"cross",label:"Can it reach the valley near −2 m from +2 m?",type:"select",options:["Choose a prediction","Yes","No","Not sure"]},
        {id:"intervals",label:"Allowed x intervals (m)",type:"text",hint:"Write both intervals; you may use √ and brackets."},
        {id:"turns",label:"Turning positions of the starting (right) region",type:"text"},
        {id:"maxSpeed",label:"Largest speed possible on its journey (m/s)",type:"number"},
        {id:"reason",label:"Why is or isn't the whole journey possible?",type:"textarea"}
      ],
      hints:[
        "Use the budget K = E − U. What sign must K have at any physically visited position?",
        "Make a short U table at x = +2, +1, 0, −1, −2 m before solving a long inequality.",
        "Shade the x-axis wherever the budget is possible. Starting at +2 m, trace a continuous path without jumping over any untested location."
      ],
      worked:[
        ["Check positions","K ≥ 0 requires (q² − 4)² ≤ 9. Take the square-root inequality: −3 ≤ q² − 4 ≤ 3, hence 1 ≤ q² ≤ 7."],
        ["Separate intervals","The allowed x values are [−√7, −1] m and [1, √7] m. These are TWO disconnected regions."],
        ["Follow the actual start","At +2 m the bead occupies the right-hand region. Moving left, it turns at +1 m. The hill at 0 has U = 16 J, which exceeds its 9 J budget. The left valley is low but NOT reachable from that start."],
        ["Calculate maximum speed","At +2 m, U = 0, so its maximum accessible K = 9 J. For 2 kg, v = √(2 × 9/2) = 3 m/s. The right-hand turning points are +1 and +√7 m."]
      ],
      checks:["I tested E − U ≥ 0, including K = 0.","I separated the two allowed regions.","I traced the connected region containing the actual start.","I found fastest motion at the lowest accessible U."],
      diagnoses:["I checked only the far destination.","I forgot to inspect the hill between the valleys.","I treated K = 0 as forbidden.","I maximized speed at maximum U.","I need to revise my algebra or units.","My model worked; I want to explain it more clearly."],
      diagnosisTips:["Check ALL intermediate positions, not just the endpoint.","Mark the central potential and the energy line on one graph.","A turning position can have zero speed for an instant.","Subtract U from E before using ½mv².","Rewrite −3 ≤ q²−4 ≤ 3 and restore metres from q.","State a connected route explicitly even when the numbers agree."],
      boundary:"Raise total energy to 17 J, keeping the same potential and bead. Is crossing x = 0 now energetically possible? What is its speed at x = 0? Explain the changed condition.",
      boundaryCheck:"At x = 0, U = 16 J. With E = 17 J, K = 1 J and v = √(2 × 1/2) = 1 m/s. The barrier is below E, so crossing is energetically possible. E = 16 J exactly is a special separatrix, not a guaranteed ordinary crossing.",
      visual:"well"
    },
    E02: {
      title:"Instantaneous power: force along motion",
      question:"Why can a moving object have zero power at an instant?",
      prereq:"One watt is one joule per second. Work depends on the component of force along displacement; power describes the rate at this instant, not an entire future journey.",
      core:"Instantaneous power is force along the CURRENT velocity: P = Fx vx + Fy vy. A perpendicular force gives zero power even if it causes acceleration.",
      guide:"A 2 kg trolley moves RIGHT at 3 m/s. A student pulls RIGHT with 6 N while resistance acts LEFT with 2 N. The floor is level.",
      steps:[
        ["Draw direction arrows","Choose right as positive: v = +3 m/s, Fpull = +6 N, Fresist = −2 N. Gravity and the normal are vertical, perpendicular to horizontal motion."],
        ["Calculate each rate","Pull power = (+6)(+3) = +18 W. Resistance power = (−2)(+3) = −6 W. Gravity and the normal each contribute 0 W."],
        ["Combine contributions","Net power = +12 W. The kinetic energy is increasing at 12 J per second AT THIS INSTANT."],
        ["Do not invent a future average","As the trolley accelerates, v can change. Thus P = Fv can change even if the forces stay the same. Average power over a period is total work ÷ elapsed time."],
        ["Reverse velocity, not forces","If the trolley momentarily moves LEFT at 3 m/s under the same force arrows, net power is (6 − 2)(−3) = −12 W."]
      ],
      contrast:"A moving body does not always gain kinetic energy. Force and velocity can be opposite (negative power) or perpendicular (zero power). Force magnitude multiplied by speed only works when aligned.",
      misconception:"Do not confuse +12 W now with +12 J gained in every later second. Net power can be zero while net force and acceleration are nonzero.",
      assumptions:"For the guide, horizontal forces at an instant, level motion, no vertical velocity; same applied force arrows in the reversal comparison. Two-dimensional force components in the fresh problem are an ADVANCED bridge: multiply corresponding horizontal arrows and add the signed contributions—no calculus required.",
      challenge:"A robot moves on a flat floor with instantaneous velocity 3 m/s RIGHT and 4 m/s FORWARD. Its motor pushes 6 N RIGHT. Resistance pushes 2 N LEFT and 1 N BACKWARD. Vertical forces are perpendicular to motion. Find the instant motor, resistance and net powers; tell whether kinetic energy is rising or falling, and explain why multiplying full force magnitude by speed is wrong.",
      fields:[
        {id:"motor",label:"Motor instantaneous power (W)",type:"number"},
        {id:"resist",label:"Resistance instantaneous power (W)",type:"number"},
        {id:"net",label:"Net instantaneous power (W)",type:"number"},
        {id:"trend",label:"Kinetic energy is...",type:"select",options:["Choose","Increasing now","Decreasing now","Unchanging now","Not sure"]},
        {id:"reason",label:"Show signed right/forward contributions, not just the final number",type:"textarea"}
      ],
      hints:[
        "Draw separate rightward and forward velocity arrows. Which force arrows have components in each direction?",
        "Make a two-column table: multiply each force's RIGHT component by 3, and FORWARD component by 4.",
        "Keep signs on resistance terms. Add the two component products for each force before adding the motor and resistance."
      ],
      worked:[
        ["Motor","Motor force = (+6, 0) N; velocity = (+3, +4) m/s. Motor power = 6×3 + 0×4 = +18 W."],
        ["Resistance","Resistance = (−2, −1) N, so resistance power = −2×3 −1×4 = −10 W."],
        ["Net instantaneous result","Net force = (+4, −1) N. Pnet = 4×3 − 1×4 = +8 W; kinetic energy is currently increasing at 8 J/s."],
        ["Why magnitudes fail","Speed magnitude is 5 m/s and net force magnitude is √17 N. Their product is NOT 8 W, because the vectors are not parallel. Only the force component along velocity transfers kinetic energy at that instant."]
      ],
      checks:["I resolved force and velocity along the same axes.","I kept resistance terms negative.","I used Pnet as an instantaneous energy-change rate.","I distinguished component products from magnitude products."],
      diagnoses:["I ignored the backward resistance.","I multiplied magnitudes instead of matching components.","I gave resistance the wrong sign.","I claimed current power is future average power.","I need to check arithmetic.","I can explain perpendicular-force zero power better."],
      diagnosisTips:["The 4 m/s forward velocity multiplies the backward resistance.","Separate each axis before adding; vectors are not all parallel.","A force opposite to its velocity component does negative power.","An instantaneous rate need not remain constant over time.","Recheck 6×3 and (−2×3−1×4).","Perpendicular forces can bend a path without changing speed at that instant."],
      boundary:"At a later instant the robot moves 1 m/s RIGHT and 4 m/s FORWARD, under the SAME forces. Find net instantaneous power. Is the robot moving? Can acceleration still be nonzero?",
      boundaryCheck:"Pnet = 4×1 −1×4 = 0 W. Speed is √(1² + 4²) = √17 m/s, not zero. Net force (+4, −1) N is nonzero and perpendicular to velocity, so acceleration exists but kinetic energy is instantaneously unchanged.",
      visual:"power"
    },
    E03: {
      title:"Spring contact → projectile flight",
      question:"Exactly when do you stop using the spring model?",
      prereq:"A spring stores ½kx², because its force falls as it relaxes. A launched object has separate horizontal and vertical motion once contact ends.",
      core:"Divide the event into phases. During contact, stored spring energy pays for friction and launch kinetic energy. After contact ends, use gravity for vertical flight time and unchanged horizontal speed for range.",
      guide:"Model A: a 1 kg puck is NOT attached to an ideal spring (k = 100 N/m) compressed 0.20 m. The horizontal surface is smooth. Model B: a DIFFERENT ball leaves a platform 1.25 m high, horizontally at 3 m/s. Use g = 10 m/s².",
      steps:[
        ["Contact has a clear end","The free puck is pushed only until the spring reaches natural length. Initially stored energy = ½×100×(0.20)² = 2 J."],
        ["Convert before separating","In the frictionless guide, at natural length ½×1×v² = 2 J, so puck speed = 2 m/s. The spring cannot pull it once contact ends."],
        ["Start a separate projectile model","The second ball begins FLIGHT horizontally. Vertical initial velocity is 0; gravity makes it fall 1.25 = ½×10×t², giving t = 0.50 s."],
        ["Use horizontal motion for range","With no air drag, vx stays 3 m/s. Its horizontal range is 3×0.50 = 1.50 m. Falling faster vertically does not reduce its horizontal velocity."],
        ["Join only when a real launcher needs both","First compute a dart's speed at release using its contact ledger; then transfer that speed into the flight equations. Never carry the spring push into free flight."]
      ],
      contrast:"The spring's initial force kx is not constant throughout release: its work is the triangular area ½kx². Flight time comes from height, not from dividing height by g.",
      misconception:"Do not carry contact friction or spring force into the air. The projectile is free only once it has left all supports, with the specified horizontal launch position.",
      assumptions:"Ideal Hookean spring, the object is NOT attached, release occurs at natural length, and no losses except any explicitly stated contact friction. Launch horizontal; constant g; no air drag. In real apparatus the geometry may differ; the contact boundary must be specified.",
      challenge:"A 0.50 kg dart is pushed by a spring with k = 125 N/m compressed 0.20 m. The dart is not attached. While the spring expands those 0.20 m, constant opposing friction = 2.5 N. At natural length it leaves a 1.25 m-high platform HORIZONTALLY. Use g = 10 m/s²; no air drag or friction in flight. Find spring energy, contact friction work, launch speed, fall time and horizontal range.",
      fields:[
        {id:"energy",label:"Initially stored spring energy (J)",type:"number"},
        {id:"friction",label:"Work of contact friction (J; include sign)",type:"number"},
        {id:"speed",label:"Horizontal launch speed (m/s)",type:"number"},
        {id:"time",label:"Flight time (s)",type:"number"},
        {id:"range",label:"Horizontal landing distance (m)",type:"number"},
        {id:"reason",label:"Where is the phase boundary, and which forces disappear?",type:"textarea"}
      ],
      hints:[
        "Mark two columns: while TOUCHING the spring, and after the dart LEAVES the platform.",
        "Compute the energy budget at natural length. For friction, work = opposing force × contact distance, with the correct sign.",
        "From horizontal launch, start with vertical fall h = ½gt². Then use horizontal speed times that duration."
      ],
      worked:[
        ["Contact energy","Stored energy = ½×125×0.20² = 2.50 J. Friction does −2.5×0.20 = −0.50 J, leaving 2.00 J of kinetic energy."],
        ["Launch speed","½×0.50×v² = 2.00, so vx = √8 ≈ 2.828 m/s. The spring and rubbing contact both end at launch."],
        ["Fall time","In the air, vertical drop is 1.25 = ½×10×t², so t = 0.50 s. Initial vertical speed is zero."],
        ["Range and force change","Range = vx t ≈ 2.828×0.50 = 1.414 m. Only gravity acts (ignoring air resistance); neither spring force nor contact friction continues during flight."]
      ],
      checks:["I marked contact and flight as different phases.","I used ½kx², not the initial force over the whole stroke.","I subtracted friction only during contact.","I used vertical motion for time and horizontal motion for range."],
      diagnoses:["I treated spring force as constant.","I forgot contact friction or its sign.","I carried spring/friction into flight.","I used t = h/g.","I mixed horizontal and vertical components.","I want to improve my units or rounding."],
      diagnosisTips:["The Hookean force decreases to zero as the spring relaxes.","The energy lost is force × CONTACT distance, opposing motion.","Once the dart leaves the launcher, contact forces cease.","For a horizontal launch, start with h = ½gt².","Gravity changes vertical velocity, not horizontal velocity here.","Check joules, seconds, m/s and metres at each stage."],
      boundary:"Keep the same launcher and platform, but make friction during contact ZERO. Find the new launch speed and range. Does the fall time change?",
      boundaryCheck:"Without friction, kinetic energy at launch = 2.50 J. vx = √(2×2.50/0.50) = √10 ≈ 3.162 m/s. The fall time stays 0.50 s; range increases to ≈ 1.581 m.",
      visual:"spring"
    },
    E04: {
      title:"Dissipative bouncing: energy is not speed",
      question:"How do tiny repeated rebounds add to a finite distance?",
      prereq:"Ignoring air drag, gravitational energy mgh becomes kinetic energy on the fall. Kinetic energy is proportional to speed SQUARED, not speed.",
      core:"If a bounce retains fraction r of the kinetic energy, the next rebound height is r times the previous height, while rebound speed is √r times the incoming speed. Count UP and DOWN each time.",
      guide:"Drop a 1 kg ball from rest at 2 m, using g = 10 m/s². Each ideal floor impact loses 75% of the incoming kinetic energy, so the retained fraction r = 0.25. Ignore air resistance.",
      steps:[
        ["First drop","It falls 2 m once and reaches the floor with K = mgh = 1×10×2 = 20 J."],
        ["First rebound","It keeps 25% of 20 J = 5 J, enough to rise h1 = 5/(1×10) = 0.5 m."],
        ["Apply the same retention each time","Next rebound heights are 0.25×0.5 = 0.125 m and 0.25×0.125 = 0.03125 m. Do not apply the 75% LOSS as a height ratio."],
        ["Compare energy and speed","With 25% energy retention, speed immediately after impact is √0.25 = 0.5 times incoming speed, not 0.25 times."],
        ["Count both directions","Distance = first 2 m drop + 2(0.5 + 0.125 + …). Optional advanced geometric sum: D = 2 + 2×0.5/(1−0.25) = 10/3 m ≈ 3.333 m."]
      ],
      contrast:"Half of the speed does not mean half of the kinetic energy: it means one-quarter of the energy. Similarly, half-energy rebounds have speed ratio √0.5.",
      misconception:"Never count only the upward legs. Use the initial drop ONCE and each complete rebound twice. A real ball ultimately stops; the infinite sequence is an ideal mathematical model.",
      assumptions:"Vertical rebounds on a level floor, fixed kinetic-energy loss fraction at impact, no energy loss during flights, no sideways motion. Geometric infinite series is an ADVANCED extension; first three heights and paired up/down distances are the prerequisite bridge.",
      challenge:"Release a ball from 2 m. On its FIRST impact it retains 75% of its pre-impact kinetic energy. On every LATER impact it retains 50%. Find the first three rebound heights, ideal total vertical distance and ratio of rebound speed to incoming speed on the FIRST impact. Explain when the rule switches.",
      fields:[
        {id:"h1",label:"First rebound height (m)",type:"number"},
        {id:"h2",label:"Second rebound height (m)",type:"number"},
        {id:"h3",label:"Third rebound height (m)",type:"number"},
        {id:"distance",label:"Total ideal vertical travel (m)",type:"number"},
        {id:"speedRatio",label:"First post/pre impact speed magnitude ratio",type:"number"},
        {id:"reason",label:"Explain the two retention rules and both-direction distance count",type:"textarea"}
      ],
      hints:[
        "Write a row for every impact: which energy-retention fraction applies to THIS row?",
        "After a rebound, the ball rises to the height corresponding to its remaining energy. Check whether a SPEED ratio must involve a square root.",
        "The first 2 m drop happens only once; every rebound contributes an upward and a downward journey. What repeats after the first impact?"
      ],
      worked:[
        ["Switch rules carefully","At first impact r0 = 0.75, so h1 = 0.75×2 = 1.5 m. Later r = 0.50, so h2 = 0.75 m and h3 = 0.375 m."],
        ["Sum the repeated rises","After the first special bounce, heights halve: 1.5 + 0.75 + 0.375 + … = 1.5/(1−0.5) = 3 m (optional infinite-series maths)."],
        ["Include all travel","The initial fall is 2 m. Rebounds go UP and DOWN, so D = 2 + 2×3 = 8 m, in the ideal model."],
        ["Check rebound speed","The first retained energy fraction is 0.75; speed ratio is √0.75 = √3/2 ≈ 0.866. It is not 0.75."]
      ],
      checks:["I switched from first-impact to later-impact fraction.","I related height to energy, speed to √energy.","I included first drop and both legs of rebounds.","I recognized the infinite series as an ideal extension."],
      diagnoses:["I kept 75% for every bounce.","I treated energy fraction as speed fraction.","I missed the initial drop.","I counted only upward travel.","I used the wrong first term or ratio.","I need to explain the ideal-model limit."],
      diagnosisTips:["Label impact 1 separately and impacts 2,3,… as a repeating rule.","Use K = ½mv² to transform an energy ratio into a speed ratio.","The released ball travels from 2 m to floor before any rebound.","Each bounce rise is followed by a fall of the same height.","Begin the repeating height sequence with h1 and ratio 0.5.","The total is a mathematical limit, not a claim that real balls bounce forever."],
      boundary:"Change the model: EVERY impact now retains 75% energy, including the first. From the same 2 m height, what is ideal total vertical travel, and why is it larger?",
      boundaryCheck:"Rebound heights form 1.5, 1.125, … m with ratio 0.75. Their sum is 1.5/(1−0.75) = 6 m; ideal travel D = 2 + 2×6 = 14 m. More retained energy means taller subsequent rebounds.",
      visual:"bounce"
    },
    E05: {
      title:"Radial force: graph area versus circular orbit",
      question:"Why can an inward force give positive potential energy?",
      prereq:"For a 1D conservative force, its work along radial displacement is −ΔU. On a circle, velocity is tangent while inward force is perpendicular. A circle needs inward acceleration v²/r.",
      core:"Two DIFFERENT operations: radial force-magnitude graph AREA gives increase in U with outward radius; the force HEIGHT at an orbit radius gives mv²/r. Only then add K + U.",
      guide:"A 1 kg bead has a conservative central force of constant magnitude 3 N pointing INWARD at positive radius r. Choose U(0) = 0 by continuous limit. Consider a steady circular orbit of radius 2 m; ignore drag.",
      steps:[
        ["Label force sign and velocity","Take outward radius positive. The signed radial force is Fr = −3 N; velocity around the circle is tangential and perpendicular to it."],
        ["Imagine moving radially outward","Against inward force, U rises by +3 N × 2 m = +6 J. This is area under the POSITIVE inward-magnitude graph, not work done while circling."],
        ["Use force at the chosen radius","For circular motion at r = 2 m, inward force = mv²/r = 3 N. So v² = 3×2/1 = 6 and v ≈ 2.45 m/s."],
        ["Combine energy only after both models","K = ½×1×6 = 3 J. The total mechanical energy of this 2 m orbit is E = U + K = 6 + 3 = 9 J."],
        ["Check the circle itself","Because force is perpendicular to tangential velocity, it does zero work along the orbit. The 6 J is a radial-position comparison, not energy added every lap."]
      ],
      contrast:"If the graph's vertical axis shows signed Fr = −3 N, its radial area is negative WORK and ΔU is the opposite sign. If it shows positive inward magnitude f = 3 N, area is POSITIVE ΔU. Read the axis.",
      misconception:"Potential energy is not automatically negative because force points inward. Use graph AREA for potential CHANGE, but graph HEIGHT at the orbit radius for circular force. Never use mv/r.",
      assumptions:"Conservative radial force for r > 0, inward magnitude f(r) ≥ 0, U(0) as a continuous reference limit. The inward direction is undefined exactly at r = 0; circular orbits considered only at r > 0. Elementary graph area and v²/r replace calculus as an explicit ADVANCED bridge. Different radius circles have different total E and are separate states.",
      challenge:"A 2 kg spacecraft is in an ideal circular orbit at r = 3 m. The conservative INWARD FORCE MAGNITUDE is 4 N from r = 0 to 2 m, then grows linearly from 4 N at r = 2 m to 8 N at r = 4 m (thus 6 N at 3 m). With U(0) = 0, find U(3), speed, K and total E. Distinguish the two graph operations and explain why the force does no work along the orbit.",
      fields:[
        {id:"potential",label:"U(3 m), using both graph areas (J)",type:"number"},
        {id:"localForce",label:"Force magnitude at r = 3 m (N)",type:"number"},
        {id:"speed",label:"Circular orbital speed (m/s)",type:"number"},
        {id:"kinetic",label:"Circular kinetic energy (J)",type:"number"},
        {id:"total",label:"Total energy of this circular orbit (J)",type:"number"},
        {id:"reason",label:"Explain area versus force height, and the zero work around a circle",type:"textarea"}
      ],
      hints:[
        "On an inward FORCE MAGNITUDE versus radius graph, compare U between radii by counting the area underneath.",
        "Start at the U(0) reference. Split radial area into 0–2 m and 2–3 m; the second section slopes.",
        "For orbit speed, ignore earlier areas and read the FORCE at 3 m. Sketch perpendicular inward force and tangential velocity before using mv²/r."
      ],
      worked:[
        ["Build potential from radial areas","First rectangle: 4×2 = 8 J. Next trapezoid from 2 to 3 m: ½(4+6)×1 = 5 J. Thus U(3) = 8 + 5 = 13 J."],
        ["Read local force independently","At 3 m, inward f(3) = 6 N. The circle condition is mv²/r = 6, so 2v²/3 = 6 and v = 3 m/s."],
        ["Compute orbit energies","K = ½×2×3² = 9 J. Total energy E(3) = U(3) + K = 13 + 9 = 22 J."],
        ["Explain no circular work","While the craft circles at constant radius, its force is inward but velocity tangential. F · v = 0. The area was an imagined RADIAL comparison, not energy continuously produced during each orbit."]
      ],
      checks:["I used both radial graph areas with correct sign.","I used the local force, not area, in mv²/r.","I found speed, K and E of the given circle.","I kept radial comparison separate from travel around the circle."],
      diagnoses:["I counted only the last area section.","I treated force height as potential energy.","I used a rectangle instead of a trapezoid.","I gave U a negative sign automatically.","I used mv/r instead of mv²/r.","I confused radial work with circular work."],
      diagnosisTips:["Begin from the reference U(0), not merely the nearest graph corner.","Force is in newtons; potential energy is an area in newton-metres.","For a sloped straight line, use average endpoint height × width.","On a positive inward-magnitude graph, outward U increases.","Inward acceleration for circular motion is v²/r.","Compare radial positions for ΔU; while circling, force is perpendicular to motion."],
      boundary:"Consider a DIFFERENT steady circle at r = 4 m, with the same force law and mass. Compute U(4), speed, K and total E(4). Why is this not the same spacecraft moving freely from the 3 m circle without extra energy?",
      boundaryCheck:"U(4) = 4×2 + ½(4+8)×2 = 8 + 12 = 20 J. Local force 8 N gives 2v²/4 = 8, so v = 4 m/s. K = ½×2×16 = 16 J and E(4) = 36 J. These are distinct circular-orbit states; the conservative force alone cannot change E from 22 to 36 J.",
      visual:"radial"
    },
    E06: {
      "title": "Ground push power versus net acceleration",
      "question": "Why isn't the power supplied by an upward push the same as net acceleration power?",
      "prereq": "A vertical force does positive work when it points with displacement; gravity does negative work during upward motion. Instantaneous power is F·v for the force of interest.",
      "core": "During ground contact, applied force pays for BOTH kinetic-energy gain and gravitational height. After separation, only gravity acts. The maximum applied power occurs at the maximum speed during the constant-force push.",
      "guide": "A 2 kg upward-launch toy starts at rest and is pushed 1.0 m upward by a constant 30 N force while its weight is 20 N. Take g=10 m/s²; after leaving the launcher it rises under gravity alone.",
      "steps": [
        [
          "Draw contact force arrows",
          "The constant applied force is +30 N; weight is −20 N. Net acceleration force is +10 N, not the full applied force."
        ],
        [
          "Write the contact work ledger",
          "Applied work +30 J, gravity work −20 J, net +10 J = change in kinetic energy from rest."
        ],
        [
          "Find speed and flight height",
          "½(2)v²=10 J, so v=√10≈3.162 m/s. After separation the further rise is v²/(2g)=0.50 m."
        ],
        [
          "Distinguish two instantaneous powers",
          "Applied push power at separation is 30√10≈94.87 W, while net force×v=10√10≈31.62 W describes dK/dt. The difference is gravitational energy gain rate."
        ],
        [
          "Explain the switch at take-off",
          "The launcher stops acting in free flight. Do not assign applied push work to the later 0.50 m rise."
        ]
      ],
      "contrast": "Multiplying NET force by speed answers kinetic-energy rate, not the full external applied mechanical power. The ground-contact displacement is different from the subsequent free-flight height.",
      "misconception": "Do not treat a coaching-labelled 'muscle power' as the net force power without specifying which force supplies the work. The original exam source/key is unresolved.",
      "assumptions": "Starts from rest; constant upward applied force during contact; no drag or other losses; launcher stops acting at separation; power means mechanical power of the applied upward force, not metabolic power.",
      "challenge": "A different 4 kg toy starts from rest. A CONSTANT upward force pushes it for 0.50 m before it separates. It then rises ANOTHER 0.80 m in free flight. Take g=10 m/s². Find its take-off speed, kinetic gain, gravity work during contact, applied push force, and the MAXIMUM instantaneous mechanical power of that applied force during contact.",
      "fields": [
        {
          "id": "takeoffSpeed",
          "label": "Take-off speed (m/s)",
          "type": "number"
        },
        {
          "id": "contactGain",
          "label": "Kinetic-energy gain during push (J)",
          "type": "number"
        },
        {
          "id": "contactGravity",
          "label": "Gravity's work during push (J)",
          "type": "number"
        },
        {
          "id": "appliedForce",
          "label": "Upward applied contact force (N)",
          "type": "number"
        },
        {
          "id": "netForce",
          "label": "Net accelerating force during contact (N)",
          "type": "number"
        },
        {
          "id": "appliedPower",
          "label": "MAXIMUM applied mechanical power (W)",
          "type": "number"
        },
        {
          "id": "model",
          "label": "Which force must be multiplied by speed for supplied push power?",
          "type": "select",
          "options": [
            "Choose a model",
            "Applied upward contact force",
            "Net accelerating force only",
            "Weight only",
            "Not sure yet"
          ]
        },
        {
          "id": "reason",
          "label": "Explain the TWO phases and why applied and net power differ",
          "type": "textarea"
        }
      ],
      "hints": [
        "Use the flight rise AFTER take-off to find speed at the contact boundary, not the push displacement.",
        "During contact, the applied push pays for kinetic gain AND gravity's negative work. Keep the contact and free-flight distances separate.",
        "The power question asks for the rate of work done by the applied upward force, not solely net acceleration; speed is highest at take-off."
      ],
      "worked": [
        [
          "Free flight determines take-off speed",
          "Extra rise 0.80 m requires v²=2gh=16 m²/s², hence v=4 m/s at separation."
        ],
        [
          "Contact energy includes rising against gravity",
          "K increases by ½(4)(4²)=32 J. Weight does −(4)(10)(0.50)=−20 J during contact, so applied work must supply 32+20=52 J."
        ],
        [
          "Find applied rather than only net force",
          "F_applied=52/0.50=104 N. Weight is 40 N down, so F_net=104−40=64 N."
        ],
        [
          "Compute power for the CORRECT force",
          "Maximum applied power at take-off is F_applied v=104×4=416 W. F_net v=64×4=256 W is the kinetic-energy rate, not total mechanical power of the push."
        ],
        [
          "Check contact and free-flight phases",
          "52 J applied energy during contact becomes 32 J kinetic plus 20 J gravitational potential. After separation, the toy rises under gravity alone."
        ]
      ],
      "checks": [
        "I used the extra 0.80 m flight height to infer take-off speed 4 m/s.",
        "I included the 20 J gravitational energy rise during the 0.50 m ground push.",
        "I calculated applied F=104 N separately from net F=64 N.",
        "I found applied push power 416 W rather than net kinetic-energy rate 256 W."
      ],
      "diagnoses": [
        "I used the 0.80 m free-flight height as contact distance.",
        "I forgot the gravitational work while the toy was still being pushed.",
        "I treated net F×v as the power delivered by the applied force.",
        "I continued the applied push into free flight.",
        "The phase model was correct but I want to check arithmetic.",
        "I'm still unsure which force provides the energy."
      ],
      "diagnosisTips": [
        "Mark the contact boundary at 0.50 m and the separate later rise of 0.80 m.",
        "Gravity acts throughout both phases, including during the push; add contact mgs to the kinetic gain.",
        "Net F explains dK/dt; applied F explains work rate delivered by the contact push.",
        "Only gravity acts during flight; no extra contact work is supplied after separation.",
        "Recheck work units (N·m=J), power units (N·m/s=W) and the energy balance.",
        "Start with two labelled boxes, CONTACT and FLIGHT, and one force arrow for each agent."
      ],
      "boundary": "The same 4 kg toy still starts from rest and is pushed upward for 0.50 m, but its later FREE flight rise is only 0.45 m. Find new take-off speed, contact applied force and maximum applied mechanical power; distinguish net power.",
      "boundaryCheck": "Later rise 0.45 m implies v²=9 and take-off v=3 m/s. Contact kinetic gain is 18 J; contact gravity rise needs 20 J. Applied work=38 J, applied force=76 N, MAXIMUM applied power=76×3=228 W. Net force=(76−40)=36 N and its kinetic-energy rate at take-off is 108 W. The 0.45 m is not the push distance.",
      "visual": "push"
    },
    E07: {
      "title": "Two incline journeys, two friction losses",
      "question": "Why does a block lose energy to friction on BOTH the ascent and the descent?",
      "prereq": "Friction always opposes current sliding. Gravity is conservative, so its work cancels when a block returns to exactly its original height.",
      "core": "Use one stopping distance in two different along-slope models: gravity and friction both oppose uphill motion, but friction opposes downhill return while gravity assists it.",
      "guide": "A 1 kg block starts uphill at 4 m/s. Gravity's component along the slope is 6 N downhill; kinetic friction magnitude is 2 N against its movement on either leg. It stops, then slides back.",
      "steps": [
        [
          "Uphill retarding work",
          "Both gravity and friction point downhill, so resistance is 6+2=8 N; initial K=½×1×4²=8 J."
        ],
        [
          "Find the uphill stopping distance",
          "The uphill distance is 8 J ÷ 8 N = 1 m. Both forces remove kinetic energy over this segment."
        ],
        [
          "Change the sign of friction on descent",
          "When sliding DOWN the plane, gravity's 6 N points with motion, while friction's 2 N points UP. Net downhill force is 6−2=4 N."
        ],
        [
          "Compute return speed",
          "The 4 N downhill net force acts over the same 1 m, so K_return=4 J and return speed=√8≈2.828 m/s."
        ],
        [
          "Check the entire round trip",
          "Gravity gives −6 J uphill and +6 J downhill (zero total); friction removes 2 J on each 1 m leg, a 4 J total loss equal to K_initial−K_return."
        ]
      ],
      "contrast": "Friction's DIRECTION changes when motion reverses, but frictional work is negative on both legs. Do not subtract the uphill gravitational potential energy a second time after returning to the same height.",
      "misconception": "A quick one-leg energy calculation ignores the second friction loss. A speed ratio must be SQUARED when using kinetic energy or distance ratios.",
      "assumptions": "Straight incline, constant kinetic friction, constant gravity component and normal force, both legs have the same distance, no air resistance; returning motion needs gravity downhill component greater than friction.",
      "challenge": "A new block is launched uphill on a rough incline of 45°. Its kinetic friction coefficient μ is constant. After stopping it returns to its original launch position at speed (2/3) of the initial speed v₀. Assume it DOES slide back and sin45°=cos45°. Determine μ from two properly signed motion phases and explain why mass and v₀ cancel.",
      "fields": [
        {
          "id": "frictionUp",
          "label": "On ascent, friction points...",
          "type": "select",
          "options": [
            "Choose",
            "Down the slope",
            "Up the slope",
            "Sideways",
            "Not sure"
          ]
        },
        {
          "id": "frictionDown",
          "label": "On descent, friction points...",
          "type": "select",
          "options": [
            "Choose",
            "Down the slope",
            "Up the slope",
            "Sideways",
            "Not sure"
          ]
        },
        {
          "id": "upFactor",
          "label": "Uphill retarding factor in units of g·sin45°",
          "type": "text",
          "hint": "Use μ and sin45°=cos45°."
        },
        {
          "id": "downFactor",
          "label": "Downhill accelerating factor in units of g·sin45°",
          "type": "text"
        },
        {
          "id": "returnRatioSquared",
          "label": "(v_return / v₀)²",
          "type": "number"
        },
        {
          "id": "mu",
          "label": "Coefficient of kinetic friction μ",
          "type": "number",
          "hint": "Give an exact fraction in your explanation; decimal is fine here."
        },
        {
          "id": "reason",
          "label": "Explain why friction costs energy on both legs and use the SAME distance",
          "type": "textarea"
        }
      ],
      "hints": [
        "Draw a separate friction arrow for UP and DOWN travel, both opposite the motion.",
        "Write the uphill stopping distance as v₀²/[2g(sin45°+μcos45°)]. The SAME distance is used on descent.",
        "Relate the RETURN SPEED SQUARED to the ratio of downhill and uphill acceleration. With 45°, sine and cosine are equal."
      ],
      "worked": [
        [
          "Two phase-specific along-slope force models",
          "On ascent, stopping acceleration magnitude is g(sin45°+μcos45°); on descent, forward acceleration is g(sin45°−μcos45°). Gravity direction stays downhill; friction reverses."
        ],
        [
          "Use one shared stopping distance",
          "d=v₀²/[2g(sinθ+μcosθ)] and v_return²=2gd(sinθ−μcosθ). Thus r²=(sinθ−μcosθ)/(sinθ+μcosθ)."
        ],
        [
          "Cancel the equal sine and cosine",
          "At 45°, r²=(1−μ)/(1+μ). The observed r=2/3 gives r²=4/9."
        ],
        [
          "Solve and check physical bound",
          "4(1+μ)=9(1−μ), giving 13μ=5 and μ=5/13≈0.384615. It is nonnegative and less than tan45°=1, so the block slides back."
        ],
        [
          "Reconcile energy losses",
          "The block returns to the same height, so gravity work over the full path is zero. Friction removes energy during ascent and descent and makes return speed smaller than v₀."
        ]
      ],
      "checks": [
        "I gave friction opposite movement separately on the uphill and downhill legs.",
        "I used the SAME stopping distance with two differently signed accelerations.",
        "I squared the 2/3 speed ratio to get 4/9, then solved μ=5/13.",
        "I checked the resulting μ is positive and low enough for descent to occur."
      ],
      "diagnoses": [
        "I drew friction down the ramp on both legs.",
        "I forgot to square the speed ratio.",
        "I used a different stopping distance for descent.",
        "I treated gravity as losing net energy on a completed round trip.",
        "My arrows were correct; I need to check the algebra.",
        "I'm not sure why two phases share the same distance."
      ],
      "diagnosisTips": [
        "Friction always points opposite the current motion, so its direction must flip.",
        "Energy is proportional to speed squared; square 2/3 before calculating μ.",
        "The block stops at the same point and returns to the same base, so each leg spans the same d.",
        "Gravity loses and regains equal potential energy on this closed vertical route; friction dissipates energy twice.",
        "Simplify (4/9)(1+μ)=1−μ without changing the original force signs.",
        "Draw a start, turning point and return arrow, then write which forces oppose each direction."
      ],
      "boundary": "On the SAME 45° incline, a new trial returns to its starting position at speed (3/4)v₀. What μ is implied, and why is it less than in the original trial?",
      "boundaryCheck": "For the 45° incline, r²=(1−μ)/(1+μ). With r=3/4, r²=9/16, so 9(1+μ)=16(1−μ). Thus 25μ=7 and μ=7/25=0.28, smaller than 5/13. Less friction means less round-trip energy loss. Gravity still cancels over the full return.",
      "visual": "incline"
    },
    E08: {
      "title": "New spring-force equilibrium, new turning point",
      "question": "Where does the spring stop after the external force suddenly changes?",
      "prereq": "Hooke's law says the spring force is −kx when positive x is rightward from natural length. Constant applied forces can do work during motion.",
      "core": "After a force switch, use ONLY the new constant force in effective potential U_eff=½kx²−F_new x. A released-from-rest oscillator has turning points symmetric about the NEW equilibrium x_eq=F_new/k.",
      "guide": "A horizontal ideal spring has k=100 N/m. Its block rests at x=+0.10 m held by +10 N. At time zero the applied force is suddenly changed to constant +20 N; it starts moving from rest, with no friction.",
      "steps": [
        [
          "Choose x axis and identify both applied forces",
          "x=0 means natural length, positive RIGHT; the initial spring force at x=+0.10 m is −10 N and old applied force +10 N balances it."
        ],
        [
          "Find the new equilibrium, not the old one",
          "After switching to +20 N, the equilibrium becomes x_eq=+20/100=+0.20 m."
        ],
        [
          "Build post-switch effective potential",
          "U_eff=½(100)x²−20x=50x²−20x J, with x in metres. The −20x term represents work of the constant new force."
        ],
        [
          "Conserve post-switch effective energy",
          "At starting rest x_i=0.10 m, E_post=U_eff(0.10)=0.5−2=−1.5 J. This is allowed: an additive energy reference can be negative."
        ],
        [
          "Find and check the far turning point",
          "The quadratic potential is symmetric about 0.20 m; the other turning point is x=2(0.20)−0.10=+0.30 m, with U_eff(0.30)=4.5−6=−1.5 J."
        ]
      ],
      "contrast": "The new effective potential (including the constant applied force) governs later motion. Spring elastic energy by itself is not conserved because the new force keeps doing work.",
      "misconception": "A turning point is a position of zero instantaneous speed, NOT automatically equilibrium. New equilibrium is x_eq=F_new/k; it is generally not x=0 or the original held position.",
      "assumptions": "Ideal Hookean spring with an attached block, frictionless horizontal axis, constant post-switch force, ideal instantaneous force jump at fixed position with zero initial speed; conserve only after switch.",
      "challenge": "A different spring with k=50 N/m holds its block at rest compressed at x_i=−0.20 m under an old force −10 N. At time zero the applied force is replaced suddenly by constant +15 N and it is released from rest. Use x positive RIGHT from natural length. Find new equilibrium, initial post-switch effective energy, far positive turning point and an energy check.",
      "fields": [
        {
          "id": "initialX",
          "label": "Initial signed spring position (m)",
          "type": "number"
        },
        {
          "id": "newEquilibrium",
          "label": "New equilibrium position (m)",
          "type": "number"
        },
        {
          "id": "initialEnergy",
          "label": "Effective energy at initial rest position (J)",
          "type": "number"
        },
        {
          "id": "turning",
          "label": "Other far positive turning position (m)",
          "type": "number"
        },
        {
          "id": "turningEnergy",
          "label": "Effective potential at far turning point (J)",
          "type": "number"
        },
        {
          "id": "model",
          "label": "Which energy is conserved after the force switch?",
          "type": "select",
          "options": [
            "Choose a model",
            "Spring elastic energy only",
            "K + spring energy − F_new·x",
            "K + spring energy − F_old·x",
            "Not sure yet"
          ]
        },
        {
          "id": "reason",
          "label": "Explain why the new equilibrium sets the turning-point symmetry",
          "type": "textarea"
        }
      ],
      "hints": [
        "Initial compression is NEGATIVE x. Put the old equilibrium and new applied force on one signed axis.",
        "Once switched to constant +15 N, use x_eq=F_new/k; do not keep the old applied force in the motion equation.",
        "For post-switch turning points K=0 and U_eff is equal. Complete the square or use symmetry about the NEW equilibrium."
      ],
      "worked": [
        [
          "Check initial holding state",
          "At x_i=−0.20 m with k=50 N/m, spring force is −kx_i=+10 N, balanced by the old external −10 N. At the moment of switching the block is at rest."
        ],
        [
          "Change to the NEW equilibrium",
          "New applied force is +15 N. Therefore kx_eq=+15 and x_eq=+0.30 m."
        ],
        [
          "Calculate post-switch effective energy",
          "U_eff=½(50)x²−15x J. At x_i=−0.20 m: U_eff=1+3=4 J; initial K=0."
        ],
        [
          "Use symmetry or solve the turning-point quadratic",
          "The other turning point is x_other=2x_eq−x_i=0.60−(−0.20)=+0.80 m. Substitution gives U_eff(0.80)=16−12=4 J, matching the starting value."
        ],
        [
          "Explain why the spring-only model fails",
          "The new external constant force moves the block and does work. Only K+½kx²−15x is conserved after the switch; spring energy alone changes."
        ]
      ],
      "checks": [
        "I identified the initial compressed position x_i=−0.20 m and the old holding force correctly.",
        "I used the NEW +15 N force to calculate equilibrium x_eq=+0.30 m.",
        "I conserved post-switch K+U_eff and found the far turning point x=+0.80 m.",
        "I checked equal effective energies 4 J at both turning points and explained why spring energy alone is insufficient."
      ],
      "diagnoses": [
        "I treated the compressed starting position as +0.20 m.",
        "I conserved spring energy alone and ignored the new force's work.",
        "I kept the old applied holding force in the new effective potential.",
        "I reflected about natural length x=0 instead of new equilibrium.",
        "My effective potential was right but I made an arithmetic error.",
        "I'm not sure how changing the force moves equilibrium."
      ],
      "diagnosisTips": [
        "With x positive rightward, compression to the left is negative; the spring force has the opposite sign.",
        "The new constant force supplies work; include −F_new x in the potential energy.",
        "Only the force actually applied after t=0 belongs in the post-switch effective potential.",
        "Turn points of a quadratic with constant forcing are symmetric about F_new/k, not natural length.",
        "Recompute U_eff at both turning positions and compare the same energy value.",
        "Start with two snapshots: old held equilibrium and new switched force, then redraw the axis."
      ],
      "boundary": "Keep k=50 N/m and initial rest position x_i=−0.20 m, but change the switched constant force to +5 N. Find the NEW equilibrium and the OTHER turning point; verify effective potential at both.",
      "boundaryCheck": "With +5 N after switch, new equilibrium is x_eq=5/50=+0.10 m and the far turning point is x=2(0.10)−(−0.20)=+0.40 m. Initial effective energy is ½(50)(0.20²)−5(−0.20)=1+1=2 J. At x=+0.40 m, U_eff=½(50)(0.40²)−5(0.40)=4−2=2 J. The new force changes the equilibrium and turning point; old holding force does not enter post-switch energy.",
      "visual": "spring-switch"
    }
  };
  const allIds = Object.keys(lessons);
  const stageNames = ["Predict","Attempt","Reconstruct","Diagnose","Repair","Boundary test"];
  const storagePrefix = "g9:wpe:extensions:v1:";
  const ns = "http://www.w3.org/2000/svg";
  const $ = (selector,scope=document) => scope.querySelector(selector);
  const node = (tag,cls,text) => {
    const element = document.createElement(tag);
    if(cls)element.className=cls;
    if(text!==undefined)element.textContent=text;
    return element;
  };
  const add = (parent,tag,cls,text) => {const e=node(tag,cls,text);parent.append(e);return e;};
  const svgNode = (parent,tag,attrs,text) => {
    const e=document.createElementNS(ns,tag);
    for(const [k,v] of Object.entries(attrs||{}))e.setAttribute(k,String(v));
    if(text!==undefined)e.textContent=text;
    parent.append(e);return e;
  };
  const key=id=>storagePrefix+id;
  const blank=id=>({schema:1,id,stage:0,prediction:"",predictionDraft:"",attemptDraft:{},first:null,hintsUsed:0,checks:[],diagnosis:null,repair:"",boundary:null});
  const states={};
  const persist=id=>{try{localStorage.setItem(key(id),JSON.stringify(states[id]));return true}catch(e){$("#save-notice").hidden=false;return false;}};
  for(const id of allIds){
    let s;
    try{s=JSON.parse(localStorage.getItem(key(id))||"null")}catch(_){}
    states[id]=(s && s.schema===1 && s.id===id && Number.isInteger(s.stage) && s.stage>=0 && s.stage<=5 && (s.stage<2 || (s.first && typeof s.first.reason==="string"))) ? s : blank(id);
  }
  let active="E01";
  let sourceLink=null;
  function button(parent,action,label,secondary=false){
    const e=add(parent,"button",secondary?"secondary":"primary",label);e.type="button";e.dataset.action=action;return e;
  }
  function list(parent,tag,items){
    const root=add(parent,tag);
    for(const item of items)add(root,"li",null,item);
    return root;
  }
  function paragraph(parent,text,cls){return add(parent,"p",cls||null,text);}
  function inputFor(parent,id,field,value){
    const wrap=add(parent,"div","field");
    const label=add(wrap,"label",null,field.label);
    const full=id+"-"+field.id;
    label.htmlFor=full;
    let e;
    if(field.type==="textarea"){e=add(wrap,"textarea");e.rows=4;}
    else if(field.type==="select"){
      e=add(wrap,"select");
      for(const choice of field.options){const opt=add(e,"option",null,choice);opt.value=choice;}
    }else{e=add(wrap,"input");e.type=field.type;e.inputMode=field.type==="number"?"decimal":"text";}
    e.id=full;e.dataset.field=field.id;e.value=value==null?"":value;
    if(field.hint)paragraph(wrap,field.hint,"field-tip");
    return e;
  }
  function stageSteps(host,state){
    const ol=add(host,"ol","step-list");
    stageNames.forEach((s,i)=>{
      const li=add(ol,"li",i===state.stage?"current":i<state.stage?"done":"pending",(i+1)+". "+s);
      if(i===state.stage)li.setAttribute("aria-current","step");
    });
  }
  function snapshot(host,s){
    const section=add(host,"section","snapshot");
    add(section,"h4",null,"Your first attempt (never overwritten by repair)");
    if(!s.first){paragraph(section,"No first attempt has been saved yet.");return}
    const dl=add(section,"dl");
    for(const [key,value] of Object.entries(s.first)){add(dl,"dt",null,key==="reason"?"Your explanation":key);add(dl,"dd",null,String(value));}
    paragraph(section,"Prediction: "+s.prediction);
  }
  function buildGuide(host,id,config){
    const guide=add(host,"section","guide");
    add(guide,"p","mini","CORE1A · Learn first");
    add(guide,"h2",null,"Build the physics idea");
    paragraph(guide,config.prereq,"prereq");
    paragraph(guide,config.core,"big-idea");
    paragraph(guide,config.guide);
    const chart=add(guide,"figure","visual");
    const svg=svgNode(chart,"svg",{viewBox:"0 0 640 290",role:"img","aria-label":id+" interactive physical model"});
    svg.id="guide-plot";
    add(chart,"figcaption",null,"Change the control. Watch what the model predicts, not just the numbers.");
    const controls=add(guide,"div","visual-controls");
    add(controls,"label",null,id==="E01"?"Total energy in the bowl (J)":id==="E02"?"Trolley velocity (m/s)":id==="E03"?"Contact friction (N)":id==="E04"?"Energy fraction retained":id==="E05"?"Circular orbit radius (m)":id==="E06"?"Applied contact force (N)":id==="E07"?"Friction on each incline leg (N)":"New switched applied force (N)").htmlFor="guide-slider";
    const slider=add(controls,"input");slider.id="guide-slider";slider.type="range";
    const settings={E01:[0,6,1,4],E02:[-3,3,1,3],E03:[0,5,0.5,0],E04:[0.1,0.75,0.05,0.25],E05:[1,4,0.5,2],E06:[22,40,2,30],E07:[0,4,0.5,2],E08:[10,25,5,20]}[id];
    [slider.min,slider.max,slider.step,slider.value]=settings.map(String);
    const readout=add(controls,"output","model-readout");readout.htmlFor="guide-slider";
    slider.addEventListener("input",()=>drawVisual(id,Number(slider.value),svg,readout));
    drawVisual(id,Number(slider.value),svg,readout);
    const ol=add(guide,"ol","guide-steps");
    for(const [title,desc] of config.steps){
      const li=add(ol,"li");
      add(li,"strong",null,title+". ");
      li.append(document.createTextNode(desc));
    }
    const more=add(guide,"details","bridge");
    add(more,"summary",null,"Compare the common wrong model");
    paragraph(more,config.contrast);
    paragraph(more,config.misconception);
    const conditions=add(guide,"details","bridge");
    add(conditions,"summary",null,"Assumptions and advanced-maths bridge");
    paragraph(conditions,config.assumptions);
  }
  const nice=n=>Number(n.toFixed(3)).toString();
  function drawVisual(id,value,svg,out){
    svg.replaceChildren();
    const path=(d,color,width=3,dash)=>svgNode(svg,"path",{d,fill:"none",stroke:color,"stroke-width":width,...(dash?{"stroke-dasharray":dash}:{})});
    const textAt=(x,y,t,fill="#183e50",size=15)=>svgNode(svg,"text",{x,y,fill,"font-size":size,"font-weight":"600"},t);
    const line=(x1,y1,x2,y2,c="#7595a5",w=2)=>svgNode(svg,"line",{x1,y1,x2,y2,stroke:c,"stroke-width":w});
    svgNode(svg,"rect",{x:0,y:0,width:640,height:290,fill:"#f5fafc",rx:12});
    if(id==="E01"){
      const X=x=>55+x*132, Y=u=>240-u*28;
      line(55,240,595,240);line(55,240,55,30);
      for(let x=0;x<=4;x++)textAt(X(x)-5,264,x+"",null,13);
      for(let u=0;u<=6;u+=2)textAt(14,Y(u)+5,u+" J",null,12);
      let curve="";for(let i=0;i<=100;i++){const x=4*i/100;curve+=(i?" L":"M")+X(x).toFixed(1)+" "+Y((x-2)**2).toFixed(1);}
      path(curve,"#156c7d",4);
      line(55,Y(value),595,Y(value),"#ca7134",3);
      textAt(390,Math.max(27,Y(value)-12),"E = "+nice(value)+" J","#a95521");
      const r=Math.sqrt(value),a=Math.max(0,2-r),b=Math.min(4,2+r);
      svgNode(svg,"rect",{x:X(a),y:244,width:Math.max(0,X(b)-X(a)),height:8,fill:"#138578"});
      textAt(165,25,"U(x) = (x − 2)² J");
      out.textContent="Allowed positions on this 0–4 m view: "+nice(a)+" to "+nice(b)+" m. Turning points touch U = E; where U > E, K would be negative.";
    }else if(id==="E02"){
      line(70,195,560,195,"#8ba7af",4);
      svgNode(svg,"rect",{x:265,y:147,width:120,height:48,rx:8,fill:"#bde1e9",stroke:"#347a90"});
      textAt(285,177,"TROLLEY");
      line(330,138,470,138,"#158977",5);textAt(391,123,"pull +6 N","#147b70");
      line(320,213,205,213,"#ba683a",5);textAt(120,236,"resistance −2 N","#995c36");
      if(value!==0){const end=325+value*45;line(325,74,end,74,"#414d99",5);textAt(244,55,"v = "+value+" m/s","#414d99");}
      else textAt(195,72,"momentarily v = 0","#414d99");
      out.textContent="Power now: pull "+nice(6*value)+" W; resistance "+nice(-2*value)+" W; NET "+nice(4*value)+" W. Instantaneous—not an average.";
    }else if(id==="E03"){
      line(55,180,590,180,"#7b9ba9",3);
      const pts=[[72,140],[88,120],[104,160],[120,120],[136,160],[152,140]];
      svgNode(svg,"polyline",{points:pts.map(p=>p.join(",")).join(" "),fill:"none",stroke:"#bf8052","stroke-width":5});
      svgNode(svg,"rect",{x:185,y:132,width:46,height:46,rx:5,fill:"#8ed0d2",stroke:"#367783"});
      line(238,110,295,110,"#18897d",4);
      line(308,95,308,190,"#b56d4d",2);
      textAt(75,45,"SPRING CONTACT");textAt(375,45,"NO SPRING FORCE");
      textAt(235,218,"Natural length / separation boundary",null,14);
      const k=2-0.2*value,v=Math.sqrt(2*k);
      out.textContent="Guide puck: spring 2.00 J; friction work −"+nice(0.2*value)+" J; launch K "+nice(k)+" J; speed "+nice(v)+" m/s. Flight model B uses a different ball.";
    }else if(id==="E04"){
      line(32,252,612,252,"#688d9c",4);
      const peaks=[2,2*value,2*value**2,2*value**3];
      const heights=peaks.map(h=>h*88);
      for(let i=0;i<4;i++){
        const x=52+i*145;
        line(x,252,x,252-heights[i],"#a3c9cb",2);
        svgNode(svg,"circle",{cx:x,cy:252-heights[i],r:8,fill:i?"#278b7e":"#b8773f"});
        textAt(Math.max(2,x-24),Math.max(20,241-heights[i]),nice(peaks[i])+" m",null,12);
      }
      textAt(60,24,"Initial drop → rebound 1 → 2 → 3");
      out.textContent="r="+nice(value)+"; heights "+peaks.slice(1).map(nice).join(", ")+" m. Speed fraction √r="+nice(Math.sqrt(value))+". Ideal full travel "+nice(2+4*value/(1-value))+" m (advanced sum).";
    }else if(id==="E05"){
      // Left: force-magnitude area; right: orbit with radial/tangential arrows.
      line(48,224,310,224);line(48,224,48,45);
      svgNode(svg,"rect",{x:49,y:120,width:55*value,height:103,fill:"#b9e8d7",stroke:"#238e75","stroke-width":2});
      line(48,120,295,120,"#157c81",4);
      textAt(56,42,"Inward magnitude f = 3 N",null,14);
      textAt(58,255,"r outward → (m)",null,13);
      textAt(53,110,"3 N",null,12);
      const cx=465,cy=160,rad=44+value*14;
      svgNode(svg,"circle",{cx,cy,r:rad,fill:"none",stroke:"#92b4bf","stroke-width":2});
      svgNode(svg,"circle",{cx,cy,r:8,fill:"#536e7c"});
      svgNode(svg,"circle",{cx:cx+rad,cy,r:9,fill:"#1d8c80"});
      line(cx+rad-7,cy,cx+rad-45,cy,"#bc6d35",4);
      line(cx+rad,cy,cx+rad,cy-64,"#495fc0",4);
      textAt(365,25,"Orbit at r = "+nice(value)+" m",null,14);
      textAt(480,105,"v tangent", "#465cb1",12);
      textAt(392,194,"F inward","#a85d2c",12);
      out.textContent="Area gives U("+nice(value)+") = "+nice(3*value)+" J. Local force 3 N sets v = "+nice(Math.sqrt(3*value))+" m/s for 1 kg. Circular K = "+nice(1.5*value)+" J; force does zero work around the circle.";
    }else if(id==="E06"){
      // Guided constant contact push; use applied force for supplied mechanical power.
      const weight=20,net=value-weight,v=Math.sqrt(Math.max(0,net));
      svgNode(svg,"rect",{x:235,y:138,width:170,height:91,rx:12,fill:"#cde8f3",stroke:"#37748d","stroke-width":3});
      line(320,135,320,34,"#138d7d",5);line(312,47,320,31,"#138d7d",5);line(328,47,320,31,"#138d7d",5);
      line(320,230,320,270,"#b16c46",5);
      textAt(332,37,"F applied = "+nice(value)+" N","#167970",16);
      textAt(341,263,"Weight = 20 N","#9a613a",13);
      textAt(238,183,"Toy mass 2 kg",null,16);
      out.textContent="Contact phase: net force "+nice(net)+" N; K at 1 m="+nice(net)+" J; take-off speed "+nice(v)+" m/s. Applied power at take-off "+nice(value*v)+" W, but net kinetic-energy rate only "+nice(net*v)+" W.";
    }else if(id==="E07"){
      const up=6+value,down=6-value,d=8/up,returnK=down*d;
      svgNode(svg,"path",{d:"M48 230L505 55",fill:"none",stroke:"#87a9b1","stroke-width":8});
      svgNode(svg,"rect",{x:233,y:133,width:64,height:38,rx:7,fill:"#cce8f1",stroke:"#396b85","stroke-width":3});
      line(231,149,145,182,"#b66f47",4);line(284,115,388,75,"#177f72",4);
      textAt(56,35,"Incline: gravity component 6 N downhill",null,16);
      textAt(48,274,"Friction opposes travel in BOTH directions.",null,14);
      textAt(340,112,"Up → / Down ←",null,15);
      out.textContent="With friction "+nice(value)+" N: uphill retarding force "+nice(up)+" N; stopping distance "+nice(d)+" m; downhill net "+nice(down)+" N; returned K "+nice(returnK)+" J and speed "+nice(Math.sqrt(2*returnK))+" m/s.";
    }else if(id==="E08"){
      const xeq=value/100,xi=0.10,xother=2*xeq-xi;
      line(35,183,615,183,"#86a4af",3);
      line(90,90,90,215,"#516f87",6);
      svgNode(svg,"polyline",{points:"95,154 112,154 123,135 134,174 145,135 156,174 167,154 198,154",fill:"none",stroke:"#b88153","stroke-width":5});
      svgNode(svg,"rect",{x:197,y:129,width:83,height:50,rx:8,fill:"#cce7f2",stroke:"#38738b","stroke-width":2});
      const mapX=x=>196+x*680;
      line(mapX(xeq),85,mapX(xeq),210,"#168476",3);
      line(mapX(xother),103,mapX(xother),214,"#bc713b",3);
      textAt(23,30,"k = 100 N/m, initial x = 0.10 m",null,15);
      textAt(29,250,"New force: +"+nice(value)+" N; green = equilibrium, orange = far turning point",null,13);
      out.textContent="After force switch: new equilibrium x="+nice(xeq)+" m; starting rest x=0.10 m; other turning point x="+nice(xother)+" m. Conserve K+½kx²−F_new x, not spring energy alone.";
    }
  }
  function renderStage(host,id,config){
    host.replaceChildren();
    const s=states[id];
    stageSteps(host,s);
    const stage=add(host,"section","stage-card");
    const heading=add(stage,"h3",null,(s.stage+1)+". "+stageNames[s.stage]);
    heading.tabIndex=-1;
    const controls=add(stage,"div","stage-actions");
    const notice=add(host,"p","status");notice.id="stage-status";notice.setAttribute("aria-live","polite");
    if(s.stage===0){
      paragraph(stage,"Make your own prediction before the calculation. 'Not sure yet' is allowed.");
      inputFor(stage,id,{id:"prediction",label:config.question,type:"textarea"},s.predictionDraft);
      button(controls,"save-prediction","Save prediction → Attempt");
    }
    if(s.stage===1){
      paragraph(stage,config.challenge,"challenge-prompt");
      paragraph(stage,"Show a model, not only numbers. Your original words and entries will be frozen when you choose 'Save first attempt'.","step-note");
      for(const field of config.fields)inputFor(stage,id,field,s.attemptDraft?.[field.id]);
      const hint=add(stage,"section","hints");
      add(hint,"h4",null,"Optional progressive help · no worked answer");
      const hintList=add(hint,"ol","hint-list");
      for(let i=0;i<Math.min(s.hintsUsed,config.hints.length);i++)add(hintList,"li",null,config.hints[i]);
      const hintButton=button(hint,"hint","Show next study cue ("+s.hintsUsed+"/"+config.hints.length+")",true);
      hintButton.disabled=s.hintsUsed>=config.hints.length;
      button(controls,"save-attempt","Save first attempt → Reconstruct");
    }
    if(s.stage===2){
      paragraph(stage,"Your first model has been saved. Compare it with the worked route; then check your steps.");
      snapshot(stage,s);
      const worked=add(stage,"section","worked");add(worked,"h4",null,"Worked reconstruction (now unlocked)");
      const ol=add(worked,"ol");for(const [heading,desc] of config.worked){const li=add(ol,"li");add(li,"strong",null,heading+". ");li.append(document.createTextNode(desc));}
      const checks=add(stage,"fieldset","self-check");
      add(checks,"legend",null,"Check what your reasoning included");
      config.checks.forEach((label,i)=>{
        const l=add(checks,"label");const c=add(l,"input");c.type="checkbox";c.value=String(i);c.dataset.check="true";c.checked=(s.checks||[]).includes(i);
        l.append(document.createTextNode(" "+label));
      });
      button(controls,"save-check","Compare → Diagnose");
    }
    if(s.stage===3){
      paragraph(stage,"Which idea will you fix first? A mistake is useful information.");
      const sel=add(stage,"select");sel.dataset.diagnosis="true";
      add(sel,"option",null,"Select a possible cause").value="";
      config.diagnoses.forEach((opt,i)=>{add(sel,"option",null,opt).value=String(i);});
      if(s.diagnosis)sel.value=String(s.diagnosis.index);
      inputFor(stage,id,{id:"why",label:"What clue tells you this was the first wrong step?",type:"textarea"},s.diagnosis?.why||"");
      button(controls,"save-diagnosis","Save diagnosis → Repair");
    }
    if(s.stage===4){
      paragraph(stage,"Use the clue, then rewrite your reasoning WITHOUT changing your original attempt.");
      const tip=add(stage,"p","diagnosis-tip",config.diagnosisTips[s.diagnosis?.index??0]);
      snapshot(stage,s);
      inputFor(stage,id,{id:"repair",label:"My repaired model and reason for the change",type:"textarea"},s.repair||"");
      button(controls,"save-repair","Save repair → Boundary test");
      const details=add(stage,"details","review-model");add(details,"summary",null,"Review previous worked model (optional)");
      for(const [head,desc] of config.worked)paragraph(details,head+": "+desc);
    }
    if(s.stage===5){
      paragraph(stage,"Change ONE condition and make a fresh prediction before opening its check:");
      paragraph(stage,config.boundary,"challenge-prompt");
      snapshot(stage,s);
      paragraph(stage,"My repair: "+s.repair,"repair-record");
      if(s.boundary===null){
        inputFor(stage,id,{id:"boundary",label:"My changed-condition prediction, working and explanation",type:"textarea"},"");
        button(controls,"save-boundary","Save boundary attempt → Open check");
      }else{
        paragraph(stage,"Your saved changed-condition attempt: "+s.boundary,"step-note");
        const check=add(stage,"section","worked");add(check,"h4",null,"Changed-condition check (now unlocked)");
        paragraph(check,config.boundaryCheck);
        const history=button(controls,"history","Review my first attempt and repair",true);
        history.setAttribute("aria-expanded","false");
        const done=add(stage,"p","done","Finished the six stages. Return to your original question and solve it using your own model.");
        if(sourceLink){const link=add(done,"a","return-original"," Return to "+sourceLink.id+" without revealing its answer");link.href=sourceLink.href;}
      }
    }
    const reset=button(controls,"reset","Start again (clears this lesson)",true);reset.classList.add("reset");
    stage.append(controls);
    heading.focus({preventScroll:true});
  }
  function readFields(host){
    const out={};host.querySelectorAll("[data-field]").forEach(e=>out[e.dataset.field]=e.value);return out;
  }
  function dispatch(host,id,config,event){
    const target=event.target.closest("button[data-action]");
    if(!target||!host.contains(target))return;
    const s=states[id],action=target.dataset.action;
    const warn=t=>$("#stage-status").textContent=t;
    if(action==="reset"){
      if(!window.confirm("Clear this lesson's prediction, first attempt, hints and repair?"))return;
      try{localStorage.removeItem(key(id))}catch(_){}
      states[id]=blank(id);render();return;
    }
    if(action==="hint"&&s.stage===1&&s.first===null){
      s.hintsUsed=Math.min(config.hints.length,s.hintsUsed+1);
      persist(id);renderStage(host,id,config);return;
    }
    if(action==="history"&&s.stage===5&&s.boundary!==null){
      const old=$(".history",host);
      if(old){old.remove();target.setAttribute("aria-expanded","false");return;}
      const history=add(host,"section","history");snapshot(history,s);
      paragraph(history,"Repaired model: "+s.repair);target.setAttribute("aria-expanded","true");return;
    }
    if(action==="save-prediction"&&s.stage===0){
      const v=$('[data-field="prediction"]',host).value.trim();
      if(!v){warn("Write a prediction, or 'Not sure yet', before continuing.");return;}
      s.prediction=v;s.predictionDraft="";s.stage=1;
    }else if(action==="save-attempt"&&s.stage===1&&s.first===null){
      const values=readFields(host);
      if(!values.reason?.trim()){warn("Write your reasoning (or 'Not sure yet') before seeing the worked reconstruction.");$('[data-field="reason"]',host).focus();return;}
      s.first={...values};s.attemptDraft={};s.stage=2;
    }else if(action==="save-check"&&s.stage===2){
      s.checks=[...host.querySelectorAll("[data-check]:checked")].map(e=>Number(e.value));s.stage=3;
    }else if(action==="save-diagnosis"&&s.stage===3){
      const val=$("[data-diagnosis]",host).value;
      if(val===""){warn("Choose one cause to investigate first.");return;}
      s.diagnosis={index:Number(val),why:$('[data-field="why"]',host).value.trim()};s.stage=4;
    }else if(action==="save-repair"&&s.stage===4){
      const val=$('[data-field="repair"]',host).value.trim();
      if(!val){warn("Explain what you repaired—or why you are still unsure.");return;}
      s.repair=val;s.stage=5;
    }else if(action==="save-boundary"&&s.stage===5&&s.boundary===null){
      const val=$('[data-field="boundary"]',host).value.trim();
      if(!val){warn("Attempt the changed condition before seeing its check.");return;}
      s.boundary=val;
    }else{return;}
    persist(id);render();
  }
  function updateProgress(){
    const completed=allIds.filter(id=>states[id].boundary!==null).length;
    $("#extension-progress").textContent=completed+" of "+allIds.length+" boundary challenges completed";
    $("#extension-meter").max=allIds.length;$("#extension-meter").value=completed;
    for(const id of allIds){const link=$('[data-lesson-link="'+id+'"]');if(link){link.classList.toggle("complete",states[id].boundary!==null);link.setAttribute("aria-current",id===active?"page":"false");}}
  }
  function render(){
    const hash=location.hash.slice(1).toUpperCase();
    if(allIds.includes(hash))active=hash;
    else if(!location.hash)active="E01";
    const config=lessons[active];
    $("#current-title").textContent=active+" · "+config.title;
    const host=$("#lesson-surface");host.replaceChildren();
    const article=add(host,"article","lesson");article.id=active;
    const header=add(article,"header","lesson-title");
    add(header,"p","mini","WPE "+active+" · Existing extension learning pack");
    add(header,"h2",null,config.title);
    paragraph(header,config.question);
    const pair=add(article,"div","learning-grid");
    buildGuide(pair,active,config);
    const challenge=add(pair,"section","challenge");
    add(challenge,"p","mini","CORE1B · A different challenge");
    add(challenge,"h2",null,"Predict → Attempt → Reconstruct");
    paragraph(challenge,"The challenge changes the setting. Think first, then use optional help. Your first model remains separate from any later repair.");
    const root=add(challenge,"div","stage-root");root.dataset.stageRoot=active;
    root.addEventListener("click",e=>dispatch(root,active,config,e));
    root.addEventListener("input",()=>{
      const s=states[active];
      if(s.stage===0)s.predictionDraft=$('[data-field="prediction"]',root)?.value||"";
      if(s.stage===1&&s.first===null)s.attemptDraft=readFields(root);
      if(s.stage===0 || s.stage===1)persist(active);
    });
    renderStage(root,active,config);
    const footer=add(article,"nav","lesson-footer");
    footer.setAttribute("aria-label","Learning navigation");
    const i=allIds.indexOf(active);
    const prev=add(footer,"a",null,i===0?"WPE chapter":"← Previous extension");prev.href=i===0?"index.html":"#"+allIds[i-1];
    const next=add(footer,"a",null,i===allIds.length-1?"Back to extensions start":"Next extension →");next.href="#"+allIds[(i+1)%allIds.length];
    if(sourceLink && sourceLink.lesson===active){const ret=add(footer,"a","return-original","Return to "+sourceLink.id+" without showing answer");ret.href=sourceLink.href;}
    updateProgress();
  }
  async function routeSource(){
    const sourceId=new URLSearchParams(location.search).get("question");
    if(!sourceId)return;
    const banner=$("#source-journey"),info=$("#source-message"),link=$("#source-return");
    if(!/^[A-Za-z0-9-]{2,64}$/.test(sourceId)){banner.hidden=false;info.textContent="Invalid source question identifier. No original question link was created.";return;}
    try{
      const res=await fetch("reasoning-paths.review.json",{cache:"no-store"});
      if(!res.ok)throw Error("No route inventory");
      const manifest=await res.json();
      if(manifest.schema!=="wpe-reasoning-route-preview/v1"||manifest.policy!=="REVIEW_NAVIGATION_ONLY__NOT_CANONICAL_PREREQUISITE"||!Array.isArray(manifest.constructions))throw Error("Invalid route inventory");
      const route=manifest.constructions.find(row=>row.id==="WPE-"+active && row.proposed_source_ids?.some(s=>s.id===sourceId&&s.reader_present));
      if(!route)throw Error("Unmapped source/lesson pair");
      sourceLink={id:sourceId,lesson:active,href:"../../preview/question-status.html?question="+encodeURIComponent(sourceId)};
      banner.hidden=false;
      $("#source-title").textContent="Your original Question Bank entry: "+sourceId;
      info.textContent="Work through this different problem, then return to "+sourceId+" to make your own attempt. This is suggested practice, not an exam answer.";
      link.hidden=false;link.href=sourceLink.href;link.textContent="Return to "+sourceId+" without showing its answer";
      render();
    }catch(_){banner.hidden=false;info.textContent="This source ID is not mapped to the selected extension. No original question link is inferred.";link.hidden=true;}
  }
  allIds.forEach((id,i)=>{
    const nav=$("#extension-navigation");
    const a=add(nav,"a",null,(i+1)+". "+lessons[id].title);
    a.href="#"+id;a.dataset.lessonLink=id;
  });
  window.addEventListener("hashchange",()=>{sourceLink=null;$("#source-journey").hidden=true;render();routeSource();});
  render();
  routeSource();
})();
