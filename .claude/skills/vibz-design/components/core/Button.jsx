import React from "react";
export function Button({variant="primary",size="md",disabled=false,children,style,...rest}){
  const pad=size==="sm"?"10px 20px":size==="lg"?"18px 40px":"14px 30px";
  const v={
    primary:{background:"var(--vibz-navy)",color:"var(--vibz-white)",border:"1px solid var(--vibz-navy)",boxShadow:"var(--shadow-emboss)"},
    secondary:{background:"transparent",color:"var(--vibz-navy)",border:"1px solid var(--border-strong)"},
    ghost:{background:"transparent",color:"var(--vibz-navy)",border:"1px solid transparent",textDecoration:"underline",textUnderlineOffset:5}
  }[variant];
  return <button disabled={disabled} {...rest} style={{font:"500 13px/1 var(--font-sans)",letterSpacing:".16em",textTransform:"uppercase",padding:pad,borderRadius:"var(--radius-pill)",cursor:disabled?"not-allowed":"pointer",opacity:disabled?.45:1,transition:"all var(--dur-fast) var(--ease-calm)",...v,...style}}>{children}</button>;
}
