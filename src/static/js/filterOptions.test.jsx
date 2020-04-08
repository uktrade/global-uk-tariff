import React from 'react';
import { mount } from 'enzyme';
import FilterOptions from './filterOptions.jsx';


describe('FilterOptions', () => {
  const props = {
    sampleSize: 25,
    searchImage: "/test-image.svg",
    filter: "test-filter",
    handleSampleSizeChange: jest.fn(),
    handleFilterChange: jest.fn()
  }
  it('renders without crashing', () => {
    mount(<FilterOptions {...props} />);
  });

  it('renders using props', () => {
    const wrapper = mount(<FilterOptions {...props} />);

    expect(wrapper.find("input").props().value).toBe(props.filter);
    expect(wrapper.find("select").props().defaultValue).toBe(props.sampleSize);
  });

  it('uses callback on filter change', () => {
    const wrapper = mount(<FilterOptions {...props} />);
    const input = wrapper.find('input');

    input.simulate('change', {target: {value: "changed"}});

    expect(props.handleFilterChange.mock.calls.length).toBe(1);
    expect(props.handleFilterChange.mock.calls[0][0].target.value).toBe("changed");
  });

  it('uses callback on sample size change', () => {
   const wrapper = mount(<FilterOptions {...props} />);
    const input = wrapper.find('select');

    input.simulate('change', {target: {value: 10}});

    expect(props.handleSampleSizeChange.mock.calls.length).toBe(1);
    expect(props.handleSampleSizeChange.mock.calls[0][0].target.value).toBe(10);
  });
});
