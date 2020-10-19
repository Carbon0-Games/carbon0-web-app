
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
      this.setState({ players: res.data.players })
    })
  }

  render() {
    let everyoneElseList = [];

    if (this.state.players.length > 3)
      for (var i = 3; i < this.state.players.length; i++) {
        everyoneElseList.push(this.state.players[i])
      }

    return (
      <>
        <h3>Others</h3>

        <table className="table table-bordered">
          <thead>
            <tr class="table-info" >
              <th scope="col">Position</th>
              <th scope="col">Username</th>
              <th scope="col">Score</th>
            </tr>
          </thead>
          <tbody>

            {everyoneElseList.map(player =>
              <tr>
                <td scope="row"> <strong>{player.position + 1}</strong></td>
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