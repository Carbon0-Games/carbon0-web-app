import React, { Component } from "react";
import axios from "axios";
// Note: the following three lines are commented out in order to simplify the DockerfileNode image, 
// and because they are unused
// import first from "../../../../static/images/Present-_Tree.png";
// import second from "../../../../static/images/3D_Carrot.png";
// import thrid from "../../../../static/images/Present-_LED.png";

const api = axios.create({
  // baseURL: `https://carbon0.herokuapp.com`
  // baseURL: `http://localhost:8000/`,
  // baseURL: `http://127.0.0.1:8000`
});

export class TopThreeUsers extends Component {
  state = {
    players: [],
  };
  constructor() {
    super();
    // making API GET call
    api.get("api/footprint-leaderboard").then((res) => {
      console.log(res.data.players);
      this.setState({ players: res.data.players });
    });
  }
  render() {
    let topThreeList = [];
    let loopLength = 3;

    if (this.state.players.length < 3) {
      loopLength = this.state.players.length;
    }

    for (let i = 0; i < loopLength; i++) {
      topThreeList.push(this.state.players[i]);
    }

    if (topThreeList.length > 0) {
      this._nameFirst = topThreeList[0].username;
      this._scoreFirst = topThreeList[0].score;

      this._nameSecond = topThreeList[1].username;
      this._scoreSecond = topThreeList[1].score;

      this._nameThird = topThreeList[2].username;
      this._scoreThird = topThreeList[2].score;
    }

    return (
      <section className='card-section'>
        <div class='p-2'>
          <h2 className='leaderboard'>1</h2>
          <div className=' card-leader'>
            <img className='card-img-top' src={first} alt='Card image cap' />
            <div className='card-body'>
              <h3 className='card-title text-center'>{this._nameFirst}</h3>
              <p className='card-text text-center leader-text'>
                {this._scoreFirst}
              </p>
            </div>
          </div>
        </div>

        <div class='p-2'>
          <h2 className='leaderboard'>2</h2>
          <div className='card'>
            <img className='card-img-top' src={second} alt='Card image cap' />
            <div className='card-body'>
              <h4 className='card-title text-center'>{this._nameSecond}</h4>
              <p className='card-text text-center'>{this._scoreSecond}</p>
            </div>
          </div>
        </div>

        <div class='p-2'>
          <h2 className='leaderboard'>3</h2>
          <div className='card'>
            <img className='card-img-top' src={thrid} alt='Card image cap' />
            <div className='card-body'>
              <h4 className='card-title text-center'>{this._nameThird}</h4>
              <p className='card-text text-center'>{this._scoreThird}</p>
            </div>
          </div>
        </div>
      </section>
    );
  }
}

export default TopThreeUsers;
