import React, { useState, useEffect } from 'react';
import './HeaderZone.css';

export default function HeaderZone() {
  const [isTitleVisible, setIsTitleVisible] = useState(false);
  const [isMenuVisible, setIsMenuVisible] = useState(false);

  useEffect(() => {
    // 타이핑 효과 시작 후 메뉴도 타이핑 효과를 주기 위해 타이머 설정
    setTimeout(() => setIsTitleVisible(true), 500); // 제목 타이핑 효과 후 시작
    setTimeout(() => setIsMenuVisible(true), 2500); // 메뉴 타이핑 효과 시작
  }, []);

  return (
    <div className="Header_Container">
      <div className="Header_area">
        <h1 className={`title ${isTitleVisible ? 'show' : ''}`}>Account DashBoard</h1>
        <div className={`Menu_bar ${isMenuVisible ? 'show' : ''}`}>
            <div className="menu">About</div>
            <div className="menu">News</div>
            <div className="menu">API</div>
            <div className="menu">Save</div>
            <div className="menu">BTC</div>
        </div>
      </div>
    </div>
  );
}
