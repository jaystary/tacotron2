import React, { Component } from "react";
import socketIOClient from "socket.io-client";

var socket;
class Header extends Component {
  constructor() {
    super();
    this.state = {
      endpoint: "http://localhost:8888/" 
    };

    socket = socketIOClient(this.state.endpoint);
  }

  render() {
    return null
  }

}

export { socket, Header };