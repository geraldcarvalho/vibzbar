import * as React from "react";
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>{variant?:"primary"|"secondary"|"ghost";size?:"sm"|"md"|"lg";disabled?:boolean;}
export function Button(props:ButtonProps):JSX.Element;
