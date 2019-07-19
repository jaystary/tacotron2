import React, { Component, useEffect, useState } from "react";
import './App.css';
import { Text_Responses } from "./components/Text";
import { SentenceForm } from "./components/SentenceForm";
import { Container } from "semantic-ui-react";



class App extends Component {
render(){


    return (

      useEffect(() => {
        fetch("/tts_response").then(response =>
          response.json().then(data => {
            setText(data.text_responses);
          })
        );
      }, []);

      <Container style={{ marginTop: 40 }}>
        <SentenceForm
          onNewText_Response={text_response =>
            setText(currentText => [text_response, ...currentText])
          }
        />
        <Text_Responses text_responses={text_responses} />
      </Container>
    );
  }
}


export default App;
