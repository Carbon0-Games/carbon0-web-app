
import React, { Component } from 'react';

import axios from 'axios';

const api = axios.create({
  baseURL: `http://localhost:8000`
  // baseURL: `http://127.0.0.1:8000`

})


export class EveryoneElse extends Component {

  state = {
  players: []
  }

  constructor() {
    super();
    api.get('api/footprint-leaderboard').then(res => {
      console.log(res.data.players)
      this.setState({ players:res.data.players})
      // players = Array.from(res.data.players);
      // const test = Object.keys(res).forEach((property) => {
      //   res[property]
      // })

    })

    // data = Array.from(props.data);

  }

  render() {

    let topThreeList = [];
    for (var i = 0; i < this.state.players.length; i++) {
      topThreeList.push(this.state.players[i])
      // console.log("yes")
    }

    return (
      <>
        <h3>API Call This Component will show everyone else</h3>

        { topThreeList.map(player => 
        
        <div key={player.id}>
          <h2  key={player.id} >{player.username} </h2>
          <p  key={player.id}>{player.score} </p>
        </div>
        )
        
        }   

      </>
    )
  }
}

export default EveryoneElse