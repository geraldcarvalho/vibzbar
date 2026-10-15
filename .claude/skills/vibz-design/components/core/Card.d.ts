import * as React from "react";
export interface CardProps{tone?:"light"|"dark";eyebrow?:string;title?:string;children?:React.ReactNode;style?:React.CSSProperties;}
export function Card(props:CardProps):JSX.Element;
