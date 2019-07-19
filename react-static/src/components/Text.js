import React from "react";
import { List, Header } from "semantic-ui-react";

export const Text_Responses = ({ text_responses }) => {
  return (
    <List>
      {text_responses.map(text_response => {
        return (
          <List.Item key={text_response.val}>
            <Header>{text_response.val}</Header>
            </List.Item>
        );
      })}
    </List>
  );
};