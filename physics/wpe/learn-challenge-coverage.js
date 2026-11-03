/* Student-first source-question router for the existing Learn → Challenge tile.
 * The 74-question evidence is reconciled against the original bank, 13
 * pre-existing lessons and F01–F03. Routes are practice, not QRT decisions.
 */
(async()=>{
  "use strict";
  const $=s=>document.querySelector(s),panel=$("#question-plan"),
        picker=$("#question-pick"),search=$("#question-search"),status=$("#question-route-status");
  const newEl=(tag,text,cls)=>{const e=document.createElement(tag);if(text!=null)e.textContent=text;if(cls)e.className=cls;return e;};
  const add=(root,tag,text,cls)=>{const e=newEl(tag,text,cls);root.append(e);return e;};
  const valid=s=>typeof s==="string"&&/^[A-Za-z0-9-]{2,64}$/.test(s);
  let bank,map,rows=[],selected=null;
  try{
    const [b,r]=await Promise.all([
      fetch("../../workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json",{cache:"no-store"}),
      fetch("learning-coverage-r1.json",{cache:"no-store"})
    ]);
    if(!b.ok||!r.ok)throw Error("Question Bank evidence unavailable");
    bank=await b.json();map=await r.json();
    if(bank.questions?.length!==74||map.schema!=="wpe-learner-coverage-r1/v1"||map.questions?.length!==74)throw Error("Source inventory changed");
    const original=new Map(bank.questions.map(q=>[q.source_id,q]));
    if(original.size!==74||map.questions.some(row=>!original.has(row.source_id)||row.stem_sha256!==original.get(row.source_id).stem_sha256))throw Error("Question IDs or source stems no longer match");
    rows=map.questions;
  }catch(err){panel.textContent="The exact question-to-lesson route cannot be verified right now. Use the Question Bank directly.";status.textContent="Learning route unavailable.";return;}
  const query=new URLSearchParams(location.search).get("question");
  selected=query && valid(query) && rows.some(x=>x.source_id===query)?query:null;
  const names={F01:"Applied power vs net power",F02:"Round-trip incline energy",F03:"Spring force switching",C01:"Every force counts",C02:"Spring contact",C03:"Constant power",C04:"Distributed mass",C05:"Choose the graph operation",C06:"Vertical-circle contact",C07:"Conveyor momentum flow",C08:"Comparing spring controls",E01:"Potential wells",E02:"Instantaneous power",E03:"Spring to projectile",E04:"Repeated bouncing",E05:"Radial force and potential"};
  function fillChoices(){
    const term=search.value.trim().toLowerCase();
    const filtered=rows.filter(row=>(row.source_id+" "+row.student_goal+" "+(names[row.primary_lesson]||"")).toLowerCase().includes(term));
    picker.replaceChildren();
    if(!filtered.length){add(picker,"option","No matching source questions").value="";picker.disabled=true;selected=null;}
    else{
      picker.disabled=false;
      for(const row of filtered){
        const opt=add(picker,"option",row.source_id+" · "+row.student_goal.slice(0,52));opt.value=row.source_id;
      }
      if(!filtered.some(x=>x.source_id===selected))selected=null;
      const prompt=add(picker,"option","Choose an original question");prompt.value="";
      picker.value=selected||"";
    }
    status.textContent=filtered.length+" of 74 source questions shown; "+map.counts.focused_new+" new focused journeys, "+map.counts.targeted+" close practice matches, "+map.counts.related+" related-only bridges, "+map.counts.missing+" genuine missing constructions.";
    draw();
  }
  const safeLessonURL=(href,source)=>{
    if(typeof href!=="string")return null;
    try{
      const url=new URL(href,location.href),loc=new URL("focused-journeys.html",location.href);
      if(url.origin!==loc.origin||url.pathname.substring(0,url.pathname.lastIndexOf("/")+1)!==loc.pathname.substring(0,loc.pathname.lastIndexOf("/")+1))return null;
      if(!/^(d3d4-self-tutor|extension-learning|focused-journeys)\.html$/.test(url.pathname.split("/").pop()))return null;
      if(url.searchParams.get("question")!==source)return null;
      return url.href;
    }catch(_){return null;}
  };
  function draw(){
    panel.replaceChildren();
    const row=rows.find(x=>x.source_id===selected);
    if(!row){
      add(panel,"h3","That question ID is not in the current 74-entry bank.");
      add(panel,"p","No lesson or source return is inferred. Choose a known ID from the selector.");
      return;
    }
    try{localStorage.setItem("g9:wpe:journey:v1",JSON.stringify({question:row.source_id,lesson:row.primary_lesson}));}catch(_){}
    const heading=add(panel,"h3",row.source_id+" · Your learning route");
    const description=add(panel,"p",row.student_goal,"student-goal");
    const summary=add(panel,"p",null,"fit-explanation");
    let fitText={
      FOCUSED_NEW:"New fully interactive reasoning journey for this physical operation.",
      TARGETED_PRACTICE:"A close reasoning match. Use a different challenge to test whether you can transfer the idea.",
      RELATED_BRIDGE:"Related practice ONLY. This lesson does not teach every operation the original question demands.",
      MISSING_CONSTRUCTION:"A necessary reasoning construction is missing. No unrelated lesson is presented as a solution."
    }[row.fit]||"Study status could not be determined.";
    summary.textContent=fitText;
    add(panel,"p","What the current teaching does NOT establish: "+row.teaching_limit,"teaching-limit");
    if(row.has_source_caution){
      const caution=add(panel,"p",row.source_science_note||"Some source physics, figures or answer-key claims are not independently resolved.","source-caution");
      caution.setAttribute("role","note");
    }
    const actions=add(panel,"nav",null,"question-actions");
    actions.setAttribute("aria-label","Question learning actions");
    const lessonHref=safeLessonURL(row.lesson_href,row.source_id);
    if(lessonHref){
      const label=row.fit==="RELATED_BRIDGE"?"Practise a RELATED idea":row.fit==="FOCUSED_NEW"?"Start the new reasoning journey":"Learn the reasoning → Fresh challenge";
      const link=add(actions,"a",label+" · "+row.primary_lesson+" ("+(names[row.primary_lesson]||"practice")+")","primary-link");
      link.href=lessonHref;
    }else{
      add(actions,"span","No dedicated student lesson available for this operation yet.","no-lesson");
    }
    const original=add(actions,"a","Return to original "+row.source_id+" (attempt first)","source-link");
    original.href="../../preview/question-status.html?question="+encodeURIComponent(row.source_id);
    const support=add(panel,"details",null,"related-support");
    add(support,"summary","What else can I practise?");
    add(support,"p","These are additional existing ideas, not automatic replacements for the original question.");
    const list=add(support,"div",null,"related-links");
    for(const l of row.related_lessons){
      if(l===row.primary_lesson||!names[l])continue;
      const sourceKnown=map.questions.some(x=>x.source_id===row.source_id&&x.related_lessons.includes(l));
      if(!sourceKnown)continue;
      // The older lesson validates its own author-proposed source associations.
      const a=add(list,"a",l+" · "+names[l]);a.href="reasoning-paths.html?question="+encodeURIComponent(row.source_id)+"#WPE-"+l;
    }
    const all=add(support,"a","See the complete 74-question learning coverage");
    all.href="question-coverage.html?question="+encodeURIComponent(row.source_id);
    if(row.fit==="MISSING_CONSTRUCTION"){
      const p=add(support,"p","You can still practise the five foundational WPE mini-lessons below, but they are not a substitute for this missing reasoning construction.");
      const a=add(support,"a","Review the foundational Work → Energy path");a.href="#work-sign";
    }
    if(location.search!==""&&new URLSearchParams(location.search).get("question")===row.source_id)heading.setAttribute("data-exact-source","true");
  }
  const skillHost=$("#skill-links");
  for(const [id,name] of Object.entries(names)){
    const page=id.startsWith("C")?"d3d4-self-tutor.html":id.startsWith("E")?"extension-learning.html":"focused-journeys.html";
    const a=add(skillHost,"a",id+" · "+name);a.href=page+"#"+id;
    a.addEventListener("click",()=>{
      try{localStorage.setItem("g9:wpe:journey:v1",JSON.stringify({question:null,lesson:id}));}catch(_){}
    });
  }
  const resume=$("#resume-journey"),notice=$("#saved-practice-status");
  function refreshResume(){
    try{
      const saved=JSON.parse(localStorage.getItem("g9:wpe:journey:v1")||"null");
      const row=rows.find(r=>r.source_id===saved?.question&&r.primary_lesson===saved.lesson&&r.lesson_href);
      if(!row&&saved?.question===null&&names[saved?.lesson]){
        const id=saved.lesson,page=id.startsWith("C")?"d3d4-self-tutor.html":id.startsWith("E")?"extension-learning.html":"focused-journeys.html";
        resume.href=page+"#"+id;resume.textContent="Resume "+id+" · "+names[id];
      }else if(row){resume.href=saved.variant==="transfer55"&&row.primary_lesson.startsWith("F")
        ?row.lesson_href.replace("#","&variant=transfer55#"):row.lesson_href;
        resume.textContent="Resume "+row.source_id+" → "+row.primary_lesson;
      }else{resume.href="#question-routes";resume.textContent="Choose a question to begin";}
    }catch(_){resume.href="#question-routes";}
  }
  refreshResume();
  $("#clear-saved-practice").addEventListener("click",()=>{
    if(!confirm("Clear ALL WPE practice, including Question Bank drafts, saved in this browser? This cannot be undone."))return;
    try{
      const prefixes=["g9:wpe:d3d4:self-tutor:v1:","g9:wpe:extensions:v1:","g9:wpe:focused:v1:","g9:wpe:core2:attempt:v1:","g9:wpe:learn-challenge:v1:","g9:wpe:learn-challenge:","g9:wpe:journey:v1"];
      for(let i=localStorage.length-1;i>=0;i--){const key=localStorage.key(i);if(key&&prefixes.some(x=>key.startsWith(x)))localStorage.removeItem(key);}
      notice.textContent="Saved WPE practice cleared on this device. Reload other open Question Bank tabs to reflect this reset.";
      refreshResume();
    }catch(_){notice.textContent="Browser storage could not be cleared here.";}
  });
  search.addEventListener("input",fillChoices);
  picker.addEventListener("change",()=>{
    selected=picker.value;
    const url=new URL(location.href);
    if(selected)url.searchParams.set("question",selected);
    url.hash="question-routes";
    history.replaceState(null,"",url.pathname+url.search+url.hash);
    draw();refreshResume();
  });
  fillChoices();
})();
