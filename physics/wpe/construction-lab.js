/* Two child-facing WPE six-stage journeys. Browser-local work is NOT independent assessment evidence. */
(()=>{"use strict";
const STEPS=["Predict","Attempt","Reconstruct","Diagnose","Repair","Boundary test"];
const CONFIG={
 C01:{
  title:"Multi-force work–energy",
  prediction:"Before any maths, which forces help the scooter move uphill, which oppose it, and which do no work? Predict whether it reaches the top.",
  fields:[
   ["motor","Motor work (J)"],
   ["friction","Friction work (J)"],
   ["gravity","Gravity work (J)"],
   ["normal","Normal force work (J)"],
   ["net","Total / net work (J)"],
   ["speed","Speed at the top (m/s)"]
  ],
  attempt:"Explain how you chose your signs and why you used the total work, not just one force.",
  hints:[
   "Compare each force with the uphill displacement. The floor's normal force points across, not along, the route.",
   "Gravity depends on height gained: its work is negative when the scooter climbs. Add all four force-work entries before finding final kinetic energy."
  ],
  diagnose:["I left out one of the forces.","I gave a work term the wrong sign.","I treated one force's work as net work.","My reasoning already matches; I want to check it carefully."],
  boundary:"Now the motor pushes with 10 N rather than 15 N. All other values stay the same. Can a scooter starting from rest reach the top? Explain using a revised energy ledger."
 },
 C02:{
  title:"Spring contact and energy transfer",
  prediction:"Predict where the unattached spring stops pushing. Will the cart still have the same speed after crossing the rough strip? Why?",
  fields:[
   ["springEnergy","Starting spring energy (J)"],
   ["releaseEnergy","Kinetic energy at spring release (J)"],
   ["releaseSpeed","Speed at spring release (m/s)"],
   ["friction","Friction work on the rough strip (J)"],
   ["finishEnergy","Kinetic energy at the far end (J)"],
   ["finishSpeed","Speed at the far end (m/s)"]
  ],
  attempt:"Explain where the contact phase ends, where friction begins, and how the two equations connect.",
  hints:[
   "The cart is not attached to the spring. Divide the trip at the spring's natural length; after that point it cannot pull or push the cart.",
   "The launch area is smooth. Only the rough strip removes energy. Pass the release kinetic energy into the next section, then subtract friction work."
  ],
  diagnose:["I continued spring work onto the rough strip.","I applied rough-strip friction during spring contact.","I forgot to carry the release kinetic energy into the second region.","My two-region model already matches; I want to check it carefully."],
  boundary:"Change only the rough strip from 0.50 m to 1.00 m. Does the cart arrive at the far end with nonzero speed? Explain the stopping boundary using energy."
 }
};
const CLS="g9:wpe:six-stage-lab:v1:";
const by=(node,selector)=>node.querySelector(selector);
const make=(tag,cl,text)=>{const node=document.createElement(tag);if(cl)node.className=cl;if(text!==undefined)node.textContent=text;return node;};
const btn=(label,handler,primary=false)=>{const b=make("button",primary?"lab-primary":"",label);b.type="button";b.addEventListener("click",handler);return b;};
const para=(target,text)=>target.append(make("p","",text));
const emptyState=()=>({schema:1,step:0,prediction:"",attempt:null,hints:0,reconstructionViewed:false,diagnosis:null,repair:null,boundary:null});
const load=(key)=>{try{const data=JSON.parse(localStorage.getItem(key));if(data&&data.schema===1&&Number.isInteger(data.step)&&data.step>=0&&data.step<=6&&
(data.step<1||typeof data.prediction==="string"&&data.prediction.trim())&&
(data.step<2||data.attempt&&typeof data.attempt==="object"&&typeof data.attempt.explanation==="string")){
 return data;}}catch(e){}return emptyState();};
const save=(key,state)=>{try{localStorage.setItem(key,JSON.stringify(state));return true;}catch(e){return false;}};
const clear=(key)=>{try{localStorage.removeItem(key);}catch(e){}};
let postAttemptPromise=null;
const getPostAttempt=()=>{if(!postAttemptPromise){
 postAttemptPromise=fetch("construction-lab-answers.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw new Error("Worked check unavailable ("+r.status+")");return r.json();}).then(j=>{if(j.schema!=="wpe-construction-lab-post-attempt/v1"||!j.C01||!j.C02)throw new Error("Worked-check format is invalid");return j;}).catch(e=>{postAttemptPromise=null;throw e;});
}return postAttemptPromise;};
const instances=[];
function updateProgress(){
 const done=instances.filter(x=>x.getState().step===6).length;
 const count=document.querySelector("#lab-progress-count");
 if(count)count.textContent=done+" of 2 reflection journeys completed";
 const bar=document.querySelector("#lab-progress-meter");if(bar)bar.value=done;
}
function attach(card,code){
 const cfg=CONFIG[code];if(!cfg)return;
 const key=CLS+code;
 let state=load(key),resetArmed=false,renderSerial=0;
 const stage=by(card,".lab-stage"),status=by(card,".lab-status"),reset=by(card,"[data-lab-reset]");
 const announce=(message,error=false)=>{status.textContent=message;status.classList.toggle("lab-error",error);};
 const persist=()=>{const ok=save(key,state);if(!ok)announce("Browser storage is unavailable. Your work can continue here but may not survive a reload.",true);updateProgress();};
 const actions=(target)=>{const bar=make("div","lab-actions");target.append(bar);return bar;};
 const field=(parent,name,label,multiline,value="")=>{
  const wrap=make("div","lab-field"),id="lab-"+code+"-"+name,l=make("label","",label);
  l.htmlFor=id;const control=make(multiline?"textarea":"input");control.id=id;control.dataset.field=name;
  if(!multiline)control.type="text";else control.rows=4;
  control.value=value;control.autocomplete="off";wrap.append(l,control);parent.append(wrap);return control;
 };
 const stageTitle=(target,title,description)=>{
  target.append(make("h4","",title));para(target,description);
 };
 const saveText=(node,message)=>{const value=node.value.trim();if(!value){announce(message,true);node.focus();return null;}return value.slice(0,3000);};
 const advance=(next)=>{state.step=next;persist();render();};
 const showOriginal=(target)=>{
  if(state.step<2||!state.attempt)return;
  const d=make("details","lab-first"),sum=make("summary","", "My locked first attempt (unchanged)");d.append(sum);
  const dl=make("dl");
  for(const [name,label] of cfg.fields){
   dl.append(make("dt","",label),make("dd","",String(state.attempt.values?.[name]??"")));
  }
  dl.append(make("dt","","My first explanation"),make("dd","",state.attempt.explanation));
  d.append(dl);target.append(d);
 };
 const appendReference=(target,lines,heading)=>{
  const panel=make("section","lab-reference"),h=make("h5","",heading);panel.append(h);
  const ol=make("ol");
  for(const line of lines){ol.append(make("li","",line));}
  panel.append(ol);target.append(panel);
 };
 const renderReference=async(target,kind,ready)=>{
  const serial=renderSerial;
  const note=make("p","","Loading the post-attempt worked model…");target.append(note);
  try{
   const doc=await getPostAttempt();
   if(serial!==renderSerial||!target.isConnected)return;
   note.remove();
   const record=doc[code];const steps=kind==="boundary"?record.boundary:record.reconstruction;
   appendReference(target,steps,kind==="boundary"?"Changed-condition model":"Worked reconstruction");
   if(kind!=="boundary")appendReference(target,record.criteria,"Check my own explanation");
   if(ready)ready();
  }catch(e){
   if(serial!==renderSerial||!target.isConnected)return;
   note.textContent="The worked model could not load. Your saved first attempt is still here.";
   note.classList.add("lab-error");
   target.append(btn("Retry the worked model",()=>render(),false));
   announce("Could not retrieve the worked check. Try again.",true);
  }
 };
 const render=()=>{
  ++renderSerial;resetArmed=false;stage.replaceChildren();
  const steps=make("ol","lab-steps");
  for(let i=0;i<STEPS.length;i++){
   const li=make("li",i<state.step?"is-done":"",String(i+1)+". "+STEPS[i]);
   if(i===state.step&&i<6)li.setAttribute("aria-current","step");
   if(state.step===6)li.classList.add("is-done");
   steps.append(li);
  }
  stage.append(steps);
  if(state.step===0){
   stageTitle(stage,"1 · Predict",cfg.prediction);
   const input=field(stage,"prediction","My prediction (in my own words)",true,state.prediction);
   const bar=actions(stage);bar.append(btn("Save prediction → Try the challenge",()=>{
    const answer=saveText(input,"Make a prediction in your own words before solving.");
    if(answer===null)return;state.prediction=answer;advance(1);announce("Prediction saved locally. No hints have been shown.");
   },true));
  } else if(state.step===1){
   stageTitle(stage,"2 · Attempt without help","Write your model and calculations before you see hints or a worked answer. This first attempt is saved separately from later repairs.");
   const grid=make("div","lab-input-grid");stage.append(grid);
   const controls={};
   for(const [name,label] of cfg.fields)controls[name]=field(grid,name,label,false);
   const reasoning=field(stage,"explanation",cfg.attempt,true);
   para(stage,"It is OK to make a mistake. We do not automatically grade your writing.");
   const bar=actions(stage);
   bar.append(btn("Lock my first attempt",()=>{
    const values={};
    for(const [name,label] of cfg.fields){const v=saveText(controls[name],"Fill in "+label+" before locking your model.");if(v===null)return;values[name]=v;}
    const explanation=saveText(reasoning,"Explain your model and why you chose these equations.");
    if(explanation===null)return;
    state.attempt={values,explanation};advance(2);announce("Your first attempt is locked. Choose an optional hint or open the worked model.");
   },true));
  } else if(state.step===2){
   stageTitle(stage,"3 · Reconstruct","Your first attempt is locked. Hints are optional. Compare your own model only when you are ready.");
   showOriginal(stage);
   const bar=actions(stage);
   if(state.hints<2){
    bar.append(btn("Show hint "+(state.hints+1),()=>{
     state.hints++;persist();render();announce("Hint "+state.hints+" opened. Your first attempt stays unchanged.");
    }));
   }
   for(let i=0;i<Math.min(state.hints,2);i++)para(stage,"Hint "+(i+1)+": "+cfg.hints[i]);
   if(!state.reconstructionViewed){
    bar.append(btn("Open worked reconstruction",()=>{
     state.reconstructionViewed=true;persist();render();announce("Worked reconstruction opened after your first attempt.");
    },true));
   }else{
    const refSlot=make("div","lab-reference-slot");stage.append(refSlot);
    const next=btn("I compared the model → Diagnose",()=>advance(3),true);next.disabled=true;
    actions(stage).append(next);
    renderReference(refSlot,"reconstruction",()=>{next.disabled=false;});
   }
  } else if(state.step===3){
   stageTitle(stage,"4 · Diagnose the reasoning","Spot the first possible mix-up in your answer—or choose a common mix-up in a friend's answer if yours looks correct.");
   showOriginal(stage);
   const wrap=make("div","lab-field"),id="lab-"+code+"-diagnose",label=make("label","","Which idea should be checked?");label.htmlFor=id;
   const select=make("select");select.id=id;select.dataset.field="diagnosis";
   const placeholder=make("option","","Choose one");placeholder.value="";select.append(placeholder);
   for(const opt of cfg.diagnose){const option=make("option","",opt);option.value=opt;select.append(option);}
   wrap.append(label,select);stage.append(wrap);
   const note=field(stage,"diagnosis-note","Why can that idea cause an incorrect solution?",true);
   const bar=actions(stage);bar.append(btn("Save diagnosis → Repair",()=>{
    if(!select.value){announce("Choose an idea to diagnose.",true);select.focus();return;}
    const reason=saveText(note,"Explain the reasoning error or why your model already works.");
    if(reason===null)return;
    state.diagnosis={choice:select.value,reason};advance(4);announce("Diagnosis saved. Your first attempt is unchanged.");
   },true));
  }else if(state.step===4){
   stageTitle(stage,"5 · Repair","Now correct the model, ledger, or region boundary. If your first answer was already right, show how you verified every important step.");
   showOriginal(stage);
   const changed=field(stage,"repair-change","What did you change or verify?",true);
   const working=field(stage,"repair-work","Show your improved working and explanation",true);
   const bar=actions(stage);bar.append(btn("Save repair → Boundary test",()=>{
    const first=saveText(changed,"Describe what you changed or checked.");if(first===null)return;
    const second=saveText(working,"Write your improved model and calculations.");if(second===null)return;
    state.repair={change:first,working:second};advance(5);announce("Repair saved separately from your original reasoning.");
   },true));
  }else if(state.step===5){
   stageTitle(stage,"6 · Boundary test",cfg.boundary);
   const input=field(stage,"boundary","My changed-condition answer and why",true);
   const bar=actions(stage);bar.append(btn("Lock boundary answer → Compare",()=>{
    const reasoning=saveText(input,"Explain what happens when the condition changes.");
    if(reasoning===null)return;
    state.boundary=reasoning;advance(6);announce("The boundary answer is locked. The comparison is below; this is not an automatic grade.");
   },true));
  }else{
   const done=make("div","lab-done");done.append(make("h4","","Six steps completed · Review your thinking"));
   para(done,"You made a prediction, locked an independent model, compared the reconstruction, diagnosed a possible error, repaired your reasoning, and tested a new condition. This is practice progress, not a score.");
   stage.append(done);showOriginal(stage);
   const record=make("details","lab-first"),summary=make("summary","","My diagnosis, repair and boundary explanation");record.append(summary);
   const details=make("dl");
   for(const [label,value] of [["Diagnosis",state.diagnosis?.choice],["Why I chose it",state.diagnosis?.reason],["What I changed",state.repair?.change],["Improved working",state.repair?.working],["Boundary answer",state.boundary]]){
    details.append(make("dt","",label),make("dd","",String(value??"")));
   }
   record.append(details);stage.append(record);
   const boundaryRef=make("div","lab-reference-slot");stage.append(boundaryRef);renderReference(boundaryRef,"boundary");
  }
  status.classList.remove("lab-error");
  if(!status.textContent)status.textContent="Saved on this browser only. Your written answers are not automatically graded.";
  updateProgress();
 };
 reset.addEventListener("click",()=>{
  if(!resetArmed){resetArmed=true;reset.textContent="Confirm: clear this journey";announce("Click once more to clear this journey's saved attempt.");return;}
  clear(key);state=emptyState();reset.textContent="Clear this journey";announce("This journey was cleared. You can start again.");render();
 });
 instances.push({getState:()=>state});render();
}
for(const [code] of Object.entries(CONFIG)){
 const card=document.querySelector('[data-lab="'+code+'"]');
 if(card)attach(card,code);
}
updateProgress();
})();
