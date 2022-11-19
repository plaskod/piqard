import React, { useState } from "react";
import { Container, Row, Col } from "react-bootstrap";

import './Button.css'

function Button({label, name, onClick}){
   
    return(
        <button className="custom-button" name={name} onClick={onClick}>
            {label}
        </button>
    )
}



export default Button;;