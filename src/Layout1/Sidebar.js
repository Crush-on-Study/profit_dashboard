import React, { useState, useEffect } from 'react';
import './Sidebar.css';
import Graph from './Graph';

const Sidebar = () => {
  const [exchangeRates, setExchangeRates] = useState({ USD: 0, KRW: 0, BTC_KRW: 0, BTC_USD: 0 });
  const [timeZones, setTimeZones] = useState({ EST: '', PST: '', KST: '' });
  const [btcData, setBtcData] = useState([]);

  // 환율 데이터 가져오기
  useEffect(() => {
    const fetchExchangeRates = async () => {
      try {
        const response = await fetch('https://api.exchangerate-api.com/v4/latest/USD'); // 환율 API 예시
        const data = await response.json();
        setExchangeRates({
          USD: 1,
          KRW: data.rates.KRW.toFixed(2),
          BTC_KRW: data.rates.BTC_KRW ? data.rates.BTC_KRW.toFixed(2) : 1,
          BTC_USD: data.rates.BTC_USD ? data.rates.BTC_USD.toFixed(2) : 1,
        });
      } catch (error) {
        console.error('환율 데이터 fetch 실패', error);
      }
    };

    fetchExchangeRates();
  }, []);

  // 비트코인 가격 데이터 가져오기 (KRW, USD 기준으로)
  useEffect(() => {
    const fetchBtcData = async () => {
      try {
        const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,krw'); // USD, KRW 기준으로 비트코인 가격 가져오기
        const data = await response.json();
        setExchangeRates((prevRates) => ({
          ...prevRates,
          BTC_KRW: data.bitcoin.krw.toFixed(2),
          BTC_USD: data.bitcoin.usd.toFixed(2),
        }));

        // 비트코인 30일 데이터 가져오기
        const chartResponse = await fetch('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30'); // 30일 데이터
        const chartData = await chartResponse.json();
        const prices = chartData.prices.map(item => ({
          timestamp: new Date(item[0]).toLocaleDateString(), // 날짜 형식으로 변환
          price: item[1].toFixed(2), // 가격을 소수점 두 자리로 표시
        }));
        setBtcData(prices);
      } catch (error) {
        console.error('비트코인 데이터 fetch 실패', error);
      }
    };

    fetchBtcData();
  }, []);

  // 시차 데이터 업데이트
  useEffect(() => {
    const updateTimes = () => {
      const now = new Date();
      const options = { timeZone: 'America/New_York', hour: '2-digit', minute: '2-digit' };
      const EST = now.toLocaleTimeString('en-US', options);

      options.timeZone = 'America/Los_Angeles';
      const PST = now.toLocaleTimeString('en-US', options);

      options.timeZone = 'Asia/Seoul';
      const KST = now.toLocaleTimeString('en-US', options);

      setTimeZones({ EST, PST, KST });
    };

    updateTimes();
    const interval = setInterval(updateTimes, 60000); // 1분마다 업데이트
    return () => clearInterval(interval);
  }, []);

  return (
    <aside className="sidebar">
      <div className="sidebar-section fade-in">
        <div className="vertical-divider"></div>
        <h3>Currency Prices</h3>
        <ul>
          <li className="typing-animation">KRW: ₩{exchangeRates.KRW}</li>
          <li className="typing-animation">BTC: ₩{exchangeRates.BTC_KRW}</li>
          <li className="typing-animation">BTC: ${exchangeRates.BTC_USD}</li>
        </ul>
        {/* Graph 컴포넌트에 30일 비트코인 데이터 전달 */}
        <Graph data={btcData} />
      </div>
      <div className="sidebar-section fade-in">
        <h3>Time Zones</h3>
        <ul>
          <li className="typing-animation">EST: {timeZones.EST}</li>
          <li className="typing-animation">PST: {timeZones.PST}</li>
          <li className="typing-animation">KST: {timeZones.KST}</li>
        </ul>
      </div>
    </aside>
  );
};

export default Sidebar;
