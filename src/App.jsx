import { useState } from "react";
import Login from "./Login";

const MN = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

const INIT = {
  salaries: [
    {id:1,name:'CEO',                         m:[8929,8929,8929,8929,8929,8929,8929,8929,8929,8929,8929,8929]},
    {id:2,name:'Programs Lead (Tamri)',        m:[3189,3189,3189,3189,1006,893,3571,3571,3571,3571,3571,3571]},
    {id:3,name:'Programs Coord. (Masho)',      m:[1276,1276,1276,1276,1276,1276,1276,1276,1531,1531,1531,1531]},
    {id:4,name:'Head of Growth (Mariam)',      m:[2551,3571,3571,3571,3571,3571,3571,3571,3571,3571,3571,3571]},
    {id:5,name:'Growth Manager 1',            m:[1020,1020,1276,0,0,0,0,0,0,0,0,1276]},
    {id:6,name:'Growth Manager 2 (Mariam K)', m:[1276,1276,1276,1276,1276,1276,1276,1276,1531,1531,1531,1531]},
    {id:7,name:'Marketing Manager',           m:[2551,2551,2551,1276,0,0,0,0,0,0,0,0]},
    {id:8,name:'Marketing Specialist (Nini)', m:[1531,1531,1531,1913,1913,1913,1913,1913,1913,1913,1913,1913]},
    {id:9,name:'Video Editor',                m:[0,0,0,1000,1000,1000,1000,1000,1000,1000,1000,1000]},
  ],
  subs: [
    {id:1,name:'Office Rent',       m:[2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500]},
    {id:2,name:'Financial Service', m:[885,885,885,885,885,885,885,885,885,885,885,885]},
    {id:3,name:'HubSpot',           m:[1800,1800,1800,1800,1800,1800,1800,1800,1800,1800,1800,1800]},
    {id:4,name:'Google G Suite',    m:[230,230,230,230,230,230,230,230,230,230,230,230]},
    {id:5,name:'DigitalOcean',      m:[287,287,287,287,287,287,287,287,383,383,383,383]},
    {id:6,name:'Bank & SMS Fees',   m:[7,37,7,7,7,37,7,7,37,7,7,37]},
    {id:7,name:'WARC (ann./12)',    m:[909,909,909,909,909,909,909,909,909,909,909,909]},
    {id:8,name:'Canva (ann.)',      m:[33,33,33,33,33,33,33,33,33,33,33,33]},
  ],
  courses: [
    {id:1,name:'Graphic Design',month:'Jan',students:3,price:1250,lecturer:2800,mat:175,mkt:1111,zoom:40},
    {id:2,name:'Marketing Management',month:'Feb',students:4,price:1500,lecturer:3500,mat:236,mkt:1021,zoom:40},
    {id:3,name:'Content Management',month:'Feb',students:0,price:1400,lecturer:0,mat:0,mkt:1638,zoom:0},
    {id:4,name:'Data Analytics',month:'Feb',students:8,price:1700,lecturer:5357,mat:420,mkt:1225,zoom:40},
    {id:5,name:'AI in Content',month:'Feb',students:8,price:1400,lecturer:3000,mat:360,mkt:1439,zoom:40},
    {id:6,name:'AI Agents',month:'Mar',students:9,price:1400,lecturer:2551,mat:405,mkt:1542,zoom:40},
    {id:7,name:'Data Science',month:'Mar',students:9,price:2700,lecturer:12117,mat:405,mkt:1369,zoom:40},
    {id:8,name:'Growth Marketing',month:'Mar',students:17,price:1500,lecturer:4000,mat:765,mkt:569,zoom:40},
    {id:9,name:'IT BA',month:'Apr',students:8,price:1500,lecturer:3571,mat:400,mkt:1334,zoom:40},
    {id:10,name:'ADS',month:'Apr',students:14,price:1400,lecturer:5357,mat:630,mkt:1385,zoom:40},
    {id:11,name:'AI SEO',month:'May',students:5,price:1400,lecturer:3061,mat:265,mkt:1651,zoom:40},
    {id:12,name:'AI Essentials',month:'May',students:5,price:1050,lecturer:2551,mat:265,mkt:1557,zoom:40},
    {id:13,name:'Data Analytics',month:'May',students:6,price:1700,lecturer:5357,mat:310,mkt:1210,zoom:40},
    {id:14,name:'GITA: IT PM',month:'May',students:7,price:1000,lecturer:3571,mat:355,mkt:262,zoom:40},
    {id:15,name:'GITA: Motion Design',month:'May',students:7,price:1000,lecturer:3000,mat:355,mkt:262,zoom:40},
    {id:16,name:'GITA: IT BA',month:'May',students:7,price:1000,lecturer:3571,mat:355,mkt:262,zoom:40},
    {id:17,name:'GITA: Python',month:'May',students:29,price:2000,lecturer:13500,mat:1305,mkt:262,zoom:40},
    {id:18,name:'GITA: C#',month:'May',students:26,price:2000,lecturer:14000,mat:1210,mkt:262,zoom:40},
    {id:19,name:'GITA: QA',month:'May',students:6,price:1000,lecturer:6300,mat:310,mkt:262,zoom:40},
    {id:20,name:'GITA: Graphic Design',month:'May',students:13,price:1000,lecturer:3150,mat:635,mkt:262,zoom:40},
    {id:21,name:'GITA: UI/UX Design',month:'May',students:15,price:1000,lecturer:3571,mat:715,mkt:262,zoom:40},
    {id:22,name:'AI in Content',month:'Jun',students:12,price:1400,lecturer:2600,mat:580,mkt:1077,zoom:40},
  ],
  corp26: [
    {id:1,name:'Georgian Railway – AI',type:'B2G',period:'Jan–Feb',revenue:6435,cog:3215,status:'Paid'},
    {id:2,name:'Silk Development – AI',type:'B2B',period:'Jan–Apr',revenue:10932,cog:2710,status:'Paid'},
    {id:3,name:'Roche Georgia – Agentic AI',type:'B2B',period:'Mar',revenue:6780,cog:1566,status:'Paid'},
    {id:4,name:'Audit – SQL, Power BI',type:'B2G',period:'Mar–May',revenue:28400,cog:10566,status:'Pending'},
    {id:5,name:'Metropol – AI Group 1',type:'B2B',period:'Apr–May',revenue:4322,cog:1023,status:'Paid'},
    {id:6,name:'Metropol – AI Group 2',type:'B2B',period:'May',revenue:3814,cog:1023,status:'Paid'},
    {id:7,name:'Metropol – AI Groups 3–4',type:'B2B',period:'Jun',revenue:7627,cog:1824,status:'Paid'},
    {id:8,name:'Archi – AI for Designers',type:'B2B',period:'Jun',revenue:8051,cog:2697,status:'Paid'},
    {id:9,name:'Helvetas – Branding Ideathon',type:'B2B',period:'Jun–Jul',revenue:25000,cog:0,status:'Active'},
  ],
  corp25: [
    {co:'Roche Georgia',pr:'AI Workshop',type:'B2B',period:'Feb',rev:5085,cost:2175,profit:2910,margin:48.5},
    {co:'Liberty Bank',pr:'IT BA',type:'B2B',period:'Apr–May',rev:14831,cost:7220,profit:7611,margin:43.5},
    {co:'GITA',pr:'Tech Weeks',type:'B2G',period:'Apr–May',rev:78814,cost:46710,profit:32104,margin:34.5},
    {co:'GWP',pr:'AI Essentials',type:'B2B',period:'Jul',rev:3814,cost:1020,profit:2793,margin:62.1},
    {co:'Czech Caritas',pr:'AI Essentials',type:'B2B',period:'Sep–Oct',rev:4500,cost:1020,profit:3480,margin:77.3},
    {co:'GITA',pr:'Startup Intern',type:'B2G',period:'Sep–Oct',rev:60169,cost:41024,profit:19145,margin:26.8},
    {co:'Silk Hospitality',pr:'AI Essentials ×2',type:'B2B',period:'Oct–Nov',rev:6780,cost:2041,profit:4739,margin:59.2},
    {co:'GITA',pr:'Innovation from Mountains',type:'B2G',period:'Oct–Nov',rev:32881,cost:24778,profit:8103,margin:20.9},
    {co:'GITA',pr:'Hackathon',type:'B2G',period:'Nov',rev:25678,cost:19189,profit:6489,margin:21.4},
    {co:'Gagua Clinic',pr:'AI Essentials',type:'B2B',period:'Nov',rev:3644,cost:800,profit:2844,margin:66.1},
    {co:'RS (Gov)',pr:'IT Management',type:'B2G',period:'Oct–Dec',rev:23771,cost:7000,profit:16771,margin:59.8},
    {co:'Silk Hospitality',pr:'AI Essentials ×2',type:'B2B',period:'Nov',rev:6780,cost:1400,profit:5380,margin:67.2},
    {co:'Silk Hospitality',pr:'AI Essentials ×1',type:'B2B',period:'Dec',rev:3390,cost:600,profit:2790,margin:69.7},
  ],
  pipeline: [
    {id:1,name:'Startup Creation Course',type:'B2B',q:'Q3',rev:15000,cog:5000,stage:'Confirmed'},
    {id:2,name:'Vibe Coding',type:'B2B',q:'Q3',rev:8000,cog:2500,stage:'Planning'},
    {id:3,name:'GITA H2 Payment',type:'B2G',q:'Q3',rev:47883,cog:0,stage:'Confirmed'},
    {id:4,name:'Content Marketing Course',type:'B2B',q:'Q3',rev:10000,cog:3500,stage:'Planning'},
  ],
};

