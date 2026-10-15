import React from "react";
export function Tag({tone="lavender",children}){
  const c=tone==="navy"?["var(--vibz-navy)","var(--vibz-white)"]:tone==="outline"?["transparent","var(--vibz-navy)"]:["var(--vibz-lavender)","var(--vibz-navy)"];
  return <span style={{display:"inline-block",background:c[0],color:c[1],border:tone==="outline"?"1px solid var(--border-strong)":"none",font:"500 11px/1 var(--font-sans)",letterSpacing:".2em",textTransform:"uppercase",padding:"8px 14px",borderRadius:"var(--radius-pill)"}}>{children}</span>;
}
