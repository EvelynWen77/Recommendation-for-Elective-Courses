import React from 'react';
import logo from './title.png';
import './App.css';
import { Layout, Row, Col, Typography } from 'antd'
import IntakeForm from './IntakeForm';
import FooterSection from './Footer';


const { Header, Footer, Sider, Content } = Layout;
const { Title } = Typography;
const headerStyle: React.CSSProperties = {
  textAlign: 'center',
  color: '#fff',
  height: 250,
  lineHeight: '64px',
  backgroundColor: 'white',
};

const contentStyle: React.CSSProperties = {
  margin: '5%',
  color: '#fff',
  paddingBottom: '100px'
};

const layoutStyle: React.CSSProperties = {
  width: '100%',
  overflow: 'hidden',
};

const footerStyle: React.CSSProperties = {
  textAlign: 'center',
  width: '100%',
  color: '#fff',
  backgroundColor: '#C0C0C0',
  position: 'fixed',
  left: 0,
  bottom: 0
};


function App() {
  return (
    <div className="App">
      <Layout style={layoutStyle}>
        <Header style={headerStyle}>
          <Row justify={'center'} align={'middle'}>
            <img className="App-logo" src={logo}></img>
            <Title level={1}>Course4U</Title>
          </Row>
        </Header>
        <Content style={contentStyle}>
          <IntakeForm />
        </Content>
        <Footer style={footerStyle}>
          <FooterSection />
        </Footer>
      </Layout>

    </div>
  );
}

export default App;
