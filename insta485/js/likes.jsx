import React from 'react';
import PropTypes from 'prop-types';

/*
 Example:
{
  "logname_likes_this": 1,
  "likes_count": 1,
  "postid": 3,
  "url": "/api/v1/p/3/likes/"
} */
class Likes extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { lognameLikes: 0, count: 0 };
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const url  = this.props.url;

    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          lognameLikes: data.logname_likes_this,
          count: data.likes_count,
        });
      })
      .catch((error) => console.log(error));
  }

  componentDidUpdate() {
    this.likeHandle();
  }

  // handler for like&unlike
  unlikeHandle() {
    const url  = this.props.url;
    fetch(url, { credentials: 'same-origin', method: 'DELETE' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .catch((error) => console.log(error));
    this.setState((preState) => ({ count: preState.count - 1 }));
  }

  likeHandle() {
    const url  = this.props.url
    fetch(url, { credentials: 'same-origin', method: 'POST' })
      .then((response) => {
        if (!response.ok && response.status !== 409) throw Error(response.statusText);
        return response.json();
      })
      .catch((error) => console.log(error));
    this.setState((preState) => ({ count: preState.count + 1 }));
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const { lognameLikes, count } = this.state;
    // TODO: lognameLikes value based on restApi
    let button = null;
    if (lognameLikes === 1) {
      // unlike button
      button = <button type="button" className="like-unlike-button" onClick={this.unlikeHandle}>unlike</button>;
    } else {
      // like button
      button = <button type="button" className="like-unlike-button" onClick={this.likeHandle}>like</button>;
    }

    const tmp = (count === 1) ? 'like' : 'likes';
    return (
    // TODO: button
      <div className="sub">
        <p>{ count }</p>
        <p>{ tmp }</p>
        <div>{ button }</div>
      </div>
    );
  }
}

Likes.propTypes = {
  url: PropTypes.string.isRequired,
  indicator1: PropTypes.number.isRequired,
};

export default Likes;
