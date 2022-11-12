import React, { useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import Select from "../Select";

import './SystemConfig.css'

import systemConfigComponents from "../../data/systemConfigComponents";
import systemConfigTemplate from "../../data/systemConfigTemplate";

function SystemConfig({systemConfig, handleSetSystemConfig}){
   
    return(
        <div className="system-config-container">
            <div className="system-config-form">
                <h5>Configuration</h5>
                <hr/>
                <Container>
                    {systemConfigTemplate.map((elem)=>(
                        <Select label={elem.label}
                                key={elem.name}
                                name={elem.name}
                                value={systemConfig[elem.name]}
                                options={systemConfigComponents[elem.name]}
                                onChange={(event) => (handleSetSystemConfig(event))} />
                    ))}
                </Container>
            </div>
        </div>
    )
}



export default SystemConfig;;