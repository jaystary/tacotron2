import React, { Component } from 'react'
import propTypes from 'prop-types'
import MessageComponent from './MessageComponent'

class MessageWindow extends Component {
  constructor (props) {
    super(props)
  }

  filterMessages (messages) {
    return messages
  }

  render () {
    const {sendMessage, messages} = this.props
    return (
        <MessageComponent
          messages={messages}
          sendMessage={sendMessage} />
      )
    }
}

MessageWindow.propTypes = {
  sendMessage: propTypes.func,
  messages: propTypes.arrayOf(propTypes.shape({
    author: propTypes.string,
    body: propTypes.string,
    timestamp: propTypes.instanceOf(Date)
  }))
}

export default MessageWindow