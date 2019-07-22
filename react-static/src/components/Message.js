import React from 'react'
import propTypes from 'prop-types'

function Message (props) {
  const {body} = props.message
  return <p>{body}</p>
}

Message.propTypes = {
  message: propTypes.shape({
    body: propTypes.string,
    timestamp: propTypes.instanceOf(Date)
  })
}

export default Message