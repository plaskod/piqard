import React, { useState } from "react";
import { Container, Row, Col } from "react-bootstrap";

import './Button.css'

function Button({label, name, className, onClick}){
    return(
        <button name={name} onClick={onClick} className={!className ? "custom-button" : className}>
            {label}
        </button>
    )
}



export default Button;;