import React, { Component, Fragment } from "react";
import ReactDOM from "react-dom";

import Dashboard from "./leads/Dashboard";

import image from "./imgs/react.png";


class App extends Component {



  render() {
    return (
      <Fragment>
        <div className="container">
          <Dashboard />
        <img src={image} alt="React Image test" />
        </div>

      </Fragment>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("app"));