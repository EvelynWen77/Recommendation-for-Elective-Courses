import React from 'react';

import {Row, Col} from 'antd';
import uwLogo from './uw.png';

const FooterSection = ():JSX.Element => {
 return <div>
   <Row align={'middle'} justify={'center'}>
      <Col span={2}>
    <img className='UW-logo' src={uwLogo} />
    </Col>
    <Col span={1}></Col>
    <Col>
    <p>Developed by Course4U team with ❤️</p>
    <p>Yingchao, Jiaqi, Zimo, Zeyuan</p>
    </Col>
    </Row>
 </div>
}

export default FooterSection;