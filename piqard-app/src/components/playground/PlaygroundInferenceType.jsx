import React from "react";
import { Container, Row, Col, Spinner } from "react-bootstrap";
import PlaygroundBenchmarkResult from "./PlaygroundBenchmarkResult";
import PlaygroundBenchmarkSelect from "./PlaygroundBenchmarkSelect";

import './PlaygroundInferenceType.css'
import PlaygroundQuestion from "./PlaygroundQuestion";
import PlaygroundQuestionResult from "./PlaygroundQuestionResult";


function PlaygroundInferenceType({isLoading, inferenceType, handleSetInferenceType, question, handleSetQuestion, handleQueryPIQARD, result}){
    
    return(
        <div className="playground-right-container">
            <Container fluid className="tabs-options-container">
                <Row>
                    <Col md={3} 
                         className={`tab-option${inferenceType === "question" ? "-active" : ""} center`}
                         onClick={()=>(handleSetInferenceType("question"))}>Question</Col>
                    <Col md={3} 
                         className={`tab-option${inferenceType === "benchmark" ? "-active" : ""} center`}
                         onClick={()=>(handleSetInferenceType("benchmark"))}>Benchmark</Col>
                    <Col md={3} className="tab-option-disabled"></Col>
                    <Col md={3} className="tab-option-disabled"></Col>
                </Row>
            </Container>
            {inferenceType === "question" && (
                <>
                <PlaygroundQuestion
                    question={question}
                    handleSetQuestion={handleSetQuestion}
                    handleQueryPIQARD={handleQueryPIQARD} />
                <PlaygroundQuestionResult isLoading={isLoading} result={result} />
                </>
            )}

            {inferenceType === "benchmark" && (
                <>
                <PlaygroundBenchmarkSelect
                    question={question}
                    handleSetQuestion={handleSetQuestion}
                    handleQueryPIQARD={handleQueryPIQARD} />
                <PlaygroundBenchmarkResult isLoadig={isLoading} result={result}/>
                </>
            )}  
        </div>

    )
}


export default PlaygroundInferenceType;