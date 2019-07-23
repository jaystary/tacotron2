import React, { Component } from "react";
// import propTypes from "prop-types";
// import MessageComponent from "./MessageComponent";

import SendMessageForm from "./SendMessageForm";
import { Container, Grid } from "semantic-ui-react";
import Player from "./PlayerComponent";
import Message from "./Message";
import {
  Element,
  Events,
  animateScroll as scroll,
  scrollSpy
} from "react-scroll";

const URL = "ws://localhost:3030";

class MessageWindow extends Component {
  state = {
    messages: []
  };

  ws = new WebSocket(URL);

  componentDidMount() {
    this.ws.onopen = () => {
      // on connecting, do nothing but log it to the console
      console.log("connected");
    };

    this.ws.onmessage = evt => {
      // on receiving a message, add it to the list of messages
      const message = JSON.parse(evt.data);
      this.addMessage(message);
    };

    this.ws.onclose = () => {
      console.log("disconnected");
      // automatically try to reconnect on connection loss
      this.setState({
        ws: new WebSocket(URL)
      });
    };

    Events.scrollEvent.register("begin", function(to, element) {
      console.log("begin", arguments);
    });

    Events.scrollEvent.register("end", function(to, element) {
      console.log("end", arguments);
    });

    scrollSpy.update();
  }

  componentDidUpdate() {
    this.scrollToBottom();
  }

  scrollToBottom = () => {
    scroll.scrollToBottom({
      containerId: "TextElement",
      duration: 1, // control speed of load text
      smooth: "linear"
    });
  };

  addMessage = message =>
    this.setState(state => ({ messages: [...state.messages, message] }));

  submitMessage = messageString => {
    // on submitting the ChatInput form, send the message, add it to the list and reset the input
    const message = { name: this.state.name, message: messageString };
    this.ws.send(JSON.stringify(message));
    this.addMessage(message);
  };

  render() {
    return (
      <Container style={{ minHeight: "100vh" }}>
        <Grid>
          <Grid.Row style={{ marginTop: 40 }}>
            <Grid.Column>
              <SendMessageForm
                onSubmitMessage={messageString =>
                  this.submitMessage(messageString)
                }
              />
            </Grid.Column>
          </Grid.Row>
          <Grid.Row style={{ minHeight: 80 }} />
          <Grid.Row columns={2}>
            <Grid.Column>
              <Player />
            </Grid.Column>
            <Grid.Column style={{ background: "#C0C0C0" }}>
              <div>
                <Element
                  name="TextElement"
                  className="element"
                  id="TextElement"
                  style={{
                    position: "relative",
                    height: "450px",
                    overflow: "auto"
                  }}
                >
                  {this.state.messages.map((message, index) => (
                    <Message key={index} message={message.message} />
                  ))}
                </Element>
              </div>
            </Grid.Column>
          </Grid.Row>
        </Grid>
      </Container>
    );
    //   <div>
    //     <SendMsgForm
    //       onSubmitMessage={messageString => this.submitMessage(messageString)}
    //     />
    //     {this.state.messages.map((message, index) => (
    //       <Text key={index} message={message.message} />
    //     ))}
    //   </div>
    // );
  }
}

export default MessageWindow;

/*
class MessageWindow extends Component {
  constructor(props) {
    super(props);
  }

  filterMessages(messages) {
    return messages;
  }

  render() {
    const { sendMessage, messages } = this.props;
    return (
      <div>
        <MessageComponent messages={messages} sendMessage={sendMessage} />
      </div>
    );
  }
}

MessageWindow.propTypes = {
  sendMessage: propTypes.func,
  messages: propTypes.arrayOf(
    propTypes.shape({
      author: propTypes.string,
      body: propTypes.string,
      timestamp: propTypes.instanceOf(Date)
    })
  )
};

export default MessageWindow;
*/
