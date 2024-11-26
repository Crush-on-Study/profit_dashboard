/*Hook import*/
import React, {useState, useEffect} from 'react';

/*레이아웃들 import*/
import HeaderZone from "./Layout1/HeaderZone" /*헤더라인*/
import LoadingScreen from './Layout0/LoadingScreen' /*로딩화면*/
import NetworkChart from './Chart_House/NetworkChart'
import BarChart from './Chart_House/BarChart'
import Sidebar from './Layout1/Sidebar';
import Footer from './Layout1/Footer';

/* App.js의 css */
import './App.css';
import { Network } from '@nivo/network';
import { Bar } from '@nivo/bar';

/* 잔고 API */
// import { fetchUpbitBalance } from './Account/upbit_Acc';

export default function MyApp() {
  const [isLoading, setIsLoading] = useState(true);
  const [isChartVisible, setIsChartVisible] = useState(false);
  const [upbitBalance, setUpbitBalance] = useState(null); // 업비트 잔고 상태

  useEffect(() => {
    // 로딩 상태 변경
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 5000);

    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (!isLoading) {
      setTimeout(() => {
        setIsChartVisible(true);
      }, 1000);

      // // 업비트 잔고 불러오기
      // fetchUpbitBalance()
      //   .then((balance) => {
      //     setUpbitBalance(balance); // 잔고 상태 업데이트
      //   })
      //   .catch((error) => {
      //     console.error("업비트 잔고 조회 중 오류 발생:", error);
      //   });
    }
  }, [isLoading]);

  return (
    <div className="app-container">
      {isLoading ? (
        <LoadingScreen />
      ) : (
        <>
          <HeaderZone />
          <Sidebar />
          <div className="main-content">
            <div className="divider"></div>
            <div className="dashboard-container">
              <div className="charts-section">
                <div className="chart-item">
                  <h3>업비트 잔고</h3>
                  {upbitBalance ? (
                    <ul>
                      {upbitBalance.map((item, index) => (
                        <li key={index}>
                          {item.currency}: {parseFloat(item.balance).toFixed(2)} {item.unit_currency}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p>잔고를 불러오는 중...</p>
                  )}
                </div>
                <div className="chart-item">
                  <h3>바이비트 잔고</h3>
                  {/* 바이비트 잔고 추가 예정 */}
                </div>
              </div>
              <div className="data-section">
                <h2>크롤링 데이터</h2>
                <p>여기에 크롤링 데이터를 표시할 것입니다.</p>
              </div>
            </div>
            <Footer />
          </div>
        </>
      )}
    </div>
  );
}