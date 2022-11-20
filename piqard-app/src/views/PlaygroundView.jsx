import axios from "axios";
import React, { useEffect, useRef, useState } from "react";
import { Container, Row, Col, Spinner } from "react-bootstrap";
import PlaygroundInferenceType from "../components/playground/PlaygroundInferenceType";
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
    const [inferenceType, setInferenceType] = useState("question");
    const [question, setQuestion] = useState(""); 
    const [result, setResult] = useState({})
    const [promptTemplate, setPromptTemplate] = useState("");
    const [isLoading, setIsLoading] = useState(false);


    
    function handleSetSystemConfig(event){
        const newSystemConfig = {...systemConfig, [event.target.name]: event.target.value};
        setSystemConfig(newSystemConfig);
    }


    function handleSetInferenceType(value){
        setInferenceType(value);
    }

    function handleSetQuestion(event){
        setQuestion(event.target.value);
    }

    function handleQueryPIQARD(event){
        setIsLoading(!isLoading);
    }

    function handleSetPromptTemplate(event){
        setPromptTemplate(event.target.value);
    }

    useDidMountEffect(() => {
        getPIQARDResult();
    }, [isLoading]);

    function getPIQARDResult(){
        async function getResult() {
          try {
            const PIQARDConfig = { piqard: systemConfig,
                                   question: question,
                                   prompt_template: promptTemplate };
            const response = await axios.post(
              `${process.env.REACT_APP_PIQARD_API_URL}/basic_query`, PIQARDConfig
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
      }, [inferenceType]);
   

    useEffect(() => {
    async function getPromptTemplate() {
        try {
            const response = await axios.post(
            `${process.env.REACT_APP_PIQARD_API_URL}/get_prompt_template`, {template_name: systemConfig.prompt_template}
            );
            setPromptTemplate(response.data.template);
        } catch (error) {
        console.log("Get prompt template error");
        setPromptTemplate("");
        }
    }

    if(systemConfig.prompt_template !== "custom_prompt"){
        getPromptTemplate();
    }else{
        setPromptTemplate("");
    }
    }, [systemConfig.prompt_template]);

    

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
                                <PromptTextBox promptName={systemConfig['prompt_template']}
                                               promptTemplate={promptTemplate}
                                               handleSetPromptTemplate={handleSetPromptTemplate}/>
                            </Col>
                            <Col md={6}>
                                <PlaygroundInferenceType isLoading={isLoading}
                                                         inferenceType={inferenceType}
                                                         handleSetInferenceType={handleSetInferenceType}
                                                         question={question}
                                                         handleSetQuestion={handleSetQuestion}
                                                         handleQueryPIQARD={handleQueryPIQARD}
                                                         result={result} />
                            </Col>
                        </Row>
                    </Container>
                </Col>
            </Row>
        </Container>
    )
}


export default PlaygroundView;