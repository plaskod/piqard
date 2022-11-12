import React, { useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import Button from "../Button";

import './PromptTextBox.css'


function PromptTextBox({prompt}){
   
    return(
        <div className="prompt-text-box-container">
            <Container>
                <h5 className="prompt-label">Prompt: {prompt}</h5>
            </Container>
            <textarea  type="text" className="prompt-text-box" disabled={prompt === 'custom_prompt' ? false : true}></textarea >
            <Container className="center">
                <Button label='Save prompt'/>
            </Container>
        </div>
    )
}



export default PromptTextBox;;