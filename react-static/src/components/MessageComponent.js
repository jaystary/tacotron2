import React, { Component } from 'react'
import propTypes from 'prop-types'
import Message from './Message'

class MessageComponent extends Component {
  constructor (props) {
    super(props)
    this.state = { message: '' }
    this.handleChange = this.handleChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
    this.scrollToBottom = this.scrollToBottom.bind(this)
  }

  handleSubmit (event) {
    event.preventDefault()
    if (this.state.message) {
      this.props.sendMessage(this.state.message)
      this.setState({ message: '' })
    }
  }

  handleChange (event) {
    const {name, value} = event.target
    this.setState({ [name]: value })
  }

  closeWindow (event) {
    //const {room, username} = this.props
    //this.props.leaveRoom(room, username)
  }

  scrollToBottom () {
    this.messageWindow.scrollTop = this.messageWindow.scrollHeight
  }

  componentDidUpdate () {
    this.scrollToBottom()
  }

  componentDidMount () {
    this.scrollToBottom()
  }

  render () {
    const {partner, messages} = this.props
    const messageList = messages.map((message, i) => {
      return (
        <Message
          message={message}
          key={i} />
      )
    })
    return (
      <div className='MessageWindow'>
        <div className='message-header'>
          <h2>{partner}</h2>
          <button onClick={this.closeWindow}>X</button>
        </div>
        <div className='message-body' ref={(el) => { this.messageWindow = el }}>
          {messageList}
        </div>
        <div className='message-input'>
          <form onSubmit={this.handleSubmit}>
            <input
              type='text'
              name='message'
              className='message'
              placeholder='your message here...'
              value={this.state.message}
              onChange={this.handleChange} />
          </form>
        </div>
      </div>
    )
  }
}

MessageComponent.propTypes = {
  messages: propTypes.arrayOf(propTypes.shape({
    body: propTypes.string,
    timestamp: propTypes.instanceOf(Date)
  })),
  sendMessage: propTypes.func
}

export default MessageComponent