import { ResponsiveBar } from '@nivo/bar';

const data = [
    { country: 'USA', value: 100 },
    { country: 'Germany', value: 80 },
    { country: 'France', value: 60 },
];

const BarChart = () => {
    return (
        <div style={{ width: '100%', height: '100%' }}>
            <ResponsiveBar
                data={data}
                keys={['value']}
                indexBy="country"
                margin={{ top: 20, right: 20, bottom: 50, left: 50 }}
                padding={0.3}
                valueScale={{ type: 'linear' }}
                indexScale={{ type: 'band', round: true }}
                colors={{ scheme: 'category10' }}
                axisTop={null}
                axisRight={null}
                axisBottom={{
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    legend: 'Country',
                    legendPosition: 'middle',
                    legendOffset: 32,
                }}
                axisLeft={{
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    legend: 'Value',
                    legendPosition: 'middle',
                    legendOffset: -40,
                }}
                enableLabel={false}
                theme={{
                    axis: {
                        ticks: {
                            text: {
                                fill: '#00ff00', // 텍스트 색상을 Dashboard와 맞게 설정
                            },
                        },
                        legend: {
                            text: {
                                fill: '#00ff00', // 축 설명 색상
                            },
                        },
                    },
                }}
                animate={true}
                motionConfig="wobbly"
            />
        </div>
    );
};

export default BarChart;
