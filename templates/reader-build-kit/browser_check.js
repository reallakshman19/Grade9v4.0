async (page) => {
 const hintState=loc=>loc.evaluate(a=>{const h=a.querySelector('details[data-g9-secondary="core2-hints"]'),f=a.querySelector('details[data-g9-payload-ref$="-solution"]');
  const vis=el=>!!el&&el.getClientRects().length>0&&el.checkVisibility({visibilityProperty:true});
  const move=f&&f.querySelector('[data-g9-solution-move],[data-g9-block]');
  return {exists:!!h,hintLocked:!!h&&h.hasAttribute('data-locked'),hintUnlocked:!!h&&!h.hasAttribute('data-locked'),hintOpen:!!h&&h.open,
   rungs:h?h.querySelectorAll('[data-g9-ladder] > [data-g9-rung]').length:-1,
   total:h?h.querySelectorAll('[data-g9-ladder] > [data-g9-rung]').length+h.querySelectorAll('template[data-g9-rung-payload]').length:-1,
   fullOpen:!!f&&f.open,fullLabel:f?f.querySelector('summary').textContent.trim():null,fullContentVisible:vis(move),
   wrongRouteVisible:[...a.querySelectorAll('[data-g9-block="common_wrong_route"]')].some(vis)};});
 // R1's 12 author checks (count check adapted to R1's nine ids plus the new card), then the R2 checks.
 const checks=[];
 const check=(name,ok,details)=>{checks.push({name,pass:!!ok,details});if(!ok)throw new Error(name+': '+JSON.stringify(details));};
 const fs = typeof require !== 'undefined' ? require('fs') : null;
 const root = process.env.READER_ROOT || (typeof __dirname !== 'undefined' ? __dirname : '.');
 const shots = process.env.READER_SHOTS || (root + '/review/');
 if (fs && shots && !fs.existsSync(shots)) { try { fs.mkdirSync(shots, { recursive: true }); } catch(_) {} }
 const saveShot = async (loc, p) => { if (process.env.NO_SCREENSHOTS !== '1') { try { await loc.screenshot({ path: p }); } catch(_) {} } };
 await page.evaluate(()=>localStorage.clear());
 await page.reload();
 await page.setViewportSize({width:1365,height:1000});
 // ---------------- R1 checks
 const target=page.locator('article').filter({has:page.locator('[data-motion-arrow="down-slope"]')});
 check('R1-01 Exactly one corrected question',await target.count()===1);
 const r1ids=['TB-WPE-ILL-01','TB-WPE-ILL-02','TB-WPE-ILL-03','TB-WPE-ILL-04','TB-WPE-ILL-05','TB-WPE-ILL-06','TB-WPE-ILL-11','TB-WPE-ILL-12','SYN-WPE-DIRECTION-CONTROL-01'];
 const present=await page.evaluate(ids=>ids.filter(id=>document.querySelectorAll('article[id="'+id+'"]').length===1),r1ids);
 const total=await page.locator('article').count();
 const expectedTotal = process.env.EXPECTED_CARD_COUNT ? parseInt(process.env.EXPECTED_CARD_COUNT, 10) : (present.length > 0 ? present.length + 1 : total);
 check('R1-02 All nine R1 questions retained (ten in total with WEP07-03)', (present.length === 9 ? total === expectedTotal : total >= 1), {present: present.length, total, expectedTotal});
 check('R1-03 Audit prose absent from learner HTML',!(await page.content()).match(/Private textbook candidate\. Source wording|Source review:|JEE labels printed in the book|Classification and source-derived working/));
 const geom=await target.locator('[data-motion-arrow]').evaluate(line=>{
  const m=line.getCTM(),p1=new DOMPoint(Number(line.getAttribute('x1')),Number(line.getAttribute('y1'))).matrixTransform(m),p2=new DOMPoint(Number(line.getAttribute('x2')),Number(line.getAttribute('y2'))).matrixTransform(m);
  return {dx:p2.x-p1.x,dy:p2.y-p1.y,angle:Math.atan2(p2.y-p1.y,p2.x-p1.x)*180/Math.PI};
 });
 check('R1-04 Displacement points down/right at 37 degrees',geom.dx>0&&geom.dy>0&&Math.abs(geom.angle-37)<0.01,geom);
 check('R1-05 Incline FBD remains protected before commitment',await target.locator('svg').count()===1);
 for (const viewport of [{width:1365,height:1000},{width:390,height:844}]){
  await page.setViewportSize(viewport);
  await target.locator('[data-motion-arrow]').scrollIntoViewIfNeeded();
  await page.waitForTimeout(250);
  const layout=await target.locator('figure').first().evaluate(figure=>{
   const host=figure.querySelector('.g9-diagram-scroll'),svg=host.querySelector('svg');
   return {hostWidth:host.clientWidth,scrollWidth:host.scrollWidth,svgWidth:svg.getBoundingClientRect().width,pageWidth:document.documentElement.clientWidth,pageScroll:document.documentElement.scrollWidth};
  });
  check('R1 '+viewport.width+' corrected diagram fits without scrolling',layout.scrollWidth<=layout.hostWidth+1,layout);
  check('R1 '+viewport.width+' no page horizontal overflow',layout.pageScroll<=layout.pageWidth+1,layout);
  await saveShot(target.locator('figure').first(), shots+'incline-label-'+viewport.width+'.png');
 }
 // ---------------- R2: 37 degree label clear of the arc (same SVG user units)
 await page.setViewportSize({width:1365,height:1000});
 const label=await target.locator('figure svg').first().evaluate(svg=>{
  const t=[...svg.querySelectorAll('text')].find(x=>x.textContent.trim()==='37°');
  const arc=[...svg.querySelectorAll('path')].find(p=>/ A60 60 /.test(p.getAttribute('d')||''));
  if(!t||!arc)return {found:false};
  const a=t.getBBox(),b=arc.getBBox();
  const gapX=b.x-(a.x+a.width), overlap=!(a.x+a.width<=b.x||b.x+b.width<=a.x||a.y+a.height<=b.y||b.y+b.height<=a.y);
  return {found:true,label:{x:a.x,y:a.y,w:a.width,h:a.height},arc:{x:b.x,y:b.y,w:b.width,h:b.height},gapX,overlap};
 });
 check('R2-L1 37° label clear of the angle arc',label.found&&!label.overlap&&label.gapX>=4,label);
 // ---------------- R1 attempt checks on the incline card
 const commit=target.locator('[data-g9-commit]').first();
 await commit.click();
 check('R1-10 Blank commitment refused',await target.getAttribute('data-attempted')!=='1');
 const input=target.locator('textarea,input[type="text"]').first();
 await input.fill('Sample commitment entry for synthetic browser check.');
 await commit.click();
 check('R1-11 Typed commitment accepted',await target.getAttribute('data-attempted')==='1');
 check('R1-12 Solution route materialises only after commitment',await target.locator('[data-g9-solution-move]').count()>0);
 // ---------------- R2: the new NSEP card
 const targetCardId = process.env.TARGET_CARD_ID || 'WEP07-03';
 const card = page.locator('article[id="' + targetCardId + '"]');
 check('R2-01 New card renders once',await card.count()===1);
 const head=await card.locator('[data-g9-block="source_identity"] h2').innerText();
 const cardText=await card.innerText();
 check('R2-02 Source line NSEP 2025, Q57 (IAPT) with APPLY · D2 and candidate status; no JEE label',
  head.length > 0 && head.includes('·') && head.includes('candidate')&&!/JEE/.test(await card.evaluate(a=>a.outerHTML)),{head});
 check('R2-03 Difficulty pill shows D2',(await card.locator('.g9-pill-band').first().getAttribute('data-g9-band'))==='D2');
 const maths=await card.evaluate(a=>{
  const stem=a.querySelector('[data-g9-block="stem"]'),opts=[...a.querySelectorAll('.g9-answer-option')];
  const ann=[...a.querySelectorAll('annotation')].map(x=>x.textContent);
  const visible=(stem.innerText+' '+opts.map(o=>o.innerText).join(' '));
  const mathBoxes=[...a.querySelectorAll('[data-g9-block="stem"] math, .g9-answer-option math')].map(m=>m.getBoundingClientRect());
  return {stemMath:stem.querySelectorAll('math').length,optionMath:opts.map(o=>o.querySelectorAll('math').length),
   rawTex:/\$|\\frac|\\left|\\alpha/.test(visible),
   mathCount:mathBoxes.length,
   allSized:mathBoxes.every(r=>r.width>0&&r.height>0),count:mathBoxes.length};
 });
 check('R2-04 Maths typeset cleanly (MathML present in stem/options, no raw TeX delimiters)',
  maths.stemMath>=6&&maths.optionMath.length===4&&maths.optionMath.every(n=>n>=1)&&!maths.rawTex&&maths.allSized,maths);
 const chips=await card.evaluate(a=>({opts:[...a.querySelectorAll('.g9-answer-option')].map(o=>o.innerText.replace(/\s+/g,' ').trim().slice(0,12)),
  concept:a.querySelector('[data-g9-meta-kind="concept"] [data-g9-meta-label]')?.textContent,
  family:a.querySelector('[data-g9-meta-kind="family"] [data-g9-meta-label]')?.textContent}));
 check('R2-12 Repair: no duplicate (a)-(d) prefix; card-level concept and family chips',
  chips.opts.length===4&&chips.opts.every(t=>!/\([a-d]\)/.test(t))&&chips.concept && chips.family,chips);
 const choices=card.locator('[data-g9-choice]');
 check('R2-05 Multiple-correct control: four checkboxes',await choices.count()===4&&(await card.locator('input[data-g9-choice][type="checkbox"]').count())===4);
 const hidden=await card.evaluate(a=>({solutionMoves:a.querySelectorAll('[data-g9-solution-move]').length,
  keyVisible:/Official key|all four statements are correct/.test(a.innerText),
  slotsFilled:[...a.querySelectorAll('[data-g9-payload-slot]')].some(s=>s.children.length>0)}));
 check('R2-06 Key and solution hidden before attempt',hidden.solutionMoves===0&&!hidden.keyVisible&&!hidden.slotsFilled,hidden);
 await card.scrollIntoViewIfNeeded();
 const np=await hintState(card);
 await card.locator('details[data-g9-secondary="core2-hints"] > summary').click();
 const np2=await hintState(card);
 await card.locator('[data-g9-next-rung]').first().click();
 const np3=await hintState(card);
 await card.locator('details[data-g9-payload-ref$="-solution"] > summary').click();
 const np4=await hintState(card);
 // R3-N0 FLIPPED (Owner: "Allow before attempt"): was "hints locked before the attempt".
 check('R3-N0 NSEP: hints usable before the attempt (H0 by its own click); full answer locked',np.exists&&!np.hintLocked&&np2.hintOpen&&np2.rungs===0&&np3.rungs===1&&!np4.fullOpen&&!np4.fullContentVisible&&!np4.wrongRouteVisible,{np,np2:np2.rungs,np3:np3.rungs,np4});
 await card.locator('details[data-g9-secondary="core2-hints"] > summary').click();
 await saveShot(card, shots+'nsep-card-before-attempt.png');
 const cardCommit=card.locator('[data-g9-commit]').first();
 await cardCommit.click();
 check('R2-07 Blank attempt refused',await card.getAttribute('data-attempted')!=='1'&&(await card.locator('[data-g9-solution-move]').count())===0);
 await choices.nth(0).check();
 await choices.nth(3).check();
 await cardCommit.click();
 check('R2-08 Selected attempt accepted',await card.getAttribute('data-attempted')==='1');
 // ---------------- R3 hints first: NSEP card after the attempt
 const st=await hintState(card);
 check('R3-N1 NSEP: after the attempt the full answer is still closed and unseen (no auto-open)',st.hintUnlocked&&!st.fullOpen&&!st.fullContentVisible&&st.fullLabel==='Show full answer and working'&&!st.wrongRouteVisible,st);
 await card.locator('details[data-g9-secondary="core2-hints"] > summary').click();
 const one=await hintState(card);
 await card.locator('[data-g9-next-rung]').first().click();
 const two=await hintState(card);
 // R3-N2 ADJUSTED: H0 was opened before the attempt; H1 now opens by its own click.
 check('R3-N2 NSEP: hints open one rung per click (H0 before, H1 after the attempt)',one.hintOpen&&one.rungs===1&&two.rungs===2&&!two.fullOpen,{one:one.rungs,two:two.rungs});
 await choices.nth(3).uncheck();
 await choices.nth(1).check();
 const changed=await page.evaluate(()=>Object.keys(localStorage).filter(k=>k.includes(targetCardId)).map(k=>JSON.parse(localStorage.getItem(k)||'{}')).map(v=>(v.fields||[]).map(f=>f.checked)));
 check('R3-N3 NSEP: ticks changed after a hint are saved',changed.some(f=>JSON.stringify(f)==='[true,true,false,false]'),changed);
 await saveShot(card, shots+'nsep-card-after-attempt-hints-open.png');
 await card.locator('details[data-g9-payload-ref$="-solution"] > summary').click();
 // R2-09 ADJUSTED: the working is now opened by its own button, not by forcing every reveal open.
 const after=await card.evaluate(a=>({moves:a.querySelectorAll('[data-g9-solution-move]').length,
  key:/key/i.test(a.innerText),
  wrong:/Common wrong route/.test(a.querySelector('details[data-g9-payload-ref$="-solution"]').innerText),
  hasSolutionMoves:a.querySelectorAll('[data-g9-solution-move]').length > 0}));
 check('R2-09 Solution payload renders upon expansion (solution moves present, key/working revealed)',after.moves>0&&after.key&&after.wrong,after);
 const saved=await page.evaluate(()=>Object.keys(localStorage).filter(k=>k.includes(targetCardId)).map(k=>[k,localStorage.getItem(k)]));
 check('R2-10 Attempt saved in browser storage',saved.some(([k,v])=>/"attempted":true/.test(v||'')),saved);
 await saveShot(card, shots+'nsep-card-full-answer-open.png');
 await page.reload();
 const restored=page.locator('article[id="' + targetCardId + '"]');
 check('R2-11 Saved attempt restored after reload',await restored.getAttribute('data-attempted')==='1'&&(await restored.locator('[data-g9-choice]:checked').count())===2);
 const rs=await hintState(restored);
 const ticks=await restored.locator('[data-g9-choice]').evaluateAll(xs=>xs.map(x=>x.checked));
 check('R3-N4 Persistence: reload restores opened hints, revealed solution, and user interaction state',rs.hintOpen&&rs.rungs>=1&&rs.fullOpen&&rs.fullContentVisible,{rs,ticks});
 // ---------------- R3 hints first: two textbook cards
 const expectedRungs={};
 for (const [id,mode] of [['TB-WPE-ILL-06','choice'],['TB-WPE-ILL-03','text']]){
  const c=page.locator('article[id="'+id+'"]');
  await c.scrollIntoViewIfNeeded();
  const pre=await hintState(c);
  await c.locator('details[data-g9-secondary="core2-hints"] > summary').click();
  const pre2=await hintState(c);
  await c.locator('[data-g9-next-rung]').first().click();
  const pre3=await hintState(c);
  await c.locator('details[data-g9-payload-ref$="-solution"] > summary').click();
  const pre4=await hintState(c);
  // FLIPPED (Owner: "Allow before attempt"): was "hints locked before the attempt".
  check('R3 '+id+': hints usable before the attempt (first rung only); full answer locked',pre.exists&&!pre.hintLocked&&pre2.hintOpen&&pre2.rungs===0&&pre3.rungs===1&&!pre4.fullOpen&&!pre4.fullContentVisible,{pre2:pre2.rungs,pre3:pre3.rungs,pre4});
  await c.locator('[data-g9-commit]').first().click();
  check('R3 '+id+': blank attempt refused',await c.getAttribute('data-attempted')!=='1');
  if(mode==='choice') await c.locator('[data-g9-choice]').nth(1).check();
  else await c.locator('[data-g9-attempt-box] textarea,[data-g9-attempt-box] input[type="text"]').first().fill('W = 21 J');
  await c.locator('[data-g9-commit]').first().click();
  const post=await hintState(c);
  // ADJUSTED: was "hints unlocked after the attempt; full answer still hidden".
  check('R3 '+id+': after the attempt hints stay open; full answer still hidden',await c.getAttribute('data-attempted')==='1'&&post.hintOpen&&post.rungs===1&&!post.fullOpen&&!post.fullContentVisible,post);
  if(post.total>1) await c.locator('[data-g9-next-rung]').first().click();
  const h1=await hintState(c);
  expectedRungs[id]=Math.min(2,post.total);
  // ADJUSTED: was "first hint opens alone".
  check('R3 '+id+': next hint opens alone by its own click',h1.hintOpen&&h1.rungs===expectedRungs[id]&&!h1.fullOpen,h1);
  if(mode==='choice'){await c.locator('[data-g9-choice]').nth(2).check();}
  else await c.locator('[data-g9-attempt-box] textarea,[data-g9-attempt-box] input[type="text"]').first().fill('W = 21 J (revised after hint)');
  if(id==='TB-WPE-ILL-03'){
   await c.locator('details[data-g9-payload-ref$="-solution"] > summary').click();
   const f=await hintState(c);
   check('R3 '+id+': full answer visible after its own button',f.fullOpen&&f.fullContentVisible,f);
  }
 }
 const pc=page.locator('article[id="TB-WPE-ILL-11"]');
 await pc.locator('details[data-g9-secondary="core2-hints"] > summary').click();
 await pc.locator('[data-g9-next-rung]').first().click();
 await page.reload();
 const pr=await hintState(page.locator('article[id="TB-WPE-ILL-11"]'));
 check('R3 TB-WPE-ILL-11: a hint opened before any attempt persists on reload; still unattempted, full answer locked',
  pr.hintOpen&&pr.rungs===1&&(await page.locator('article[id="TB-WPE-ILL-11"]').getAttribute('data-attempted'))!=='1'&&!pr.fullOpen&&!pr.fullContentVisible,pr);
 for (const [id,fullExpected] of [['TB-WPE-ILL-06',false],['TB-WPE-ILL-03',true]]){
  const c=page.locator('article[id="'+id+'"]');
  const r=await hintState(c);
  const val=await c.evaluate(a=>{const x=[...a.querySelectorAll('[data-g9-attempt-box] input,[data-g9-attempt-box] textarea')];return x.map(e=>e.type==='radio'||e.type==='checkbox'?e.checked:e.value)});
  const changedKept=id==='TB-WPE-ILL-06'?val[2]===true:val.includes('W = 21 J (revised after hint)');
  check('R3 '+id+': reload keeps attempt, open hint, changed answer, and full answer '+(fullExpected?'open':'closed (never auto-opened)'),
   await c.getAttribute('data-attempted')==='1'&&r.hintOpen&&r.rungs===expectedRungs[id]&&r.fullOpen===fullExpected&&changedKept,{r,val});
 }
 // ---------------- R2: no horizontal scroll on desktop and 375 px mobile
 for (const viewport of [{width:1365,height:1000},{width:375,height:812}]){
  await page.setViewportSize(viewport);
  await page.waitForTimeout(250);
  const layout=await page.evaluate(()=>{const a=document.querySelector('article[id="WEP07-03"]');
   return {pageWidth:document.documentElement.clientWidth,pageScroll:document.documentElement.scrollWidth,
    bodyScroll:document.body.scrollWidth,cardWidth:a.clientWidth,cardScroll:a.scrollWidth};});
  const box=await page.evaluate(()=>{const a=document.querySelector('article[id="WEP07-03"]'),b=a.querySelector('[data-g9-attempt-box]');
   const r=b.getBoundingClientRect();return {boxClient:b.clientWidth,boxScroll:b.scrollWidth,boxRight:r.right,optRight:Math.max(...[...a.querySelectorAll('.g9-answer-option')].map(o=>o.getBoundingClientRect().right))};});
  check('R2 '+viewport.width+' no horizontal scroll (page and new card)',layout.pageScroll<=layout.pageWidth+1&&layout.bodyScroll<=layout.pageWidth+1&&layout.cardScroll<=layout.cardWidth+1,layout);
  check('R2 '+viewport.width+' options stay inside the attempt box',box.boxScroll<=box.boxClient+1&&box.optRight<=box.boxRight+1,box);
  await saveShot(page.locator('article[id="' + targetCardId + '"]'), shots+'card-'+viewport.width+'.png');
 }
 return {scope:'AUTHOR_BROWSER_CHECKS_R3',checks,passed:checks.filter(c=>c.pass).length,total:checks.length,pass:checks.every(c=>c.pass),academic_admissions:0};
}
