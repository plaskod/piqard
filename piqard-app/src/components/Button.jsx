import React, { useState } from "react";
import { Container, Row, Col } from "react-bootstrap";

import './Button.css'

function Button({label, name, onChange}){
   
    return(
        <button className="custom-button" name={name} onChange={onChange}>
            {label}
        </button>
    )
}



export default Button;;