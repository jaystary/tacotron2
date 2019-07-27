import React, { Component } from "react";
import "./App.css";
import MessageWindow from "./components/MessageWindow";
import { socket, Header } from "./components/Header";


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      sentence: "",
      id: "",
      messages: [],
      };

    this.messagewindowElement = React.createRef();
  }
  

  handleChange(event) {
    const { name, value } = event.target;
    this.setState({ [name]: value });
  }

/*
  sendMessage(message, id, route) {
    console.log("sending")
    socket.emit(
      'send_message',
      {
        route,
        id: id,
        body: message,
        timeStamp: Date.now()
      }
    )
  }

  setSocketListeners() {
    socket.on("message", data => {
      console.log("Logging incomcing Message")
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

    socket.on("activate_socket", message => {
      
      console.log("connected");
      //if (this.state.username) {
      //  socket.emit('activate_user', { username: this.state.username })
      //}
    });

    socket.on("send_message", message => {
      
      console.log("sending Message");
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
  */

  getData = resp => {
    console.log(resp);
    //this.setState({ food_data: foodItems });
  };


  echoResponse = resp => {
    console.log(resp)
  };

  doSomething(){
    socket.emit("getdata", "Hello World.");
  }
  

  componentDidMount() {
    //this.loadMessages();
    //this.setSocketListeners();
    //this.messagewindowElement.current.submitMessage("Hello")
   
    socket.on("getdata", this.getData);
    socket.on("echo", this.echoResponse);
    socket.emit("echo");

  }

  componentWillUnmount() {
    socket.off("getdata");
    socket.off("echo");
  }


  handleOnSubmit = e => {
    e.preventDefault();
    //this.sendMessage("Hello World. How are you", 1, "infer");
    this.doSomething()
  };


  render() {
    return (
      <div className="App">
      < Header/>
        <MessageWindow ref={this.messagewindowElement} />
        <form onSubmit={this.handleOnSubmit}>
        <button type="submit">Inside Custom</button>
      </form>
       
      </div>
    );
  }
}

export default App;
