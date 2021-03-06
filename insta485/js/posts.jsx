/* eslint-disable prefer-const */
import React from 'react';
import PropTypes from 'prop-types';
import Post from './post';

/*
 Example:
    {
  "next": "",
  "results": [
    {
      "postid": 3,
      "url": "/api/v1/p/3/"
    },
    {
      "postid": 2,
      "url": "/api/v1/p/2/"
    },
    {
      "postid": 1,
      "url": "/api/v1/p/1/"
    }
  ],
  "url": "/api/v1/p/"
} */
class Posts extends React.Component {
  /* Display number of image and post owner of a single post
   */

  static getPost(postid, link) {
    // console.log('static getPost', postid, link);
    if (link !== '') {
      return (
        <li key={postid}>
          <Post url={link} postid={postid} />
        </li>
      );
    }
    return (<h1>GetPost Loading</h1>);
  }

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { posts: [{ postid: 0, url: '' }], length: 0 };
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;
    const perfEntries = String(window.performance.getEntriesByType('Navigation'));
    if (perfEntries === 'back_forward') {
      this.setState(window.history.state);
    } else {
      fetch(url, { credentials: 'same-origin' })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          // console.log('start setstate');
          this.setState({
            posts: data.results,
            length: data.results.length,
          });
          const { posts, length } = this.state;
          window.history.pushState({ posts, length }, '', '/');
          console.log('setstate success');
        })
        .catch((error) => console.log(error));
    }
    // Call REST API to get the post's information
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const { posts, length } = this.state;
    // console.log(length);
    // console.log(posts[0].postid);
    let renderedPost = [];
    if (length && posts.length !== 0) {
      // const renderedPost = Posts.getPost(posts[0].postid, posts[0].url);
      let i = 0;
      for (;i < posts.length; i += 1) {
        renderedPost.push(Posts.getPost(posts[i].postid, posts[i].url));
      }
    }
    return (
      <ul>
        { renderedPost }
      </ul>
    );
  }
}

Posts.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Posts;
