import React, { Component } from 'react';
import { Container, Visibility, Sticky, Rail, Button } from 'semantic-ui-react';


export default class Layout extends Component {
    state = {
        calculations: {
          direction: 'none',
          height: 0,
          width: 0,
          topPassed: false,
          bottomPassed: false,
          pixelsPassed: 0,
          percentagePassed: 0,
          topVisible: false,
          bottomVisible: false,
          fits: false,
          passing: false,
          onScreen: false,
          offScreen: false,
        }
    };

    handleContextRef = contextRef => this.setState({ contextRef });
    handleUpdate = (e, { calculations }) => this.setState({ calculations });


    render() {
        const { calculations, contextRef } = this.state;

        return(
            <div id="topOfPage" ref={this.handleContextRef}>

                <Visibility onUpdate={this.handleUpdate}>
                    {/* <Header/> */}

                    <style>{`
                        html, body {
                            background-color: #051d2e !important;
                        }
                    `}</style>

                    <Rail
                        internal
                        position="left"
                        // attached
                        style={{ top: "auto", height: "auto", width: "auto" }}
                    >
                        {(calculations.percentagePassed * 100).toFixed() < 2 ? null : (
                            <Sticky offset={10} context={contextRef}>
                                <Button 
                                    color='black'
                                    // compact
                                    className="icon"
                                    as='a'
                                    href='#topOfPage'
                                >top of page</Button>
                            </Sticky>
                        )}
                    </Rail>

                    {/* This is required for all future props. */}
                    <Container textAlign='center'>
                        {this.props.children}
                    </Container>

                    {/* <Footer/> */}

                </Visibility>
            </div>
        );
    }   
};
