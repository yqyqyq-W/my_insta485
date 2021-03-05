/* eslint-disable prefer-const */
import React from 'react';
import PropTypes from 'prop-types';

/*
 Example:
    {
  "comments": [
    {
      "commentid": 1,
      "owner": "awdeorio",
      "owner_show_url": "/u/awdeorio/",
      "postid": 3,
      "text": "#chickensofinstagram"
    },
    {
      "commentid": 2,
      "owner": "jflinn",
      "owner_show_url": "/u/jflinn/",
      "postid": 3,
      "text": "I <3 chickens"
    },
    {
      "commentid": 3,
      "owner": "michjc",
      "owner_show_url": "/u/michjc/",
      "postid": 3,
      "text": "Cute overload!"
    }
  ],
  "url": "/api/v1/p/3/comments/"
} */
class Comments extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      comments: [{
        commentid: 0,
        owner: '',
        owner_show_url: '',
        postid: 0,
        text: '',
        inputVal: '',
      }],
      length: 0,
    };
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;

    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          comments: data.comments,
          length: data.comments.length,
        });
      })
      .catch((error) => console.log(error));
  }

  getComment(index) {
    const { comments } = this.state;
    console.log('start getcomment');
    if (comments.length > index) {
      return (
        <li key={comments[index].commentid}>
          <a className="t" href={comments[index].owner_show_url}>{comments[index].owner}</a>
          <p>{ comments[index].text }</p>
          <br />
          <br />
        </li>
      );
    }
    return (<h1>GetComment Loading</h1>);
  }

  updatePost(event) {
    const { url } = this.props;
    event.preventDefault();
    console.log('event.target.value', event.target.value);
    fetch(url, {
      credentials: 'same-origin', method: 'POST', text: event.target.value, headers: { 'Content-Type': 'application/json' },
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        console.log('updatePost setstate');
        this.setState((preState) => ({ comments: preState.comment.push(data) }));
      })
      .catch((error) => console.log(error));
    this.setState((preState) => ({ length: preState.length + 1 }));
  }

  handleChange(event){
    this.setState({inputVal:event.target.value})
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const { length } = this.state;

    let tmp = [];
    if (length) {
      let i = 0;
      for (; i < length; i += 1) {
        tmp.push(this.getComment(i));
      }
    }
    // console.log(length);
    // TODO:add comment update html

    return (
      <div>
        <ul>
          { tmp }
        </ul>
        <form className="comment-form" onSubmit={(e) => this.updatePost(e)}>
          <input type="text" value={this.state.inputVal} onChange={this.handleChange}/>
        </form>
      </div>
    );
  }
}

Comments.propTypes = {
  url: PropTypes.string.isRequired,
};
export default Comments;
