import React, { Component } from 'react';
// import Header from './Header.js';
// import Footer from './Footer.js';
// import Head from 'next/head';
import { Container, Visibility, Sticky, Rail } from 'semantic-ui-react';


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
                        attached
                        style={{ top: "auto", height: "auto", width: "100%" }}
                    >
                        {(calculations.percentagePassed * 100).toFixed() < 10 ? null : (
                            <Sticky offset={5} context={contextRef} bottomOffset={0} style={{ marginLeft: '100px' }}>
                                <a href="#topOfPage">Top of Page</a>
                            </Sticky>
                        )}
                    </Rail>

                    {/* This is required for all future props. */}
                    <Container fluid='true' textAlign='center'>
                        {this.props.children}
                    </Container>

                    {/* <Footer/> */}

                </Visibility>
            </div>
        );
    }   
};
