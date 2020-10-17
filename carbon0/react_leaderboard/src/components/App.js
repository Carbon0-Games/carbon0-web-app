import React, { Component, Fragment } from "react";
import ReactDOM from "react-dom";

import Dashboard from "./leads/Dashboard";
import "./imgs/style.css";


class App extends Component {

  render() {
    return (
      <Fragment>
        <div className="container">
          <Dashboard />
        </div>

      </Fragment>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("app"));