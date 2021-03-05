import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import Likes from './likes';
import Comments from './comments';
/*
 Example:
    {
      "age": "2017-09-28 04:33:28",
      "img_url": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
      "owner": "awdeorio",
      "owner_img_url": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
      "owner_show_url": "/u/awdeorio/",
      "post_show_url": "/p/1/",
      "url": "/api/v1/p/1/"
    } */
class Post extends React.Component {
  /* Display number of image and post owner of a single post
   */

  static doubleHandle() {
    Likes.likeHandle();
    // this.setState((preState) => ({ likeUrl: preState.likeUrl }));
  }

  constructor(props) {
    // Initialize mutable state
    console.log('post start ctor');
    super(props);
    this.state = {
      imgUrl: '', owner: '', ownerImgUrl: '', age: '', ownerUrl: '', postUrl: '', likeUrl: '',
    };
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url, postid } = this.props;

    // Call REST API to get the post's information
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        console.log('after fetch error');
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        console.log('after fetch');
        this.setState({
          imgUrl: data.img_url,
          owner: data.owner,
          ownerImgUrl: data.owner_img_url,
          age: moment(data.age).fromNow(),
          ownerUrl: data.owner_show_url,
          postUrl: data.post_show_url,
          likeUrl: '/api/v1/p/'.concat(postid, '/likes/'),
          commentsUrl: '/api/v1/p/'.concat(postid, '/comments/'),
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const {
      imgUrl, owner, ownerImgUrl, age, ownerUrl, postUrl, likeUrl, commentsUrl,
    } = this.state;
    console.log('post render');
    // Render number of post image and post owner
    if (likeUrl !== '' && commentsUrl !== '') {
      return (
        <div className="post">
          <a className="users" href={ownerUrl}>
            <img className="userImage" src={ownerImgUrl} alt="null" />
            <p>{ owner }</p>
          </a>
          <a href={postUrl} className="sub">{ age }</a>
          <img className="postImage" src={imgUrl} alt="null" onDoubleClick={this.doubleHandle} />
          <Likes url={likeUrl} />
          <br />
          <br />
          <Comments url={commentsUrl} />
          <br />
          <br />
        </div>
      );
    }
    return (<h1>Post Loading</h1>);
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired, postid: PropTypes.number.isRequired,
};

export default Post;
