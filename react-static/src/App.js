import React, { useState } from "react";
import './App.css';
import { Text_Responses } from "./components/Text";
import { SentenceForm } from "./components/SentenceForm";
import { Container } from "semantic-ui-react";


function App() {
  const [setText] = useState();
  return (
    <Container style={{ marginTop: 40 }}>
      <SentenceForm
        onNewText_Response={text_response =>
          setText(currentText => [text_response, ...currentText])
        }
      />
    </Container>
  );
}

export default App;
