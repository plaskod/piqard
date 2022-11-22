import React from "react";
import { Container, Spinner } from "react-bootstrap";
import './PlaygroundQuestionResult.css'


function PlaygroundQuestionResult({isLoading, result}){   
    return(
        <>
            <Container className="result-label-container">
                <h5 className="label">Result:</h5>
            </Container>
            {isLoading ? (<Container className="center">
                            <Spinner />
                         </Container>) : (
                        <Container className="result-container">
                        <label className="label">Answer:</label>
                        <Container>  
                            <div className="question-answer">  
                                {result.answer}
                            </div>
                        </Container>
                        <label className="label">Retrieved context:</label>
                        <Container>
                            <div className="question-contex">
                            <Container>
                                <ul>
                                    {result.context.map((doc) => (
                                        <li>{doc}</li>
                                    ))}
                                </ul>
                            </Container>
                            </div>
                        </Container>
                    </Container>
            )}
           
        </>
    )
}



export default PlaygroundQuestionResult;