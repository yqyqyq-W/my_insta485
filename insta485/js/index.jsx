import React from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
import Post from './post';

class Index extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    super(props);

    this.state = {
      url: '/api/v1/p/',
      postList: [],
      nextUrl: '',
      hasMore: true,
    };
    this.fetchData = this.fetchData.bind(this);
  }

  componentDidMount() {
    // const { url } = this.props;
    const { url } = this.state;
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        // console.log('index response');
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // console.log('index setstate');
        this.setState({
          postList: data.results,
          nextUrl: data.next,
          hasMore: data.next !== '',
        });
      })
      .catch((error) => console.log(error));
  }

  fetchData() {
    const { state } = this;
    const url = state.nextUrl;
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        // console.log('index response');
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // console.log('index setstate');
        this.setState({
          postList: state.postList.concat(data.results),
          nextUrl: data.next,
          hasMore: data.next !== '',
        });
        // console.log('index setstate success');
        window.history.replaceState({ state }, null);
      })
      .catch((error) => console.log(error));
  }

  // TODO: response time
  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const { postList, hasMore } = this.state;
    // let queryString = url + "?size=" + String(numPost);
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
          dataLength={postList.length} // This is important field to render the next data
          next={this.fetchData}
          hasMore={hasMore}
          loader={<h4>Loading...</h4>}
          endMessage={(<div />)}
        >
          <ul>
            {postList.map((item) => (
              <li key={item.postid}>
                <Post url={item.url} postid={item.postid} />
              </li>
            ))}
          </ul>

        </InfiniteScroll>
      </div>
    );
  }
}

export default Index;
