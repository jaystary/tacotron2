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

class MessageWindow extends Component {
  state = {
    messages: [],
    message: ""
  };

  componentDidMount() {

    //socket.on("get_data", this.getData);
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

  componentWillUnmount() {
   // socket.off("get_data");
  }

  scrollToBottom = () => {
    scroll.scrollToBottom({
      containerId: "TextElement",
      duration: 1, // control speed of load text
      smooth: "linear"
    });
  };

  getData = response => {
    console.log(response);
    //const message = { name: this.state.name, message: messageString };
    //this.setState(state => ({ messages: [...state.messages, message] }));
    //this.setState({ food_data: foodItems });
  };

  submitMessage = messageString => {
    //socket.emit("get_data", messageString);
  };

  render() {
    return (
      <Container style={ContainerStyle}>
        <Grid>
          <Grid.Row style={InptutStyle}>
            <Grid.Column>
              <SendMessageForm
                onSubmitMessage={messageString =>
                  this.submitMessage(messageString)
                }
              />
            </Grid.Column>
          </Grid.Row>
          <Grid.Row>
            <Grid.Column style={TextMessageStyle}>
              <Element
                name="TextElement"
                className="element"
                id="TextElement"
                style={ElementStyle}
              >
                {this.state.messages.map((message, index) => (
                  <Message key={index} message={message.message} />
                ))}
              </Element>
            </Grid.Column>
          </Grid.Row>
          <Grid.Row>
            <Player />
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

const ContainerStyle = { minHeight: "100vh" };
const InptutStyle = { marginTop: 40 };
const TextMessageStyle = {
  marginLeft: "10px",
  marginRight: "10px",
  background: "#93b5b3",
  borderRadius: "4px"
};
const ElementStyle = {
  position: "relative",
  height: "350px",
  overflow: "auto"
};

export default MessageWindow;
