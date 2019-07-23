import React, { Component } from "react";
import { Button, Form, TextArea } from "semantic-ui-react";

class SendMessageForm extends Component {
  state = {
    message: ""
  };

  render() {
    return (
      <Form
        action="."
        onSubmit={e => {
          e.preventDefault();
          this.props.onSubmitMessage(this.state.message);
          this.setState({ message: "" });
        }}
      >
        <Form.Field>
          <TextArea
            rows="15"
            placeholder={"Enter your sentences..."}
            value={this.state.message}
            onChange={e => this.setState({ message: e.target.value })}
          />
        </Form.Field>

        <Button type="submit" value={"Send"}>
          Send
        </Button>
      </Form>
    );
  }
}

export default SendMessageForm;