// ── helpers ──────────────────────────────────────────────────────────────────
const fmt = n => '₾ ' + Math.round(n).toLocaleString('en-US');
const pct = n => (+n).toFixed(1) + '%';
const ann = x => x.m.reduce((a,v)=>a+v,0);
const cpnl = c => {
  const rv=c.students*c.price, rx=rv/1.18, cs=c.lecturer+c.mat+c.mkt+c.zoom;
  return {rv,rx,cs,gp:rv-cs,net:rx-cs,mg:rx>0?(rx-cs)/rx*100:0};
};
const MarginBadge = ({v}) => {
  const cls = v>=50?'bg-emerald-900/40 text-emerald-300':v>=25?'bg-amber-900/40 text-amber-300':'bg-red-900/40 text-red-400';
  return <span className={`inline-block px-2 py-0.5 rounded text-xs font-bold ${cls}`}>{pct(v)}</span>;
};
const TypeTag = ({t}) => t==='B2G'
  ? <span className="text-xs font-bold bg-emerald-900/30 text-emerald-400 px-1.5 py-0.5 rounded">B2G</span>
  : <span className="text-xs font-bold bg-violet-900/30 text-violet-400 px-1.5 py-0.5 rounded">B2B</span>;
const StatusBadge = ({s}) => {
  const m={Paid:'bg-emerald-900/40 text-emerald-300',Active:'bg-amber-900/40 text-amber-300',Pending:'bg-red-900/40 text-red-400',Confirmed:'bg-violet-900/40 text-violet-300',Planning:'bg-slate-700 text-slate-300',Upcoming:'bg-slate-700 text-slate-300'};
  return <span className={`inline-block px-2 py-0.5 rounded text-xs font-bold ${m[s]||'bg-slate-700 text-slate-300'}`}>{s}</span>;
};
const MonthFilter = ({active,onChange}) => (
  <div className="flex gap-1.5 flex-wrap mb-4">
    {['All',...MN].map(m=>(
      <button key={m} onClick={()=>onChange(m)}
        className={`px-3 py-1 rounded-full text-xs font-medium border transition-all ${active===m?'bg-violet-600 text-white border-violet-600':'border-slate-700 text-slate-400 hover:border-violet-500 hover:text-white'}`}>
        {m}
      </button>
    ))}
  </div>
);
const Th = ({ch,right}) => <th className={`px-3 py-2.5 text-left text-[10px] font-semibold uppercase tracking-widest text-slate-500 bg-slate-800/60 border-b border-slate-700 ${right?'text-right':''}`}>{ch}</th>;
const Td = ({ch,right,cls=''}) => <td className={`px-3 py-2.5 border-b border-slate-800 text-sm ${right?'text-right font-mono':''} ${cls}`}>{ch}</td>;
const Card = ({label,value,sub,color='text-white'}) => (
  <div className="bg-slate-800 border border-slate-700 rounded-xl p-4">
    <div className="text-[10px] font-semibold uppercase tracking-widest text-slate-500 mb-2">{label}</div>
    <div className={`font-bold text-xl mb-1 ${color}`} style={{fontFamily:'Space Grotesk,sans-serif'}}>{value}</div>
    <div className="text-xs text-slate-400">{sub}</div>
  </div>
);
const Section = ({title,badge,action,children}) => (
  <div className="bg-slate-800 border border-slate-700 rounded-xl mb-4 overflow-hidden">
    <div className="flex items-center justify-between px-5 py-3.5 border-b border-slate-700">
      <div className="flex items-center gap-2 font-semibold text-sm" style={{fontFamily:'Space Grotesk,sans-serif'}}>
        {title}{badge&&<span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-700 text-slate-400 font-semibold">{badge}</span>}
      </div>
      {action}
    </div>
    {children}
  </div>
);
const TotRow = ({cols}) => (
  <tr className="bg-slate-700/60 font-bold text-sm" style={{fontFamily:'Space Grotesk,sans-serif'}}>
    {cols.map((c,i)=><td key={i} className={`px-3 py-2.5 ${c.right?'text-right font-mono':''}`}>{c.v}</td>)}
  </tr>
);
const AddBtn = ({onClick}) => (
  <button onClick={onClick} className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-violet-600 text-white hover:bg-violet-700 transition-all">+ Add</button>
);

// ── BAR CHART ────────────────────────────────────────────────────────────────
const BarChart = ({items}) => {
  const max = Math.max(...items.map(i=>i.v), 1);
  return (
    <div className="p-4">
      <div className="flex items-end gap-2 h-32 border-b border-slate-700 pb-1 mb-3">
        {items.map((it,i)=>(
          <div key={i} className="flex-1 flex flex-col items-center group relative">
            <div className="absolute -top-6 left-1/2 -translate-x-1/2 bg-slate-700 text-white text-[10px] px-1.5 py-0.5 rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-all pointer-events-none z-10" style={{fontFamily:'Space Grotesk'}}>
              {fmt(it.v)}
            </div>
            <div className="w-full rounded-t" style={{height:`${Math.max(it.v/max*120,3)}px`,background:it.c}}/>
          </div>
        ))}
      </div>
      <div className="flex flex-wrap gap-2">
        {items.map((it,i)=>(
          <div key={i} className="flex items-center gap-1.5 text-[11px] text-slate-400">
            <div className="w-2 h-2 rounded-sm" style={{background:it.c}}/>
            {it.l}: {fmt(it.v)}
          </div>
        ))}
      </div>
    </div>
  );
};

// ── PAGES ─────────────────────────────────────────────────────────────────────
function Dashboard({data}) {
  const mi = data.selMonth;
  const salM = data.salaries.reduce((a,x)=>a+x.m[mi],0);
  const subM = data.subs.reduce((a,x)=>a+x.m[mi],0);
  const salA = data.salaries.reduce((a,x)=>a+ann(x),0);
  const subA = data.subs.reduce((a,x)=>a+ann(x),0);
  const cRev = data.courses.reduce((a,c)=>a+cpnl(c).rv,0);
  const cNet = data.courses.reduce((a,c)=>a+cpnl(c).net,0);
  const cRx  = data.courses.reduce((a,c)=>a+cpnl(c).rx,0);
  const crpR = data.corp26.reduce((a,p)=>a+p.revenue,0);
  const crpC = data.corp26.reduce((a,p)=>a+p.cog,0);
  const crpP = crpR-crpC;
  const totR = cRev+crpR;
  const gitaR = data.courses.filter(c=>c.name.startsWith('GITA')).reduce((a,c)=>a+cpnl(c).rv,0);
  const ownR = cRev-gitaR;
  const b2bR = data.corp26.filter(x=>x.type==='B2B').reduce((a,p)=>a+p.revenue,0);
  const b2gR = data.corp26.filter(x=>x.type==='B2G').reduce((a,p)=>a+p.revenue,0);
  const lecT = data.courses.reduce((a,c)=>a+c.lecturer,0);
  const mktT = data.courses.reduce((a,c)=>a+c.mkt,0);
  const topC = [...data.courses].filter(c=>cpnl(c).rx>0).sort((a,b)=>cpnl(b).mg-cpnl(a).mg)[0];
  const wrstC = [...data.courses].filter(c=>cpnl(c).rx>0).sort((a,b)=>cpnl(a).mg-cpnl(b).mg)[0];
  const gitaDep = totR>0?(gitaR+b2gR)/totR*100:0;
  return (
    <div>
      <div className="mb-6"><div className="text-2xl font-bold mb-1" style={{fontFamily:'Space Grotesk'}}>Financial Overview</div><div className="text-slate-400 text-sm">2026 H1 · Courses + Corporate actuals</div></div>
      <div className="grid grid-cols-4 gap-3 mb-5">
        <Card label="H1 Total Revenue" value={fmt(totR)} sub={`Courses ${fmt(cRev)} · Corp ${fmt(crpR)}`} color="text-emerald-400"/>
        <Card label="Course Net Profit" value={fmt(cNet)} sub={`Margin ${pct(cRx>0?cNet/cRx*100:0)} · excl. VAT`} color={cNet>=0?'text-emerald-400':'text-red-400'}/>
        <Card label="Corporate Net Profit" value={fmt(crpP)} sub={`Margin ${pct(crpR>0?crpP/crpR*100:0)}`} color="text-emerald-400"/>
        <Card label={`Fixed Costs · ${MN[mi]}`} value={fmt(salM+subM)} sub={`${fmt(salA+subA)} full-year budget`} color="text-amber-400"/>
      </div>
      <div className="grid grid-cols-2 gap-4 mb-4">
        <Section title="📈 Revenue Mix">
          <BarChart items={[{l:'Own Courses',v:ownR,c:'#6c63ff'},{l:'GITA Courses',v:gitaR,c:'#a39df0'},{l:'Corp B2B',v:b2bR,c:'#00d4aa'},{l:'Corp B2G',v:b2gR,c:'#4ec9b0'}]}/>
        </Section>
        <Section title="💸 Cost Structure">
          <BarChart items={[{l:'Salaries',v:salA,c:'#ff5f7e'},{l:'Admin+Subs',v:subA,c:'#a39df0'},{l:'Lecturer Fees',v:lecT,c:'#6c63ff'},{l:'Advertising',v:mktT,c:'#ffa94d'},{l:'Corp COG',v:crpC,c:'#00d4aa'}]}/>
        </Section>
      </div>
      <Section title="💡 CFO Insights">
        <div className="p-4 space-y-2">
          {[
            ['🏆',`Best margin: ${topC?.name} (${topC?.month}) at ${pct(cpnl(topC||{students:0,price:0,lecturer:0,mat:0,mkt:0,zoom:0}).mg)}. Low ad spend + strong cohort.`],
            ['⚠️',`GITA + B2G = ${pct(gitaDep)} of H1 revenue. Audit (₾28,400) pending collection — watch vs. ${fmt(salM+subM)}/month fixed.`],
            ['📉',`Lowest margin: ${wrstC?.name} (${wrstC?.month}). Set a minimum enrollment threshold before launching.`],
            ['💼',`2026 salary budget: ${fmt(salA)}. CEO = ${pct(8929*12/salA*100)} of total payroll. H1 fixed budget: ${fmt((salA+subA)/2)}.`],
          ].map(([icon,text],i)=>(
            <div key={i} className="flex gap-3 bg-slate-700/40 border border-slate-700 rounded-lg p-3">
              <span className="text-base">{icon}</span>
              <span className="text-xs text-slate-300 leading-relaxed">{text}</span>
            </div>
          ))}
        </div>
      </Section>
    </div>
  );
}

function FixedCosts({data,setData}) {
  const mi = data.selMonth;
  const salM = data.salaries.reduce((a,x)=>a+x.m[mi],0);
  const subM = data.subs.reduce((a,x)=>a+x.m[mi],0);
  const salA = data.salaries.reduce((a,x)=>a+ann(x),0);
  const subA = data.subs.reduce((a,x)=>a+ann(x),0);
  return (
    <div>
      <div className="mb-6"><div className="text-2xl font-bold mb-1" style={{fontFamily:'Space Grotesk'}}>📌 Fixed Costs</div><div className="text-slate-400 text-sm">2026 budget · select month to view</div></div>
      <div className="flex gap-1.5 flex-wrap mb-4">
        {MN.map((m,i)=>(
          <button key={m} onClick={()=>setData(d=>({...d,selMonth:i}))}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-all ${i===mi?'bg-violet-600 text-white border-violet-600':'border-slate-700 text-slate-400 hover:border-violet-500 hover:text-white'}`}>{m}</button>
        ))}
      </div>
      <Section title="👥 Salaries" badge={`${data.salaries.filter(x=>x.m[mi]>0).length} active`}>
        <table className="w-full">
          <thead><tr><Th ch="Name / Role"/><Th ch={`${MN[mi]} (₾)`} right/><Th ch="Annual Budget (₾)" right/><Th ch="Active Months" right/></tr></thead>
          <tbody>
            {data.salaries.map(s=>(
              <tr key={s.id} className={`hover:bg-slate-700/30 ${s.m[mi]===0?'opacity-40':''}`}>
                <Td ch={s.name}/>
                <Td ch={s.m[mi]>0?<span className="font-semibold text-white">{fmt(s.m[mi])}</span>:'—'} right/>
                <Td ch={fmt(ann(s))} right/>
                <Td ch={`${s.m.filter(v=>v>0).length} mo`} right cls="text-slate-400 text-xs"/>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="flex justify-between items-center px-4 py-3 bg-slate-700/50 text-sm font-semibold" style={{fontFamily:'Space Grotesk'}}>
          <span>Total Salaries</span>
          <span>{fmt(salM)} <span className="text-slate-400 font-normal text-xs">/ {fmt(salA)} annual</span></span>
        </div>
      </Section>
      <Section title="🏢 Admin & Subscriptions" badge={`${data.subs.length} items`}>
        <table className="w-full">
          <thead><tr><Th ch="Item"/><Th ch={`${MN[mi]} (₾)`} right/><Th ch="Annual Budget (₾)" right/></tr></thead>
          <tbody>
            {data.subs.map(s=>(
              <tr key={s.id} className="hover:bg-slate-700/30">
                <Td ch={s.name}/>
                <Td ch={fmt(s.m[mi])} right/>
                <Td ch={fmt(ann(s))} right/>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="flex justify-between items-center px-4 py-3 bg-slate-700/50 text-sm font-semibold" style={{fontFamily:'Space Grotesk'}}>
          <span>Total Admin & Subs</span>
          <span>{fmt(subM)} <span className="text-slate-400 font-normal text-xs">/ {fmt(subA)} annual</span></span>
        </div>
      </Section>
      <div className="flex justify-between items-center px-5 py-4 bg-slate-800 border border-slate-700 rounded-xl text-base font-bold" style={{fontFamily:'Space Grotesk'}}>
        <span>🔒 Total Fixed Costs · {MN[mi]}</span>
        <span className="text-amber-400">{fmt(salM+subM)}</span>
      </div>
    </div>
  );
}

function CoursesPage({data,setData}) {
  const [filterM, setFilterM] = useState('All');
  const [detId, setDetId] = useState(null);
  const filtered = filterM==='All' ? data.courses : data.courses.filter(c=>c.month===filterM);
  const tR=filtered.reduce((a,c)=>a+cpnl(c).rv,0);
  const tC=filtered.reduce((a,c)=>a+cpnl(c).cs,0);
  const tG=tR-tC, tN=filtered.reduce((a,c)=>a+cpnl(c).net,0);
  const tRx=filtered.reduce((a,c)=>a+cpnl(c).rx,0);
  const det = detId ? data.courses.find(c=>c.id===detId) : null;
  return (
    <div>
      <div className="mb-5"><div className="text-2xl font-bold mb-1" style={{fontFamily:'Space Grotesk'}}>🎓 Courses P&L</div><div className="text-slate-400 text-sm">2026 actuals · Net Profit = Revenue excl. VAT − Costs · click row for detail</div></div>
      <MonthFilter active={filterM} onChange={m=>{setFilterM(m);setDetId(null);}}/>
      <Section title="Programs" badge={`${filtered.length}`} action={<AddBtn onClick={()=>setData(d=>({...d,courses:[...d.courses,{id:Date.now(),name:'New Course',month:'Q3',students:10,price:1400,lecturer:2000,mat:400,mkt:800,zoom:40}]}))}/>}>
        <div className="overflow-x-auto">
        <table className="w-full min-w-[800px]">
          <thead><tr><Th ch="Program"/><Th ch="Month"/><Th ch="Students" right/><Th ch="Price ₾" right/><Th ch="Revenue ₾" right/><Th ch="Costs ₾" right/><Th ch="Gross Profit ₾" right/><Th ch="Net Profit ₾" right/><Th ch="Margin" right/><Th ch=""/></tr></thead>
          <tbody>
            {filtered.map(c=>{
              const {rv,cs,gp,net,mg}=cpnl(c);
              return (
                <tr key={c.id} onClick={()=>setDetId(detId===c.id?null:c.id)} className="cursor-pointer hover:bg-slate-700/40">
                  <Td ch={c.name}/>
                  <Td ch={<span className="text-slate-400 text-xs">{c.month}</span>}/>
                  <Td ch={c.students} right/>
                  <Td ch={c.price} right/>
                  <Td ch={fmt(rv)} right/>
                  <Td ch={fmt(cs)} right/>
                  <Td ch={<span className={gp>=0?'text-emerald-400':'text-red-400'}>{fmt(gp)}</span>} right/>
                  <Td ch={<span className={`font-semibold ${net>=0?'text-emerald-400':'text-red-400'}`}>{fmt(net)}</span>} right/>
                  <Td ch={<MarginBadge v={mg}/>} right/>
                  <Td ch={<button onClick={e=>{e.stopPropagation();setData(d=>({...d,courses:d.courses.filter(x=>x.id!==c.id)}));}} className="text-red-400 text-xs hover:text-red-300 px-2">✕</button>}/>
                </tr>
              );
            })}
          </tbody>
          <tfoot>
            <TotRow cols={[{v:'TOTAL'},{v:''},{v:''},{v:''},{v:fmt(tR),right:true},{v:fmt(tC),right:true},{v:fmt(tG),right:true},{v:<span className={tN>=0?'text-emerald-400':'text-red-400'}>{fmt(tN)}</span>,right:true},{v:<MarginBadge v={tRx>0?tN/tRx*100:0}/>,right:true},{v:''}]}/>
          </tfoot>
        </table>
        </div>
      </Section>
      {det && (()=>{
        const rv=det.students*det.price, rx=rv/1.18, tot=det.lecturer+det.mat+det.mkt+det.zoom, net=rx-tot;
        return (
          <div className="bg-slate-700/40 border border-slate-700 rounded-xl p-4 mt-2">
            <div className="font-semibold mb-3" style={{fontFamily:'Space Grotesk'}}>📋 {det.name} ({det.month}) — Cost Detail</div>
            <table className="w-full max-w-lg text-sm">
              <thead><tr><Th ch="Category"/><Th ch="₾" right/><Th ch="% of Rev excl. VAT" right/></tr></thead>
              <tbody>
                {[['Lecturer Fee',det.lecturer],['Merch & Materials',det.mat],['Advertising',det.mkt],['Zoom',det.zoom]].map(([label,val])=>(
                  <tr key={label} className="hover:bg-slate-700/30"><Td ch={label}/><Td ch={fmt(val)} right/><Td ch={rx>0?pct(val/rx*100):'—'} right/></tr>
                ))}
                <TotRow cols={[{v:'Total Costs'},{v:fmt(tot),right:true},{v:rx>0?pct(tot/rx*100):'—',right:true}]}/>
                <tr className="text-slate-400 text-xs"><Td ch="Revenue incl. VAT"/><Td ch={fmt(rv)} right/><Td ch="—" right/></tr>
                <tr className="text-slate-400 text-xs"><Td ch="VAT (18%)"/><Td ch={<span className="text-red-400">− {fmt(rv-rx)}</span>} right/><Td ch="—" right/></tr>
                <tr><Td ch="Revenue excl. VAT" cls="text-slate-300"/><Td ch={fmt(rx)} right/><Td ch="100%" right/></tr>
                <tr><Td ch={<span className={`font-bold ${net>=0?'text-emerald-400':'text-red-400'}`}>Net Profit</span>}/><Td ch={<span className={`font-bold ${net>=0?'text-emerald-400':'text-red-400'}`}>{fmt(net)}</span>} right/><Td ch={<MarginBadge v={rx>0?net/rx*100:0}/>} right/></tr>
              </tbody>
            </table>
          </div>
        );
      })()}
    </div>
  );
}

function CorporatePage({data,setData}) {
  const [tab,setTab] = useState('26');
  const tR26=data.corp26.reduce((a,p)=>a+p.revenue,0);
  const tC26=data.corp26.reduce((a,p)=>a+p.cog,0);
  const tP26=tR26-tC26;
  const ppR=data.pipeline.reduce((a,p)=>a+p.rev,0);
  const b2b=data.corp26.filter(p=>p.type==='B2B').reduce((a,p)=>a+p.revenue,0);
  const b2g=data.corp26.filter(p=>p.type==='B2G').reduce((a,p)=>a+p.revenue,0);
  return (
    <div>
      <div className="mb-5"><div className="text-2xl font-bold mb-1" style={{fontFamily:'Space Grotesk'}}>🏢 Corporate Projects</div><div className="text-slate-400 text-sm">B2B + B2G · 2026 actuals + 2025 history</div></div>
      <div className="grid grid-cols-3 gap-3 mb-5">
        <Card label="2026 Revenue" value={fmt(tR26)} sub={`B2B ${fmt(b2b)} · B2G ${fmt(b2g)}`} color="text-emerald-400"/>
        <Card label="2026 Net Profit" value={fmt(tP26)} sub={`Margin ${pct(tR26>0?tP26/tR26*100:0)}`} color="text-emerald-400"/>
        <Card label="Q3–Q4 Pipeline" value={fmt(ppR)} sub={`${data.pipeline.length} projects incl. GITA H2`} color="text-amber-400"/>
      </div>
      <div className="flex border-b border-slate-700 mb-4">
        {[['26','2026 Actuals'],['25','2025 History'],['pp','Pipeline']].map(([id,label])=>(
          <button key={id} onClick={()=>setTab(id)} className={`px-5 py-2.5 text-sm font-medium border-b-2 transition-all -mb-px ${tab===id?'border-violet-500 text-violet-400':'border-transparent text-slate-400 hover:text-white'}`}>{label}</button>
        ))}
      </div>
      {tab==='26' && (
        <Section title="2026 Projects" badge={`${data.corp26.length}`} action={<AddBtn onClick={()=>setData(d=>({...d,corp26:[...d.corp26,{id:Date.now(),name:'New Project',type:'B2B',period:'Q3',revenue:0,cog:0,status:'Upcoming'}]}))}/>}>
          <table className="w-full">
            <thead><tr><Th ch="Project"/><Th ch="Type"/><Th ch="Period"/><Th ch="Revenue ₾" right/><Th ch="COG ₾" right/><Th ch="Net Profit ₾" right/><Th ch="Margin" right/><Th ch="Status"/><Th ch=""/></tr></thead>
            <tbody>
              {data.corp26.map(p=>{const pf=p.revenue-p.cog,mg=p.revenue>0?pf/p.revenue*100:0;return(
                <tr key={p.id} className="hover:bg-slate-700/30">
                  <Td ch={p.name}/>
                  <Td ch={<TypeTag t={p.type}/>}/>
                  <Td ch={<span className="text-slate-400 text-xs">{p.period}</span>}/>
                  <Td ch={fmt(p.revenue)} right/>
                  <Td ch={fmt(p.cog)} right/>
                  <Td ch={<span className={`font-semibold ${pf>=0?'text-emerald-400':'text-red-400'}`}>{fmt(pf)}</span>} right/>
                  <Td ch={<MarginBadge v={mg}/>} right/>
                  <Td ch={<StatusBadge s={p.status}/>}/>
                  <Td ch={<button onClick={()=>setData(d=>({...d,corp26:d.corp26.filter(x=>x.id!==p.id)}))} className="text-red-400 text-xs hover:text-red-300 px-2">✕</button>}/>
                </tr>
              );})}
            </tbody>
            <tfoot><TotRow cols={[{v:'TOTAL 2026'},{v:''},{v:''},{v:fmt(tR26),right:true},{v:fmt(tC26),right:true},{v:fmt(tP26),right:true},{v:<MarginBadge v={tR26>0?tP26/tR26*100:0}/>,right:true},{v:''},{v:''}]}/></tfoot>
          </table>
        </Section>
      )}
      {tab==='25' && (()=>{
        const t25r=data.corp25.reduce((a,p)=>a+p.rev,0),t25c=data.corp25.reduce((a,p)=>a+p.cost,0),t25p=data.corp25.reduce((a,p)=>a+p.profit,0);
        return (
          <Section title="2025 Completed" badge="13 projects">
            <table className="w-full">
              <thead><tr><Th ch="Company"/><Th ch="Project"/><Th ch="Type"/><Th ch="Period"/><Th ch="Revenue ₾" right/><Th ch="Cost ₾" right/><Th ch="Profit ₾" right/><Th ch="Margin" right/></tr></thead>
              <tbody>{data.corp25.map((p,i)=>(
                <tr key={i} className="hover:bg-slate-700/30">
                  <Td ch={p.co}/><Td ch={p.pr}/><Td ch={<TypeTag t={p.type}/>}/><Td ch={<span className="text-slate-400 text-xs">{p.period}</span>}/>
                  <Td ch={fmt(p.rev)} right/><Td ch={fmt(p.cost)} right/>
                  <Td ch={<span className="text-emerald-400">{fmt(p.profit)}</span>} right/>
                  <Td ch={<MarginBadge v={p.margin}/>} right/>
                </tr>
              ))}</tbody>
              <tfoot><TotRow cols={[{v:'TOTAL 2025'},{v:''},{v:''},{v:''},{v:fmt(t25r),right:true},{v:fmt(t25c),right:true},{v:fmt(t25p),right:true},{v:<MarginBadge v={t25r>0?t25p/t25r*100:0}/>,right:true}]}/></tfoot>
            </table>
          </Section>
        );
      })()}
      {tab==='pp' && (()=>{
        const tpr=data.pipeline.reduce((a,p)=>a+p.rev,0),tpc=data.pipeline.reduce((a,p)=>a+p.cog,0),tpp=tpr-tpc;
        return (
          <Section title="Q3–Q4 Pipeline" badge={`${data.pipeline.length}`} action={<AddBtn onClick={()=>setData(d=>({...d,pipeline:[...d.pipeline,{id:Date.now(),name:'New Project',type:'B2B',q:'Q3',rev:0,cog:0,stage:'Planning'}]}))}/>}>
            <table className="w-full">
              <thead><tr><Th ch="Project"/><Th ch="Type"/><Th ch="Quarter"/><Th ch="Est. Revenue ₾" right/><Th ch="Est. COG ₾" right/><Th ch="Est. Profit ₾" right/><Th ch="Margin" right/><Th ch="Stage"/><Th ch=""/></tr></thead>
              <tbody>{data.pipeline.map(p=>{const pf=p.rev-p.cog,mg=p.rev>0?pf/p.rev*100:0;return(
                <tr key={p.id} className="hover:bg-slate-700/30">
                  <Td ch={p.name}/><Td ch={<TypeTag t={p.type}/>}/><Td ch={<span className="text-slate-400 text-xs">{p.q}</span>}/>
                  <Td ch={fmt(p.rev)} right/><Td ch={fmt(p.cog)} right/>
                  <Td ch={<span className={pf>=0?'text-emerald-400':'text-red-400'}>{fmt(pf)}</span>} right/>
                  <Td ch={<MarginBadge v={mg}/>} right/>
                  <Td ch={<StatusBadge s={p.stage}/>}/>
                  <Td ch={<button onClick={()=>setData(d=>({...d,pipeline:d.pipeline.filter(x=>x.id!==p.id)}))} className="text-red-400 text-xs hover:text-red-300 px-2">✕</button>}/>
                </tr>
              );})}
              </tbody>
              <tfoot><TotRow cols={[{v:'PIPELINE'},{v:''},{v:''},{v:fmt(tpr),right:true},{v:fmt(tpc),right:true},{v:fmt(tpp),right:true},{v:<MarginBadge v={tpr>0?tpp/tpr*100:0}/>,right:true},{v:''},{v:''}]}/></tfoot>
            </table>
          </Section>
        );
      })()}
    </div>
  );
}

// ── APP ───────────────────────────────────────────────────────────────────────
export default function App() {
  const [auth, setAuth] = useState(() => sessionStorage.getItem('cfo_auth') === '1');
  const [page, setPage] = useState('db');
  const [data, setData] = useState({...INIT, selMonth:0});

  if (!auth) {
    return <Login onAuth={() => { sessionStorage.setItem('cfo_auth', '1'); setAuth(true); }} />;
  }

  const pages = [
    {id:'db',label:'📊 Dashboard'},
    {id:'fx',label:'📌 Fixed Costs'},
    {id:'co',label:'🎓 Courses P&L'},
    {id:'cp',label:'🏢 Corporate'},
  ];

  return (
    <div className="flex min-h-screen" style={{background:'#0f1117',color:'#e8eaf0',fontFamily:'Inter,sans-serif'}}>
      {/* Sidebar */}
      <nav className="w-48 flex-shrink-0 flex flex-col sticky top-0 h-screen" style={{background:'#1a1d27',borderRight:'1px solid #2e3350'}}>
        <div className="px-4 py-5 border-b" style={{borderColor:'#2e3350'}}>
          <div className="text-[10px] font-semibold tracking-widest text-slate-500 uppercase mb-1">Commschool</div>
          <div className="text-lg font-bold" style={{fontFamily:'Space Grotesk'}}>Digital <span style={{color:'#6c63ff'}}>CFO</span></div>
        </div>
        <div className="py-2 flex-1">
          {pages.map(p=>(
            <button key={p.id} onClick={()=>setPage(p.id)}
              className={`w-full flex items-center gap-2 px-4 py-2.5 text-sm font-medium transition-all border-l-2 text-left ${page===p.id?'text-violet-400 border-violet-500 bg-slate-700/40':'text-slate-400 border-transparent hover:text-white hover:bg-slate-700/20'}`}>
              {p.label}
            </button>
          ))}
        </div>
        <div className="px-4 py-4 border-t" style={{borderColor:'#2e3350'}}>
          <div className="text-[10px] text-slate-600 leading-relaxed mb-3">₾ GEL · 2026<br/>H1 actuals imported</div>
          <button
            onClick={() => { sessionStorage.removeItem('cfo_auth'); setAuth(false); }}
            className="w-full text-[11px] font-medium text-slate-500 hover:text-red-400 transition-all py-1.5 rounded-lg border border-slate-700 hover:border-red-800">
            🔒 Lock
          </button>
        </div>
      </nav>
      {/* Main */}
      <main className="flex-1 overflow-auto p-7">
        {page==='db' && <Dashboard data={data}/>}
        {page==='fx' && <FixedCosts data={data} setData={setData}/>}
        {page==='co' && <CoursesPage data={data} setData={setData}/>}
        {page==='cp' && <CorporatePage data={data} setData={setData}/>}
      </main>
    </div>
  );
}
