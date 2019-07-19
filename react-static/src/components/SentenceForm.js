import React, { useState } from "react";
import { Form, Input, Button } from "semantic-ui-react";

export const SentenceForm = ({ onNewSentence }) => {
  const [sentence, setSentence] = useState("");

  
  return (
    <Form>
      <Form.Field>
        <Input
          placeholder="Input Text"
          value={sentence}
          onChange={e => setSentence(e.target.value)}
        />
      </Form.Field>
      <Form.Field>
        <Button



          onClick={async () => {
            const value = { sentence };
            fetch("/infer_tts", {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify(value)
            });
            console.log(sentence)
            var evtSource = new EventSource("/infer_tts");
            evtSource.onmessage = function(e) {
            var obj = JSON.stringify(e.data);
            console.log(obj)
            }


          }}
        >
          submit
        </Button>
      </Form.Field>
    </Form>
  );
};

 