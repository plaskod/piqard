import React, { useEffect, useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import benchmarkExamples from "../../data/benchamarkExamples";
import Button from "../Button";

import Select from "../Select";
import './PlaygroundQuestion.css'


function PlaygroundQuestion({isCustomQuestion, handleIsCustomQuestion, question, handleSetQuestion}){

    return(
        <>
            <Container>
                <h5 className="label">Question:</h5>
            </Container>
            <Container className="question-container">
                <Container className="question-checkbox-container">
                    <label>Custom</label>
                    <input type='checkbox'
                           className="question-checkbox"
                           checked={isCustomQuestion}
                           onChange={() => (handleIsCustomQuestion(!isCustomQuestion))}></input>
                </Container>
                <Container>
                    {isCustomQuestion ? (
                        <div >
                            <input className="question-input"  value={question} onChange={(event) => (handleSetQuestion(event))}/>
                        </div>    
                    ) : (
                        <Select name="question"
                                value={question}
                                options={benchmarkExamples}
                                onChange={(event) => (handleSetQuestion(event))}/>
                    )}
                </Container>
                <Container className="center">
                    <Button label="Run"/>
                </Container>
            </Container>
        </>
    )
}



export default PlaygroundQuestion;