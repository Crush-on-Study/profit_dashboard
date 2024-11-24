// src/MainContent1/NetworkChart.js
import React from 'react';
import { ResponsiveNetwork } from '@nivo/network';

const MyResponsiveNetwork = ({ data }) => (
  <ResponsiveNetwork
    data={data}
    margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
    linkDistance={e => e.distance}
    centeringStrength={0.3}
    repulsivity={6}
    nodeSize={n => n.size}
    activeNodeSize={n => 1.5 * n.size}
    nodeColor={e => e.color}
    nodeBorderWidth={1}
    nodeBorderColor={{
      from: 'color',
      modifiers: [
        ['darker', 0.8],
      ],
    }}
    linkThickness={n => 2 + 2 * n.target.data.height}
    linkBlendMode="multiply"
    linkColor="#FFFF00"
    motionConfig="wobbly"
  />
);

const NetworkChart = () => {
  // 예시 데이터
  const data = {
    nodes: [
      {
        "id": "Node 1",
        "height": 1,
        "size": 24,
        "color": "rgb(97, 205, 187)"
      },
      {
        "id": "Node 2",
        "height": 1,
        "size": 24,
        "color": "rgb(97, 205, 187)"
      },
      {
        "id": "Node 3",
        "height": 1,
        "size": 24,
        "color": "rgb(97, 205, 187)"
      },
      {
        "id": "Node 4",
        "height": 1,
        "size": 24,
        "color": "rgb(97, 205, 187)"
      },
      {
        "id": "Node 5",
        "height": 1,
        "size": 24,
        "color": "rgb(97, 205, 187)"
      },
      {
        "id": "Node 6",
        "height": 1,
        "size": 24,
        "color": "rgb(97, 205, 187)"
      },
      {
        "id": "Node 7",
        "height": 1,
        "size": 24,
        "color": "rgb(97, 205, 187)"
      },
      {
        "id": "Node 8",
        "height": 1,
        "size": 24,
        "color": "rgb(97, 205, 187)"
      },
      {
        "id": "Node 9",
        "height": 1,
        "size": 24,
        "color": "rgb(97, 205, 187)"
      },
      {
        "id": "Node 10",
        "height": 1,
        "size": 24,
        "color": "rgb(97, 205, 187)"
      },
      {
        "id": "Node 0",
        "height": 2,
        "size": 32,
        "color": "rgb(244, 117, 96)"
      },
      {
        "id": "Node 1.0",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 1.1",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 1.2",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 1.3",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 2.0",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 2.1",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 2.2",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 2.3",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 2.4",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 2.5",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 3.0",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 3.1",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 3.2",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 3.3",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 4.0",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 4.1",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 4.2",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 4.3",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 5.0",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 5.1",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 5.2",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 5.3",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 5.4",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 5.5",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 6.0",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 6.1",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 6.2",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 6.3",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 6.4",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 6.5",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 6.6",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 6.7",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 7.0",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 7.1",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 7.2",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 7.3",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 8.0",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 8.1",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 8.2",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 8.3",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 8.4",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 8.5",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 9.0",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 9.1",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 9.2",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 9.3",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 9.4",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 9.5",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 9.6",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 9.7",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 9.8",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 10.0",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 10.1",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 10.2",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 10.3",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 10.4",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      },
      {
        "id": "Node 10.5",
        "height": 0,
        "size": 12,
        "color": "rgb(232, 193, 160)"
      }
    ],
    links: [
      {
        "source": "Node 0",
        "target": "Node 1",
        "distance": 80
      },
      {
        "source": "Node 1",
        "target": "Node 1.0",
        "distance": 50
      },
      {
        "source": "Node 1",
        "target": "Node 1.1",
        "distance": 50
      },
      {
        "source": "Node 1",
        "target": "Node 1.2",
        "distance": 50
      },
      {
        "source": "Node 1",
        "target": "Node 1.3",
        "distance": 50
      },
      {
        "source": "Node 0",
        "target": "Node 2",
        "distance": 80
      },
      {
        "source": "Node 2",
        "target": "Node 2.0",
        "distance": 50
      },
      {
        "source": "Node 2",
        "target": "Node 2.1",
        "distance": 50
      },
      {
        "source": "Node 2",
        "target": "Node 2.2",
        "distance": 50
      },
      {
        "source": "Node 2",
        "target": "Node 2.3",
        "distance": 50
      },
      {
        "source": "Node 2",
        "target": "Node 2.4",
        "distance": 50
      },
      {
        "source": "Node 2",
        "target": "Node 2.5",
        "distance": 50
      },
      {
        "source": "Node 0",
        "target": "Node 3",
        "distance": 80
      },
      {
        "source": "Node 3",
        "target": "Node 1",
        "distance": 80
      },
      {
        "source": "Node 3",
        "target": "Node 8",
        "distance": 80
      },
      {
        "source": "Node 3",
        "target": "Node 3.0",
        "distance": 50
      },
      {
        "source": "Node 3",
        "target": "Node 3.1",
        "distance": 50
      },
      {
        "source": "Node 3",
        "target": "Node 3.2",
        "distance": 50
      },
      {
        "source": "Node 3",
        "target": "Node 3.3",
        "distance": 50
      },
      {
        "source": "Node 0",
        "target": "Node 4",
        "distance": 80
      },
      {
        "source": "Node 4",
        "target": "Node 4.0",
        "distance": 50
      },
      {
        "source": "Node 4",
        "target": "Node 4.1",
        "distance": 50
      },
      {
        "source": "Node 4",
        "target": "Node 4.2",
        "distance": 50
      },
      {
        "source": "Node 4",
        "target": "Node 4.3",
        "distance": 50
      },
      {
        "source": "Node 0",
        "target": "Node 5",
        "distance": 80
      },
      {
        "source": "Node 5",
        "target": "Node 3",
        "distance": 80
      },
      {
        "source": "Node 5",
        "target": "Node 9",
        "distance": 80
      },
      {
        "source": "Node 5",
        "target": "Node 5.0",
        "distance": 50
      },
      {
        "source": "Node 5",
        "target": "Node 5.1",
        "distance": 50
      },
      {
        "source": "Node 5",
        "target": "Node 5.2",
        "distance": 50
      },
      {
        "source": "Node 5",
        "target": "Node 5.3",
        "distance": 50
      },
      {
        "source": "Node 5",
        "target": "Node 5.4",
        "distance": 50
      },
      {
        "source": "Node 5",
        "target": "Node 5.5",
        "distance": 50
      },
      {
        "source": "Node 0",
        "target": "Node 6",
        "distance": 80
      },
      {
        "source": "Node 6",
        "target": "Node 6.0",
        "distance": 50
      },
      {
        "source": "Node 6",
        "target": "Node 6.1",
        "distance": 50
      },
      {
        "source": "Node 6",
        "target": "Node 6.2",
        "distance": 50
      },
      {
        "source": "Node 6",
        "target": "Node 6.3",
        "distance": 50
      },
      {
        "source": "Node 6",
        "target": "Node 6.4",
        "distance": 50
      },
      {
        "source": "Node 6",
        "target": "Node 6.5",
        "distance": 50
      },
      {
        "source": "Node 6",
        "target": "Node 6.6",
        "distance": 50
      },
      {
        "source": "Node 6",
        "target": "Node 6.7",
        "distance": 50
      },
      {
        "source": "Node 0",
        "target": "Node 7",
        "distance": 80
      },
      {
        "source": "Node 7",
        "target": "Node 7.0",
        "distance": 50
      },
      {
        "source": "Node 7",
        "target": "Node 7.1",
        "distance": 50
      },
      {
        "source": "Node 7",
        "target": "Node 7.2",
        "distance": 50
      },
      {
        "source": "Node 7",
        "target": "Node 7.3",
        "distance": 50
      },
      {
        "source": "Node 0",
        "target": "Node 8",
        "distance": 80
      },
      {
        "source": "Node 8",
        "target": "Node 8.0",
        "distance": 50
      },
      {
        "source": "Node 8",
        "target": "Node 8.1",
        "distance": 50
      },
      {
        "source": "Node 8",
        "target": "Node 8.2",
        "distance": 50
      },
      {
        "source": "Node 8",
        "target": "Node 8.3",
        "distance": 50
      },
      {
        "source": "Node 8",
        "target": "Node 8.4",
        "distance": 50
      },
      {
        "source": "Node 8",
        "target": "Node 8.5",
        "distance": 50
      },
      {
        "source": "Node 0",
        "target": "Node 9",
        "distance": 80
      },
      {
        "source": "Node 9",
        "target": "Node 9.0",
        "distance": 50
      },
      {
        "source": "Node 9",
        "target": "Node 9.1",
        "distance": 50
      },
      {
        "source": "Node 9",
        "target": "Node 9.2",
        "distance": 50
      },
      {
        "source": "Node 9",
        "target": "Node 9.3",
        "distance": 50
      },
      {
        "source": "Node 9",
        "target": "Node 9.4",
        "distance": 50
      },
      {
        "source": "Node 9",
        "target": "Node 9.5",
        "distance": 50
      },
      {
        "source": "Node 9",
        "target": "Node 9.6",
        "distance": 50
      },
      {
        "source": "Node 9",
        "target": "Node 9.7",
        "distance": 50
      },
      {
        "source": "Node 9",
        "target": "Node 9.8",
        "distance": 50
      },
      {
        "source": "Node 0",
        "target": "Node 10",
        "distance": 80
      },
      {
        "source": "Node 10",
        "target": "Node 8",
        "distance": 80
      },
      {
        "source": "Node 10",
        "target": "Node 10.0",
        "distance": 50
      },
      {
        "source": "Node 10",
        "target": "Node 10.1",
        "distance": 50
      },
      {
        "source": "Node 10",
        "target": "Node 10.2",
        "distance": 50
      },
      {
        "source": "Node 10",
        "target": "Node 10.3",
        "distance": 50
      },
      {
        "source": "Node 10",
        "target": "Node 10.4",
        "distance": 50
      },
      {
        "source": "Node 10",
        "target": "Node 10.5",
        "distance": 50
      }
    ]
  };

  return (
    <div style={{ height: '500px' }}>
      <MyResponsiveNetwork data={data} />
    </div>
  );
};

export default NetworkChart;
