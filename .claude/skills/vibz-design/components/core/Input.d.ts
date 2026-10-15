import * as React from "react";
export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement>{label?:string;}
export function Input(props:InputProps):JSX.Element;
