import React from "react";
import { Container, Form } from "react-bootstrap";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRightToBracket, faArrowRotateBack } from '@fortawesome/free-solid-svg-icons'

import './QuestionBox.css'


function QuestionBox({question, isLoading, handleSetQuestion, getPIQARDResult, clearMemory}){
    return(
        <Container fluid className="questionbox-container center">
            <div className="questionbox center">
                <Container>
                    <input type="text"
                           readOnly={isLoading}
                           required
                           value={question}
                           onChange={(e) => (handleSetQuestion(e))}
                           onKeyDown={e => {
                            if (e.key === 'Enter') {
                                if(!isLoading){
                                    getPIQARDResult(e);
                                }else{
                                    alert("Please wait for the previous request to finish");
                                }
                            }
                          }}
                           placeholder="Question"
                           className="questionbox-question"/>
                    <FontAwesomeIcon className={`enter-icon ${isLoading ? "disabled-icon" : ""}`}
                                     icon={faArrowRightToBracket}
                                     onClick={()=>(!isLoading && getPIQARDResult())}/>
                    <FontAwesomeIcon className={`enter-icon ${isLoading ? "disabled-icon" : ""}`}
                                     icon={faArrowRotateBack}
                                     onClick={()=>(!isLoading && clearMemory())}/>
                </Container>
            </div>
        </Container>
    )
}


export default QuestionBox;