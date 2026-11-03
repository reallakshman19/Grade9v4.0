/* WPE C01–C04 interactive student practice. Client-side only: NOT secured answers,
 * not authenticated learner evidence, not academic Core1A/B acceptance.
 * Source author packs: WPE-C01 through C04 (multi-force, spring, power, hanging rope).
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

  };

  function initState(lesson) {
    return {schema:1,lesson,stage:0,prediction:null,first:null,reconstruction:null,diagnosis:null,repair:null,boundary:null};
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
      textArea(card,"prediction-"+lesson,"What do you think will happen?",config.prediction,state.prediction||"");
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
      });
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
      }
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
      state.prediction=prediction;state.stage=1;
    } else if(kind==="lock-attempt" && state.stage===1 && !state.first) {
      const values=formValues(root);
      if(!values.reason){
        warn(root,"Write a few words explaining your thinking—or 'I'm not sure'. Then you can see the worked steps.");
        root.querySelector('[data-input="reason"]').focus();
        return;
      }
      state.first=values;state.stage=2;
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
  let storageWorks=true;
  const states={};
  // Read every topic state before the first render updates the shared counter.
  Object.keys(lessons).forEach(lesson=>{states[lesson]=load(lesson);});
  Object.keys(lessons).forEach(lesson=>{
    const root=document.querySelector('[data-stage-root="'+lesson+'"]');
    if(root){root.addEventListener("click",event=>update(lesson,event));render(lesson,false);}
  });
})();