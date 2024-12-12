import type { FormProps } from 'antd';
import React from 'react';
import { Button, Checkbox, Form, Input, Select, Radio, Row, Col, Space } from 'antd';
import interestValues from "./interests.json";
import allCourses from './courses.json';
import ResultTable from './ResultTable';

enum LoadingState {
    LOADING,
    LOADED
}

enum Class {
    FRESHMAN,
    SOPHOMORE,
    JUNIOR,
    SENIOR,
    GRADUATE
}

enum Major {
    APPLIED_MATH,
    MATH,
    ECE,
    CSE
}

type FieldType = {
    id: string;
    class: Class;
    major: Major;
    interest: string[];
    coursesTaken: string[];
};



const onFinishFailed: FormProps<FieldType>['onFinishFailed'] = (errorInfo) => {
    console.log('Failed:', errorInfo);
};

const IntakeForm = (): JSX.Element => {
    const [interests, setInterests] = React.useState<string[]>([]);
    const [coursesTaken, setCoursesTaken] = React.useState<string[]>([]);
    const [results, setResults] = React.useState<string[]>([]);
    const [userName, setUserName] = React.useState<string>('');
    const [loadingState, setLoadingState] = React.useState<LoadingState>(LoadingState.LOADED);
    console.log(results);
    const onFinish: FormProps<FieldType>['onFinish'] = async (values) => {
        try {
            setLoadingState(LoadingState.LOADING);
            setUserName(values.id);
            const URL = 'http://35.86.83.100:8000/recommend/';
            const response = await fetch(URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(values),
            });
            const data = await response.json();
            // Data extraction is subject to change based on the actual data structure
            const courses = data['recommended_course_ids'];
            setResults(courses);
            setLoadingState(LoadingState.LOADED);
        } catch (err) {
            console.error(err);
            setLoadingState(LoadingState.LOADED);
        }

    };
    return (
        <>
            <Form
                name="basic"
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
                autoComplete="off"
            >
                <Form.Item<FieldType>
                    label="Name"
                    name="id"
                    rules={[{ required: true, message: 'Please enter your name' }]}
                >
                    <Input />
                </Form.Item>
                <Form.Item<FieldType>
                    label="Year of college"
                    name="class"
                    rules={[{ required: true, message: 'Please select your class' }]}
                >
                    <Select
                        options={[
                            { label: 'Freshman', value: Class.FRESHMAN },
                            { label: 'Sophomore', value: Class.SOPHOMORE },
                            { label: 'Junior', value: Class.JUNIOR },
                            { label: 'Senior', value: Class.SENIOR },
                            { label: 'Graduate', value: Class.GRADUATE },
                        ]}
                    />
                </Form.Item>
                <Form.Item<FieldType>
                    label="Major"
                    name="major"
                    rules={[{ required: true, message: 'Please select your major' }]}
                >
                    <Select
                        options={[
                            { label: 'Applied Mathematics', value: Major.APPLIED_MATH },
                            { label: 'Mathematics', value: Major.MATH },
                            { label: 'Electrical and Computer Engineering', value: Major.ECE },
                            { label: 'Computer Science and Engineering', value: Major.CSE },
                        ]}
                    />
                </Form.Item>
                <Form.Item<FieldType>
                    label="Interest"
                    name="interest"
                    rules={[{ required: true, message: 'Please select at least one interest' }]}
                >
                    <Select
                        mode="multiple"
                        maxCount={2}
                        value={interests}
                        style={{ width: '100%' }}
                        onChange={setInterests}
                        options={interestValues.values.map(value => ({
                            value: value,
                            label: value
                        }))}
                    />
                </Form.Item>
                <Form.Item<FieldType>
                    name="coursesTaken"
                    label="Courses taken"
                    rules={[{ required: true, message: 'Please select courses you took' }]}>
                    <Select
                        mode="multiple"
                        style={{ width: '100%' }}
                        placeholder="Search by course ID"
                        defaultValue={[]}
                        onChange={setCoursesTaken}
                        options={allCourses.courses.map(course => ({
                            value: course['Course ID'],
                            label: `${course['Course ID']} - ${course['Course Name']}`
                        }))}
                    />
                </Form.Item>
                <Form.Item label={null}>
                    <Button type="primary" htmlType="submit" loading={loadingState === LoadingState.LOADING}>
                        Find your courses
                    </Button>
                </Form.Item>
            </Form>
            {
                results.length > 0
                && loadingState === LoadingState.LOADED
                && <ResultTable courses={results} userName={userName} />
            }
        </>
    )
}

export default IntakeForm;