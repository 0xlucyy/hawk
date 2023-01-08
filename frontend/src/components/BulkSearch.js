import React, { Component } from 'react'
import axios from 'axios';
import { Form, TextArea, Button, Label, Input, Tab, Message, Icon } from 'semantic-ui-react'
import { HandleCardContext, handleCardHeader} from './Card.js'
// import fetch from 'node-fetch';
// console.log(`data: ${JSON.stringify(markets)}`)


export default class BulkSearch extends Component {
  state = {
    payload: null,
    activeButton: 'bulkSearch', // sets default landing page
    loading: false,
    bulk_search_text: '',
    bulk_search_results: null,
    post_search: false,
    file: null,
    fileName: null,

    // Error related.
    error: false,
    errorMessage: '',
    hidden: true,
  };

  set_bulk_search = () => {
    this.setState({ activeButton: 'bulkSearch' });
  }

  set_file_search = () => {
    this.setState({ activeButton: 'fileSearch' });
  }

  set_text_value = (event) => {
    this.setState({bulk_search_text: event.target.value});
  }

  process_text = async (e) => {
    e.preventDefault();
    if (this.state.bulk_search_text !== '') {
      // console.log(`data: ${JSON.stringify(this.state.bulk_search_text)}`)
      var cleaned = (this.state.bulk_search_text.replace(/\n/g,',')).trim();
      console.log(`[ACTION] Searching for: ${JSON.stringify(cleaned)} ...`)

      const params = new URLSearchParams();
      params.append('domains', cleaned);

      const response = await fetch('http://127.0.0.1:5000/api/v1/bulkSearch', {method: 'POST', body: params});
      const search_results = await response.json();

      await this.setState({bulk_search_results: search_results})
      await this.setState({post_search: true})

      console.log(`[ACTION] Results: ${JSON.stringify(search_results)} ...`)
      console.log(`[ACTION] Postsearch: ${JSON.stringify(this.state.post_search)} ...`)
    } else {
      console.log("text is ''")
    }
  }

  clear_search_text = () => {
    this.setState({bulk_search_text: ''});
  }

  print = (event) => {
    console.log(`file name: ${this.state.fileName}`)
    console.log(`file: ${JSON.stringify(this.state.file)}`)
  }

  onFormSubmit = e => {
    e.preventDefault(); // Stop form submit
    console.log("[ACTION] Submitting form ...");
    this.fileUpload(this.state.file);
  };

  fileUpload = async file => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      axios.post("/file/upload/enpoint").then(response => {
        console.log(response);
        console.log(response.status);
        // this.setState({ statusCode: response.status }, () => {
        //   // console.log(
        //   //   "This is the response status code --->",
        //   //   this.state.statusCode
        //   // );
        // });
      });
    } catch (error) {
      console.error(Error(`Error uploading file ${error.message}`));
    }
  };

  fileChange = e => {
    this.setState(
      { file: e.target.files[0], fileName: e.target.files[0].name },
      () => {
        console.log(
          "[ACTION] File chosen --->",
          this.state.file,
          console.log("File name  --->", this.state.fileName)
        );
      }
    );
  };


  render() {
    return (
      <div className="BulkSearch" id="bulksearch" class="ui hidden section divider">
      {
        this.state.activeButton === 'bulkSearch' ? (
          <div>

          <Form class="ui form" hidden={this.state.post_search}>
            <Button.Group fluid>
              <Button
                onClick={this.set_bulk_search}
                positive={this.state.activeButton === 'bulkSearch'}>Bulk Search
              </Button>
              
              <Button.Or />

              <Button
                secondary
                onClick={this.set_file_search}
                positive={this.state.activeButton === 'fileSearch'}>Load from File
              </Button>
            </Button.Group>

            <div class="ui hidden section divider"></div>

            <TextArea
              placeholder='Enter one ENS domain per line'
              style={{'backgroundColor':'black', 'color':'white', minHeight: 500}}
              type="text"
              value={this.state.bulk_search_text}
              defaultValue={this.state.bulk_search_text}
              onChange={ (event) => {
                this.set_text_value(event)
              }}
            />

            <Button.Group fluid>
              <Button
                primary
                onClick={this.process_text}
                loading={this.state.loading}>search
              </Button>
              
              <Button
                secondary
                onClick={this.clear_search_text}>
                clear
              </Button>
            </Button.Group>
          </Form>
          </div>
        ) : (
          <div>
            <Tab.Pane attached={false} inverted>
              <Label
                as='a'
                color='green'
                image
                onClick={this.set_bulk_search}
                // attached="left"
                fluid
              >
                <img src='hawk.png' />
                Back to search
              </Label>

              <div class="ui hidden section divider"></div>

              <Form onSubmit={this.onFormSubmit}>
                <Form.Field>
                
                <label style={{color: 'white'}}>File input & upload</label>
                
                <Button as="label" htmlFor="file" type="button" animated="fade">
                  <Button.Content visible>
                    <Icon name="file" />
                  </Button.Content>
                  <Button.Content hidden>Choose a File</Button.Content>
                </Button>
                
                <input
                  type="file"
                  id="file"
                  hidden
                  onChange={this.fileChange}
                />
                <Form.Input
                  fluid
                  label="File Chosen: "
                  placeholder="Use the above bar to browse your file system"
                  readOnly
                  value={this.state.fileName}
                  // color='white'
                  inverted
                />

                <Button style={{ marginTop: "20px" }} type="submit">
                  Upload
                </Button>
              </Form.Field>
            </Form>
          </Tab.Pane>

            {/* <Button
              as="label"
              htmlFor="file"
              type="button"
              circular
              onClick={this.print}
            >
              Some button stuff
            </Button>
            <Input 
              type="file"
              id="file"
              style={{ display: "hidden", color: "white" }}
              value={this.state.file}
              onChange={ (event) => {
                this.setState({ file: event.target.files });
              }}
            /> */}
          </div>
        )
      }
    </div>
    )
  }
}