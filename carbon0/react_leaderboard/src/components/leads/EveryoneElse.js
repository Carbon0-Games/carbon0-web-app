
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
      // console.log(res.data.players)
      this.setState({ players: res.data.players })
    })
  }

  render() {
    let everyoneElseList = [];
    let ids = []

    if (this.state.players.length > 3)
      for (var i = 3; i < this.state.players.length; i++) {
        everyoneElseList.push(this.state.players[i])
      }

    for (var i = 3; i < everyoneElseList.length + 3; i++) {
      ids.push(i)
    }

    console.log(ids)

    return (
      <>
        <h3>Everyone Else</h3>

        { everyoneElseList.map(player =>
          <div key={player.id}>
            <h4 key={player.id} >{player.username} </h4>
            <p key={player.id}>{player.score} </p>
          </div>
        )
        }

        <table className="table">
          <thead>
            <tr>
              <th scope="col">Position</th>
              <th scope="col">Username</th>
              <th scope="col">Score</th>
            </tr>
          </thead>
          <tbody>

            {everyoneElseList.map(player =>
              <tr>
                {/* {ids.map(id => <th scope="row">{id}</th>
                )} */}
                <th scope="row">{player.id}</th>
                <td>{player.username}</td>
                <td>{player.score}</td>

              </tr>

            )}
          </tbody>
        </table>

      </>
    )
  }
}

export default EveryoneElse