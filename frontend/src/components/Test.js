import React, { Component } from 'react';
import { Grid, Image, List } from 'semantic-ui-react';

// Coma & period color functionality
const c = ( <span style={{"color":"white"}}>,</span> );
const p = ( <span style={{"color":"red"}}>.</span> );

class Test extends Component {
    render() {
        return(
            <Grid celled>
                <Grid.Row>
                    <Grid.Column width={12}>

                        {console.log(`I AM HERE ${this.props}`)}
                        {console.log(`I AM HERE ${this.props.testing}`)}

                        <span style={{"color":"white", "padding":"300px", "font-size":"27px", "font-weight":"bold"}}>Some of my Skills
                        <span style={{"color":"red"}}>.</span></span>

                        <List style={{"color":"white"}} as="h2">
                            <List.Item>
                            <span style={{"color":"red", "font-size":"20px", "font-weight":"normal"}}>Languages</span> <span style={{"color":"white", "font-size":"20px", "font-weight":"normal"}}>: Python{c} Javascript{c} Node{c} React{c} HTML{c} SQL{c} Shell{p}</span>
                            </List.Item>

                            <List.Item></List.Item>
                            <List.Item></List.Item>

                            <List.Item>
                                <span style={{"color":"red", "font-size":"20px", "font-weight":"normal"}}>AWS Services</span> <span style={{"color":"white", "font-size":"20px", "font-weight":"normal"}}>: Serverless Framework{c} Lambda{c} Layers{c} API Gateway{c} SNS{c} SQS{c} S3{c} EC2{c} Cloud9{c} Cloudformation{c} Cloudwatch{c} IAM{p}</span>
                            </List.Item>

                            <List.Item></List.Item>
                            <List.Item></List.Item>

                            <List.Item>
                            <span style={{"color":"red", "font-size":"20px", "font-weight":"normal"}}>Proficiencies</span> <span style={{"color":"white", "font-size":"20px", "font-weight":"normal"}}>
                                : Selenium{c} Headless Chromium{c} Firebase{c} Pusher{c} Docker{c} Flask{c} SQLAlchemy{c} Gmail Api{c} Cron{c} Unittest{c} Pytest{c} CircleCi{c} Oh-My-Zsh{c} Trello{c} Aha{c} Jira{c} Postman{c} Git{c} GitKraken{c} SourceTree{c} MySQLWorkbench{c} DataGrip{c} Command line mastery {c} Mocha{c} VSCode{c} DataGrip{p}
                            </span>
                            </List.Item>

                            <List.Item></List.Item>
                            <List.Item></List.Item>

                            {/* <List.Item>
                            <span style={{"color":"red", "font-size":"20px", "font-weight":"normal"}}>More Tools</span> <span style={{"color":"white", "font-size":"20px", "font-weight":"normal"}}>: Docker{c} Flask{c} SQLAlchemy{c} Unittest{c} Pytest{c} Mocha{c} Selenium{c} Headless Chromium{p}</span>
                            </List.Item>

                            <List.Item></List.Item>
                            <List.Item></List.Item> */}

                            <List.Item>
                            <span style={{"color":"red", "font-size":"20px", "font-weight":"normal"}}>Blockchain Specific Proficiencies</span> <span style={{"color":"white", "font-size":"20px","font-weight":"normal"}}>: Open Zepplin{c} Ganache{c} Truffle{c} Remix{c} Metamask{c} Infura{p}</span>
                            </List.Item>

                            <List.Item></List.Item>
                        </List>
                    </Grid.Column>

                    <Grid.Column width={4}>
                        <Image style={{"marginTop":"59px"}} size="large" src="../static/assets/skills.png"/>
                    </Grid.Column>
                    
                </Grid.Row>
            </Grid>
        );
    }
}
export default Test;