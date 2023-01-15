import axios from "axios";
import { useState } from "react";
import { Col, Container, Row } from "react-bootstrap";

import observation from '../../assets/chain_trace/observation.png'
import thought from '../../assets/chain_trace/thought.png'
import action from '../../assets/chain_trace/action.png'
import answer from '../../assets/chain_trace/answer.png'
import error from '../../assets/chain_trace/error.png'


import './ResultChainNode.css'

function ResultChainNode({node}){
    const typeDict = {'thought': 'Thought', 'action': 'Action', 'observation': 'Observation', 'finish': 'Answer', 'error': 'Error'}
    const imageDict = {'thought': thought, 'action': action, 'observation': observation, 'finish': answer, 'error': error}

    return(
        <Container fluid className={`resultchain-node-container ${node.type === 'finish' ? 'resultchain-node-answer-container' : ''}`}>
            <Row>
                <Col md={3}>
                    <div className="center">
                        <img className="resultchain-node-image" src={imageDict[node.type]} alt="node"/>
                    </div>
                    <Container className="center">
                        <h4 className="type-text">{typeDict[node.type]}</h4>
                    </Container>
                </Col>
                <Col md={9}>
                    <p style={{whiteSpace: "pre-wrap"}}>{node.data}</p>
                </Col>
            </Row>



        </Container>
    )
}

export default ResultChainNode;