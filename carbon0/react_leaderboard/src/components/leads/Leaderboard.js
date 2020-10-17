import React, { Component } from 'react'
import axios from 'axios';

const api = axios.create({
  baseURL: `http://localhost:8000`
  // baseURL: `http://127.0.0.1:8000`
})

export class Leaderboard extends Component {
  state = {
    players: []
    }
    constructor() {
      super();
      api.get('api/footprint-leaderboard').then(res => {
        console.log(res.data.players)
        this.setState({ players:res.data.players})
      })
  
    }
  render() {
    let topThreeList = [];
    var loopLength = 3;

    if (this.state.players.length < 3) {
      loopLength = this.state.players.length
    }
    for (var i = 0; i < loopLength; i++) {
      topThreeList.push(this.state.players[i])
    }

    return (
      <div>
        <h1 className="leaderboard">Leaderboard</h1>
        { topThreeList.map(player => 
        
        <div key={player.id}>
          <h2  key={player.id} >{player.username} </h2>
          <p  key={player.id}>{player.score} </p>
        </div>
        )      
        } 
      </div>
    )
  }
}

export default Leaderboard