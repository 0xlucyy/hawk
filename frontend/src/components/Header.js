import React, { Component } from 'react'
import { Menu, Header, Image } from 'semantic-ui-react'
import { Link } from "react-router-dom"


export default class _Header extends Component {
  constructor(props) {
    super(props);
    this.state = {activeItem: this.props.active};
    this.handleItemClick = this.props.handler.bind(this);
  }

  handleItem = async (e, { name }) => {
    await this.setState({ activeItem: name });
    console.log(`HEADER: ${this.state.activeItem}`);
    await this.props.handler;
  }

  render() {
    const { activeItem } = this.props.active

    return (
      <div>
        <Menu inverted pointing vertical>
          <Header
            inverted
            as='h2'
            attached='top'
            textAlign='center'
            className='header'
            color='green'
          >
            ENS Hawk
          </Header>

          <Menu.Item
            as={Link}
            to="/"
            name='home'
            active={activeItem === 'home'}
            onClick={this.handleItemClick}
          />
          <Menu.Item
            as={Link}
            to="/"
            name='expiring'
            active={activeItem === 'expiring'}
            onClick={this.handleItemClick}
          />
          <Menu.Item
            as={Link}
            to="/"
            name='all'
            active={activeItem === 'all'}
            onClick={this.handleItemClick}
          />
          <Menu.Item
            as={Link}
            to="/contacts/1"
            name='contact'
            active={activeItem === 'contact'}
            onClick={this.handleItemClick}
            // target='_blank'
          />
        </Menu>
      </div>
    )
  }
}
