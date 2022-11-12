import React, { useState } from "react";
import { Container, Row, Col } from "react-bootstrap";

import './Select.css'

function Select({label, options, name, value, onChange}){
   
    return(
        <div className="select-container">
            <label className="select-label">{label}</label>
            <select className="select-component" name={name} value={value} onChange={onChange}>
                {options && options.map((option) =>(
                    <option value={option} selected={option === value}>{option}</option>
                ))}
            </select>
        </div>
    )
}



export default Select;;