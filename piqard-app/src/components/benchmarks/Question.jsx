import { useState } from "react";
import { Container } from "react-bootstrap";

import downwardArrow from "../../assets/icons/downward-arrow.png"
import upwardArrow from "../../assets/icons/upward-arrow.png"


import './Question.css'

function Question({question}){
    const [isContextVisible, setIsContextVisible] = useState(false);

    return(
        <Container className="question-container">
            <Container>
                <span className="bold">Question: </span>{question.question}
            </Container>
            <Container>
                <span className="bold">Possible answers: </span>{question.possible_answers}
            </Container>
            <Container>
                <span className="bold">Answer: </span>{question.answer}
            </Container>
            <Container>
                <span className="bold">Predicted answer: </span>{question.predicted_answer}
            </Container>
            <Container>
                <span className="bold">Context <img src={ isContextVisible ? upwardArrow : downwardArrow }
                                                    className='context-arrow'
                                                    onClick={()=>{setIsContextVisible(!isContextVisible)}}/> </span>
                {isContextVisible && (
                    <Container>
                        {question.context}
                    </Container>
                )}
            </Container>
        </Container>
    )
}

export default Question;