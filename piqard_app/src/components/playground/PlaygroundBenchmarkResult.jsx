import React, { useEffect, useState } from "react";
import { Container, Row, Col, Spinner } from "react-bootstrap";
import './PlaygroundBenchmarkResult.css'


function PlaygroundBenchmarkResult({isLoading, result}){   
    return(
        <>
            <Container className="result-label-container">
                <h5 className="label">Result:</h5>
            </Container>
            {isLoading ? (<Container className="center">
                            <Spinner />
                         </Container>) : (
                        <Container className="result-container">
                            <div className="result-scores-container">
                                <label className="label">Scores:</label>
                                <ul>
                                {Object.entries(result).map(([name, value])=> (
                                    <li><span className="score-name">{name}</span> = {value.toFixed(5)}</li>
                                    )
                                )}
                                </ul>
                            </div>
                        </Container>)}
        </>
    )
}



export default PlaygroundBenchmarkResult;