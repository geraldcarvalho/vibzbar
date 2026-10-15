import React from "react";
export function Input({label,style,...rest}){
  return <label style={{display:"block",font:"500 12px/1 var(--font-sans)",letterSpacing:".18em",textTransform:"uppercase",color:"var(--vibz-navy)"}}>{label}
    <input {...rest} style={{display:"block",width:"100%",boxSizing:"border-box",marginTop:10,padding:"14px 16px",font:"400 16px/1.2 var(--font-sans)",letterSpacing:0,textTransform:"none",color:"var(--vibz-navy)",background:"var(--vibz-white)",border:"1px solid var(--border-strong)",borderRadius:"var(--radius-md)",boxShadow:"var(--shadow-deboss)",outline:"none",...style}}/>
  </label>;
}
