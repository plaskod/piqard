import React from "react";
import { Container }from "react-bootstrap";
import Button from "../Button";
import './PlaygroundQuestion.css'


function PlaygroundQuestion({question, handleSetQuestion, handleQueryPIQARD}){

    return(
        <Container fluid className="question-container">
                <label className="label">Question:</label>
                <div >
                    <input className="question-input"  value={question} onChange={(event) => (handleSetQuestion(event))}/>
                </div>    
            <Container className="center">
                <Button label="Query" onClick={(e) => (handleQueryPIQARD(e))}/>
            </Container>
        </Container>
    )
}



export default PlaygroundQuestion;