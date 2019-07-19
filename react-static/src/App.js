import React, { useEffect, useState } from "react";
import "./App.css";
import { Text_Responses } from "./components/Text";
import { SentenceForm } from "./components/SentenceForm";
import { Container, Grid } from "semantic-ui-react";
import Player from "./components/PlayerComponent";

function App() {
  const [text_responses, setText] = useState([]);

  useEffect(() => {
    fetch("/tts_response").then(response =>
      response.json().then(data => {
        setText(data.text_responses);
      })
    );
  }, []);

  return (
    <Container style={{ marginTop: 40 }}>
      <Grid>
        <Grid.Column width={8}>
          <SentenceForm
            onNewText_Response={text_response =>
              setText(currentText => [text_response, ...currentText])
            }
          />
        </Grid.Column>
        <Grid.Column width={8}>
          <h1>Text</h1>
          <Text_Responses text_responses={text_responses} />
        </Grid.Column>

        <Player />
      </Grid>
    </Container>
  );
}

export default App;
