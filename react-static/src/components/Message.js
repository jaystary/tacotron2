import React from "react";
// import propTypes from "prop-types";

class Message extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      message: ""
    };
  }

  render() {
    return <div>{this.props.message}</div>;
  }
}

export default Message;

/*
function Message(props) {
  const { body } = props.message;
  return <p>{body}</p>;
}

Message.propTypes = {
  message: propTypes.shape({
    body: propTypes.string,
    timestamp: propTypes.instanceOf(Date)
  })
};

export default Message;
*/
