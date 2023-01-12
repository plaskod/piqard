import { Container } from "react-bootstrap";

import Question from "./Question";

import './QuestionsList.css'

function QuestionsList({questions}){
    return(
        <Container className="questions-list-container">
            <Container fluid className="center">
                <h1>Questions</h1>
            </Container>
            <hr/>
            {questions.map((question) => (
                <Question question={question}/>
            ))}
        </Container>
    )
}

export default QuestionsList;