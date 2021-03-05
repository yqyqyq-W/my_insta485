import React from 'react';
import PropTypes from 'prop-types';
import InfiniteScroll from 'react-infinite-scroll-component';
// import Posts from './posts';
import Post from './post';

class Index extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    // console.log('index ctor');
    super(props);
    this.state = {
      nextPage: '',
      items: [],
    };
    this.fetchData = this.fetchData.bind(this);
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    // console.log('index start get url');
    // TODO: url
    const { url } = this.props;
    // console.log('index get url');
    // Call REST API to get the post's information
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        // console.log('index response');
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // console.log('index setstate');
        this.setState({
          nextPage: data.next,
          items: data.results,
        });
        // console.log('index setstate success');
      })
      .catch((error) => console.log(error));
  }

  fetchData() {
    const { nextPage } = this.state;
    fetch(nextPage, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState(
          () => ({
            nextPage: data.next,
            items: state.items.concat(data.results),
          }),
        );
      })
      .catch((error) => console.log(error));
  }

  // TODO: response time
  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const hasMore = this.state.nextPage !== '';
    const { postsUrl } = this.state;
    // Render number of post image and post owner
    // console.log(postsUrl);
    // if (postsUrl === '') {
    //   return (
    //   // TODO:infinite scroll
    //
    //     <h1>Loading</h1>);
    // }
    // return (
    //   <div>
    //     <Posts url={postsUrl} />
    //   </div>
    // );
    return (
      <div>
        <InfiniteScroll
          dataLength={state.items.length} // This is important field to render the next data
          next={state.fetchData}
          hasMore={hasMore}
          loader={<h3>Loading...</h3>}
          endMessage={(
            <p>
              <b>Yay! You have seen it all</b>
            </p>
          )}
        >

          {state.items.map((item) => (
            <Post url={item.url} key={item.postid} />
          ))}

        </InfiniteScroll>
      </div>
    );
  }
}

Index.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Index;
