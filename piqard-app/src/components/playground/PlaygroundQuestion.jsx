import React, { useEffect, useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import benchmarkExamples from "../../data/benchamarkExamples";
import Button from "../Button";

import Select from "../Select";
import './PlaygroundQuestion.css'


function PlaygroundQuestion({isBenchmark, handleSetIsBenchmark, question, handleSetQuestion, handleQueryPIQARD}){

    return(
        <>
            <Container>
                <h5 className="label">Question:</h5>
            </Container>
            <Container className="question-container">
                <Container className="question-checkbox-container">
                    <label>Benchmark</label>
                    <input type='checkbox'
                           className="question-checkbox"
                           checked={isBenchmark}
                           onChange={() => (handleSetIsBenchmark(!isBenchmark))}></input>
                </Container>
                <Container>
                    {isBenchmark ? (
                        <Select name="question"
                                value={question}
                                options={benchmarkExamples}
                                onChange={(event) => (handleSetQuestion(event))}/>
                    ) : (
                        <div >
                            <input className="question-input"  value={question} onChange={(event) => (handleSetQuestion(event))}/>
                        </div>    
                    )
                    }
                </Container>
                <Container className="center">
                    <Button label="Run" onClick={(e) => (handleQueryPIQARD(e))}/>
                </Container>
            </Container>
        </>
    )
}



export default PlaygroundQuestion;