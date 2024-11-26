import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, LineElement, Title, Tooltip, Legend, PointElement } from 'chart.js';

// Chart.js에서 필요한 요소들 등록
ChartJS.register(
  CategoryScale,
  LinearScale,
  LineElement,
  Title,
  Tooltip,
  Legend,
  PointElement
);

const Graph = ({ data }) => {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Bitcoin Price (USD)',
        data: [],
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: false,
        tension: 0.1,
        yAxisID: 'y1', // 가격을 위한 Y축
      },
    ],
  });

  useEffect(() => {
    if (data.length > 0) {
      const labels = data.map(item => item.timestamp); // 날짜
      const prices = data.map(item => item.price); // 가격

      setChartData({
        labels: labels,
        datasets: [
          {
            label: 'Bitcoin Price (USD)',
            data: prices,
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: false,
            tension: 0.1,
            yAxisID: 'y1', // 가격 Y축
          },
        ],
      });
    }
  }, [data]);

  return (
    <div style={{ width: '100%', height: '400px', marginLeft: 0 }}>
      <Line
        data={chartData}
        options={{
          responsive: true,
          maintainAspectRatio: false,
          layout: {
            padding: {
              left: 0, // 들여쓰기 제거
              right: 10,
              top: 10,
              bottom: 10,
            },
          },
          scales: {
            x: {
              type: 'category',
              title: {
                display: true,
                text: 'Date',
                padding: 10,
              },
            },
            y1: {
              beginAtZero: false,
              title: {
                display: true,
                text: 'Bitcoin Price (USD)',
                padding: 15,
              },
              ticks: {
                padding: 10,
              },
              position: 'left',
            },
          },
        }}
      />
    </div>
  );
};

export default Graph;
