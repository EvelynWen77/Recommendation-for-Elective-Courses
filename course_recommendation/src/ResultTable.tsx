import React from 'react';
import { Space, Table, Tag, Alert} from 'antd';
import type { TableProps } from 'antd';
import allCourses from './courses.json';

interface ResultTableProps {
    courses: string[];
    userName: string;
}

interface ResultCourseDetails {
    id: string;
    credit: number;
    name: string;
    description: string;
    prerequists: string;
}

const columns: TableProps<ResultCourseDetails>['columns'] = [
    {
        title: 'Course ID',
        dataIndex: 'id',
        key: 'id',
        render: (id) => <Tag key={id} color='geekblue'>{id}</Tag>
    },
    {
        title: 'Name',
        dataIndex: 'name',
        key: 'name',
    },
    {
        title: 'prerequists',
        key: 'prerequists',
        dataIndex: 'prerequists',
        render: (prerequists) => prerequists || 'N/A'
    },
    {
        title: 'Credit',
        dataIndex: 'credit',
        key: 'credit',
    },
    {
        title: 'Description',
        dataIndex: 'description',
        key: 'description',
    }
];

const ResultTable = (props: ResultTableProps): JSX.Element => {

    const results = props.courses;
    const rows = results.map(result => {
        const course = allCourses.courses.find(course => result === course['Course ID'])!;
        return {
            id: course['Course ID'],
            name: course['Course Name'],
            credit: course['Credits'],
            description: course['Course Description'],
            prerequists: course['Prerequisites']
        };
    })
    return <>
    <Alert message={`Hi ${props.userName}, here're recommended courses for you based on your input:`} type="success"/>
    <Table<ResultCourseDetails> columns={columns} dataSource={rows} pagination={false}/>
        </>

}

export default ResultTable;