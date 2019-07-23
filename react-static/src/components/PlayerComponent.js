import React, { Component } from "react";
import { Button } from "semantic-ui-react";
import ReactPlayer from "react-player";

class Player extends Component {
  state = {
    url: null,
    playing: true,
    volume: 0.8,
    muted: false,
    played: 0,
    loaded: 0,
    playbackRate: 1.0
  };

  load = url => {
    this.setState({
      url,
      played: 0,
      loaded: 0,
      pip: false
    });
  };

  playPause = () => {
    this.setState({ playing: !this.state.playing });
  };
  stop = () => {
    this.setState({ url: null, playing: false });
  };

  setVolume = e => {
    this.setState({ volume: parseFloat(e.target.value) });
  };
  toggleMuted = () => {
    this.setState({ muted: !this.state.muted });
  };
  setPlaybackRate = e => {
    this.setState({ playbackRate: parseFloat(e.target.value) });
  };

  onPlay = () => {
    console.log("onPlay");
    this.setState({ playing: true });
  };
  onPause = () => {
    console.log("onPause");
    this.setState({ playing: false });
  };
  onSeekMouseDown = e => {
    this.setState({ seeking: true });
  };
  onSeekChange = e => {
    this.setState({ played: parseFloat(e.target.value) });
  };
  onSeekMouseUp = e => {
    this.setState({ seeking: false });
    this.player.seekTo(parseFloat(e.target.value));
  };

  onProgress = state => {
    console.log("onProgress", state);
    // We only want to update time slider if we are not currently seeking
    if (!this.state.seeking) {
      this.setState(state);
    }
  };

  renderLoadButton = (url, label) => {
    return <Button onClick={() => this.load(url)}>{label}</Button>;
  };

  ref = player => {
    this.player = player;
  };
  render() {
    const {
      url,
      playing,
      volume,
      muted,
      played,
      loaded,
      playbackRate
    } = this.state;

    return (
      <section className="section">
        <div className="player-wrapper">
          <ReactPlayer
            ref={this.ref}
            className="react-player"
            width="100%"
            height="100%"
            url={url}
            playing={playing}
            playbackRate={playbackRate}
            volume={volume}
            muted={muted}
            onPlay={this.onPlay}
            onPause={this.onPause}
            onProgress={this.onProgress}
          />
        </div>
        <table style={{ color: "white" }}>
          <tbody align="left">
            <tr>
              <th>Controls</th>
              <td>
                <Button onClick={this.stop}>Stop</Button>
                {"   "}
                <Button onClick={this.playPause}>
                  {playing ? "Pause" : "Play"}
                </Button>
              </td>
            </tr>
            <tr>
              <th>Speed</th>
              <td>
                <Button onClick={this.setPlaybackRate} value={1}>
                  1x
                </Button>{" "}
                <Button onClick={this.setPlaybackRate} value={1.5}>
                  1.5x
                </Button>{" "}
                <Button onClick={this.setPlaybackRate} value={2}>
                  2x
                </Button>{" "}
              </td>
            </tr>
            <tr>
              <th>Seek</th>
              <td>
                <input
                  type="range"
                  min={0}
                  max={1}
                  step="any"
                  value={played}
                  onMouseDown={this.onSeekMouseDown}
                  onChange={this.onSeekChange}
                  onMouseUp={this.onSeekMouseUp}
                />
              </td>
            </tr>
            <tr>
              <th>Volume</th>
              <td>
                <input
                  type="range"
                  min={0}
                  max={1}
                  step="any"
                  value={volume}
                  onChange={this.setVolume}
                />
              </td>
            </tr>
            <tr>
              <th>
                <label htmlFor="muted">Muted</label>
              </th>
              <td>
                <input
                  id="muted"
                  type="checkbox"
                  checked={muted}
                  onChange={this.toggleMuted}
                />
              </td>
            </tr>
            <tr>
              <th>Played</th>
              <td>
                <progress max={1} value={played} />
              </td>
            </tr>
            <tr>
              <th>Loaded</th>
              <td>
                <progress max={1} value={loaded} />
              </td>
            </tr>
            <tr>
              <th>Files</th>
              <td>
                {this.renderLoadButton(
                  "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
                  "mp3"
                )}
              </td>
            </tr>
            <tr>
              <th>Custom URL</th>
              <td>
                <input
                  ref={input => {
                    this.urlInput = input;
                  }}
                  type="text"
                  placeholder="Enter URL"
                />{" "}
                <Button
                  onClick={() => this.setState({ url: this.urlInput.value })}
                >
                  Load
                </Button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>
    );
  }
}

export default Player;
