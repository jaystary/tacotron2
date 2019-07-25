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


  submitMessage = messageString => {
   const message = { name: this.state.name, message: messageString };
  this.setState(state => ({ messages: [...state.messages, message] }));
  };


  render() {
    return (
      <Container style={ContainerStyle}>
        <Grid>
          <Grid.Row style={GridStylePart1}>
            <Grid.Column>
              <SendMessageForm
                onSubmitMessage={messageString =>
                  this.submitMessage(messageString)
                }
              />
            </Grid.Column>
          </Grid.Row>
          <Grid.Row style={GridStylePart2} columns={2}>
            <Grid.Column>
              <Player />
            </Grid.Column>
            <Grid.Column style={TextMessageStyle}>
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

const ContainerStyle = { minHeight: "100vh" };
const GridStylePart1 = { marginTop: 40 };
const GridStylePart2 = { marginTop: 80 };
const TextMessageStyle = { background: "#a4d7e1", borderRadius: "4px" };

export default MessageWindow;

