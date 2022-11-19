import React, { useEffect, useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import './PlaygroundResult.css'


function PlaygroundResult({isBenchmark, result}){   
    return(
        <>
            <Container className="result-label-container">
                <h5 className="label">Result:</h5>
            </Container>
            <Container className="result-container">
                {isBenchmark ? (
                    <div className="result-scores-container">
                        <h5>Scores:</h5>
                        <ul>
                        {Object.entries(result).map(([name, value])=> (
                            <li><span className="score-name">{name}</span> = {value.toFixed(5)}</li>
                            )
                        )}
                        </ul>
                    </div>
                ) : (
                    <>
                    <h6>Answer:</h6>
                    <Container>  
                        <div className="question-answer">  
                            {result.answer}
                        </div>
                    </Container>
                    <h6>Retrieved context:</h6>
                    <Container>
                        <div className="question-contex">
                            {result.context}
                        </div>
                    </Container>
                    </>
                )}
            </Container>
        </>
    )
}



export default PlaygroundResult;