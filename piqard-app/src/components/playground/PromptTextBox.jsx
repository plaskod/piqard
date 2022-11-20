import React, { useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import Button from "../Button";

import './PromptTextBox.css'


function PromptTextBox({promptName, promptTemplate, handleSetPromptTemplate}){
   
    return(
        <div className="prompt-text-box-container">
            <Container>
                <h5 className="prompt-label">Prompt: {promptName}</h5>
            </Container>
            <textarea type="text"
                      className="prompt-text-box"
                      disabled={promptName === 'custom_prompt' ? false : true}
                      value={promptTemplate}
                      onChange={(event)=>(handleSetPromptTemplate(event))}></textarea >
            <Container className="center">
                <Button label='Save prompt'/>
            </Container>
        </div>
    )
}



export default PromptTextBox;;