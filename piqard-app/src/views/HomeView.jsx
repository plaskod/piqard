import { Container, Row, Col } from "react-bootstrap";
import Button from "../components/Button";

import './HomeView.css';

import documents from '../assets/icons/documents.png';
import question from '../assets/icons/question.png';
import workflow from '../assets/icons/workflow.png';
import command from '../assets/icons/command.png';

function HomeView(){
    return(
        <Container className="home-view-container" fluid>
            <Container className="main-hero" fluid>
                <Row className="main-hero-row">
                    <Col md={7} className="hero-col">
                        <div className='image'>

                        </div>
                    </Col>
                    <Col md={5} className="center hero-col">
                        <div className="command-prompt">
                            <div className="command-prompt-nav"><img src={command} className="commend-prompt-icon"/>Command Prompt</div>
                            <div className="command-prompt-content">
                                PIQARD [Version 1.0.0]<br/>
                                (c) 2023 Piqard Corporation. All rights reserved.<br/>
                                <br/>
                                <span className="slogan">C:\Piqard{">"} Prompting is the future!<br/></span>
                                C:\Piqard{">"} Do you want to start? [y/n]:<br/>
                                <Button label="Get started now!" className="prompt-button"/>
                            </div>
                        </div>
                    </Col>
                </Row>
            </Container>
            <Container className="home-info-container" fluid>
                    <Row className="home-info-row">
                        <Col md={4} className="center">
                            <div className="home-info-col">
                                <Container className="info-icon">
                                    <img src={documents} />
                                </Container>
                                <Container>{":\\>"} <span className="stylized-text">Retrieve information</span><br/>from knowledge base.</Container>
                            </div>
                        </Col>
                        <Col md={4} className="center">
                            <div className="home-info-col">
                                <Container className="info-icon">
                                    <img src={question} />
                                </Container>
                                <Container>{":\\>"} Query the<br/><span className="stylized-text">large language model.</span></Container>
                            </div>
                        </Col>
                        <Col md={4} className="center">
                            <div className="home-info-col">
                                <Container className="info-icon">
                                    <img src={workflow} />
                                </Container>
                                <Container>{":\\>"} Analize the <span className="stylized-text">answer</span><br/>step by step.</Container>
                            </div>
                        </Col>
                    </Row>
            </Container>
        </Container>
    )
}

export default HomeView;