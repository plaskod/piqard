import React from "react";
import { Container } from "react-bootstrap";
import benchmarkExamples from "../../data/benchamarkExamples";
import Button from "../Button";

import Select from "../Select";
import './PlaygroundBenchmarkSelect.css'


function PlaygroundBenchmarkSelect({question, handleSetQuestion, handleQueryPIQARD}){

    return(
        <>
            <Container className="question-container">
                <label className="label">Benchmark:</label>
                <Select name="question"
                        value={question}
                        options={benchmarkExamples}
                        onChange={(event) => (handleSetQuestion(event))}/>
                <Container className="center">
                    <Button label="Test" onClick={(e) => (handleQueryPIQARD(e))}/>
                </Container>
            </Container>
        </>
    )
}

export default PlaygroundBenchmarkSelect;