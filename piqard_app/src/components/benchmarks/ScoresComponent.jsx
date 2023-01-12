import { Container } from "react-bootstrap";

import './ScoresComponent.css'

function ScoresComponent({scores}){
    return(
        <div className="scores-container">
            <h3>Scores</h3>
            <ul>
            {Object.entries(scores).map(([name, value])=> (
                <li><span className="score-name">{name}</span> = {value.toFixed(5)}</li>
                )
            )}
            </ul>
        </div>
    )
}

export default ScoresComponent;