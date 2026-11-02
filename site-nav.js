(()=>{"use strict";
const run=()=>{
if(document.getElementById('grade9-universal-nav'))return;
const src=document.querySelector("script[data-grade9-nav]")?.src;
if(!src)return;
const base=new URL("./",src);
const here=location.pathname,root=base.pathname;
const isBank=here.endsWith("/question-status.html");
const isLibrary=here.includes("/batches/");
const title=isBank?"Question Bank":isLibrary?"WPE Examples":"Physics · WPE";
const host=document.createElement("div");host.id="grade9-universal-nav";
const shadow=host.attachShadow({mode:"open"});
const style=document.createElement("style");
style.textContent=":host{all:initial;display:block}*,*:before,*:after{box-sizing:border-box}.bar{background:#102f43;border-bottom:2px solid #76cdbd;color:#fff;font:600 13px/1.4 system-ui,-apple-system,Segoe UI,sans-serif;padding:9px clamp(12px,3vw,32px);display:flex;align-items:center;gap:8px 18px;flex-wrap:wrap}.brand{color:#eafff9;font-weight:850;text-decoration:none;font-size:14px;margin-right:auto;white-space:nowrap}.group{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:center}a{display:inline-block;color:#d1ebf7;text-decoration:none;border-radius:7px;padding:7px 9px;white-space:nowrap}a:hover,a:focus-visible{background:#ffffff23;color:#fff}a:focus-visible{outline:3px solid #e9b54e;outline-offset:2px}.here{font-size:11px;color:#9ad7cd;background:#21475a;border-radius:30px;padding:5px 9px;white-space:nowrap}@media(max-width:550px){.brand{flex-basis:100%}.bar{gap:3px 6px;padding:7px 10px}a{padding:8px 7px;font-size:12px}.here{display:none}}";
const bar=document.createElement("nav");bar.className="bar";bar.setAttribute("aria-label","Grade9 main and chapter navigation");
const links=[["🎓 Grade9",base.href+"index.html","brand"],["🏠 Home",base.href+"index.html"],["⚛️ Physics",base.href+"physics/index.html"],["📐 Maths",base.href+"mathematics/index.html"],["🧪 Chemistry",base.href+"chemistry/index.html"],["🧩 Examples",base.href+"preview/batches/reader.html"],["⚡ WPE",base.href+"physics/wpe/index.html"],["📚 Question Bank",base.href+"physics/wpe/question-bank.html"],["✏️ Practice",base.href+"preview/practice.html"],["🧭 Architecture",base.href+"architecture/index.html"]];
for(const [text,url,cl] of links){const a=document.createElement("a");a.href=url;a.textContent=text;if(cl)a.className=cl;bar.appendChild(a)}
const label=document.createElement("span");label.className="here";label.textContent=title;bar.appendChild(label);
shadow.append(style,bar);document.body.insertBefore(host,document.body.firstChild)
};
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",run,{once:true});else run();
})();