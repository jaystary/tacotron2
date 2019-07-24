import React, { Component } from "react";
import "./App.css";
import MessageWindow from "./components/MessageWindow";
import io from "socket.io-client";

const socket = io("http://localhost:8888");

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      sentence: "",
      id: "",
      messages: [],
      };

    this.handleChange = this.handleChange.bind(this);
    this.messagewindowElement = React.createRef();
  }
  

  handleChange(event) {
    const { name, value } = event.target;
    this.setState({ [name]: value });
  }

  sendMessage(message, id) {
    socket.emit("send_message", {
      id: id,
      body: message,
      timeStamp: Date.now()
    });
  }

  setSocketListeners() {
    socket.on("message", data => {
      console.log(data.message);
    });

    socket.on("message_sent", message => {
      this.setState({ messages: [...this.state.messages, message] }, () => {
        window.localStorage.setItem(
          "messages",
          JSON.stringify(this.state.messages)
        );
      });
    });

    socket.on("activate_socket", sentence => {
      this.messagewindowElement.current.addMessage("Hello");
      console.log("connected");
      //if (this.state.username) {
      //  socket.emit('activate_user', { username: this.state.username })
      //}
    });
  }


  loadMessages() {
    const savedMessages = window.localStorage.getItem("messages");
    if (savedMessages) {
      this.setState({ messages: JSON.parse(savedMessages) || [] });
    }
  }

  componentDidMount() {
    this.loadMessages();
    this.setSocketListeners();
   
  }

  render() {
    return (
      <div className="App">
        <MessageWindow ref={this.messagewindowElement} />
       
      </div>
    );
  }
  /*
  render() {
    const { messages } = this.state;

    return (
      <div className="App">
        <MessageWindow messages={messages} sendMessage={this.sendMessage} />
      </div>
    );
  }*/
}

export default App;
