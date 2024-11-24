// src/MainContent1/Chart.js
import React from 'react';
import { ResponsiveBar } from '@nivo/bar';

const data = [
  {
    country: 'USA',
    'hot dog': 150,
    burger: 120,
    kebab: 200,
    fries: 220,
  },
  {
    country: 'Germany',
    'hot dog': 100,
    burger: 110,
    kebab: 170,
    fries: 150,
  },
  {
    country: 'France',
    'hot dog': 90,
    burger: 80,
    kebab: 180,
    fries: 140,
  },
  {
    country: 'UK',
    'hot dog': 120,
    burger: 100,
    kebab: 160,
    fries: 190,
  },
];

const Chart = () => {
  return (
    <div style={{ height: '500px' }}>
      <ResponsiveBar
        data={data}
        keys={['hot dog', 'burger', 'kebab', 'fries']}
        indexBy="country"
        margin={{ top: 50, right: 130, bottom: 50, left: 60 }}
        padding={0.3}
        layout="vertical"
        colors={{ scheme: 'nivo' }}
        animate={true}
        motionConfig="gentle"
        axisTop={null}
        axisRight={null}
        axisBottom={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: 'Food items',
          legendPosition: 'middle',
          legendOffset: 32,
        }}
        axisLeft={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: 'Countries',
          legendPosition: 'middle',
          legendOffset: -40,
        }}
      />
    </div>
  );
};

export default Chart;
