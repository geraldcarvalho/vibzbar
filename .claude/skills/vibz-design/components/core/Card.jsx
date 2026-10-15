import React from "react";
export function Card({tone="light",eyebrow,title,children,style}){
  const dark=tone==="dark";
  return <div style={{background:dark?"var(--vibz-navy)":"var(--vibz-white)",color:dark?"var(--vibz-white)":"var(--vibz-navy)",borderRadius:"var(--radius-lg)",padding:"var(--space-6)",boxShadow:dark?"none":"var(--shadow-card)",border:dark?"none":"1px solid var(--border-subtle)",...style}}>
    {eyebrow&&<div style={{font:"500 12px/1 var(--font-sans)",letterSpacing:".22em",textTransform:"uppercase",opacity:.8,marginBottom:16}}>{eyebrow}</div>}
    {title&&<div style={{font:"700 32px/1.1 var(--font-serif-display)",letterSpacing:"-.02em",marginBottom:12}}>{title}</div>}
    <div style={{font:"400 16px/1.55 var(--font-sans)"}}>{children}</div>
  </div>;
}
