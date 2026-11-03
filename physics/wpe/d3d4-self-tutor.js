/* WPE C01–C08 and E01–E05 interactive student practice. Client-side only: NOT secured answers,
 * not authenticated learner evidence, not academic Core1A/B acceptance.
 * Source author packs: WPE-C01 through C08 and WPE-E01 through E05; all source-theme joins are proposed and unqualified.
 */
(() => {
  "use strict";

  const stages = ["Predict", "Attempt", "Reconstruct", "Diagnose", "Repair", "Boundary test"];
  const signChoices = ["Positive (+)", "Negative (−)", "Zero (0)", "I'm not sure"];
  const lessons = {
    C01: {
      title: "Every force counts",
      version: 1,
      prediction: "Which forces help the scooter move up the ramp, which oppose it, and which do no work? Will it speed up?",
      hints: ["First choose the scooter as the system. Which way is its displacement while climbing?","Assign a work sign to each force before calculating. The normal force is perpendicular to the ramp, but gravity is not.","Add all signed work, then compare that total with the change in kinetic energy. Check whether the result permits motion from rest."],
      diagnosisFeedback: ["List motor, friction, gravity and normal force separately; choose the scooter as your system.","Use the uphill displacement as the reference direction. Friction opposes it; gravity also removes energy as height rises.","Only the sum of work by all forces equals ΔK. Rebuild your signed ledger before solving for speed.","The normal force is perpendicular to the surface displacement, so its work is zero.","Keep your force ledger; inspect signs, units and whether the final K is physically possible.","Start with a free-body sketch and label each force's angle to displacement."],
      fields: [
        {id:"system",type:"select",label:"What object are you following?",options:["The scooter", "Only the motor", "Only the friction", "I'm not sure"]},
        {id:"motor",type:"select",label:"Work done by the motor?",options:signChoices},
        {id:"friction",type:"select",label:"Work done by friction?",options:signChoices},
        {id:"gravity",type:"select",label:"Work done by gravity?",options:signChoices},
        {id:"normal",type:"select",label:"Work done by the normal force?",options:signChoices},
        {id:"netWork",type:"number",label:"Net work by all forces (J)",hint:"Use + or − for the total."},
        {id:"topSpeed",type:"number",label:"Speed at the top (m/s)",hint:"You can use a rounded number."},
        {id:"canReach",type:"select",label:"Will it reach the top?",options:["Yes", "No", "I'm not sure"]},
        {id:"reason",type:"textarea",label:"Explain your force arrows, energy ledger and reasoning",hint:"You can write 'I'm not sure' and learn from the next step."}
      ],
      worked: [
        ["Pick the system", "Follow the 3 kg scooter moving 2 m uphill. Its normal force is perpendicular to the slope."],
        ["Make a four-force ledger", "Motor work = +15 × 2 = +30 J. Friction = −3 × 2 = −6 J. Gravity = −mgh = −3 × 10 × 0.5 = −15 J. Normal force = 0 J."],
        ["Add all the work", "Net work = +30 − 6 − 15 + 0 = +9 J. It is incorrect to set friction work alone equal to the change in kinetic energy."],
        ["Find the final speed", "It starts from rest, so initial kinetic energy is 0 J. Final kinetic energy = 9 J. Because ½ × 3 × v² = 9, v² = 6 and v ≈ 2.45 m/s. It reaches the top."]
      ],
      rubric: [
        "I followed the scooter as the system and identified all four forces.",
        "I matched each work sign to the scooter's uphill displacement.",
        "I included gravity and gave zero work to the perpendicular normal force.",
        "I used net work = change in kinetic energy to find speed."
      ],
      diagnoses: [
        "I left gravity out of my ledger.",
        "I gave friction or gravity the wrong sign.",
        "I used only friction work instead of total work.",
        "I gave the normal force nonzero work.",
        "My model was fine; I want to double-check the arithmetic.",
        "I'm not sure what went wrong yet."
      ],
      repairPrompt: "Write your corrected force ledger and final speed. Explain what you changed from your first try (or why no change was needed).",
      boundaryPrompt: "Now the scooter's motor pulls with only 10 N uphill. Everything else is unchanged and it starts from rest. Can it climb the whole ramp? Explain using the energy ledger or the forces—not just yes or no.",
      boundaryCheck: [
        "Motor work over a hypothetical full climb would be +10 × 2 = +20 J.",
        "Friction and gravity still require −6 J and −15 J, so net work over the full ramp would be −1 J.",
        "A scooter starting at rest has 0 J initial kinetic energy, and cannot finish with −1 J. It cannot climb the whole ramp without extra energy.",
        "Another check: downhill gravity component = mgh / 2 m = 7.5 N. Together with 3 N friction, resistance is 10.5 N, more than the motor's 10 N."
      ]
    },
    C02: {
      title: "When the spring stops pushing",
      version: 1,
      prediction: "At what point does the spring stop pushing? Will the cart's speed be the same at spring release and after the rough strip?",
      hints: ["Split the journey into spring contact and travel beyond the spring. What marks the moment an unattached spring stops pushing?","Calculate the stored elastic energy while compressed; use it to determine kinetic energy at release before adding any rough-strip losses.","On the rough strip, the spring no longer supplies work. Deduct frictional work from the release kinetic energy and check whether K stays nonnegative."],
      diagnosisFeedback: ["Mark the natural-length point as the end of contact for an unattached spring.","Use friction only where the track is rough; the initial spring contact phase is smooth.","Write the separate energy balances for the release and the end of the rough strip.","Check the elastic energy ½kx² and negative friction work before using K=½mv².","Keep the two-region model; verify the square and square-root arithmetic.","Sketch both regions with a clear boundary; list which forces act in each."],
      fields: [
        {id:"boundary",type:"select",label:"When does spring contact end?",options:["When the spring returns to natural length", "At the far end of the rough strip", "The spring keeps pushing forever", "I'm not sure"]},
        {id:"springEnergy",type:"number",label:"Initial spring energy (J)"},
        {id:"releaseSpeed",type:"number",label:"Speed right when contact ends (m/s)"},
        {id:"frictionWork",type:"number",label:"Work done by friction on the rough strip (J)",hint:"Use a negative sign if it removes energy."},
        {id:"finalSpeed",type:"number",label:"Speed at the end of the rough strip (m/s)"},
        {id:"canCross",type:"select",label:"Can the cart cross the 0.50 m strip?",options:["Yes", "No", "I'm not sure"]},
        {id:"reason",type:"textarea",label:"Explain the two regions and the equations you chose",hint:"Name the contact phase and the rough-strip phase. 'I'm not sure' is okay."}
      ],
      worked: [
        ["Split the journey", "Region A: smooth contact as the spring goes from compressed to natural length. Region B: the 0.50 m rough strip after the cart is no longer touching the spring."],
        ["Energy at spring release", "Stored spring energy = ½ × 200 × 0.10² = 1.00 J. In smooth contact it becomes 1.00 J of kinetic energy. For the 2 kg cart: ½ × 2 × v² = 1, so release speed = 1.00 m/s."],
        ["Energy in the rough region", "The spring is no longer pushing. Friction work = −1 N × 0.50 m = −0.50 J, so final kinetic energy = 1.00 − 0.50 = 0.50 J."],
        ["Check the speed and route", "½ × 2 × v² = 0.50, giving v = √0.50 ≈ 0.707 m/s. The cart still has positive kinetic energy at the strip's end, so it crosses."]
      ],
      rubric: [
        "I marked where the unattached spring reaches natural length and stops pushing.",
        "I found spring energy and release speed using the smooth contact phase only.",
        "I included friction only on the separate rough strip.",
        "I carried release kinetic energy into the second region and found final speed."
      ],
      diagnoses: [
        "I kept adding spring force after contact ended.",
        "I added friction during the smooth spring-release section.",
        "I used the release speed again at the strip's far end.",
        "I mixed up spring energy, friction work or mass.",
        "My model was fine; I want to double-check the arithmetic.",
        "I'm not sure what went wrong yet."
      ],
      repairPrompt: "Redraw the contact boundary in words, then write a corrected two-region energy calculation and final speed. What changed?",
      boundaryPrompt: "Make the rough strip 1.00 m long instead of 0.50 m, keeping friction at 1 N. The cart starts from rest with the same spring. Does it reach the far end with a nonzero speed? Explain what happens there.",
      boundaryCheck: [
        "At spring release, the cart still has 1.00 J of kinetic energy.",
        "A 1.00 m strip with 1 N friction removes 1.00 J: friction work = −1.00 J.",
        "At the far end, kinetic energy would be exactly 0 J and speed 0 m/s. It reaches the endpoint and stops, but does not pass it with nonzero speed.",
        "A longer rough strip would require more energy than the cart has; without another push it cannot cross that longer strip."
      ]
    },
    C03: {
      title: "Energy added each second",
      version: 1,
      prediction: "With constant motor power, do we gain equal kinetic energy every second, equal speed every second, or both? Which graph will be straight?",
      hints: ["Identify what the source controls: a fixed rate of energy transfer, not a fixed force. What are the units of watts?","Write a K-versus-time table starting with the kinetic energy at t=0. Convert each K to speed only after that.","Read graph slopes: K–time slope is power; v–time slope is acceleration; displacement–time slope is speed. These slopes need not have the same shape."],
      diagnosisFeedback: ["Return to the units: watts are joules per second, not newtons or metres per second squared.","The trolley is already moving. Compute K₀ from its mass and starting speed before adding energy.","Use K=½mv² after each time row; equal energy increments do not mean equal speed increments.","Name both axes before describing a graph: energy, speed and displacement have different slopes.","Check the assumptions: net power is constant on a smooth track, but force P/v falls as speed grows.","Start with the distinction between power, work and kinetic energy. Compare units before equations."],
      fields: [
        {id:"powerMeaning",type:"select",label:"What does 18 W tell us?",options:["The motor adds 18 J every second", "The force is always 18 N", "The trolley gains 18 m/s every second", "I'm not sure"]},
        {id:"initialEnergy",type:"number",label:"Kinetic energy at the start (J)",hint:"Remember: the trolley is already moving at 2 m/s."},
        {id:"energyAt2",type:"number",label:"Total kinetic energy after 2 s (J)",hint:"Include the initial kinetic energy."},
        {id:"speedAt2",type:"number",label:"Speed after 2 s (m/s)",hint:"A rounded decimal is fine."},
        {id:"energyAt6",type:"number",label:"Total kinetic energy after 6 s (J)"},
        {id:"speedAt6",type:"number",label:"Speed after 6 s (m/s)"},
        {id:"energyGraph",type:"select",label:"Shape of kinetic energy against time?",options:["Straight rising line", "Curving line that flattens", "Horizontal line", "I'm not sure"]},
        {id:"speedGraph",type:"select",label:"Shape of speed against time?",options:["Straight rising line", "Rising curve that gradually flattens", "Horizontal line", "I'm not sure"]},
        {id:"distanceGraph",type:"select",label:"Shape of displacement against time?",options:["Straight rising line", "Rising curve that gets steeper", "Horizontal line", "I'm not sure"]},
        {id:"acceleration",type:"select",label:"Is acceleration constant?",options:["Yes", "No", "I'm not sure"]},
        {id:"reason",type:"textarea",label:"Show your time → energy → speed table and explain the three graph shapes",hint:"It's okay to say 'I'm not sure' at any step."}
      ],
      worked: [
        ["Start with the trolley's own energy", "The 3 kg trolley starts at 2 m/s. K₀ = ½ × 3 × 2² = 6 J. Power is 18 W = 18 J of added kinetic energy each second, not 18 N."],
        ["Make a two-time energy table", "At 2 seconds, added energy = 18 × 2 = 36 J, total K = 6 + 36 = 42 J. At 6 seconds, added = 18 × 6 = 108 J, total K = 6 + 108 = 114 J."],
        ["Turn energy into speed", "Using K = ½mv²: at 2 s, v² = 2 × 42 / 3 = 28, so v ≈ 5.29 m/s. At 6 s, v² = 2 × 114 / 3 = 76, so v ≈ 8.72 m/s."],
        ["Choose the right graph shape", "K–time is a rising straight line (equal joules added each second). Speed–time rises but gradually flattens. Displacement–time rises and gets steeper because its slope is speed. You do not need to calculate exact distance."],
        ["Check acceleration", "It is not constant: at positive speed, the driving force F = P / v gets smaller as the trolley speeds up. Constant power does not mean constant force or equal speed gains each second."]
      ],
      rubric: [
        "I used 18 W as joules per second and included the trolley's starting energy.",
        "I built both time → added energy → total kinetic energy → speed rows.",
        "I used the correct axes to describe the three different graph shapes.",
        "I explained why constant power does not mean constant acceleration."
      ],
      diagnoses: [
        "I treated watts as newtons or as a fixed acceleration.",
        "I forgot the starting kinetic energy.",
        "I added the same speed each second instead of the same energy.",
        "I mixed up the speed, displacement and kinetic-energy graph shapes.",
        "My model was fine; I want to double-check the arithmetic.",
        "I'm not sure what went wrong yet."
      ],
      repairPrompt: "Correct the first wrong entry in your time–energy–speed table or your graph explanation. Give both speeds and say whether acceleration stays constant. What did you change?",
      boundaryPrompt: "The SAME 3 kg trolley still starts at 2 m/s, but the motor now supplies 9 W (half the original power). What is its speed after 2 seconds? Does that make its acceleration constant? Explain.",
      boundaryCheck: [
        "The trolley starts with K₀ = ½ × 3 × 2² = 6 J. The power is now 9 J/s.",
        "After 2 s it gains 9 × 2 = 18 J, so the total kinetic energy is 6 + 18 = 24 J.",
        "From ½ × 3 × v² = 24, we get v² = 16 and speed = 4 m/s.",
        "Acceleration is still not constant: the motor supplies constant power, so as speed grows its driving force F = P / v decreases. Power changed, not the kind of model."
      ]
    },
    C04: {
      title: "Only the hanging part",
      version: 1,
      prediction: "As you pull the rope upward from 4 m hanging to 2 m hanging, what happens to the hanging mass and the position of its middle? Will this take as much work as lifting all of it?",
      hints: ["Find the rope's mass per metre. Only the part below the edge contributes nonzero gravitational potential energy for the chosen zero.","Draw two separate hanging pieces. In each, both the hanging mass and its centre depth depend on the hanging length.","Find the potential energy in each picture relative to the platform, then subtract final minus initial for a very slow, frictionless lift."],
      diagnosisFeedback: ["Use mass per metre times hanging length, not the mass of the rope already on the table.","The hanging length changes, so hanging mass must be recalculated for the after-picture.","For a uniform hanging piece, its centre is halfway down that piece.","Use one fixed height-zero and calculate final potential energy minus initial potential energy.","Keep the two-picture model and recheck arithmetic and signs.","Make a before/after table with hanging length, mass, centre depth and U."],
      fields: [
        {id:"massPerMetre",type:"number",label:"Mass per metre of rope (kg/m)",hint:"Divide the whole rope mass by the whole rope length."},
        {id:"startMass",type:"number",label:"Mass hanging BEFORE the pull (kg)",hint:"Only 4 m out of 8 m hangs at the start."},
        {id:"startDepth",type:"number",label:"Depth of the hanging part's middle BEFORE (m below platform)"},
        {id:"startU",type:"number",label:"Gravitational potential energy BEFORE (J)",hint:"Choose platform height as zero. Below it is negative."},
        {id:"endMass",type:"number",label:"Mass hanging AFTER the pull (kg)",hint:"2 m still hangs. The hanging mass has changed."},
        {id:"endDepth",type:"number",label:"Depth of the hanging part's middle AFTER (m below platform)"},
        {id:"endU",type:"number",label:"Gravitational potential energy AFTER (J)"},
        {id:"helperWork",type:"number",label:"Positive work by the helper (J)",hint:"Take final potential energy minus initial potential energy."},
        {id:"modelChoice",type:"select",label:"Which mass model did you use?",options:["Only the hanging mass in each state", "The whole 4 kg rope in both states", "The mass hanging at the start for both states", "I'm not sure"]},
        {id:"reason",type:"textarea",label:"Describe the two hanging-length pictures and explain how you found the work",hint:"Describe the middle of each hanging piece. You may write 'I'm not sure'."}
      ],
      worked: [
        ["Start with mass per metre", "The 8 m rope has 4 kg of mass, so 4 ÷ 8 = 0.5 kg per metre. Only the hanging length contributes energy below platform height."],
        ["Draw the BEFORE state", "Initially 4 m hangs: hanging mass = 0.5 × 4 = 2 kg. Its middle is halfway down, at 2 m below the platform. With U = 0 on the platform, U_before = −2 × 10 × 2 = −40 J."],
        ["Draw the AFTER state", "Only 2 m remains hanging: mass = 0.5 × 2 = 1 kg; its middle is 1 m below the platform. U_after = −1 × 10 × 1 = −10 J."],
        ["Subtract final minus initial", "The helper pulls slowly on a smooth edge, so their positive work equals the rise in gravitational potential energy: (−10) − (−40) = +30 J."],
        ["Explain the key decision", "Both the hanging mass and its centre-of-mass depth shrink. Using the entire 4 kg rope or the starting hanging mass for the final state would model the wrong picture."]
      ],
      rubric: [
        "I found the mass per metre and used only the mass actually hanging in each state.",
        "I placed the middle of each uniform hanging piece halfway down.",
        "I calculated a separate potential energy before and after, using the platform as zero.",
        "I subtracted final minus initial and explained why the helper's work is positive."
      ],
      diagnoses: [
        "I treated the whole 4 kg rope as if it were hanging.",
        "I kept the hanging mass unchanged after pulling.",
        "I placed the middle at the bottom of the hanging piece.",
        "I mixed up the minus signs when subtracting potential energies.",
        "My model was fine; I want to double-check the arithmetic.",
        "I'm not sure what went wrong yet."
      ],
      repairPrompt: "Write a corrected BEFORE and AFTER table with hanging mass, middle depth and potential energy, then the helper's work. Explain which picture or subtraction you fixed.",
      boundaryPrompt: "Start with the SAME 8 m, 4 kg rope with 4 m hanging. Now pull it COMPLETELY onto the smooth platform (0 m hanging). How much work is needed, and why is this more than stopping with 2 m still hanging?",
      boundaryCheck: [
        "The starting hanging part is unchanged: 2 kg, with its middle 2 m below the platform, so U_before = −40 J.",
        "If the rope is fully on the platform, 0 m hangs: U_after = 0 J.",
        "The slow helper's work is U_after − U_before = 0 − (−40) = +40 J.",
        "That exceeds the +30 J partial-lift case because the helper lifts the remaining hanging 2 m section as well. The full rope does not rise by one identical height."
      ]
    },
    C05: {
      title: "Read the axes first",
      version: 1,
      prediction: "Which new graph card needs an area, and which two need a slope? What units should your answers use?",
      hints: ["Read each graph's vertical and horizontal axis labels, then ask what UNIT the question wants. Force × distance makes joules; distance ÷ time makes metres per second.","For the U–position graph, draw an arrow showing that potential rises to the right. A conservative force points opposite the direction of increasing potential. For card T, use only the requested 2–5 s interval."],
      diagnosisFeedback: ["Put the horizontal axis unit under the force graph. Multiply newtons by metres to get work; the line's slope has different units.","Find the change in U divided by change in position, then reverse its sign to get conservative force. The U–x area does not represent force.","Circle the requested 2–5 s interval, read its two displacement values and divide their difference by three seconds.","Start each card with 'vertical axis / horizontal axis / operation / resulting unit' before doing any number work.","Check your units and signs against the axes once more. If they match, keep the original reasoning and explain why.","Use one card at a time and start from its axis names. A small table is enough; you don't need all three answers at once."],
      fields: [
        {id:"graphR",type:"select",label:"Card R: How do you find work from force against position?",options:["Area between the line and x-axis", "Slope of the line", "Area under a potential–position line", "I'm not sure"]},
        {id:"workR",type:"number",label:"Card R: Work over 0–4 m (J)",hint:"The force rises from 0 N to 8 N. Think about a triangle."},
        {id:"graphS",type:"select",label:"Card S: How do you find the conservative force from U against x?",options:["Area under the graph", "Negative slope of the line", "Positive slope of the line", "I'm not sure"]},
        {id:"forceS",type:"number",label:"Card S: Conservative force (N)",hint:"Give a minus sign if the force points left."},
        {id:"graphT",type:"select",label:"Card T: How do you find velocity from displacement against time?",options:["Area below the curve", "Slope of the segment from 2–5 s", "Slope of the entire 0–5 s span", "I'm not sure"]},
        {id:"speedT",type:"number",label:"Card T: Velocity from 2–5 s (m/s)"},
        {id:"unitChoice",type:"select",label:"Which units belong to R, S and T, in that order?",options:["J, N, m/s", "N/m, J, m/s", "J, J, m", "I'm not sure"]},
        {id:"reason",type:"textarea",label:"Explain how the axes told you to use area or slope for all three cards",hint:"Use the pattern: axes → operation → quantity → units. 'I'm not sure' is okay."}
      ],
      worked: [
        ["R: read F against x", "The y-axis is force (N) and the x-axis is position (m). Work is the signed AREA under F–x. A triangle rising 0 to 8 N over 4 m has area ½ × 4 × 8 = +16 J. Its slope is NOT work."],
        ["S: read U against x", "Potential energy rises from 2 J at 0 m to 8 J at 2 m. The slope is (8 − 2) ÷ (2 − 0) = +3 J/m, and a conservative force is the NEGATIVE slope: F = −3 N. The area under U–x is not work."],
        ["T: read s against t", "Between 2 s and 5 s, displacement rises from 4 m to 16 m. The slope of THAT straight segment is (16 − 4) ÷ (5 − 2) = +4 m/s. The earlier 0–2 s part has a different slope and is not the interval asked."],
        ["Check the meaning of units", "Force × position → N·m = J of work; change in potential energy ÷ position → J/m = N of force, with a minus sign; change in displacement ÷ time → m/s of velocity."],
        ["What if the graph has a corner?", "Card T has a sharp join at 2 s. It has a well-defined slope from 2 to 5 s, but at the exact corner a single instantaneous slope is not defined. Always check which interval is requested."]
      ],
      rubric: [
        "I identified the horizontal and vertical axes and chose area, negative slope and slope, in that order.",
        "I used the triangular force–position AREA for +16 J of work instead of its line slope.",
        "I remembered the negative sign for the conservative force and got −3 N.",
        "I used only the 2–5 s segment and gave +4 m/s with the correct units."
      ],
      diagnoses: [
        "I used the slope of the force–position graph as work.",
        "I used the area of the potential–position graph or forgot the negative force sign.",
        "I measured the full 0–5 s interval instead of the 2–5 s segment.",
        "I mixed up units or did not look at the axes first.",
        "My model was fine; I want to double-check the arithmetic.",
        "I'm not sure what went wrong yet."
      ],
      repairPrompt: "For each card, write its axes, the chosen operation and the physical answer with units. Circle in words the first wrong choice in your original explanation. What did you fix?",
      boundaryPrompt: "Imagine Card R is drawn with the SAME rising triangle from 0 to 8 N over 4 horizontal units, but the horizontal axis is now TIME (0–4 s), not position. What does the AREA under a force–time graph represent? Is it still work? Give the quantity and unit.",
      boundaryCheck: [
        "Read the altered axes FIRST: vertical F in newtons, horizontal t in seconds.",
        "The triangular area is still ½ × 4 × 8 = 16 numerically, but now its unit is N·s, not N·m.",
        "Area under FORCE–TIME is IMPULSE (change in momentum), so the result is +16 N·s for the shown positive force.",
        "It is NOT 16 J of work. A graph's meaning depends on its labeled axes, even when the shape looks identical."
      ]
    },
    C06: {
      title: "Stay on the circle?",
      version: 1,
      prediction: "The ball has enough energy to be at the top height in a calculation. Does that alone prove its string can stay taut? At the top, which way is inward and can a string push?",
      hints: ["Draw two arrows at the top of the circular path: one toward the centre and one in the direction of gravity. What direction would the tension in a taut string pull?","First use the height rise from bottom to top to estimate top speed from energy. THEN compare the inward force it needs with the weight that already points inward. A string cannot provide an outward push."],
      diagnosisFeedback: ["Separate the tests: reaching the top HEIGHT using energy is not the same as staying on the taut circular route.","At the top, the centre is below the ball. Redraw downward gravity and downward string tension before forming the radial-force equation.","A negative computed tension means the assumed taut-string model is invalid. A string cannot push; use this sign as a physical check.","Speed is tangent to the circle while inward acceleration has magnitude v²/r. Label their directions separately before calculating.","Recheck the 2r height difference, top-speed squared and force signs. Explain whether your initial model already did both tests.","Try two small calculations: 'energy allows this height?' and 'tension can pull inward?' The second decision is what the first cannot answer."],
      fields: [
        {id:"topInward",type:"select",label:"At the top of a vertical circle, which direction is toward its centre?",options:["Downward", "Upward", "Along its tangential velocity", "I'm not sure"]},
        {id:"heightRise",type:"number",label:"Height change from bottom to top (m)",hint:"The rise is twice the circle's 1 m radius."},
        {id:"candidateSpeedSquared",type:"number",label:"Candidate top speed squared, v² (m²/s²)",hint:"Use energy only for a hypothetical taut circle: v_top² = v_bottom² − 4gr."},
        {id:"candidateSpeed",type:"number",label:"Candidate top speed (m/s)"},
        {id:"energyPossible",type:"select",label:"Does energy alone allow a ball to be at the top height?",options:["Yes", "No", "I'm not sure"]},
        {id:"radialEquation",type:"select",label:"Which equation is valid at the top WHILE the string is taut?",options:["T + mg = mv²/r", "T − mg = mv²/r", "T = mg + mv²/r", "I'm not sure"]},
        {id:"topTension",type:"number",label:"Calculated top string tension (N)",hint:"A negative answer is a warning about the model."},
        {id:"staysTaut",type:"select",label:"Can this string remain taut all the way over the top?",options:["Yes", "No", "I'm not sure"]},
        {id:"reason",type:"textarea",label:"Explain the two checks—energy AND inward force—and what your tension sign means",hint:"Say what a real string can and cannot do. You may write 'I'm not sure'."}
      ],
      worked: [
        ["Check the height with energy", "The top is 2r = 2 × 1 = 2 m higher than the bottom. For a hypothetical taut circle, v_top² = v_bottom² − 4gr = 7² − 4 × 10 × 1 = 9. So candidate top speed = 3 m/s. Energy ALONE would allow that height."],
        ["Draw the top inward arrow", "At the very TOP, the centre of the circle is DOWNWARD. Both gravity mg and the taut-string tension T would point downward. The radial-force equation is T + mg = mv_top²/r."],
        ["Check the force the string would need", "For 1 kg, g = 10 and r = 1: needed inward force mv²/r = 1 × 9 ÷ 1 = 9 N, while gravity alone pulls inward with 10 N. Thus T = 9 − 10 = −1 N."],
        ["Interpret impossible negative tension", "A string can PULL but cannot PUSH. T = −1 N is not a real pulling tension. The imagined taut circular trajectory is impossible: the string goes slack BEFORE the top. After slackening, the bob is no longer constrained to the original circle."],
        ["State the difference between tests", "The correct conclusion is NOT 'the ball has too little energy to reach the height'. The energy test passes, but the radial-force (taut-string) test fails. Both are needed for a full taut circle."]
      ],
      rubric: [
        "I used the 2 m rise and calculated the candidate top speed squared from energy.",
        "I marked inward as downward at the top and wrote T + mg = mv²/r.",
        "I calculated −1 N and recognized it as an impossible pulling tension, not a normal negative force.",
        "I concluded the string slackens before the top; energy alone does not guarantee a taut circle."
      ],
      diagnoses: [
        "I assumed enough energy automatically means the ball stays on its circle.",
        "I drew the top inward direction or force signs incorrectly.",
        "I accepted negative tension as a real string pushing outward.",
        "I mixed up v²/r (inward acceleration) with tangential speed or acceleration.",
        "My model was fine; I want to double-check the arithmetic.",
        "I'm not sure what went wrong yet."
      ],
      repairPrompt: "Draw in words the top centre arrow and write BOTH the energy and radial-force checks. What must you correct about a negative tension and whether the string remains taut?",
      boundaryPrompt: "Keep the SAME 1 kg ball and 1 m light string, but start it at the bottom at 8 m/s instead of 7 m/s. Compute candidate top v² and the top tension. Could the string remain taut through the top now? Explain both checks.",
      boundaryCheck: [
        "For the hypothetical taut circle, v_top² = 8² − 4 × 10 × 1 = 64 − 40 = 24 m²/s². The energy test passes.",
        "At the top, inward is down and T + mg = mv²/r. Thus T = 1 × 24 / 1 − 1 × 10 = +14 N.",
        "The top tension is positive, so the string CAN remain taut at the top; under the ideal lossless conditions, the complete circular path is physically possible.",
        "For comparison, the ideal minimum bottom speed for a just-taut top is √(5gr) = √50 ≈ 7.07 m/s. Seven was slightly too low; eight is above it."
      ]

    },
    C07: {
      title: "Momentum arrives every second",
      version: 1,
      prediction: "The chips arrive already moving right. Does the belt need to speed them up? Will extra motor power all become the chips' kinetic energy, or might some become heat?",
      hints: ["Draw a one-second batch of arriving chips. Label their incoming horizontal speed and outgoing belt speed, and use kilograms EACH second rather than total chips accumulated.","Calculate the force from mass-per-second × speed change. Motor power uses BELT speed, while kinetic-energy change uses both squared speeds. What is left over during slipping?"],
      diagnosisFeedback: ["Use a control-volume picture: count new kilograms per second, not the entire stock already riding the conveyor.","Underline the 1 m/s incoming speed and the feed rule 'half the belt speed'. Recompute the horizontal velocity gain before force.","The motor keeps the belt moving, so its pickup force moves at BELT speed. Recalculate mechanical power at that speed.","Make a three-column energy ledger: motor input, chip kinetic-energy gain, and heat. Do not force the first two columns to match.","Check units in each line: kg/s × m/s makes N; N × m/s makes W. Then test whether the three power entries balance.","Start with two arrows, 'before' and 'after', and a small box labelled 'kg each second'. Keep each calculation separate."],
      fields: [
        {id:"model",type:"select",label:"Which object or flow are you following?",options:["Incoming kilograms of chips each second", "All chips ever collected on the belt", "Only the empty belt", "I'm not sure"]},
        {id:"flowRate",type:"number",label:"Mass of new chips per second (kg/s)",hint:"The feed rate equals half the numerical belt speed."},
        {id:"deltaVelocity",type:"number",label:"Horizontal velocity gain per kilogram (m/s)",hint:"Subtract incoming rightward speed from outgoing belt speed."},
        {id:"pickupForce",type:"number",label:"Force needed on new chips (N)",hint:"Flow rate multiplied by horizontal velocity gain."},
        {id:"motorPower",type:"number",label:"Extra motor power for pickup (W)",hint:"Force needed to hold belt speed × belt speed."},
        {id:"chipEnergy",type:"number",label:"Rate of chips' horizontal kinetic-energy gain (W)",hint:"½ × kilograms per second × (outgoing speed squared − incoming speed squared)."},
        {id:"heatRate",type:"number",label:"Rate of heat during speed matching (W)",hint:"Extra motor power minus chips' kinetic-energy-gain rate."},
        {id:"energyModel",type:"select",label:"Where does the extra motor power go?",options:["Part to chips' kinetic energy and part to frictional heating", "All to chips' kinetic energy", "All to gravity", "I'm not sure"]},
        {id:"reason",type:"textarea",label:"Explain your incoming → outgoing momentum picture and the three power rates",hint:"Start with kilograms each second, then explain why motor power is not equal to the chips' kinetic-energy gain. 'I'm not sure' is okay."}
      ],
      worked: [
        ["Read the feed rate and arrival speed", "The belt speed is 4 m/s, so the feeder delivers 4 ÷ 2 = 2 kg of chips EACH SECOND. Chips arrive already moving right at 1 m/s and leave at 4 m/s: Δv = 4 − 1 = +3 m/s."],
        ["Change momentum per second", "Horizontal force on the incoming stream is mass rate × Δv = 2 × (4 − 1) = +6 N. The chips push the belt backward with 6 N, so the motor must supply an extra 6 N forward to hold belt speed."],
        ["Find pickup-related motor power", "Motor power = extra forward force × belt speed = 6 N × 4 m/s = 24 W. Use belt speed, NOT incoming chip speed, for this motor power."],
        ["Compute kinetic-energy gain separately", "Each second, 2 kg of chips change speed from 1 to 4 m/s: gain rate = ½ × 2 × (4² − 1²) = 15 W. They did NOT start with zero horizontal kinetic energy."],
        ["Balance input, gain and heat", "Motor pickup power = 24 W; chips' kinetic-energy-gain rate = 15 W. The difference is 9 W of frictional heat in this idealized pickup. Check: ½ × 2 × (4 − 1)² = 9 W, so 24 = 15 + 9."]
      ],
      rubric: [
        "I used kilograms arriving EACH SECOND, not all the accumulated chips, and included the nonzero incoming rightward velocity.",
        "I used force = mass flow rate × (outgoing speed − incoming speed), giving +6 N.",
        "I used BELT speed to find 24 W of extra motor power and distinguished that from 15 W of chips' kinetic-energy gain.",
        "I balanced the 9 W heat rate and explained the speed-matching friction."
      ],
      diagnoses: [
        "I treated all chips already on the belt as the mass to accelerate.",
        "I forgot the incoming 1 m/s or ignored the given feed-rate rule.",
        "I used incoming speed rather than belt speed for motor power.",
        "I assumed all motor power becomes horizontal kinetic energy and forgot heat.",
        "My model was fine; I want to double-check the arithmetic.",
        "I'm not sure what went wrong yet."
      ],
      repairPrompt: "Redraw the incoming → outgoing chip speeds in words. Recalculate the flow rate, force and the separate 24 W motor, 15 W kinetic gain and 9 W heat entries. Explain the first difference from your original attempt.",
      boundaryPrompt: "The chips STILL arrive moving right at 1 m/s, and the feeder STILL delivers half the numerical belt speed in kg/s. But now the belt moves at 2 m/s instead of 4 m/s. Find the mass flow rate, pickup force, extra motor power, chips' kinetic-energy-gain rate and heat rate. Do all five merely halve? Why?",
      boundaryCheck: [
        "At 2 m/s, the flow rate is 2 ÷ 2 = 1 kg/s. The chips' horizontal speed gain is 2 − 1 = 1 m/s.",
        "Force on incoming chips = 1 × 1 = +1 N. Extra motor pickup power = 1 N × 2 m/s = 2 W.",
        "Chips' horizontal kinetic-energy-gain rate = ½ × 1 × (2² − 1²) = 1.5 W.",
        "Heat rate = 2 − 1.5 = 0.5 W. Check: ½ × 1 × (2 − 1)² = 0.5 W.",
        "The numbers do NOT all halve, because the mass flow, belt speed and incoming-to-outgoing velocity DIFFERENCE all change. Other motor losses remain outside this idealized model."
      ]
    },
    C08: {
      title: "What stays the same?",
      version: 1,
      prediction: "At equal compression, which pad looks stiffer from the 4 cm measurement? Will the stiffer pad store more energy under BOTH equal-extension and equal-final-force tests?",
      hints: ["First convert 4 centimetres to metres. Infer each k from the lab measurement using final force divided by compression; the two tests come AFTER this measurement.","Label Test X 'same compression' and Test Y 'same FINAL force'. For Y the softer spring compresses farther, so calculate each new x = F/k instead of reusing X's 5 cm."],
      diagnosisFeedback: ["Remember: 4 cm is 0.04 m and 5 cm is 0.05 m. Recalculate k in N/m before the energy comparisons.","Write 'same extension' over X and 'same final force' over Y. Each condition chooses a different comparison; stiffness alone does not choose the winner.","Test Y must use each spring's own compression under 12 N. Find x = F/k for Blue and Gold, then use elastic energy.","For a slowly increasing Hookean force, the area under the force–extension graph is a TRIANGLE: ½ × final force × extension.","Check that both tests use slow loading and final equilibrium conditions. Review the ordering without erasing the first try.","Start by writing what is held the SAME in each experiment; then calculate one spring at a time."],
      fields: [
        {id:"kBlue",type:"number",label:"Blue pad stiffness (N/m)",hint:"4 cm is 0.04 m. Use k = final force ÷ compression."},
        {id:"kGold",type:"number",label:"Gold pad stiffness (N/m)"},
        {id:"testXChoice",type:"select",label:"Test X: both compressed by 5 cm. Which stores more energy?",options:["Blue pad", "Gold pad", "Same energy", "I'm not sure"]},
        {id:"xBlue",type:"number",label:"Test X: Blue elastic energy (J)",hint:"Use ½ × k × 0.05²."},
        {id:"xGold",type:"number",label:"Test X: Gold elastic energy (J)"},
        {id:"testYChoice",type:"select",label:"Test Y: both reach 12 N FINAL force. Which stores more energy?",options:["Blue pad", "Gold pad", "Same energy", "I'm not sure"]},
        {id:"yBlueExtension",type:"number",label:"Test Y: Blue compression at final force (m)",hint:"New compression = 12 N ÷ stiffness."},
        {id:"yGoldExtension",type:"number",label:"Test Y: Gold compression at final force (m)"},
        {id:"yBlue",type:"number",label:"Test Y: Blue elastic energy (J)",hint:"At equal FINAL force use F² ÷ (2k), or ½ × final force × compression."},
        {id:"yGold",type:"number",label:"Test Y: Gold elastic energy (J)"},
        {id:"control",type:"select",label:"Why can the ranking reverse?",options:["Test X fixes compression; Test Y fixes FINAL force", "Both tests fix compression", "Both tests fix force throughout compression", "I'm not sure"]},
        {id:"reason",type:"textarea",label:"Explain how you inferred both stiffnesses and why the energy ranking switches",hint:"Use a small table: fixed extension versus fixed final force. You can write 'I'm not sure'."}
      ],
      worked: [
        ["Infer stiffness from the first measurements", "At a shared compression of 4 cm = 0.04 m, Blue needs 8 N so k_Blue = 8 ÷ 0.04 = 200 N/m. Gold needs 16 N so k_Gold = 16 ÷ 0.04 = 400 N/m. Gold is stiffer."],
        ["Test X fixes compression, not force", "Both pads are compressed 5 cm = 0.05 m. Blue stores ½ × 200 × 0.05² = 0.25 J. Gold stores ½ × 400 × 0.05² = 0.50 J. GOLD, the stiffer pad, stores more at fixed compression."],
        ["Test Y fixes FINAL force, not compression", "For the SAME final equilibrium force of 12 N: Blue compresses 12 ÷ 200 = 0.06 m; Gold compresses 12 ÷ 400 = 0.03 m. They do NOT have the same compression."],
        ["Compute stored energy at equal final force", "Elastic energy is F² ÷ (2k). Blue stores 12² ÷ (2 × 200) = 0.36 J; Gold stores 12² ÷ (2 × 400) = 0.18 J. BLUE, the softer pad, stores more at fixed FINAL force."],
        ["Explain the reversal and the loading triangle", "For fixed compression, U = ½kx² grows with k. For fixed final force, U = F²/(2k) falls with k. During slow loading the force rises from zero, so energy is ½ × final F × compression—not final F × compression."]
      ],
      rubric: [
        "I converted 4 cm to 0.04 m and inferred Blue 200 N/m and Gold 400 N/m.",
        "I labelled Test X as fixed 5 cm compression and calculated 0.25 J (Blue) and 0.50 J (Gold).",
        "I labelled Test Y as fixed FINAL 12 N force, found different final compressions, and calculated 0.36 J (Blue) and 0.18 J (Gold).",
        "I explained why the stiffer spring wins X but the softer wins Y, without treating final force as constant throughout slow loading."
      ],
      diagnoses: [
        "I used centimetres as metres when inferring stiffness.",
        "I assumed the stiffer pad always stores more energy.",
        "I treated Test Y as though both pads had equal compression.",
        "I multiplied final force × compression instead of the triangular loading area.",
        "My model was fine; I want to double-check the arithmetic.",
        "I'm not sure what went wrong yet."
      ],
      repairPrompt: "Circle in words what is fixed in X and Y. Make a corrected comparison table: each stiffness, both energies at 5 cm, then both energies at FINAL force 12 N and why the winner changes.",
      boundaryPrompt: "Repeat Test Y with the SAME ideal pads, but slowly increase the FINAL force to 24 N (double 12 N). How many times larger does each stored energy become? Calculate Blue and Gold energies, name which pad stores more, and explain why.",
      boundaryCheck: [
        "At a fixed stiffness, stored energy for a slowly increased FINAL force is F² ÷ (2k). Doubling F makes F² four times bigger.",
        "Blue at 24 N stores 24² ÷ (2 × 200) = 1.44 J, four times the former 0.36 J.",
        "Gold at 24 N stores 24² ÷ (2 × 400) = 0.72 J, four times the former 0.18 J.",
        "BLUE still stores more at the same FINAL force, because it is softer and compresses farther. This does not mean a suddenly applied constant 24 N force acts through the entire extension."
      ]

    },
    E01: {
      "title": "Can the bead reach the other valley?",
      "version": 1,
      "prediction": "Two valleys have equally low potential energy. Is that alone enough for a bead to travel from the right valley to the left? Why?",
      "hints": [
        "At each position, kinetic energy is what remains after subtracting potential from the fixed total. A forbidden position has a negative leftover.",
        "Sketch the energy line on the whole double-well graph. A destination can be individually allowed but disconnected from the starting interval.",
        "Find the turning positions by setting kinetic energy to zero. The crucial decision is whether every point along the path stays accessible."
      ],
      "diagnosisFeedback": [
        "Check the entire continuous route, not just whether the destination has U below the energy budget.",
        "A turning point has zero kinetic energy and can still be reached. Mark boundaries, not forbidden endpoints.",
        "Find the connected allowed region containing your STARTING position. Two separate shaded regions are not traversable from one to the other.",
        "Speed is largest where allowed potential energy is LOWEST, because kinetic energy is the remaining E−U.",
        "Recheck the dimensionless position q=x/(1 m) and the inequality without changing a correct physical model.",
        "Use a value table at q=−2, 0 and +2 before solving the turning points; uncertainty is a useful starting observation."
      ],
      "fields": [
        {
          "id": "barrier",
          "type": "number",
          "label": "Potential energy at the central barrier x=0 (J)",
          "hint": "Use q=0 in U=(q²−4)² J."
        },
        {
          "id": "route",
          "type": "select",
          "label": "Can the bead start at +2 m and travel continuously to −2 m?",
          "options": [
            "Yes, both wells are low",
            "No, the two allowed regions are disconnected",
            "Yes, because potential is never negative",
            "I'm not sure"
          ]
        },
        {
          "id": "rightTurning",
          "type": "number",
          "label": "Right valley inner turning position (m)",
          "hint": "This is the nearest turning point to the central hill."
        },
        {
          "id": "outerTurning",
          "type": "number",
          "label": "Right valley outer turning position (m)",
          "hint": "An approximation is fine."
        },
        {
          "id": "leftRegion",
          "type": "select",
          "label": "Which shape describes the allowed regions at 9 J?",
          "options": [
            "One continuous interval through the middle",
            "Two separate intervals, one in each valley",
            "Only the single positions x=±2 m",
            "I'm not sure"
          ]
        },
        {
          "id": "maximumSpeed",
          "type": "number",
          "label": "Maximum possible speed in the starting valley (m/s)"
        },
        {
          "id": "reason",
          "type": "textarea",
          "label": "Explain the energy inequality AND why the route is or is not connected",
          "hint": "You can write 'I'm not sure' and compare your first thinking later."
        }
      ],
      "worked": [
        [
          "Choose a dimensionless coordinate",
          "Let q=x/(1 m), so U=(q²−4)² J. At q=−2 and +2 U=0; at q=0 the barrier is 16 J."
        ],
        [
          "Check allowable positions",
          "K=E−U must be nonnegative. At E=9 J, (q²−4)²≤9 means |q²−4|≤3, so 1≤q²≤7."
        ],
        [
          "Keep each connected region separate",
          "Allowed x intervals are [−√7,−1] m and [1,√7] m. Starting at +2 m, the bead can move only within the RIGHT interval; x=+1 m is a turning point and the 16 J barrier blocks travel to the other valley."
        ],
        [
          "Find peak speed where U is smallest",
          "In the right well U(+2)=0, so K_max=9 J. With m=2 kg, ½mv²=9 gives v_max=3 m/s. A position with K=0 is an allowed turning point."
        ],
        [
          "Explain why destination and path differ",
          "A low-potential left valley exists but cannot be reached along the axis from the right well with only 9 J. The whole connected route, not a promising endpoint, decides accessibility."
        ]
      ],
      "rubric": [
        "I used K=E−U≥0, rather than trusting the appearance of two low valleys.",
        "I identified two DISCONNECTED allowed intervals at 9 J and the starting right-hand region.",
        "I marked the right inner turning point at +1 m and the outer at √7 m and explained the central barrier.",
        "I located the maximum speed where U is smallest and computed 3 m/s with correct mass and units."
      ],
      "diagnoses": [
        "I assumed low-energy endpoints guarantee a connected path.",
        "I treated a turning point with K=0 as forbidden.",
        "I joined two allowed regions even though the barrier is above E.",
        "I located maximum speed at maximum U.",
        "My model was sound; I need to check the algebra.",
        "I'm not sure which step failed."
      ],
      "repairPrompt": "Rewrite the first wrong idea about E−U or connectivity. Show both allowed intervals, the starting region, a turning point, and the speed in a valley. Explain what changed.",
      "boundaryPrompt": "Keep U=(q²−4)² J and mass 2 kg, but raise the total energy to 17 J. Can this bead now pass the central hill at x=0? Find the speed at x=0 and explain why the earlier barrier restriction changed.",
      "boundaryCheck": [
        "The potential at x=0 is still 16 J, but total energy is now 17 J. The central barrier is energetically accessible.",
        "At x=0, K=17−16=1 J. With mass 2 kg, ½mv²=1 J, so v=1 m/s.",
        "Now there is a connected route across the central hill. The borderline exactly E=16 J is special: reaching the unstable peak can be asymptotic, so we chose E=17 J.",
        "The source-themed exam item WEP07-03 is separately disputed and not promoted by this authored exercise."
      ]
    },
    E02: {
      "title": "Power follows the direction of motion",
      "version": 1,
      "prediction": "If a robot moves diagonally while the motor pushes right and resistance pulls backward, does every force increase its kinetic energy? Could net power be zero even while it moves?",
      "hints": [
        "Draw right/forward axes and write the current velocity as two components. Each force contributes only along its own component of velocity.",
        "Assign signs first: rightward motor work-rate is positive here, while a backward resistance component removes energy.",
        "Compute force·velocity as F_right×v_right plus F_forward×v_forward for each force. Do not multiply whole vector magnitudes unless their directions agree."
      ],
      "diagnosisFeedback": [
        "A force's instantaneous power depends on its alignment with velocity, not just on whether it is a motor.",
        "Keep the leftward/backward resistance contributions negative; use signs in each component product.",
        "A two-dimensional dot product is a sum of signed aligned components, not force magnitude times speed magnitude.",
        "Power at an instant is dK/dt. It does not mean the same number of joules appears in every future second.",
        "Recheck the force and velocity arrows and the units N·m/s=W without replacing a valid model.",
        "Start with a two-column x and y table, draw directions, and allow yourself an 'unsure' statement."
      ],
      "fields": [
        {
          "id": "netFx",
          "type": "number",
          "label": "Net force in rightward x direction (N)"
        },
        {
          "id": "netFy",
          "type": "number",
          "label": "Net force in forward y direction (N)",
          "hint": "Backward is negative."
        },
        {
          "id": "motorPower",
          "type": "number",
          "label": "Motor's instantaneous power (W)"
        },
        {
          "id": "resistPower",
          "type": "number",
          "label": "Resistance's instantaneous power (W)",
          "hint": "It can be negative."
        },
        {
          "id": "netPower",
          "type": "number",
          "label": "Net instantaneous power (W)"
        },
        {
          "id": "model",
          "type": "select",
          "label": "Which calculation is valid for these diagonal vectors?",
          "options": [
            "Net force magnitude × total speed",
            "Signed x contributions + signed y contributions",
            "All force contributions are positive",
            "I'm not sure"
          ]
        },
        {
          "id": "energyTrend",
          "type": "select",
          "label": "What happens to kinetic energy at that moment?",
          "options": [
            "Increasing right now",
            "Decreasing right now",
            "Instantaneously constant",
            "I'm not sure"
          ]
        },
        {
          "id": "reason",
          "type": "textarea",
          "label": "Explain your force arrows, both component products, and the meaning of an instantaneous rate",
          "hint": "Why is the product of total magnitudes not always correct?"
        }
      ],
      "worked": [
        [
          "Read force and velocity components",
          "Right/forward axes: v=(3,4) m/s. Motor force=(6,0) N; resistance=(−2,−1) N; net force=(4,−1) N."
        ],
        [
          "Motor power uses aligned components",
          "P_motor=6×3+0×4=+18 W. Its direction is along the rightward component of velocity."
        ],
        [
          "Resistance removes energy along two components",
          "P_resist=(−2)×3+(−1)×4=−6−4=−10 W. The backward resistance matters, not only the force opposite the motor."
        ],
        [
          "Compute the net instantaneous kinetic-energy rate",
          "Net power=18−10=+8 W, so dK/dt=+8 J/s at that instant. It is NOT a claim about the following full second."
        ],
        [
          "Check the dot-product model",
          "Net F=(4,−1) and v=(3,4). Their dot product is 4×3−1×4=8 W. |F|×|v|=√17×5 W would be wrong because the vectors are not parallel."
        ]
      ],
      "rubric": [
        "I used velocity (3,4) m/s and net force (4,−1) N in matching axes.",
        "I computed motor power +18 W and resistance power −10 W with signed component products.",
        "I found +8 W net power and interpreted it as an instantaneous dK/dt, not a future constant rate.",
        "I explained why force magnitude times speed magnitude is not generally a correct dot product."
      ],
      "diagnoses": [
        "I treated motor power as positive regardless of velocity alignment.",
        "I made leftward/backward resistance contributions positive.",
        "I used total force magnitude × total speed instead of signed components.",
        "I treated instantaneous power as an amount guaranteed every future second.",
        "My signed model was fine; I should recheck arithmetic.",
        "I'm not sure which direction matters."
      ],
      "repairPrompt": "Redraw the right/forward arrows; write each force's two signed component products and re-evaluate the current kinetic-energy trend. Explain the first correction.",
      "boundaryPrompt": "At another instant the same net force (4 N right, 1 N backward) acts, but velocity is 1 m/s right and 4 m/s forward. Find net instantaneous power. Is the robot still moving? Can it accelerate despite zero instantaneous kinetic-energy rate?",
      "boundaryCheck": [
        "New velocity is (1,4) m/s and net force is (4,−1) N.",
        "Dot product: P_net=4×1+(−1)×4=0 W, so dK/dt=0 at THIS instant.",
        "Its speed is √(1²+4²)=√17 m/s, so it is moving. Nonzero net force means nonzero acceleration; the force is instantaneously perpendicular to velocity.",
        "Zero instantaneous power does not mean zero force or stop; it means no instantaneous change in kinetic energy."
      ]
    },
    E03: {
      "title": "Where spring contact ends and flight begins",
      "version": 1,
      "prediction": "If friction acts while a spring pushes a dart, does ALL spring energy become launch motion? Does spring force keep acting after the dart has left the platform?",
      "hints": [
        "Draw a vertical line at the spring's natural length. Identify what acts on the dart BEFORE and AFTER that line.",
        "In the contact phase use spring energy ½kx² minus friction force×contact distance. The launch kinetic energy determines horizontal speed.",
        "Once the dart is in free flight, time depends on vertical drop and gravity; horizontal range depends on launch speed × flight time."
      ],
      "diagnosisFeedback": [
        "An unattached spring stops at natural length; it cannot keep pushing or pulling the dart in the air.",
        "Subtract the contact-only friction work from initial spring energy before calculating launch kinetic energy.",
        "Spring force varies with compression; using its initial magnitude throughout the release overestimates its work.",
        "Free-flight vertical time comes from h=½gt², not t=h/g, because initial vertical speed is zero.",
        "Check units and distinguish horizontal launch speed from vertical fall speed at landing.",
        "Start by drawing two regions: contact energy and flight kinematics. 'I'm not sure' is allowed."
      ],
      "fields": [
        {
          "id": "boundary",
          "type": "select",
          "label": "Where does the spring's force stop?",
          "options": [
            "At its natural length, where dart leaves the edge",
            "Halfway through the flight",
            "At the ground",
            "I'm not sure"
          ]
        },
        {
          "id": "springEnergy",
          "type": "number",
          "label": "Starting spring energy (J)"
        },
        {
          "id": "frictionLoss",
          "type": "number",
          "label": "Energy lost to friction during spring contact (J)",
          "hint": "Give the positive energy lost; friction does negative work."
        },
        {
          "id": "launchEnergy",
          "type": "number",
          "label": "Dart kinetic energy just as contact ends (J)"
        },
        {
          "id": "launchSpeed",
          "type": "number",
          "label": "Horizontal launch speed (m/s)",
          "hint": "Approximate square roots are fine."
        },
        {
          "id": "flightTime",
          "type": "number",
          "label": "Time falling from platform to floor (s)"
        },
        {
          "id": "range",
          "type": "number",
          "label": "Horizontal landing distance (m)"
        },
        {
          "id": "reason",
          "type": "textarea",
          "label": "Explain the contact-only friction ledger and why horizontal flight has no spring force",
          "hint": "Name the boundary between models."
        }
      ],
      "worked": [
        [
          "Divide into two physical phases",
          "The spring contacts the unattached dart only until natural length at the platform edge. Friction acts over this 0.20 m contact release; neither spring nor contact friction acts in flight."
        ],
        [
          "Build the contact energy ledger",
          "Initial U_s=½×125×0.20²=2.50 J. Friction loss is 2.5×0.20=0.50 J. K_launch=2.50−0.50=2.00 J."
        ],
        [
          "Convert launch energy to horizontal speed",
          "With m=0.50 kg, ½mv_x²=2 J gives v_x²=8 and v_x=√8≈2.828 m/s."
        ],
        [
          "Free flight uses separate vertical and horizontal rules",
          "From height h=1.25 m with initial vertical speed zero and g=10, h=½gt² gives t=0.50 s. Horizontal speed stays √8 m/s in ideal flight."
        ],
        [
          "Find the range and cross-check",
          "Range=√8×0.50=√2≈1.414 m. Do not use the spring's initial force kx as constant for all 0.20 m; elastic work is the triangle area ½kx²."
        ]
      ],
      "rubric": [
        "I separated spring CONTACT (with friction) from free FLIGHT (without spring/contact friction).",
        "I correctly budgeted 2.50 J spring energy minus 0.50 J friction into 2.00 J launch kinetic energy.",
        "I obtained the horizontal launch speed √8 m/s, then vertical flight time 0.50 s.",
        "I used independent horizontal range = launch speed × flight time ≈1.414 m with correct assumptions."
      ],
      "diagnoses": [
        "I continued the spring force after contact ended.",
        "I forgot to subtract friction in the launch energy budget.",
        "I treated the initial spring force as constant throughout compression.",
        "I used h/g for flight time instead of h=½gt².",
        "My two-model reasoning was fine; I need to verify a calculation.",
        "I'm not sure when one model ends."
      ],
      "repairPrompt": "Mark spring natural length and the platform edge. Rebuild the contact energy ledger and the separate vertical-time/horizontal-distance equations; state why your first model changed.",
      "boundaryPrompt": "Remove friction only from the 0.20 m spring-contact region. The spring, dart mass and 1.25 m platform height stay the same. What is the new horizontal launch speed and range? Does the 0.50 s fall time change?",
      "boundaryCheck": [
        "Without friction, all 2.50 J spring energy becomes horizontal launch kinetic energy.",
        "½×0.50×v²=2.50 J gives v²=10 and v=√10≈3.162 m/s.",
        "The fall time is still √(2×1.25/10)=0.50 s because the platform height and zero initial vertical speed are unchanged.",
        "The range increases to √10×0.50≈1.581 m. Only the launch speed and horizontal range change; spring/contact friction never acts during flight."
      ]
    },
    E04: {
      "title": "Which energy fraction survives each bounce?",
      "version": 1,
      "prediction": "A first impact retains 75% of energy, then later impacts retain 50%. Does rebound speed follow the same fraction as energy? Should the 75% rule repeat?",
      "hints": [
        "Energy retained after collision determines the NEXT maximum height. A percentage of energy does not equal the same percentage of speed.",
        "Build a small table: bounce 1 has its own fraction, bounce 2 and later share a new repeating fraction.",
        "Count the first DROP once and then both UP and DOWN legs of every rebound. The infinite rebound heights use the later fraction as their ratio."
      ],
      "diagnosisFeedback": [
        "The first floor impact uses 75% retention; the 50% retention rule applies only to later impacts.",
        "Rebound height is proportional to energy retained; rebound speed is proportional to the square root of energy retained.",
        "Keep a separate first term and later ratio when summing a geometric sequence.",
        "Count the first 2 m drop once and each complete rebound distance twice, upward then downward.",
        "Recheck the arithmetic in the height table and the convergence of the geometric series.",
        "Start by writing one impact per table row; you can leave an unknown and explain the model."
      ],
      "fields": [
        {
          "id": "firstHeight",
          "type": "number",
          "label": "First rebound maximum height (m)"
        },
        {
          "id": "secondHeight",
          "type": "number",
          "label": "Second rebound maximum height (m)"
        },
        {
          "id": "thirdHeight",
          "type": "number",
          "label": "Third rebound maximum height (m)"
        },
        {
          "id": "firstRetention",
          "type": "select",
          "label": "Which energy retention applies to the FIRST impact?",
          "options": [
            "75%",
            "50%",
            "25%",
            "I'm not sure"
          ]
        },
        {
          "id": "laterRetention",
          "type": "select",
          "label": "Which energy retention repeats for later impacts?",
          "options": [
            "75%",
            "50%",
            "25%",
            "I'm not sure"
          ]
        },
        {
          "id": "distanceRule",
          "type": "select",
          "label": "How do you count ideal total travel?",
          "options": [
            "Original drop + twice the sum of rebound heights",
            "Original drop + sum of rebound heights",
            "Twice the original drop only",
            "I'm not sure"
          ]
        },
        {
          "id": "totalTravel",
          "type": "number",
          "label": "Total ideal travel including the original drop (m)"
        },
        {
          "id": "firstSpeedRatio",
          "type": "number",
          "label": "First rebound SPEED divided by pre-impact speed",
          "hint": "Approximately; square-root relation."
        },
        {
          "id": "reason",
          "type": "textarea",
          "label": "Explain why the first term and later repeating ratio differ and how you counted both travel directions",
          "hint": "Say 'I'm not sure' if the sequence rule is new to you."
        }
      ],
      "worked": [
        [
          "Treat the first impact separately",
          "The ball is dropped from 2 m. It retains 75% of impact energy, so its FIRST rebound height is h₁=0.75×2=1.50 m."
        ],
        [
          "Later impacts follow a different rule",
          "From bounce 2 onward, energy retention is 50%. Rebound heights are h₂=0.5×1.50=0.75 m, h₃=0.5×0.75=0.375 m and so on."
        ],
        [
          "Distance includes two legs per rebound",
          "The starting 2 m downward drop occurs once. Each complete bounce adds its upward height AND the following downward height: D=2+2(h₁+h₂+h₃+⋯)."
        ],
        [
          "Use the correct geometric first term and ratio",
          "The rebound heights have first term 1.50 m and repeating ratio 0.50. Sum=1.50/(1−0.50)=3.00 m. Total ideal vertical distance D=2+2×3=8.00 m."
        ],
        [
          "Do not confuse speed and energy fractions",
          "Speed immediately after impact divided by pre-impact speed is √0.75≈0.866, not 0.75. Speed squares to give kinetic energy."
        ]
      ],
      "rubric": [
        "I used 75% energy retention ONLY at the first impact, obtaining h₁=1.50 m.",
        "I switched to 50% for all later impacts, giving h₂=0.75 m and h₃=0.375 m.",
        "I counted the 2 m original drop once plus UP and DOWN rebound legs, so total travel is 8 m.",
        "I explained the sqrt(0.75) speed fraction rather than treating energy and speed percentages as identical."
      ],
      "diagnoses": [
        "I applied the 75% rule to every impact.",
        "I treated an energy fraction as the same speed fraction.",
        "I used the wrong first term or repeating ratio in the series.",
        "I counted only up or down, or omitted the original drop.",
        "The model was right but I should check the geometric sum.",
        "I'm not sure what repeats after the first impact."
      ],
      "repairPrompt": "Make a new bounce table with FIRST retention 75% then LATER retention 50%. Write the two-direction travel formula and explain why the old ratio was wrong.",
      "boundaryPrompt": "Now every single impact retains 75% of energy, starting from the same 2 m drop. Find the ideal total vertical travel distance, counting both ascent and descent. Why is it larger than the mixed-rule case?",
      "boundaryCheck": [
        "Every rebound height now has the SAME ratio 0.75, starting with 1.50 m.",
        "The geometric rebound-height sum is 1.50/(1−0.75)=6 m.",
        "Total ideal distance = original 2 m drop + 2×6 m = 14 m.",
        "This ideal infinite-bounce enrichment ignores eventual real-world cessation; use only under the given ideal assumptions."
      ]
    },
    E05: {
      "title": "Area gives potential; local force makes the circle",
      "version": 1,
      "prediction": "A central force points inward while a spacecraft moves around a circle. Does the inward force continuously add energy during a circular orbit? What should a positive inward-force-magnitude graph say about U as radius grows?",
      "hints": [
        "Label the force graph vertical axis as POSITIVE inward-force magnitude f(r). Outward radial coordinate is positive, so radial force is −f(r).",
        "For potential at 3 m, consider the entire radius from 0, not only the last segment; a piecewise graph needs separate area pieces.",
        "For orbital speed, do not use area as the local force. Read the graph height at the orbit and use inward mv²/r."
      ],
      "diagnosisFeedback": [
        "A positive inward-force magnitude graph has dU/dr=+f(r); the signed radial force is negative.",
        "Potential at 3 m needs the rectangle 0–2 m PLUS the trapezoid 2–3 m from the chosen U(0) reference.",
        "Distinguish graph area for potential DIFFERENCE from graph height for local circular force.",
        "For a circular orbit, inward acceleration magnitude is v²/r; don't use mv/r or treat radius as arc length.",
        "Check arithmetic in trapezoid and kinetic-energy formula, including signs and units.",
        "Sketch inward force and tangent velocity separately; a radial force does no work on steady circular motion."
      ],
      "fields": [
        {
          "id": "firstArea",
          "type": "number",
          "label": "Potential rise from 0 to 2 m (J)"
        },
        {
          "id": "secondArea",
          "type": "number",
          "label": "Additional potential rise from 2 to 3 m (J)"
        },
        {
          "id": "potential",
          "type": "number",
          "label": "Potential energy U at r=3 m (J)"
        },
        {
          "id": "forceAt3",
          "type": "number",
          "label": "Inward force magnitude at r=3 m (N)"
        },
        {
          "id": "speed",
          "type": "number",
          "label": "Required circular speed at 3 m (m/s)"
        },
        {
          "id": "kinetic",
          "type": "number",
          "label": "Circular kinetic energy at 3 m (J)"
        },
        {
          "id": "total",
          "type": "number",
          "label": "Total mechanical energy for this 3 m orbit (J)"
        },
        {
          "id": "motion",
          "type": "select",
          "label": "What work does the inward central force do while radius stays 3 m?",
          "options": [
            "Zero, because force is perpendicular to velocity",
            "Positive equal to graph area",
            "Negative equal to graph area",
            "I'm not sure"
          ]
        },
        {
          "id": "reason",
          "type": "textarea",
          "label": "Explain why area and local force are different graph operations, with the force/velocity arrows",
          "hint": "Name the graph's vertical axis and the radial reference U(0)=0."
        }
      ],
      "worked": [
        [
          "Choose radial sign and reference",
          "Positive r is OUTWARD; inward force magnitude f(r)>0 means signed radial force F_r=−f(r)=−dU/dr. With U(0)=0, increasing r raises U by the area under positive f(r)."
        ],
        [
          "Find potential using both graph regions",
          "From 0–2 m, 4 N×2 m=8 J. From 2–3 m, force magnitude rises 4 to 6 N, a trapezoid (4+6)/2×1=5 J. Thus U(3)=8+5=13 J."
        ],
        [
          "Use LOCAL force, not area, for circular speed",
          "At radius 3 m the inward force magnitude is 6 N. With mass 2 kg, mv²/r=6 gives v²=6×3/2=9 and v=3 m/s."
        ],
        [
          "Compute kinetic and total energy",
          "K=½×2×3²=9 J; total E=U+K=13+9=22 J for this chosen 3 m circular orbit."
        ],
        [
          "Check zero work around the circle",
          "The steady inward force is perpendicular to tangential velocity; it does no work during travel at fixed radius. The positive area concerns hypothetical RADIAL displacement between radii, not distance traveled along the circle."
        ]
      ],
      "rubric": [
        "I separated a positive inward-force-magnitude graph from signed radial force and used U(0)=0.",
        "I added the full 8 J rectangle and 5 J trapezoid to obtain U(3)=13 J.",
        "I used the LOCAL 6 N at r=3 m in mv²/r, obtaining v=3 m/s and K=9 J.",
        "I found E=22 J and explained why the radial force does zero work while the object travels around the circle."
      ],
      "diagnoses": [
        "I treated inward force magnitude as negative potential rise.",
        "I used only the last graph segment and forgot the first rectangle.",
        "I confused local force with area under force-versus-radius graph.",
        "I used mv/r rather than mv²/r or the wrong radius.",
        "My two-operation model was right; I need to recheck numbers.",
        "I'm not sure why force is perpendicular to orbital motion."
      ],
      "repairPrompt": "Draw a positive outward radius axis, mark inward force and tangent velocity, then rebuild both graph-area contributions AND local circular-force calculation. Explain the first corrected inference.",
      "boundaryPrompt": "Consider a SEPARATE steady circular orbit at radius 4 m under the same force law and 2 kg mass. Find U(4), local inward force, required speed, kinetic energy and E. Why must this not be described as a free conservative move from the 3 m orbit to 4 m?",
      "boundaryCheck": [
        "U(4) = (4 N×2 m) + ((4+8)/2×2 m) = 8+12=20 J.",
        "At 4 m the force magnitude is 8 N, so mv²/r=8 gives v²=16 and v=4 m/s.",
        "K=½×2×4²=16 J; total E=U+K=20+16=36 J.",
        "These are different steady circular ORBITS with different energies. A conservative inward force does zero work while radius stays constant, and the spacecraft cannot spontaneously change circular orbit energies without a separate process."
      ]
    }
  };

  function initState(lesson) {
    return {schema:1,lesson,stage:0,prediction:null,predictionDraft:"",draft:null,first:null,hintsUsed:0,reconstruction:null,diagnosis:null,repair:null,boundary:null};
  }
  function storageKey(lesson) { return "g9:wpe:d3d4:self-tutor:v1:"+lesson; }
  function load(lesson) {
    try {
      const value = JSON.parse(localStorage.getItem(storageKey(lesson)));
      if(value && value.schema===1 && value.lesson===lesson &&
         Number.isInteger(value.stage) && value.stage>=0 && value.stage<=5 &&
         (value.stage<2 || (value.first && typeof value.first.reason==="string")))
        return value;
    } catch (_) { /* Private mode and malformed storage are both supported. */ }
    return initState(lesson);
  }
  function persist(lesson, state) {
    try { localStorage.setItem(storageKey(lesson), JSON.stringify(state)); return true; }
    catch (_) { return false; }
  }
  function erase(lesson) { try { localStorage.removeItem(storageKey(lesson)); } catch (_) {} }
  function el(tag, className, text) {
    const node = document.createElement(tag);
    if(className) node.className = className;
    if(text!==undefined) node.textContent = String(text);
    return node;
  }
  function addText(parent, tag, className, text) { const n=el(tag,className,text);parent.append(n);return n; }
  function addButton(parent, action, label, variant) {
    const button=el("button",variant||"primary",label);
    button.type="button"; button.dataset.action=action;parent.append(button);return button;
  }
  function stageHeader(root, state) {
    const ol=el("ol","step-list");
    ol.setAttribute("aria-label","Learning steps");
    stages.forEach((name,i)=>{
      const li=el("li",i===state.stage?"current":i<state.stage?"done":"upcoming",(i+1)+". "+name);
      if(i===state.stage)li.setAttribute("aria-current","step");
      ol.append(li);
    });
    root.append(ol);
  }
  function note(root, text, style) {addText(root,"p",style||"step-notice",text);}
  function actions(root) {return root.appendChild(el("div","stage-actions"));}
  function labelFor(root,control,name) {
    const label=el("label",null,name);label.htmlFor=control.id;root.append(label);return label;
  }
  function textArea(root,id,label,hint,defaultValue) {
    const control=el("textarea");
    control.id=id;control.dataset.input=id;control.rows=4;
    labelFor(root,control,label);
    if(hint) note(root,hint,"field-help");
    control.value=defaultValue||"";
    root.append(control);
    return control;
  }
  function select(root,id,label,options) {
    const control=el("select");control.id=id;control.dataset.input=id;
    labelFor(root,control,label);
    let opt=el("option",null,"Choose, or select 'I'm not sure'");
    opt.value="";control.append(opt);
    options.forEach(option=>{opt=el("option",null,option);opt.value=option;control.append(opt);});
    root.append(control);
  }
  function number(root,id,label,hint) {
    const control=el("input");control.type="number";control.step="any";control.inputMode="decimal";control.id=id;control.dataset.input=id;
    labelFor(root,control,label);
    if(hint)note(root,hint,"field-help");
    root.append(control);
  }
  function snapshot(root,state,config) {
    const box=el("section","snapshot");
    addText(box,"strong",null,"Your saved first try — unchanged");
    const dl=el("dl");
    addText(dl,"dt",null,"Prediction");
    addText(dl,"dd",null,state.prediction||"(No prediction written)");
    config.fields.forEach(field=>{
      addText(dl,"dt",null,field.label);
      addText(dl,"dd",null,(state.first && state.first[field.id]) || "(Not sure / blank)");
    });
    box.append(dl);root.append(box);
  }
  function workedList(root, rows, heading) {
    const box=el("section","worked");
    addText(box,"h5",null,heading);
    const list=el("ol");
    rows.forEach(row=>{
      const li=el("li");
      addText(li,"strong",null,row[0]+": ");
      li.append(document.createTextNode(row[1]));
      list.append(li);
    });
    box.append(list);root.append(box);
  }
  function rubricBlock(root,config,checkable,prior) {
    const box=el("section","rubric");
    addText(box,"h5",null,"Check your reasoning, not just the final number");
    const ul=el("ul");
    config.rubric.forEach((item,i)=>{
      const li=el("li");
      if(checkable) {
        const input=el("input");input.type="checkbox";input.value=String(i);input.dataset.rubric=String(i);
        if(prior && prior.includes(i))input.checked=true;
        const label=el("label");label.append(input,document.createTextNode(" "+item));li.append(label);
      } else li.textContent=item;
      ul.append(li);
    });
    box.append(ul);root.append(box);
  }
  function formValues(root) {
    const values={};
    root.querySelectorAll("[data-input]").forEach(field=>{values[field.dataset.input]=field.value.trim();});
    return values;
  }
  function render(lesson, focus) {
    const config=lessons[lesson], state=states[lesson];
    const root=document.querySelector('[data-stage-root="'+lesson+'"]');
    root.replaceChildren();
    stageHeader(root,state);
    const card=el("section","stage-card");root.append(card);
    const stage=state.stage;
    const top=addText(card,"h4",null,(stage+1)+". "+stages[stage]);
    top.tabIndex=-1;
    if(stage===0) {
      note(card,"Make a prediction first. You don't need to be correct.", "stage-desc");
      textArea(card,"prediction-"+lesson,"What do you think will happen?",config.prediction,state.predictionDraft||state.prediction||"");
      addButton(actions(card),"save-prediction","Keep my prediction and try the problem");
    } else if(stage===1) {
      note(card,"Try the new problem independently. Work in any order and write how you decided. It's fine to say 'I'm not sure'.", "stage-desc");
      note(card,"Prediction saved: "+(state.prediction||"(not sure)"),"step-note");
      const form=el("div","attempt-fields");card.append(form);
      config.fields.forEach(field=>{
        const id=lesson+"-"+field.id;
        if(field.type==="select")select(form,id,field.label,field.options);
        if(field.type==="number")number(form,id,field.label,field.hint);
        if(field.type==="textarea")textArea(form,id,field.label,field.hint,"");
        const input=form.querySelector("#"+id);
        input.dataset.input=field.id;
        if(state.draft && typeof state.draft[field.id]==="string")input.value=state.draft[field.id];
      });
      note(card,"Your unfinished answers are saved on this browser as you type. You can come back to this skill later.","draft-note");
      const hints=config.hints||[];
      if(hints.length){
      const help=el("section","progressive-hints");help.dataset.hintPanel="true";
      addText(help,"strong",null,"Optional thinking hints — no worked answer");
      hints.slice(0,state.hintsUsed||0).forEach((hint,i)=>note(help,"Hint "+(i+1)+": "+hint,"hint-text"));
      card.append(help);
      const hintButton=addButton(actions(card),"next-hint","Show next hint ("+(state.hintsUsed||0)+"/"+hints.length+")","secondary");
      if((state.hintsUsed||0)>=hints.length)hintButton.disabled=true;
      }
      note(card,"Your answers will be frozen as your first attempt. A separate repair comes later.","stage-help");
      addButton(actions(card),"lock-attempt","Save my first attempt and reconstruct");
    } else if(stage===2) {
      note(card,"Now the worked steps are available. Compare them with your original model; we don't grade your writing.", "stage-desc");
      snapshot(card,state,config);
      workedList(card,config.worked,"Worked reconstruction");
      rubricBlock(card,config,true,state.reconstruction||[]);
      addButton(actions(card),"save-reconstruction","I compared the steps → Diagnose");
    } else if(stage===3) {
      note(card,"Find the first difference between your model and the worked steps, even if your number happened to match.", "stage-desc");
      snapshot(card,state,config);
      select(card,lesson+"-diagnosis","Which issue did you find first?",config.diagnoses);
      const field=card.querySelector("#"+lesson+"-diagnosis");field.dataset.input="diagnosis";
      textArea(card,lesson+"-diagnosisWhy","Why did you choose that issue?","If you got it right, explain what you double-checked.","");
      addButton(actions(card),"save-diagnosis","Keep my diagnosis → Repair");
    } else if(stage===4) {
      note(card,"Make a new version of the reasoning. Your original first attempt stays saved above.", "stage-desc");
      snapshot(card,state,config);
      const issueIndex=config.diagnoses.indexOf(state.diagnosis?.issue);
      if(issueIndex>=0 && config.diagnosisFeedback?.[issueIndex])note(card,"Try this repair: "+config.diagnosisFeedback[issueIndex],"diagnostic-tip");
      textArea(card,lesson+"-repair","My repaired calculation and explanation",config.repairPrompt,"");
      addButton(actions(card),"save-repair","Keep my repair → Boundary test");
    } else if(stage===5) {
      if(state.boundary===null) {
        note(card,"A small change to the physics can change the conclusion. Try this one yourself.", "stage-desc");
        addText(card,"p","reflection",config.boundaryPrompt);
        textArea(card,lesson+"-boundary","My answer to the changed-condition test","It's okay to say what you are unsure about.","");
        addButton(actions(card),"save-boundary","Save my boundary test and compare");
      } else {
        addText(card,"p","response-done","Boundary test completed. You've practised all six thinking stages!");
        const answer=el("section","snapshot");
        addText(answer,"strong",null,"Your boundary-test response");
        addText(answer,"p",null,state.boundary);
        card.append(answer);
        workedList(card,config.boundaryCheck.map((v,i)=>["Step "+(i+1),v]),"Compare the changed-condition reasoning");
        note(card,"These are self-check criteria, not a score. The stored first try and later repair are distinct.","stage-help");
        addButton(actions(card),"review-history","View original attempt and repair","secondary");
        if(sourceRoute && sourceRoute.lesson===lesson){
          const a=el("a","return-original","Return to "+sourceRoute.id+" and try the original question independently");
          a.href=sourceRoute.href;card.append(a);
        }
      }
    }
    // Once the first model is locked, the full reasoning stays available for
    // self-diagnosis and repair without exposing the boundary answer in advance.
    if(stage===3 || stage===4 || (stage===5 && state.boundary===null)){
      const ref=el("details","review-model");
      addText(ref,"summary",null,"Review the worked steps while thinking");
      workedList(ref,config.worked,"Worked model — open when you need it");
      card.append(ref);
    }
    const footer=actions(root);
    addButton(footer,"reset","Start this skill again (clears saved work)","danger");
    const msg=addText(root,"p","step-notice","");
    msg.setAttribute("aria-live","polite");msg.dataset.notice="true";
    if(!storageWorks)msg.textContent="This browser did not allow local saving. You can still work through this page, but your progress may disappear on reload.";
    if(focus)top.focus({preventScroll:true});
    updateProgress();
  }
  function updateProgress() {
    let count=0;
    Object.keys(lessons).forEach(lesson=>{ if(states[lesson].boundary!==null)count++; });
    const label=document.getElementById("overall-count");
    const meter=document.getElementById("overall-meter");
    if(label)label.textContent=count+" of "+Object.keys(lessons).length+" challenges completed";
    if(meter){meter.max=Object.keys(lessons).length;meter.value=count;}
  }
  function warn(root, text) {
    const notice=root.querySelector("[data-notice]");
    if(notice)notice.textContent=text;
  }
  function update(lesson, event) {
    const root=document.querySelector('[data-stage-root="'+lesson+'"]');
    const action=event.target.closest("button[data-action]");
    if(!action || !root.contains(action))return;
    const kind=action.dataset.action;
    let state=states[lesson];
    if(kind==="next-hint" && state.stage===1 && !state.first){
      const used=Math.min(configHintCount(lesson),state.hintsUsed||0);
      if(used>=configHintCount(lesson))return;
      state.hintsUsed=used+1;
      const panel=root.querySelector("[data-hint-panel]");
      note(panel,"Hint "+state.hintsUsed+": "+lessons[lesson].hints[used],"hint-text");
      action.textContent="Show next hint ("+state.hintsUsed+"/"+configHintCount(lesson)+")";
      if(state.hintsUsed>=configHintCount(lesson))action.disabled=true;
      if(!persist(lesson,state))storageWorks=false;
      return;
    }
    if(kind==="reset") {
      if(!window.confirm("Clear this skill's saved prediction, first try and later repairs?"))return;
      erase(lesson);states[lesson]=initState(lesson);render(lesson,true);return;
    }
    if(kind==="review-history") {
      const old=root.querySelector(".history");
      if(old){old.remove();return;}
      const panel=el("section","history");
      snapshot(panel,state,lessons[lesson]);
      const repair=el("section","snapshot");
      addText(repair,"strong",null,"Your separate repair");
      addText(repair,"p",null,state.repair||"(no repair written)");
      panel.append(repair);
      action.parentNode.before(panel);return;
    }
    if(kind==="save-prediction" && state.stage===0) {
      const prediction=root.querySelector("textarea").value.trim();
      if(!prediction){warn(root,"Write a prediction or 'I'm not sure' so you can compare it later.");return;}
      state.prediction=prediction;state.stage=1;state.predictionDraft="";
    } else if(kind==="lock-attempt" && state.stage===1 && !state.first) {
      const values=formValues(root);
      if(!values.reason){
        warn(root,"Write a few words explaining your thinking—or 'I'm not sure'. Then you can see the worked steps.");
        root.querySelector('[data-input="reason"]').focus();
        return;
      }
      state.first=values;state.stage=2;state.draft=null;
    } else if(kind==="save-reconstruction" && state.stage===2) {
      state.reconstruction=[...root.querySelectorAll("[data-rubric]:checked")].map(x=>Number(x.value));
      state.stage=3;
    } else if(kind==="save-diagnosis" && state.stage===3) {
      const data=formValues(root);
      state.diagnosis={issue:data.diagnosis||"I'm not sure what went wrong yet.",why:data[lesson+"-diagnosisWhy"]||""};
      state.stage=4;
    } else if(kind==="save-repair" && state.stage===4) {
      const data=formValues(root);
      const repaired=data[lesson+"-repair"]||"";
      if(!repaired){warn(root,"Write what you changed—or that you are still unsure.");return;}
      state.repair=repaired;state.stage=5;
    } else if(kind==="save-boundary" && state.stage===5 && state.boundary===null) {
      const answer=root.querySelector("textarea").value.trim();
      if(!answer){warn(root,"Write your idea or 'I'm not sure' before opening the boundary check.");return;}
      state.boundary=answer;
    } else return;
    const saved=persist(lesson,state);
    if(!saved)storageWorks=false;
    render(lesson,true);
  }
  // Drafts live only in this browser. Committed first responses remain separate
  // and cannot be replaced by editing a later repair.
  function saveUnfinishedInput(lesson,event){
    const state=states[lesson];
    if(state.stage===0 && event.target.matches("textarea")){
      state.predictionDraft=event.target.value;
    }else if(state.stage===1 && !state.first && event.target.matches("[data-input]")){
      const root=document.querySelector('[data-stage-root="'+lesson+'"]');
      state.draft=formValues(root);
    }else return;
    if(!persist(lesson,state))storageWorks=false;
  }
  const configHintCount=lesson=>(lessons[lesson].hints||[]).length;
  let sourceRoute=null;
  async function bindSourceJourney(){
    const sourceId=new URLSearchParams(location.search).get("question");
    const lesson=location.hash.replace(/^#/,"");
    if(!sourceId||!/^[-A-Za-z0-9]{2,64}$/.test(sourceId)||!Object.prototype.hasOwnProperty.call(lessons,lesson))return;
    try{
      const response=await fetch("reasoning-paths.review.json");
      if(!response.ok)return;
      const d=await response.json();
      if(d.schema!=="wpe-reasoning-route-preview/v1"||!Array.isArray(d.constructions))return;
      const row=d.constructions.find(r=>r.id==="WPE-"+lesson && r.proposed_source_ids?.some(q=>q.id===sourceId && q.reader_present));
      if(!row)return;
      const href="../../preview/question-status.html?question="+encodeURIComponent(sourceId);
      sourceRoute={id:sourceId,lesson,href};
      const banner=document.getElementById("source-journey");
      document.getElementById("source-journey-title").textContent="Your original question: "+sourceId;
      document.getElementById("source-journey-message").textContent=sourceId==="EX-M79"
        ?"This lesson investigates constant power as a comparison. The original gives a speed–distance relationship: decide its own physical model when you return."
        :"Learn the method through a different situation, try the challenge, then return to your original question.";
      const link=document.getElementById("source-journey-return");link.href=href;link.textContent="Return to "+sourceId+" without showing its answer";
      banner.hidden=false;
      const footer=document.querySelector("#"+lesson+" .unit-next");
      if(footer){const a=el("a","return-original","↩ Solve "+sourceId+" yourself");a.href=href;footer.append(a);}
      const state=states[lesson];
      if(state.boundary!==null)render(lesson,false);
    }catch(_){/* No invented return link if the source manifest is unavailable. */}
  }
  let storageWorks=true;
  const states={};
  // Read every topic state before the first render updates the shared counter.
  Object.keys(lessons).forEach(lesson=>{states[lesson]=load(lesson);});
  Object.keys(lessons).forEach(lesson=>{
    const root=document.querySelector('[data-stage-root="'+lesson+'"]');
    if(root){root.addEventListener("click",event=>update(lesson,event));root.addEventListener("input",event=>saveUnfinishedInput(lesson,event));root.addEventListener("change",event=>saveUnfinishedInput(lesson,event));render(lesson,false);}
  });
  bindSourceJourney();
})();