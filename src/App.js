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

export default function MyApp() {
  const [isLoading, setIsLoading] = useState(true);
  const [isChartVisible, setIsChartVisible] = useState(false);

  useEffect(() => {
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
                  <BarChart />
                </div>
                <div className="chart-item">
                  <NetworkChart />
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