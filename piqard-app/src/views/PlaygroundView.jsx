import axios from "axios";
import React, { useEffect, useRef, useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import PlaygroundQuestion from "../components/playground/PlaygroundQuestion";
import PlaygroundResult from "../components/playground/PlaygroundResult";
import PromptTextBox from "../components/playground/PromptTextBox";

import SystemConfig from "../components/playground/SystemConfig";
import systemConfigTemplate from "../data/systemConfigTemplate";
import './PlaygroundView.css'


const useDidMountEffect = (func, deps) => {
    const didMount = useRef(false);
    useEffect(() => {
      if (didMount.current) {
        if (deps[0]){
            func();
        }
      } else {
        didMount.current = true;
      }
    }, deps);
  };


function PlaygroundView(){
    const [systemConfig, setSystemConfig] = useState(systemConfigTemplate.reduce(function (p, n) {
        return {...p, [n.name]: n.name === 'prompt_template' ? 'custom_prompt' : null};
    }, {}));
    const [isBenchmark, setIsBenchmark] = useState(false);
    const [question, setQuestion] = useState(""); 
    const [result, setResult] = useState({})
    const [isLoading, setIsLoading] = useState(false);


    
    function handleSetSystemConfig(event){
        const newSystemConfig = {...systemConfig, [event.target.name]: event.target.value};
        setSystemConfig(newSystemConfig);
    }


    function handleSetIsBenchmark(value){
        setIsBenchmark(value)
    }

    function handleSetQuestion(event){
        setQuestion(event.target.value);
    }

    function handleQueryPIQARD(event){
        setIsLoading(!isLoading);
    }

    useDidMountEffect(() => {
        getPIQARDResult();
    }, [isLoading]);

    function getPIQARDResult(){
        async function getResult() {
          try {
            const PIQARDConfig = { piqard: systemConfig,
                                   question: isBenchmark ? null : question,
                                   benchmark: isBenchmark ? question : null};
            const response = await axios.post(
              `${process.env.REACT_APP_PIQARD_API_URL}`, PIQARDConfig
            );
            setResult(response.data);
            setIsLoading(false);
          } catch (error) {
            console.log("Error with PIQARD api");
            setIsLoading(false);
          }
        }
    
        getResult();
    }

    useEffect(() => {
        setQuestion("");
      }, [isBenchmark]);
   



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
                                <PromptTextBox prompt={systemConfig['prompt_template']}/>
                            </Col>
                            <Col md={6}>
                                <div className="playground-right-container">
                                    <PlaygroundQuestion isBenchmark={isBenchmark}
                                                        handleSetIsBenchmark={handleSetIsBenchmark}
                                                        question={question}
                                                        handleSetQuestion={handleSetQuestion}
                                                        handleQueryPIQARD={handleQueryPIQARD} />
                                    <PlaygroundResult isBenchmark={isBenchmark}
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