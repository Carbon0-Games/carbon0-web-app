
import React, { Component } from 'react';

import axios from 'axios';

const api = axios.create({
  baseURL: `http://localhost:8000`
})


export class Leads extends Component {

  state = {
  courses: []
  }

  constructor() {
    super();
    api.get('api/footprint-leaderboard').then(res => {
      console.log(res.data)
      console.log("test loging out")
      this.setState({ courses:res.data})
    })
  }


  componentDidMount() {
    console.log(courses)
  }
  
  render() {

  

    return (
      <div>
        <h1>Leads List LEAD PAGE MODIFied</h1>

        {/* { this.state.courses.map(course => 
        
        <div key={course.id}>
        
        <h2>{course.username} </h2>
        <p>{course.score} </p>
        
        </div>
        )
        
        } */}

      </div>
    )
  }
}

export default Leads