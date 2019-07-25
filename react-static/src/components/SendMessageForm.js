import React, { Component } from "react";
import { Button, Form, TextArea } from "semantic-ui-react";
class SendMessageForm extends Component {
  state = {
    message: ""
  };

  render() {
    return (
      <div>
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
              rows="20"
              placeholder={"Enter your sentences..."}
              value={this.state.message}
              onChange={e => this.setState({ message: e.target.value })}
            />
          </Form.Field>
          <Form.Field>
            <Button color="primary" type="submit" value={"Send"}>
              Send
            </Button>
          </Form.Field>
        </Form>
      </div>
    );
  }
}

export default SendMessageForm;
