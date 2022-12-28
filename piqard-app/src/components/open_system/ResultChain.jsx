import axios from "axios";
import { useState } from "react";
import { Container } from "react-bootstrap";


import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRotateBack } from '@fortawesome/free-solid-svg-icons'

import './ResultChain.css'
import ResultChainNode from "./ResultChainNode";

function ResultChain({chainTrace, tryAgainFunction}){


    const baseInfo = () => {
        return(
            <div className="base-info">
                <h1><span className="base-info-span">PIQARD</span> Open System</h1>
                <p>Enter a question to get started</p> 
            </div>
        )
    }

    const tryAgain = () => {
        return(
            <div className="base-info">
                <h3><span className="base-info-span">PIQARD</span> Open System</h3>
                <p className="try-again-button" onClick={() =>{tryAgainFunction()}}>Try again  <FontAwesomeIcon className="try-again-icon" icon={faArrowRotateBack}/></p> 
            </div>
        )
    }

    return(
        <Container fluid className="resultchain-container center">
            {chainTrace === undefined ? 
                baseInfo() :
                <div className="node-list">
                    {chainTrace.map((node) => (node.type.includes("prompt") ? <></> : <ResultChainNode node={node}/> ))}
                    {tryAgain()}
                </div>}
           
        </Container>
    )
}

export default ResultChain;