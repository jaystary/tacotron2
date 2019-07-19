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
            const response = await fetch("/tts_infer", {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify(value)
            });

            if (response.ok) {
              console.log("response worked!");
              onNewSentence(onNewSentence);
              setSentence("");
            }
          }}
        >
          submit
        </Button>
      </Form.Field>
    </Form>
  );
};