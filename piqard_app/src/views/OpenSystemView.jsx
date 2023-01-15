import axios from "axios";
import { useState } from "react";
import { Container, Spinner } from "react-bootstrap";
import QuestionBox from "../components/open_system/QuestionBox";
import ResultChain from "../components/open_system/ResultChain";


import './OpenSystemView.css'

function OpenSystemView(){
    const [question, setQuestion] = useState("");
    const [result, setResult] = useState({})
    const [isLoading, setIsLoading] = useState(false);

    function handleSetQuestion(e){
        setQuestion(e.target.value);
    }

    function tryAgainFunction(){
        setQuestion("");
        setResult({});
    }

    function clearMemory(){
      setQuestion("");
      setResult({});
    }

    function getPIQARDResult(){
        async function getResult() {
          try {
            const response = await axios.post(
              `${process.env.REACT_APP_PIQARD_API_URL}/opensystem`, {question: question}
            );
            setResult(response.data);
            setIsLoading(false);
          } catch (error) {
            setResult({'chain_trace': [{'type': 'error', 'data': "Sorry, I couldn't answer your question. \nPossible solutions: \n- check your internet connection \n- try to rephrase your question \n- wait a while for the external API to restart and try again"}]});
            setIsLoading(false);
            console.log("Error with PIQARD api");
          }
        }
        setIsLoading(true);
        getResult();
    }

    return(
        <Container fluid className="opensystemview-container">
            <QuestionBox question={question}
                         isLoading={isLoading}
                         handleSetQuestion={handleSetQuestion}
                         getPIQARDResult={getPIQARDResult}
                         clearMemory={clearMemory}/>

            {isLoading ?
                <Container className="spinner-container center"><Spinner /></Container> : 
                <ResultChain chainTrace={result ? result.chain_trace : []}
                             tryAgainFunction={tryAgainFunction}/>
            }
        </Container>
    )
}

export default OpenSystemView;