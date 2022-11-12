import React, { useEffect, useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import PlaygroundQuestion from "../components/playground/PlaygroundQuestion";
import PlaygroundResult from "../components/playground/PlaygroundResult";
import PromptTextBox from "../components/playground/PromptTextBox";

import SystemConfig from "../components/playground/SystemConfig";
import systemConfigTemplate from "../data/systemConfigTemplate";
import './PlaygroundView.css'

function PlaygroundView(){
    const [systemConfig, setSystemConfig] = useState(systemConfigTemplate.reduce(function (p, n) {
        return {...p, [n.name]: n.name === 'prompt' ? 'custom_prompt' : null};
    }, {}));
    const [isCustomQuestion, setIsCustomQuestion] = useState(false);
    const [question, setQuestion] = useState(""); 
    const [result, setResult] = useState({})

    
    function handleSetSystemConfig(event){
        const newSystemConfig = {...systemConfig, [event.target.name]: event.target.value};
        setSystemConfig(newSystemConfig);
    }


    function handleIsCustomQuestion(value){
        setIsCustomQuestion(value)
    }

    function handleSetQuestion(event){
        setQuestion(event.target.value);
    }

    useEffect(() => {
        setQuestion("");
      }, [isCustomQuestion]);
   



    return(
        <Container fluid className="content-view">
            <Row className="full-height non-padding-margin">
                <Col md={2} className="non-padding-margin">
                    <SystemConfig systemConfig={systemConfig} handleSetSystemConfig={handleSetSystemConfig}/>
                </Col>
                <Col md={10} className="non-padding-margin">
                    <Container>
                        <Row>
                            <Col md={6}>
                                <PromptTextBox prompt={systemConfig['prompt']}/>
                            </Col>
                            <Col md={6}>
                                <div className="playground-right-container">
                                    <PlaygroundQuestion isCustomQuestion={isCustomQuestion}
                                                        handleIsCustomQuestion={handleIsCustomQuestion}
                                                        question={question}
                                                        handleSetQuestion={handleSetQuestion} />
                                    <PlaygroundResult isCutomQuestion={isCustomQuestion}
                                                      result={result}/>
                                </div>
                            </Col>
                        </Row>
                    </Container>
                </Col>
            </Row>
        </Container>
    )
}


export default PlaygroundView;