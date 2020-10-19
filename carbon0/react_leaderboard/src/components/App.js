import React, { Component, Fragment } from "react";
import ReactDOM from "react-dom";
import 'bootstrap';
import Leaderboard from "./leads/Leaderboard";
import "./css/style.css";


class App extends Component {

  render() {
    return (
      <Fragment>
        <div className="container">
          <Leaderboard />
        </div>
      </Fragment>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("app"));