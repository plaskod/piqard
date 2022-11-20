import React, { useEffect, useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import Select from "../Select";

import './SystemConfig.css'

import systemConfigTemplate from "../../data/systemConfigTemplate";
import axios from "axios";

function SystemConfig({systemConfig, handleSetSystemConfig}){
    const [systemConfigComponents, setSystemConfigComponents] = useState({})
   
    useEffect(() => {
        async function getConfig() {
          try {
              const response = await axios.get(
                `${process.env.REACT_APP_PIQARD_API_URL}/get_config_components`,
              );
              setSystemConfigComponents(response.data);
          } catch (error) {
            console.log("Get config components error");
            setSystemConfigComponents({});
          }
        }
    
        getConfig();
      }, []);


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