
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
    api.get('/api/leads/').then(res => {
      console.log(res.data)
      console.log("test loging out")
      this.setState({ courses:res.data})
    })
  }

  render() {
    return (
      <div>
        <h1>Leads List LEAD PAGE</h1>
        { this.state.courses.map(course => 
        
        <div key={course.id}>
        
        <h2>{course.name} </h2>
        <p>{course.message} </p>
        
        </div>
        )
        
        }

      </div>
    )
  }
}

export default Leads