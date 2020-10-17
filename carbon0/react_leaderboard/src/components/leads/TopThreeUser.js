import React, { Component } from 'react'
import axios from 'axios';
import 'bootstrap';
import image from "../imgs/react.png";


const api = axios.create({
  baseURL: `http://localhost:8000`
  // baseURL: `http://127.0.0.1:8000`
})

export class TopThreeUser extends Component {
  state = {
    players: []
  }
  constructor() {
    super();
    api.get('api/footprint-leaderboard').then(res => {
      // console.log(res.data.players)
      this.setState({ players: res.data.players })
    })

  }
  render() {
    var topThreeList = [];
    var loopLength = 3;

    if (this.state.players.length < 3) {
      loopLength = this.state.players.length
    }
    for (var i = 0; i < loopLength; i++) {
      topThreeList.push(this.state.players[i])
    }


  if (topThreeList.length > 0) {
    this._nameFirst = topThreeList[0].username
    this._scoreFirst = topThreeList[0].score

    this._nameSecond = topThreeList[1].username
    this._scoreSecond = topThreeList[1].score

    this._nameThird = topThreeList[2].username
    this._scoreThird = topThreeList[2].score
  }

  // console.log(Object.keys(testt))


    return (
      <section className="card-section">
         {/* { topThreeList.map(player =>
          <div key={player.id}>
            <h4 key={player.id} >{player.username} </h4>
            <p key={player.id}>{player.score} </p>
          </div>
        )
        } */}
        <card >
          <h2 className="leaderboard">2</h2>
          <div class="card" className="card">
            <img class="card-img-top" src={image} alt="Card image cap" />
            <div class="card-body">
              <h5 class="card-title text-center">{this._nameSecond}</h5>
              <p class="card-text text-center">{this._scoreSecond}</p>
            </div>
          </div>
        </card>

        <card>
          <h2 className="leaderboard">1</h2>
          <div class="card" className="card-leader">
            <img class="card-img-top" src={image} alt="Card image cap" />
            <div class="card-body">
              <h5 class="card-title text-center">{this._nameFirst}</h5>
              <p class="card-text text-center">{this._scoreFirst}</p>
            </div>
          </div>
        </card>

        <card>
          <h2 className="leaderboard">3</h2>
          <div class="card" className="card">
            <img class="card-img-top" src={image} alt="Card image cap" />
            <div class="card-body">
            <h5 class="card-title text-center">{this._nameThird}</h5>
              <p class="card-text text-center">{this._scoreThird}</p>
            </div>
          </div>
        </card>

      </section>
    )
  }
}

export default TopThreeUser