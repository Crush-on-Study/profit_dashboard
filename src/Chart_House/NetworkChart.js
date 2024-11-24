import { ResponsiveNetwork } from '@nivo/network';

const data = {
    nodes: [
        { id: 'node1', color: 'hsl(205,70%,50%)', size: 10 },
        { id: 'node2', color: 'hsl(95,70%,50%)', size: 20 },
        { id: 'node3', color: 'hsl(55,70%,50%)', size: 15 },
    ],
    links: [
        { source: 'node1', target: 'node2', distance: 80 },
        { source: 'node2', target: 'node3', distance: 100 },
    ],
};

const NetworkChart = () => {
    return (
        <div style={{ width: '100%', height: '100%' }}>
            <ResponsiveNetwork
                data={data}
                margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
                linkDistance={(e) => e.distance}
                centeringStrength={0.3}
                repulsivity={6}
                nodeSize={(n) => n.size}
                activeNodeSize={(n) => 1.5 * n.size}
                nodeColor={(e) => e.color}
                nodeBorderWidth={1}
                nodeBorderColor={{
                    from: 'color',
                    modifiers: [['darker', 0.8]],
                }}
                linkThickness={(n) => 2 + 2 * n.target.data.height}
                linkBlendMode="multiply"
                tooltip={(node) => (
                    <div
                        style={{
                            padding: '8px',
                            background: '#000000', // 어두운 배경
                            color: '#00ff00', // Dashboard 색상과 일치
                            borderRadius: '5px',
                            fontSize: '14px',
                            fontWeight: 'bold',
                            boxShadow: '0 2px 5px rgba(0, 0, 0, 0.5)',
                        }}
                    >
                        <strong>{node.id}</strong>
                    </div>
                )}
                motionConfig="wobbly"
            />
        </div>
    );
};

export default NetworkChart;
